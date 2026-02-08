# Claude Agent SDK Session Manager

Build a full-stack application for managing Claude Agent SDK sessions. An agentic chat interface where users can create sessions, chat with Claude agents, see tool usage inline, and resume any past conversation with full history.

## Problem Statement

The Claude Agent SDK doesn't expose an API to fetch historical messages when resuming a session. Claude remembers the context internally, but you can't programmatically retrieve past messages to display in a UI.

**Solution**: Store messages in our own database while using the SDK's session_id for context resumption.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Vite, Tailwind, shadcn/ui |
| Backend | Python, FastAPI, sse-starlette |
| Database | SQLite with aiosqlite |
| Agent SDK | claude-agent-sdk |

## Project Structure

```
agent-session-manager/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app entry
│   │   ├── database.py       # SQLite connection + queries
│   │   ├── models.py         # Pydantic models
│   │   ├── routes/
│   │   │   ├── sessions.py   # Session CRUD
│   │   │   └── chat.py       # Chat with SSE streaming
│   │   └── sdk_client.py     # Claude Agent SDK wrapper
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SessionSidebar.tsx
│   │   │   ├── ChatView.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBlock.tsx
│   │   │   ├── ToolUseCard.tsx
│   │   │   └── NewSessionDialog.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── README.md
```

## Agent Build Order & Communication

When building with an agent team, agents MUST follow this contract-first sequence:

### Phase 1: Database Agent
1. Build schema, CRUD functions, Pydantic models
2. **Send function signatures and model definitions** to lead
3. Lead verifies and forwards to backend agent

### Phase 2: Backend Agent (after receiving DB contract)
1. Build FastAPI app, routes, SSE streaming, SDK client
2. **Send complete API contract** to lead — must include:
   - Exact endpoint URLs with trailing slashes noted
   - Exact request/response JSON shapes
   - Exact SSE event format with all event types
   - Status codes for success and error cases
3. Lead verifies and forwards to frontend agent

### Phase 3: Frontend Agent (after receiving API contract)
1. Build React app, components, API client **conforming exactly to the verified API contract**
2. Do NOT guess endpoint URLs or response shapes — use what was provided

### Phase 4: Lead Validation
1. Contract diff — compare backend's actual endpoints vs frontend's fetch calls
2. Start both servers
3. Run E2E browser tests

## Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,              -- Claude SDK session_id
    title TEXT NOT NULL,
    system_prompt TEXT,               -- Optional custom system prompt
    working_directory TEXT,
    model TEXT DEFAULT 'claude-sonnet-4-20250514',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,               -- 'user', 'assistant', 'system'
    content TEXT,
    message_type TEXT NOT NULL,       -- 'text', 'tool_use', 'tool_result', 'thinking'
    tool_name TEXT,
    tool_input TEXT,                  -- JSON
    tool_output TEXT,                 -- JSON
    is_error BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_session ON messages(session_id);
```

## API Contract

**IMPORTANT:** This is the authoritative API contract. Both backend and frontend MUST conform to these exact specifications. The lead agent should verify alignment before integration.

### Endpoints

| Method | Endpoint (exact) | Request Body | Response |
|--------|-------------------|-------------|----------|
| GET | `/health` | — | `{"status": "ok"}` |
| POST | `/api/sessions/` | `{"title": "...", "system_prompt?": "...", "working_directory?": "...", "model?": "..."}` | `SessionResponse` (200) |
| GET | `/api/sessions/` | — | `SessionResponse[]` (200) |
| GET | `/api/sessions/{id}` | — | `{"session": SessionResponse, "messages": MessageResponse[]}` (200) or 404 |
| POST | `/api/sessions/{id}/chat` | `{"message": "..."}` | SSE stream |
| DELETE | `/api/sessions/{id}` | — | 204 No Content |

**Note:** POST and GET list endpoints use **trailing slash** (`/api/sessions/`). GET by ID, DELETE, and chat do NOT use trailing slash.

### Response Shapes

**SessionResponse:**
```json
{"id": "uuid", "title": "string", "system_prompt": "string|null", "working_directory": "string|null", "model": "string", "created_at": "ISO8601", "last_accessed": "ISO8601"}
```

**MessageResponse:**
```json
{"id": 1, "session_id": "uuid", "role": "user|assistant", "content": "string|null", "message_type": "text|thinking|tool_use|tool_result", "tool_name": "string|null", "tool_input": "string|null", "tool_output": "string|null", "is_error": false, "timestamp": "ISO8601"}
```

**GET /api/sessions/{id} returns a NESTED object** (not flat):
```json
{
  "session": { SessionResponse },
  "messages": [ MessageResponse, ... ]
}
```
The frontend must destructure this into a flat `SessionWithMessages` for its internal state.

## SDK Integration

### Authentication

**NO MOCKING REQUIRED.** We are already authenticated with Anthropic via global CLI auth. The Claude Agent SDK automatically uses these credentials. Do not mock the SDK or create fake responses — test against the real API.

### Key Pattern: Dual Storage with Text Accumulation

**IMPORTANT:** The SDK streams text in small chunks. Do NOT store each chunk as a separate database row — this causes the frontend to render N separate bubbles when loading message history. Instead, **accumulate text chunks** and store ONE row per complete text response.

```python
async def chat(session_id: str, user_message: str):
    # 1. Store user message in OUR database
    await db.add_message(session_id, "user", user_message, "text")

    # 2. Accumulate text chunks, store other types immediately
    accumulated_text = ""

    async for msg in query(prompt=user_message, options=ClaudeAgentOptions(resume=session_id)):
        if msg.type == "text":
            accumulated_text += msg.content  # Accumulate, don't store yet
        elif msg.type == "tool_use":
            # Flush accumulated text before tool use
            if accumulated_text:
                await db.add_message(session_id, "assistant", accumulated_text, "text")
                accumulated_text = ""
            await db.add_message(session_id, "assistant", None, "tool_use", tool_name=msg.tool_name, ...)
        elif msg.type == "done":
            # Flush remaining accumulated text
            if accumulated_text:
                await db.add_message(session_id, "assistant", accumulated_text, "text")
                accumulated_text = ""

        # 3. Yield EVERY event to frontend via SSE (streaming feel)
        yield msg
```

This way the frontend gets real-time streaming chunks, but the database stores one clean row per response.

### Capturing Session ID

For new sessions, capture the session_id from the init message:

```python
if isinstance(message, SystemMessage) and message.subtype == "init":
    session_id = message.data.get("session_id")
```

### SSE Event Types

```typescript
type StreamMessage =
  | { type: 'text'; content: string }
  | { type: 'thinking'; content: string }
  | { type: 'tool_use'; tool_name: string; tool_input: object }
  | { type: 'tool_result'; content: string; is_error: boolean }
  | { type: 'session_init'; session_id: string }
  | { type: 'done'; session_id: string; total_cost_usd: number; duration_ms: number }
```

## Cross-Cutting Concerns

These behaviors span multiple agents and MUST be explicitly assigned during the build:

| Concern | Owner | Coordinates With | Detail |
|---------|-------|-----------------|--------|
| Text chunk accumulation | Backend | Frontend | Backend accumulates streamed text chunks into ONE DB row. Frontend renders one bubble per DB row on reload. |
| URL trailing slashes | Backend | Frontend | FastAPI router uses trailing slashes on collection endpoints (`/api/sessions/`). Frontend fetch URLs must match exactly. |
| Response envelope | Backend | Frontend | GET session returns `{"session": {...}, "messages": [...]}`, NOT a flat object. Frontend must destructure. |
| UI accessibility | Frontend | Lead (for E2E testing) | All interactive elements need `aria-label` attributes. Delete buttons must be clickable (not `opacity-0` without focus fallback). |
| SSE event format | Backend | Frontend | Exact JSON shapes for each event type documented in API Contract. Both sides must match. |

## Frontend Components

### SessionSidebar
- List of sessions sorted by last_accessed
- New session button opens NewSessionDialog
- Click session to load it
- Delete button per session with `aria-label="Delete session"` (must be visible on hover AND focus for accessibility/automation)

### NewSessionDialog
- Title input (required)
- System prompt textarea (optional, placeholder with examples)
- Working directory input (optional, defaults to ".")
- Create button

### ChatView
- Message input at bottom
- Send button (disabled while streaming)
- Shows session title and metadata

### MessageList
- Scrollable container
- Auto-scroll on new messages
- Groups consecutive assistant messages

### MessageBlock
Renders based on message_type:
- **text**: Chat bubble (user=blue right, assistant=gray left)
- **tool_use**: ToolUseCard component
- **tool_result**: Inline result (collapsible if long)
- **thinking**: Italic, muted, collapsed by default

### ToolUseCard
- Icon + tool name header
- Collapsed: one-line summary
- Expanded: formatted JSON input and output
- Error state styling for is_error=true

## Styling

- shadcn/ui as component base
- Tailwind for custom styling
- Dark mode support
- Responsive: sidebar collapses on mobile
- User messages: right-aligned, blue background
- Assistant messages: left-aligned, gray background
- Tool cards: subtle border, expand/collapse animation

## Dependencies

### Backend
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sse-starlette>=1.8.0
aiosqlite>=0.19.0
claude-agent-sdk>=0.1.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### Frontend
```
react
react-dom
typescript
vite
tailwindcss
@shadcn/ui
lucide-react
```

## Acceptance Criteria

1. **New Session**: User creates session with title + optional system prompt → session saved
2. **Chat**: User sends message → response streams in real-time → tool usage visible inline
3. **Resume**: User clicks past session → full message history loads → can continue chatting
4. **Delete**: User deletes session → session and messages removed
5. **Error Handling**: Network/SDK errors displayed gracefully
6. **Responsive**: Works on desktop and mobile

## Validation

Each agent validates their own domain before reporting done. The lead agent runs end-to-end validation after all agents complete.

### Database Validation

Run from `backend/`:

```bash
# 1. Schema creation
python -c "
import asyncio
from app.database import init_db, get_db
asyncio.run(init_db())
print('✓ Schema created')
"

# 2. CRUD operations
python -c "
import asyncio
from app.database import *

async def test():
    await init_db()

    # Create session
    session_id = 'test-123'
    await create_session(session_id, 'Test Session', 'You are helpful', '.')
    print('✓ Session created')

    # Add messages
    await add_message(session_id, 'user', 'Hello', 'text')
    await add_message(session_id, 'assistant', 'Hi there!', 'text')
    print('✓ Messages added')

    # Fetch session with messages
    session = await get_session_with_messages(session_id)
    assert session['title'] == 'Test Session'
    assert len(session['messages']) == 2
    print('✓ Session fetch works')

    # List sessions
    sessions = await list_sessions()
    assert any(s['id'] == session_id for s in sessions)
    print('✓ Session list works')

    # Delete cascade
    await delete_session(session_id)
    session = await get_session_with_messages(session_id)
    assert session is None
    print('✓ Delete cascade works')

asyncio.run(test())
"
```

### Backend Validation

Run from `backend/`:

```bash
# 1. Start the server
uvicorn app.main:app --reload &
sleep 2

# 2. Health check
curl -s http://localhost:8000/health | grep -q "ok" && echo "✓ Server running"

# 3. Create session
SESSION=$(curl -s -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "system_prompt": "Be concise"}' | jq -r '.id')
echo "✓ Created session: $SESSION"

# 4. List sessions
curl -s http://localhost:8000/api/sessions | jq -e '.[] | select(.title == "Test")' && echo "✓ Session in list"

# 5. Get session
curl -s http://localhost:8000/api/sessions/$SESSION | jq -e '.title' && echo "✓ Session fetch works"

# 6. SSE streaming (send message, capture first event)
timeout 30 curl -s -N -X POST "http://localhost:8000/api/sessions/$SESSION/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Say hello in one word"}' | head -5
echo "✓ SSE streaming works"

# 7. Verify message persisted
curl -s http://localhost:8000/api/sessions/$SESSION | jq -e '.messages | length > 0' && echo "✓ Messages persisted"

# 8. Delete session
curl -s -X DELETE http://localhost:8000/api/sessions/$SESSION && echo "✓ Session deleted"

# 9. Confirm deletion
curl -s http://localhost:8000/api/sessions/$SESSION | jq -e '. == null' && echo "✓ Deletion confirmed"
```

### Frontend Validation

Run from `frontend/`:

```bash
# 1. Dependencies install
npm install && echo "✓ Dependencies installed"

# 2. TypeScript compiles
npx tsc --noEmit && echo "✓ TypeScript valid"

# 3. Build succeeds
npm run build && echo "✓ Build successful"

# 4. Dev server starts
npm run dev &
sleep 3
```

Use the **[Vercel Agent Browser CLI](https://github.com/vercel-labs/agent-browser)** to validate UI (without backend):

```bash
# Install if needed
npm install -g agent-browser
agent-browser install  # Downloads Chromium

# Validate static UI elements
agent-browser open "http://localhost:5173"
agent-browser snapshot -i  # Get interactive elements
# Verify: sidebar exists, 'New Session' button visible, chat area renders
agent-browser screenshot validation.png
```

**Frontend agent validates** (no backend needed):
1. Sidebar renders with empty state
2. New Session dialog opens and closes
3. Components render without console errors
4. Dark mode toggle works (if implemented)
5. Responsive layout at different widths

### End-to-End Validation (Lead Agent)

After all agents report done, the lead agent spins up both servers and runs E2E validation using the **[Vercel Agent Browser CLI](https://github.com/vercel-labs/agent-browser)**.

**IMPORTANT:** No mocking. We are already authenticated with Anthropic. Test against the real API.

```bash
# Start both servers
cd backend && uvicorn app.main:app --port 8000 &
cd frontend && npm run dev &
sleep 5

# Install agent-browser if needed
npm install -g agent-browser
agent-browser install
```

Use the Agent Browser CLI to run the full E2E flow:

```bash
# 1. CREATE SESSION
agent-browser open "http://localhost:5173"
agent-browser snapshot -i
agent-browser click @<new-session-button-ref>
agent-browser fill @<title-input-ref> "E2E Test"
agent-browser fill @<system-prompt-ref> "Be extremely brief"
agent-browser click @<create-button-ref>

# 2. VERIFY SESSION appears in sidebar
agent-browser snapshot -i
# Confirm "E2E Test" visible in sidebar

# 3. SEND MESSAGE
agent-browser fill @<chat-input-ref> "What is 2+2?"
agent-browser click @<send-button-ref>

# 4. VERIFY RESPONSE streams in (wait for completion)
agent-browser snapshot -i
# Confirm response shows "4" or similar

# 5. TOOL USE - trigger a tool
agent-browser fill @<chat-input-ref> "Use a tool to list files in the current directory"
agent-browser click @<send-button-ref>

# 6. VERIFY TOOL card appears
agent-browser snapshot -i
# Confirm tool use card with Bash/Read tool visible

# 7. REFRESH page
agent-browser open "http://localhost:5173"

# 8. VERIFY PERSISTENCE - session still in sidebar with history
agent-browser snapshot -i
agent-browser click @<e2e-test-session-ref>
# Confirm message history loaded

# 9. CONTINUE CHAT
agent-browser fill @<chat-input-ref> "What did I ask you first?"
agent-browser click @<send-button-ref>

# 10. VERIFY CONTEXT - Claude remembers
agent-browser snapshot -i
# Confirm response mentions 2+2

# 11. DELETE session
agent-browser click @<delete-button-ref>

# 12. VERIFY DELETE
agent-browser snapshot -i
# Confirm "E2E Test" removed from sidebar

agent-browser screenshot e2e-final.png
```

**Success criteria:**
- All 12 steps pass
- No server errors in terminal (check uvicorn output)
- SSE streaming works (responses appear incrementally, not all at once)
- Session persistence works across page refresh
- Tool use cards render correctly with real tool output (not mocked)

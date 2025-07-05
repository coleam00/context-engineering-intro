gemini -p "@./
# ──────────────────────────────────────────────────────────────
#  Context-Engineering Migration Prompt  ▸  Claude → Gemini CLI
# ──────────────────────────────────────────────────────────────
## 1 ▸ ROLE
You are **Gemini CLI** operating in autonomous *code-mod* mode
with full read/write authority on this repository.  
_Think step-by-step, validate aggressively, and minimise risk._

## 2 ▸ GOAL
Convert the repo so it uses **Gemini CLI** instead of **the previous tool**
while preserving the original Context-Engineering workflow.

### Deliverables
1. **Renamed assets**  
   * `CLAUDE.md` → `GEMINI_CLI.md`  
   * `.claude/` → `.gemini/` (keep contents)
2. **Rewritten docs**  
   * Update *every* reference to the previous tool to “Gemini CLI”.  
   * Replace slash-commands (`/generate-prp`, `/execute-prp`, etc.)  
     with equivalent `gemini -p` calls that use the *@include* syntax.  
   * Insert a “Quick Start” box showing `npm install -g @google/gemini-cli`
     and `gemini` login steps. :contentReference[oaicite:0]{index=0}
3. **Patch set**  
   * Provide UNIX-ready `git mv` commands **and** unified `patch` blocks
     for every changed file so the user can `git apply` them verbatim.
4. **Safety net**  
   * All changes must live on a new branch `gemini-cli`.
   * No file grows beyond **500 non-blank lines**.
5. **Success message** that lists:
   * Updated files & byte counts
   * Exact commands to run tests / sanity checks

## 3 ▸ CONSTRAINTS  (Context-Engineering Rules)
- **Plan-first gating:**  
  1️⃣ *Propose* a numbered action plan.  
  2️⃣ *Wait* for my explicit “Approved” before executing.
- **One action per step:** keep patches small and reviewable.
- **Explicit tool cues:**  
  Prefix shell snippets with `RUN_SHELL:` and patches with `FILE_PATCH:`.
- **Include context upfront:** you already have the entire repo via `@./`.
- **Aggressive validation:** after applying patches, run  
  `gemini -p "List all files and search for the string 'the previous tool' → expect 0 hits"`.

## 4 ▸ RESOURCES (already in context)
- Current repo files (`@./`)
- Original *Claude* rules in `CLAUDE.md`
- Example PRPs and INITIAL specs
- README quick-start showing slash commands

## 5 ▸ OUTPUT FORMAT
Return **one** top-level Markdown document containing:
```markdown
### PLAN
1. …
2. …

### RUN_SHELL
```bash
git checkout -b gemini-cli
…
FILE_PATCH
patch
Copy
Edit
--- a/README.md
+++ b/README.md
@@
- In the previous tool, run:
-/generate-prp INITIAL.md
+Using Gemini CLI:
+gemini -p "@INITIAL.md Generate a full PRP in Markdown, save as PRPs/<slug>.md"
NEXT_STEP
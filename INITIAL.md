# Build a production‑ready Model Context Protocol (MCP) server template repository

## FEATURE:

Create a reusable, production‑grade monorepo template for building MCP servers by composing tools, resources, and prompts. The template supports multiple transports, pluggable auth and RBAC, strong DX and CI, observability, and a React demo UI.

Scope and Deliverables (summary):
- Monorepo structure with packages/server, packages/ui, packages/shared, examples/, docs/, scripts/, .github/workflows/
- Transports: stdio (default), HTTP (chunked), SSE; WebSocket behind FEATURE_WS=true
- Core constituents: Typed tools (zod), resources (read‑only/computed, pagination/streaming), prompts (templated bundles)
- AuthN/AuthZ: NoAuth, API key, HMAC, OAuth2 Client Credentials, mTLS; RBAC with role policies + allowlists (deny‑by‑default)
- Config & DX: CLI > env > config file > defaults; dotenv; CLI serve + scaffold; strict TS; ESLint; Prettier; Husky + lint‑staged; ESM build; graceful shutdown; health checks
- Observability: pino logs (redaction, req ids), OpenTelemetry hooks (opt‑in), standardized error shapes, backpressure/concurrency
- Testing: Vitest unit/integration; e2e smoke (UI→server HTTP/SSE/WS; stdio path with reference client)
- Documentation: Root README, server/UI READMEs, docs/ (architecture, extending, security, operations), examples/README, research with citations and ADRs

Acceptance Criteria (summary):
- All transports compile/run; stdio + HTTP/SSE default; WS opt‑in
- ≥3 tools, ≥2 resources, ≥2 prompt bundles (with tests)
- Auth providers selectable via config; RBAC enforced in tests
- CI passes lint, type‑check, unit/integration/e2e on Node 24.x (linux + macOS)
- Example UI can invoke at least one tool and one resource via HTTP/SSE
- No secrets committed; .env.example provided; logs redact sensitive fields
- CLI scaffold works to create new tool/resource stubs

## EXAMPLES:

See `examples/README.md` for a catalog and usage guidance.
Planned included examples (all TypeScript):
- Tools:
  - echo: Echos validated input; showcases zod I/O schemas, idempotency guidance, timeouts/cancellation
  - http_fetch: Validated HTTP GET with safe headers and size limits; streaming response support
  - file_metadata: Reads file stats (path allowlist, size/time fields); demonstrates errors and redaction
- Resources:
  - server_info: Version, transports enabled, uptime
  - time: Current server time, optional TZ parameter
- Prompt bundles (versioned):
  - general-tools: Parameterized prompts for calling tools with safe defaults
  - troubleshooting: Prompts guiding retries/backoff, minimal reproduction, and diagnostics

## DOCUMENTATION:

Primary references to guide design/implementation (to be expanded in docs/research):
- Model Context Protocol (MCP) docs: https://docs.claude.com/en/docs/mcp
- MCP SDKs (TypeScript/Node) – official repos/READMEs
- Fastify (HTTP/SSE): https://fastify.dev/
- ws (WebSocket): https://github.com/websockets/ws
- zod (validation): https://zod.dev/
- pino (logging): https://github.com/pinojs/pino
- OpenTelemetry JS: https://opentelemetry.io/docs/instrumentation/js/
- React + Vite + Tailwind (UI): https://react.dev/ • https://vitejs.dev/ • https://tailwindcss.com/
- Transport/security guidance for stdio/HTTP/SSE/WS (to be cited in docs/research)

## OTHER CONSIDERATIONS:

- Tech stack:
  - Runtime: Node.js 24.x (ESM), TypeScript 5.x
  - Server: Fastify (HTTP/SSE), ws (WS optional), native stdio handler
  - Validation: zod; Logging: pino; UI: React 18 + TailwindCSS v4.1 + Vite
  - Package manager: npm workspaces (default; can switch to pnpm if required)
- Transports are feature‑flagged; expose a consistent Transport interface (start/stop/request/stream). Enable/disable per config.
- AuthN: NoAuth (dev opt‑in), API Key (Bearer), HMAC (clock skew tolerance), OAuth2 Client Credentials (introspection or JWKS), mTLS (with pinning option)
- AuthZ: RBAC policy layer (admin, read_only, custom) with tool/resource allowlists; deny‑by‑default
- Security: Secrets from env; never logged; redact in logs; rate limiting; request size/timeouts per transport; CORS for UI/dev only; CSRF not needed for token APIs; strict zod validation for all inputs
- Configuration precedence: CLI > env > config file (JSON/YAML) > defaults; dotenv for local dev; `.env.example` provided
- DX/Build: ESM build via tsup/tsc; emit d.ts; strict TS (noImplicitAny, exactOptionalPropertyTypes); ESLint + Prettier; Husky + lint‑staged; graceful shutdown (SIGINT/SIGTERM); `/healthz`, `/readyz`
- Observability: Structured logging with request ids and redaction; OpenTelemetry hooks (opt‑in) for traces/metrics; consistent error shapes for MCP responses; backpressure and concurrency limits; performance budget guidance
- Testing: Vitest for unit/integration; spin up per‑transport server in tests; snapshot protocol envelopes where stable; e2e smoke for UI→server and stdio path
- CI: GitHub Actions matrix (Node 24.x on linux + macOS) running lint, type‑check, unit, integration, e2e smoke
- Non‑goals: Non‑Node runtimes; production infra beyond minimal Dockerfile; long‑term storage (stub interfaces only)

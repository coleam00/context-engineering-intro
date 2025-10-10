---
name: "MCP Server Monorepo Template PRP"
description: Production-ready MCP server template enabling fast composition of tools, resources, and prompts across multiple transports with pluggable auth/RBAC, strong DX, observability, tests, and a demo UI.
---

## Purpose
Build a reusable, production-grade monorepo that teams can clone to create specific MCP servers. Emphasize composition (tools/resources/prompts), transport adapters, pluggable auth, strict TypeScript, robust testing, and developer ergonomics.

## Scope (from INITIAL)
- Monorepo: packages/server, packages/ui, packages/shared, examples, docs, scripts, .github/workflows
- Transports: stdio, HTTP (chunked), SSE; WebSocket (experimental, FEATURE_WS=true)
- Auth: NoAuth, API Key, HMAC, OAuth2 Client Credentials (introspection/JWKS), mTLS; RBAC (deny-by-default) with role allowlists
- Tools/Resources/Prompts: typed (zod), streaming/pagination support, versioned prompt bundles
- Config & DX: CLI > env > config > defaults; dotenv; CLI serve/scaffold; strict TS; ESLint/Prettier; Husky; tsup/tsc ESM build; health/ready; graceful shutdown
- Observability: pino with redaction + request ids; OpenTelemetry hooks; backpressure; concurrency limits; error shape normalization
- Testing: Vitest unit/integration; e2e smoke (UI→server HTTP/SSE, stdio path)
- Docs: root README, server/UI READMEs, docs/{architecture, extending, security, operations, research}, examples/README

## Success Criteria
- All transports compile/run; stdio+HTTP+SSE default; WS opt-in
- ≥3 tools, ≥2 resources, ≥2 prompt bundles with tests
- Auth providers selectable via config; RBAC enforced in tests
- CI passes: lint, type-check, unit/integration/e2e on Node 24.x (linux+macOS)
- UI can invoke at least one tool and one resource over HTTP/SSE
- No secrets committed; .env.example present; logs redact sensitive fields
- Scaffold CLI works for tool/resource creation

## Architecture (high-level)
- packages/shared
  - types/: shared TypeScript interfaces (Transport, AuthProvider, Tool, Resource, Error shapes)
  - schemas/: zod schemas for tool & resource IO; config schema
  - utils/: logger factory, redaction, request ids, otel helpers (no-op by default)
- packages/server
  - core/: server bootstrap, config loader (CLI>env>file>defaults), health/ready, graceful shutdown
  - transports/: stdio.ts, http.ts (chunked), sse.ts, ws.ts (experimental, FEATURE_WS)
  - auth/: providers (noauth, api-key, hmac, oauth2, mtls) implementing AuthProvider
  - rbac/: role policies, allowlists, enforcement middleware
  - tools/: sample tools (echo, http_fetch, file_metadata)
  - resources/: sample resources (server_info, time)
  - prompts/: bundles v1 (general-tools, troubleshooting)
  - cli/: mcp-template serve|scaffold
  - observability/: pino logger, redaction, otel hooks
  - tests/: unit, integration per transport, snapshots for envelopes
- packages/ui
  - React + Tailwind + Vite demo to exercise HTTP/SSE (and WS when enabled)
  - Pages: Home, Tool runner, Resource viewer, Streaming demo

## Key Interfaces (packages/shared)
- Transport: start(), stop(), handle(req):Promise<Res>, stream?(req):AsyncIterable<Chunk>
- AuthProvider: authenticate(ctx):Promise<Identity|null>
- PolicyEngine: authorize(identity, action, target): boolean
- Tool<I,O>: name, input zod, output zod, run(input, ctx):Promise<O>
- Resource<Q,O>: name, query zod, output zod, get(query, ctx):Promise<O> | AsyncIterable<O>

## Configuration & CLI
- Precedence: CLI args > env vars > config file (JSON/YAML) > defaults
- dotenv in dev; .env.example provided
- CLI:
  - mcp-template serve --transport [stdio|http|sse|ws] --port 8787 --config ./config.yaml
  - mcp-template scaffold tool|resource --name <name>

## Security & AuthN/Z
- Secrets only via env; redact in logs; never echo secrets
- Providers:
  - NoAuth (dev opt-in)
  - ApiKeyAuth (Authorization: Bearer <token>)
  - HmacAuth (signed body+headers; tolerate clock skew)
  - OAuth2Auth (client credentials; introspection or JWKS; cache keys)
  - MtlsAuth (require valid client cert; optional pinning)
- RBAC policy: roles (admin, read_only, custom); allowlists per tool/resource; deny-by-default
- Rate limiting, request size/timeouts per transport; CORS only for UI/dev; CSRF not needed for token APIs

## Observability & Reliability
- pino structured logging with request ids; redaction for Authorization, secrets, cookies
- OpenTelemetry (opt-in): span hooks around tool/resource execution; metric counters
- Centralized error mapping to consistent MCP error shapes
- Backpressure for streaming; configurable concurrency limits
- Health endpoints: /healthz, /readyz; graceful shutdown (SIGINT/SIGTERM)

## Testing & CI
- Unit tests (Vitest): tools, resources, auth providers, transports (adapters)
- Integration: spin up per-transport server; exercise representative tool/resource; snapshot envelopes
- E2E smoke: UI→server via HTTP/SSE/WS (as enabled); stdio path via reference client
- CI matrix: Node 24.x on ubuntu-latest and macos-latest; run lint, type-check, build, tests

## Implementation Plan (tasks)
1) Research & ADRs
   - Collect ≥10 sources (see Research) and write docs/adr for transports/auth/SDK selection
2) Bootstrap monorepo & tooling
   - npm workspaces; TS strict; ESLint/Prettier; Vitest; Husky + lint-staged; CI workflows
3) Server core
   - shared interfaces; config loader; stdio transport; HTTP (chunked) + SSE; WS behind FEATURE_WS
4) Auth & RBAC
   - NoAuth, ApiKey, Hmac (skew), OAuth2 (introspection/JWKS), Mtls; role policies + allowlists
5) Examples
   - Tools: echo, http_fetch, file_metadata; Resources: server_info, time; Prompts: general-tools, troubleshooting
6) Observability & hardening
   - pino + redaction; otel hooks; error normalization; health/ready; timeouts; rate limiting; backpressure
7) UI demo
   - React+Tailwind app; call server over HTTP/SSE; display streaming
8) Docs & polish
   - all READMEs; docs/; research index; scripts; Dockerfile; release workflow

## Validation Gates (must be executable)
```bash
# Repo root
npm install

# Lint & types
npm run lint && npm run type-check

# Build all packages
npm run build --workspaces

# Unit + integration + e2e (matrix in CI; locally run linux/macos equivalent)
npm test --workspaces

# Server health
npm -w packages/server run start -- --transport http --port 8787 &
curl -fsS http://localhost:8787/healthz && curl -fsS http://localhost:8787/readyz
pkill -f "--transport http" || true
```

## External Research (initial seed; expand to ≥10 with summaries in docs/research)
- Claude MCP docs: https://docs.claude.com/en/docs/mcp
- Model Context Protocol site: https://modelcontextprotocol.io/
- MCP TypeScript SDK (if applicable): https://github.com/modelcontextprotocol/sdk
- Fastify (HTTP/SSE): https://fastify.dev/docs/latest/Reference/Server/
- fastify-sse-v2: https://github.com/mcollina/fastify-sse-v2
- ws WebSocket: https://github.com/websockets/ws
- zod: https://zod.dev/
- pino logging: https://github.com/pinojs/pino
- OpenTelemetry JS: https://opentelemetry.io/docs/instrumentation/js/
- Node.js streams/backpressure: https://nodejs.org/api/stream.html

## Confidence
Score: 7/10 — Plan is detailed with clear validation gates and phased tasks. Confidence will increase after research/ADRs and transport prototypes (stdio + HTTP/SSE) are validated locally.


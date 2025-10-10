# Example Catalog for MCP Template

This folder will contain sample tools, resources, and prompt bundles for the MCP server template. Use these examples as references when adding new capabilities to your own server.

Included (planned):

## Tools
- echo: Validated echo with zod schemas; demonstrates idempotency guidance, timeouts, and cancellation.
- http_fetch: Safe HTTP GET with allowlisted headers, response size limit, and optional streaming.
- file_metadata: Filesystem metadata (allowlisted paths) with redaction of sensitive fields and robust error handling.

## Resources
- server_info: Server version, enabled transports, uptime.
- time: Current server time with optional timezone parameter.

## Prompt Bundles
- general-tools (v1): Parameterized prompts for invoking tools and interpreting outputs safely.
- troubleshooting (v1): Prompts for retries, backoff, and diagnostic collection.

## How to use these examples
- Read each example's docstring and comments for usage and extension points.
- Follow the zod schemas for inputs/outputs. All inputs must be validated.
- Use the scaffold command to generate new tools/resources with the same structure.

## Testing
- Each example includes Vitest unit tests. Run them within the server workspace (packages/server) once the monorepo is bootstrapped.

## Security & Policies
- By default, RBAC denylists everything; examples will include role allowlists (admin/read_only) demonstrating safe defaults.

## Notes
- These examples are meant to be copied/adapted; keep files under 500 LOC and prefer composition over inheritance.


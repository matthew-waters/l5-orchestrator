# Source Layout

The `src/` package is organized to keep core business logic isolated from
infrastructure concerns and delivery mechanisms.

## apps/

Application entrypoints and wiring. This is where frameworks live
(FastAPI, worker runners), along with HTTP routes and middleware.

## domain/

Core business logic and workflows. This layer should be free of
infrastructure details, so it can be reused and tested in isolation.

## adapters/

Integration points for external systems (database, S3, AWS).
Adapters encapsulate connection details, persistence, and SDK usage.

## shared/

Common utilities and types used across layers (logging, time helpers,
shared types, and small cross-cutting helpers).

## API auth

API requests should include an `X-API-Key` header. The server hashes the key
and resolves the tenant before handling tenant-scoped routes.

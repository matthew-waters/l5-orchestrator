# Database Adapter

This package owns all database integration details, keeping SQLAlchemy wiring
and persistence logic out of the domain and API layers.

## What lives here

- `base.py`: the shared SQLAlchemy `Base` class for ORM models.
- `models/`: ORM table mappings and enum types.
- `session.py`: database URL construction, engine setup, and session factory.
- `repositories/`: thin data-access classes (queries and persistence).
- `engine.py`: low-level engine helpers.

## Usage pattern

1. API layer depends on `get_db()` to obtain a session.
2. Service layer uses repositories to read/write entities.
3. Models remain the single source of truth for schema mapping.

This separation keeps domain logic independent of the database and makes it
easier to test or swap database implementations later.

## Admin script

Tenant creation is handled via a server-side script in
`scripts/admin/create_tenant.py`
so it is not exposed through the public API.

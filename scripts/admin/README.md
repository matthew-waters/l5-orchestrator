# Admin Scripts

## create_tenant.py

Creates a tenant record and prints a one-time API key.

Run:

```bash
python -m scripts.admin.create_tenant "Tenant Name"
```

## create_fleet.py

Creates a fleet record (admin only).

Run:

```bash
python -m scripts.admin.create_fleet "Fleet Name" '{"key":"value"}' --description "Optional"
```

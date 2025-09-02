# Docker Compose Lab — Flask + PostgreSQL

This lab spins up **two containers**:

- **web**: a Flask app with a form and a table of results
- **db**: a PostgreSQL database

The page includes a **visual connectivity map** showing `web ↔ db` status.

## Prerequisites

- Docker and Docker Compose

## Run

```bash
docker compose up --build
```

Then open **http://localhost:8080**.

## What to Try

1. Submit a record using the form (name, email, message).
2. Watch the table update.
3. See the connectivity chip and the diagram (green = connected).

## Tear Down

```bash
docker compose down -v
```

## Notes

- Database credentials are in `docker-compose.yml` for demo simplicity.
- The `web` app auto-creates the `submissions` table if it doesn't exist.

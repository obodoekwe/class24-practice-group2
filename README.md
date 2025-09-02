# Docker Compose Lab — Flask + PostgreSQL (Animated + Live Logs)

Two containers:
- **web** (Flask) — form + table + animated connectivity + **live logs viewer**
- **db** (PostgreSQL)

### Run
```bash
docker compose up --build
```
Open http://localhost:8080.

### Live Logs
The web app mounts the host Docker socket **read-only** and uses Server-Sent Events (SSE) to stream logs from `lab_web` and `lab_db`.
Buttons allow pause/resume and clearing the panes. Limit: 500 lines per pane.

> Note: mounting `/var/run/docker.sock` exposes Docker engine access to the `web` container. Keep this to **demo/dev** environments.

### Clean up
```bash
docker compose down -v
```

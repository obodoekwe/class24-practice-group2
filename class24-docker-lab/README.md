# 🧪 Docker Fundamentals Lab — Build, Push, Compose, Debug

Welcome! This lab is designed as a **simple, practical workflow** you can run in class. You’ll containerize a tiny web app, build and tag an image, push it to **your** container registry, wire that image into a Compose file, bring it up, and then do bite‑sized debugging quickfires.

> Estimated time: 45–75 minutes • Difficulty: Beginner

---

## What you’ll use
- Docker Engine + Compose v2
- A registry account (Docker Hub works great)

Directory map:
```
starter/                 # tiny Flask app you will containerize
compose/app-compose.template.yml
debug/
  compose-port-mismatch.yml
  compose-wrong-tag.yml
  compose-unhealthy.yml
  broken-cmd/
    Dockerfile
    app.py
    compose.yml
```

---

## Part A — Create a Dockerfile (10–15 min)

**Goal:** Containerize the app in `starter/app/`.

1. Open `starter/` and create a file named **Dockerfile** with these requirements:
   - Base image: `python:3.11-slim`
   - `WORKDIR /app`
   - Copy `requirements.txt` then install: `pip install --no-cache-dir -r requirements.txt`
   - Copy the rest of the app
   - Default env: `PORT=5000`
   - Expose port 5000
   - Start command: `python app.py`
2. From inside `starter/`, build and tag the image:
   ```bash
   docker build -t <your-registry-username>/simple-web:v1 .
   ```

**Checkpoint:** Run it locally.
```bash
docker run --rm -p 8080:5000 -e WHO="You" <your-registry-username>/simple-web:v1
# open http://localhost:8080
# CTRL+C to stop
```

📝 **Paste your image URI here:** `_________________________________________`

---

## Part B — Push to your registry (5–10 min)

1. Log in if you haven’t:
   ```bash
   docker login
   ```
2. Push:
   ```bash
   docker push <your-registry-username>/simple-web:v1
   ```

✅ **Deliverable:** The image is visible under your account online.

---

## Part C — Compose it (10–15 min)

**Goal:** Use your pushed image in Compose.

1. Open `compose/app-compose.template.yml` and **replace**:
   ```yaml
   image: IMAGE_URI_HERE
   ```
   with your image, e.g. `docker.io/you/simple-web:v1`
2. Bring it up:
   ```bash
   docker compose -f compose/app-compose.template.yml up -d
   docker compose -f compose/app-compose.template.yml ps
   docker compose -f compose/app-compose.template.yml logs -f
   ```
3. Visit http://localhost:8080 and confirm the healthcheck passes.

🧹 Tear down when done:
```bash
docker compose -f compose/app-compose.template.yml down
```

---

## Part D — Debugging quickfires (10–25 min)

Each quickfire is a **small broken scenario**. Launch it, inspect, and fix. Keep notes of the minimal fix.

### 1) Port mismatch
File: `debug/compose-port-mismatch.yml`
```bash
docker compose -f debug/compose-port-mismatch.yml up -d
docker compose -f debug/compose-port-mismatch.yml ps
docker compose -f debug/compose-port-mismatch.yml logs -f
```
**Question:** Why can’t you reach the app at http://localhost:8080 ? What one‑line change fixes it?  
**Hint:** Container port ≠ host mapping.

---

### 2) Wrong image tag
File: `debug/compose-wrong-tag.yml`
```bash
docker compose -f debug/compose-wrong-tag.yml up -d
docker compose -f debug/compose-wrong-tag.yml ps
```
**Question:** Why is the service stuck in `ImagePullBackOff` / `NotFound`?  
**Hint:** Compare the tag in the file vs. what exists in your registry.

---

### 3) Broken CMD
Folder: `debug/broken-cmd/`
```bash
cd debug/broken-cmd
docker compose -f compose.yml up --build
```
**Question:** Why does the container exit immediately? What single line should you change?  
**Hint:** `server.py` vs `app.py`.

---

### 4) Unhealthy healthcheck
File: `debug/compose-unhealthy.yml`
```bash
docker compose -f debug/compose-unhealthy.yml up -d
docker compose -f debug/compose-unhealthy.yml ps
```
**Question:** Why does the container remain `unhealthy`? What endpoint does the app actually expose?  
**Hint:** Try curling the container at `localhost:5000` from inside: `docker exec -it <container> sh`

---

## Handy commands
```bash
docker build -t repo/name:tag .
docker run --rm -p 8080:5000 repo/name:tag
docker push repo/name:tag

docker compose -f FILE up -d
docker compose -f FILE ps
docker compose -f FILE logs -f
docker compose -f FILE down
```

---

## (Optional) Answer key
<details><summary>Show fixes</summary>

- **Port mismatch:** change `ports: "8080:5001"` → `"8080:5000"` (or make the app listen on 5001).  
- **Wrong tag:** update `image:` to a tag that exists (e.g., `<you>/simple-web:v1`).  
- **Broken CMD:** in `debug/broken-cmd/Dockerfile`, set `CMD ["python", "app.py"]` and add `pip install -r requirements.txt` if you want real Flask.  
- **Unhealthy:** healthcheck points to `/status` but the app exposes `/health`. Change the test to curl `/health` or update the app to serve `/status` too.

</details>

Have fun; break things gently, fix them surgically.

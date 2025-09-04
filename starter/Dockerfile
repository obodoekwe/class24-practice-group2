# syntax=docker/dockerfile:1.7
FROM python:3.11-slim

# Good defaults: no .pyc, unbuffered logs, and no pip cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# If your app *truly* needs curl at runtime, uncomment:
# RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Keep layer caching: deps first
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Then app code
COPY . .

# Drop privileges
RUN useradd -m app && chown -R app:app /app
USER app

EXPOSE 5000
CMD ["python", "app.py"]

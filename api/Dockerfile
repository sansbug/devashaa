# Backend: Flask + Swiss Ephemeris. Build context is ./api (self-contained).
FROM python:3.11-slim

# tzdata for historical timezone offsets (birth-time → UTC needs the full db).
RUN apt-get update && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code + the .se1 ephemeris files (ephe/ ships inside the image, ~1.9 MB).
COPY . .

# Render (and most hosts) inject $PORT. Default 5174 for local `docker run`.
ENV PORT=5174
EXPOSE 5174

# gunicorn, not the Flask dev server. swisseph config is thread-local and every
# entry point calls _configure_thread(), so gthread workers are safe here.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 60 app:app"]

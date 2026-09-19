# Explicit Docker build avoids Railpack/BuildKit's generated secret mounts.
# Railway environment variables are supplied only when the container runs.
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Native runtime support for OCR, PDF rendering and numerical Python wheels.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        g++ \
        libgomp1 \
        libstdc++6 \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /usr/sbin/nologin nabil \
    && chown -R nabil:nabil /app

USER nabil

EXPOSE 8080

# Shell form lets Railway's PORT expand at runtime; no build secrets needed.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]

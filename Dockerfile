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
# Use CPU-only PyTorch for multilingual embeddings, not multi-GB CUDA wheels.
RUN python -m pip install --no-cache-dir 'torch==2.5.1+cpu' --index-url https://download.pytorch.org/whl/cpu
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Fail the image build if the production landing/learning UI contract regresses.
RUN python -m scripts.validate_nabil_ui \
    && python -m scripts.test_ui_integration \
    && python -m scripts.test_worksheet_exports \
    && python -m py_compile app/main.py app/api/routes_chat.py app/api/routes_worksheet.py scripts/start_server.py

RUN useradd --create-home --shell /usr/sbin/nologin nabil \
    && chown -R nabil:nabil /app

USER nabil

EXPOSE 8080

# Resolve Railway's PORT in Python; compatible with both Docker CMD and Railway overrides.
CMD ["python", "-m", "scripts.start_server"]

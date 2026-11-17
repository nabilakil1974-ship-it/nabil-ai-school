FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-ara tesseract-ocr-fra tesseract-ocr-eng && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY school-directors-archive/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY school-directors-archive/ ./
ENV PORT=10000
CMD ["sh","-c","uvicorn app:app --host 0.0.0.0 --port ${PORT}"]

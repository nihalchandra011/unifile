# Smaller base cuts build time and size
FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install only what we need, without recommended extras
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer libreoffice-calc libreoffice-impress libreoffice-draw \
    fonts-dejavu fonts-liberation \
    ghostscript qpdf imagemagick \
    tesseract-ocr tesseract-ocr-eng \
    ocrmypdf \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# requirements.txt is already next to this Dockerfile in /backend
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy the backend source
COPY . /app

ENV PORT=8080
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "—port", "8080"]

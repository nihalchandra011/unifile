# backend/Dockerfile
FROM ubuntu:24.04


ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
libreoffice \
libreoffice-writer libreoffice-impress libreoffice-calc \
imagemagick ghostscript python3 python3-pip && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
COPY . /app


ENV PORT=8080
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

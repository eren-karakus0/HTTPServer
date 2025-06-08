FROM python:3.9-slim

WORKDIR /app

# Kod ve statikleri kopyala
COPY server.py .
COPY static ./static

# Log dosyası yaratılabilmesi için izin
RUN touch server.log

# Port exposeları
EXPOSE 8080

# Başlatma komutu
CMD ["python", "server.py"]

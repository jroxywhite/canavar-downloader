# Python 3.10 tabanlı bir Linux imajı kullan
FROM python:3.10-slim

# Sunucuya FFmpeg ve gerekli sistem araçlarını yükle
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Çalışma dizinini ayarla
WORKDIR /app

# Dosyaları kopyala
COPY . .

# Python kütüphanelerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı başlat (Gunicorn ile)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
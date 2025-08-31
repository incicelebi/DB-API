# Python 3.10 tabanlı minimal imaj
FROM python:3.10-slim

# Çalışma dizini oluştur
WORKDIR /app

# Gereksinim dosyasını kopyala
COPY requirements.txt .

# Gereksinimleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . .

# Uygulamayı başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

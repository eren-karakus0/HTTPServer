# Basit Python HTTP Sunucusu

Bu proje, Python ile sıfırdan geliştirilmiş, Docker ile containerize edilebilen basit bir HTTP sunucusudur.

## Özellikler

- `GET` ve `HEAD` isteklerini destekler  
- `/static` klasöründeki HTML/CSS/JS dosyalarını sunar  
- `/api/hello` endpoint’inden JSON döner  
- `POST /api/echo` ile gönderilen JSON’u geri döner  
- MIME tipi yönetimi  
- Çoklu bağlantı desteği (threading)  
- 404, 500, 501 hata kodları  
- İstekleri `server.log` dosyasına yazar  

## Kurulum

1. Depoyu klonlayın:  
   ```bash
   git clone https://github.com/eren-karakus0/HTTPServer.git
   cd HTTPServer

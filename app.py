import time
import random
import os
from google import genai
# Prometheus kütüphanesini ve sayaç modüllerini içeri alıyoruz
from prometheus_client import start_http_server, Counter

# 1. PROMETHEUS METRİKLERİNİ TANIMLAMA
# 'http_requests_total' adında bir sayaç oluşturuyoruz ve status (200 veya 500) etiketini ekliyoruz
REQUEST_COUNTER = Counter(
    'http_requests_total', 
    'Toplam HTTP istek sayisi ve durum kodlari', 
    ['status', 'method', 'path']
)

# 2. GEMINI GÜVENLİK AYARI (TOKEN KORUMASI)
# Ortam değişkenlerinde gerçek anahtar yoksa sistem tamamen BEDAVA modda çalışır
API_KEY = os.environ.get("AI_API_KEY", "")
MOCK_MODE = API_KEY == "" or API_KEY == "mock"

print("🚀 HTTP Log Streamer ve Prometheus Metrik Sunucusu Baslatildi...", flush=True)

# Prometheus'un sayıları toplayacağı gizli kapıyı (port 8000) açıyoruz
try:
    start_http_server(8000)
    print("📊 Prometheus metrikleri http://localhost:8000/metrics adresinden yayinlaniyor.", flush=True)
except Exception as e:
    print(f"⚠️ Prometheus sunucusu baslatilamadi (Muhtemelen port kullanimda): {str(e)}", flush=True)

METHODS = ["GET", "POST", "PUT", "DELETE"]
PATHS = ["/api/v1/users", "/login", "/health", "/api/v1/products", "/checkout"]
ERROR_POOL = [
    "500 Internal Server Error: Database connection lost.",
    "500 Internal Server Error: Redis connection refused.",
    "500 Internal Server Error: NullPointerException in Auth Service."
]

while True:
    zar = random.randint(1, 100)
    method = random.choice(METHODS)
    path = random.choice(PATHS)
    
    if zar <= 85:
        # BAŞARILI DURUM: Ekrana log bas ve Prometheus sayacını (200 OK) olarak 1 artır
        print(f"[INFO] 127.0.0.1 - - {method} {path} HTTP/1.1 200 OK", flush=True)
        REQUEST_COUNTER.labels(status="200", method=method, path=path).inc()
    else:
        # HATALI DURUM: Ekrana log bas ve Prometheus sayacını (500 Error) olarak 1 artır
        secilen_hata = random.choice(ERROR_POOL)
        print("\n------------------------------------------------------------", flush=True)
        print(f"[ERROR] 127.0.0.1 - - {method} {path} HTTP/1.1 {secilen_hata}", flush=True)
        REQUEST_COUNTER.labels(status="500", method=method, path=path).inc()
        
        if MOCK_MODE:
            # %100 BEDAVA TEST ALANI (Token harcamaz)
            print("[TEST MODU] Gercek API_KEY bulunamadi. Sahte Gemini Servisi kullaniliyor...", flush=True)
            time.sleep(0.5)  # Yapay zeka gecikme simülasyonu
            print(f"GEMINI ANALIZI (MOCK):\n[BEDAVA ANALIZ] {secilen_hata} icin lokal test cozumu uretildi. Cüzdan güvende.", flush=True)
        else:
            # GERÇEK MOD (Sadece sen istersen açılır)
            print("[INFO] Hata analizi icin GERCEK Gemini API'ye baglaniliyor...", flush=True)
            try:
                client = genai.Client(api_key=API_KEY)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Sen kidemli bir DevOps muhendisisin. Su HTTP 500 hatasini analiz et ve cok kisa, tek satirlik bir cozum onerisi yaz: {secilen_hata}"
                )
                print(f"GEMINI ANALIZI:\n{response.text}", flush=True)
            except Exception as e:
                print(f"[ERROR] Gemini API cagrisi basarisiz oldu: {str(e)}", flush=True)
                
        print("------------------------------------------------------------\n", flush=True)
                
    time.sleep(4)

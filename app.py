import time
import random
import os
from google import genai

API_KEY = os.environ.get("AI_API_KEY", "")

print(" HTTP Log Streamer Baslatildi...", flush=True)

METHODS = ["GET", "POST", "PUT", "DELETE"]
PATHS = ["/api/v1/users", "/login", "/health", "/api/v1/products", "/checkout"]
ERROR_POOL = [
    "500 Internal Server Error: Database connection lost.",
    "500 Internal Server Error: Redis connection refused.",
    "500 Internal Server Error: NullPointerException in Auth Service."
]

while True:
    zar = random.randint(1, 100)
    
    if zar <= 85:
        method = random.choice(METHODS)
        path = random.choice(PATHS)
        print(f"[INFO] 127.0.0.1 - - {method} {path} HTTP/1.1 200 OK", flush=True)
    else:
        secilen_hata = random.choice(ERROR_POOL)
        method = random.choice(METHODS)
        path = random.choice(PATHS)
        
        print("\n------------------------------------------------------------", flush=True)
        print(f"[ERROR] 127.0.0.1 - - {method} {path} HTTP/1.1 {secilen_hata}", flush=True)
        print("[INFO] Hata analizi icin Gemini API'ye baglaniliyor...", flush=True)
        
        if not API_KEY or API_KEY == "":
            print("[WARN] AI_API_KEY bulunamadi! Yapay zeka analizi atlaniyor.", flush=True)
        else:
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

from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
from datetime import datetime

app = FastAPI()

# --- MONGO DB BAĞLANTISI ---
# Görselindeki orijinal srv linkini aldım ve senin şifrenle (G8raxRc2UnkNRly) jilet gibi birleştirdim aga.
MONGO_URL = "mongodb+srv://sunia3844_db_user:G8raxRc2UnkNRly@divine.bcfiwr4.mongodb.net/?retryWrites=true&w=majority&appName=divine"

client = pymongo.MongoClient(MONGO_URL)
db = client["DivineInfectionDB"]  # Kalıcı veri tabanı (Database) adın
collection = db["OyuncuVerileri"]  # Bilgilerin saklanacağı döküman tablosu (Collection)

class OyuncuVerisi(BaseModel):
    UserId: int
    UserName: str
    Gold: int

@app.get("/")
def home():
    # Cron-job.org buraya gelip GET isteği atacak ve bu temiz çıktıyı okuyacak.
    # Böylece Render 15 dakika hareketsiz kalmayıp kış uykusuna YATAMAYACAK!
    return {"durum": "Sunucu uyanik ve tetikte!", "zaman": str(datetime.now())}

@app.post("/kaydet")
def veri_kaydet(veri: OyuncuVerisi):
    # Roblox'tan veri fırlatıldığında burası tetiklenir
    print(f"Roblox'tan Gelen -> ID: {veri.UserId}, Isim: {veri.UserName}, Altin: {veri.Gold}")
    
    # Kalıcı deftere (MongoDB) veriyi güvenle yazma / güncelleme (Upsert) işlemi:
    collection.update_one(
        {"UserId": veri.UserId},  # Listede bu ID'de biri var mı?
        {"$set": {"UserName": veri.UserName, "Gold": veri.Gold, "SonKayit": datetime.now()}},  # Varsa altınını güncelle
        upsert=True  # Yoksa sıfırdan yeni kayıt satırı aç
    )
    
    return {"status": "success", "mesaj": f"{veri.UserName} verisi kalici deftere işlendi!"}
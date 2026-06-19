import os

import firebase_admin
from firebase_admin import credentials, firestore

path = "/etc/secrets/serviceaccountkey.json"

db = None

try:
    if os.path.exists(path):
        if not firebase_admin._apps:
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
    else:
        print("Firebase anahtarı bulunamadı; veritabanı devre dışı.")
except Exception as e:
    print(f"Firebase başlatılamadı, veritabanı devre dışı: {e}")
    db = None


def check_db_connection():
    if db is None:
        return False
    try:
        db.collection("test_connection").limit(1).get()
        return True
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        return False
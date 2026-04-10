import firebase_admin
from firebase_admin import credentials, firestore
import os


current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, "serviceAccountKey.json")


if not firebase_admin._apps:
    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def check_db_connection():
    try:
        
        db.collection("test_connection").get()
        return True
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        return False
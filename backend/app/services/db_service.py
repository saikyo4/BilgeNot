from datetime import datetime

from app.database import firebase_config


class DBService:
    @staticmethod
    def save_result(operation: str, input_text: str, output_text: str):

        db = firebase_config.db
        if db is None:
            return None
        try:
            doc = {
                "operation": operation,
                "input_text": input_text,
                "output_text": output_text,
                "created_at": datetime.now().isoformat(),
            }
            ref = db.collection("results").add(doc)
            return ref[1].id
        except Exception as e:
            print(f"Veritabanına kayıt hatası: {e}")
            return None
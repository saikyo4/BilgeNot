import os
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def summarize_text(self, text: str):
        if not text:
            return "Özetlenecek metin bulunamadı."
        
        prompt = f"Aşağıdaki ders notunu sınav öncesi tekrar edilebilecek şekilde özetle:\n\n{text}"
        response = self.model.generate_content(prompt)
        return response.text

    def generate_quiz(self, text: str):
        if not text:
            return "Quiz oluşturulacak metin bulunamadı."
            
        prompt = f"Aşağıdaki metne dayanarak 3 soruluk çoktan seçmeli quiz hazırla. Şıklar A, B, C, D olsun. Cevap anahtarını en sona ekle:\n\n{text}"
        response = self.model.generate_content(prompt)
        return response.text

gemini_service = GeminiService()

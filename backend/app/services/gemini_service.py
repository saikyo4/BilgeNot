import os
from google import genai


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else None
        self.model_name = "gemini-2.0-flash"

    def _generate(self, prompt: str) -> str:
        if self.client is None:
            return "Yapılandırma hatası: GEMINI_API_KEY tanımlı değil."
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text

    def summarize_text(self, text: str):
        if not text:
            return "Özetlenecek metin bulunamadı."
        prompt = (
            "Aşağıdaki ders notunu sınav öncesi tekrar edilebilecek şekilde özetle:\n\n"
            f"{text}"
        )
        return self._generate(prompt)

    def generate_quiz(self, text: str):
        if not text:
            return "Quiz oluşturulacak metin bulunamadı."
        prompt = (
            "Aşağıdaki metne dayanarak 3 soruluk çoktan seçmeli quiz hazırla. "
            "Şıklar A, B, C, D olsun. Cevap anahtarını en sona ekle:\n\n"
            f"{text}"
        )
        return self._generate(prompt)


gemini_service = GeminiService()
from langchain_ollama import OllamaLLM

class OllamaClient:
    def __init__(self, model_name: str ="llama3:8b"):
        print(f"{model_name} başlatılıyor")
        self.OllamaLLM = OllamaLLM(model=model_name)
        print("Başlatıldı")

    def invoke(self, prompt: str)-> str:
        #verilen prompt ile modeli çağırıp yanıtı döndürür
        try:
            response = self.OllamaLLM.invoke(prompt)
            return response
        except Exception as e:
            return f"Bir hata oluştu: {e}"
import json
import os
import asyncio
from typing import Dict, Any, Optional



class PromptService:
    """
    JSON dosyasından prompt konfigürasyonlarını asenkron olarak yükler ve erişimi sağlar.
    """

    def __init__(self, file_path: str = "prompts.json"):

       #olurda prompt.json yerini değiştirdikten sonra hata alırsanız bu satırdan düzenleyin !!

        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', file_path)
        self.prompts: Dict[str, Any] = {}
        # NOT: __init__ metodu asenkron olamaz. Yükleme işlemini
        # sınıf örneği oluşturulduktan sonra, harici bir async fonksiyonla çağırmalıyız.
        print("PromptService başlatıldı. Yükleme için 'await service.load_prompts()' çağırılmalı.")

    async def load_prompts(self):
        #jsonu çeker ve self.prompts a yükler
        print(f"🔄 Prompt dosyasını asenkron olarak okuyor: {self.file_path}")

        # 1. Dosya Kontrolü (asyncio.to_thread ile senkron I/O'yu yönetme)
        file_exists = await asyncio.to_thread(os.path.exists, self.file_path)
        if not file_exists:
            raise FileNotFoundError(f"HATA: Prompt dosyası bulunamadı: {self.file_path}")

        # 2. Dosya Okuma ve JSON Yükleme (asyncio.to_thread ile yönetme)
        try:
            def sync_load():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)

            # Senkron işi asenkron bağlamda çalıştır
            self.prompts = await asyncio.to_thread(sync_load)
            print(f"✅ Promptlar başarıyla yüklendi. {len(self.prompts.keys())} anahtar.")

        except json.JSONDecodeError as e:
            raise ValueError(f"HATA: prompts.json dosyası bozuk. JSON hatası: {e}")
        except Exception as e:
            raise Exception(f"Beklenmedik yükleme hatası: {e}")

    def get_prompt(self, category: str, key: str, **kwargs) -> Optional[str]:
       #promptu çekiyor
        if not self.prompts:
            raise RuntimeError("PromptService yüklenmemiş. Lütfen önce 'await service.load_prompts()' çağırın.")

        prompt_template = self.prompts.get(category, {}).get(key)

        if prompt_template is None:
            print(f"⚠️ UYARI: '{category}.{key}' prompt anahtarı bulunamadı.")
            return None

        # Formatlama (senkron işlem)
        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            print(f"HATA: Prompt '{key}' içinde formatlanması gereken değişken eksik: {e}")
            return prompt_template


# --- Kullanım Örneği ---
async def main_test():
    # 1. Sınıfı başlat
    service = PromptService(file_path="ollama/prompt.json")  # Dosya adını ayarlayın

    # 2. Asenkron yükleme metodunu çağır ve await ile bekle
    # Bu adımı atlamak RuntimeError fırlatır!
    await service.load_prompts()

    # 3. Prompt'u çek
    prompt = service.get_prompt(
        category="SYSTEM_INSTRUCTIONS",
        key="SUMMARY_EXPERT",
        length="uzun ve detaylı"
    )
    print("\nÇekilen Prompt:")
    print(prompt)


if __name__ == "__main__":
    # test etmek için eğer yoksa ollamanın altına prompt.json yazın, ya da varolan dosyayı oraya taşıyın.
    asyncio.run(main_test())
    pass
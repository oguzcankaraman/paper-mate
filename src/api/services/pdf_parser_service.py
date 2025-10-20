from langchain_core.documents import Document
from pdf_processing.pdf_parser import PdfProcessor
from typing import Dict, Any, List


class PdfParserService:
    def __init__(self):
        self.pdf_processor = PdfProcessor()
        print("PdfParserService başlatıldı")

    async def api_parse_pdf(self, pdf_path: str) -> Dict[str, Any]:

        try:
            # pdf_processor'daki metodun async olduğunu varsayıyoruz.
            parsed_document: List[Document] = await self.pdf_processor.parse_pdf(pdf_path=pdf_path)


            return {
                "success": True,
                # 2. İYİLEŞTİRME: İşlenen metni ayrı bir alanda döndürmek daha kullanışlıdır.
                "message": "PDF başarıyla işlendi.",
                "page_content": parsed_document.page_content,
                "metadata": parsed_document.metadata  # İsteğe bağlı, metadatayı da ekleyebiliriz.
            }


        except FileNotFoundError:
            return {
                "success": False,
                "message": f"Hata: Belirtilen yolda PDF dosyası bulunamadı: {pdf_path}"
            }
        except Exception as e:
            # Hata kodu yerine, net bir hata mesajı döndürmek kullanıcı için daha faydalıdır.
            print(f"PDF işlenirken beklenmedik bir hata oluştu: {e}")
            return {
                "success": False,
                "message": f"PDF işlenirken beklenmedik bir hata oluştu. Detay: {type(e).__name__} - {str(e)}"
            }
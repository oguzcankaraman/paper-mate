from langchain_core.documents import Document
from src.pdf_processing.pdf_parser import PdfProcessor  # pdf_processor.py'den içe aktarılıyor
from typing import Dict, Any, List

class PdfParserService:
    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 150):
        # PdfProcessor'ı başlatırken chunking parametrelerini de geçirebiliriz.
        # Bu, PdfProcessor sınıfının yapıcı (constructor) metoduna bağlıdır.
        # (Önceki cevaplarda PdfProcessor'a bu parametreleri eklemiştik.)
        self.pdf_processor = PdfProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        print("PdfParserService başlatıldı.")

    # Yeni ve İyileştirilmiş Metot: Hem Yükleme hem Parçalama
    async def api_process_and_chunk_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        PDF'i yükler, formatlar, parçalara ayırır ve API için uygun bir JSON yanıtı döndürür.
        """
        try:
            print(f"API isteği alındı. PDF yolu: {pdf_path}")

            # TEK METOT ÇAĞRISI: Hem yükleme hem de parçalama işlemini yapar.
            # PdfProcessor'da bu metodu kullandığınızı varsayıyoruz.
            chunks: List[Document] = await self.pdf_processor.process_and_chunk_pdf(pdf_path=pdf_path)

            if not chunks:
                return {
                    "success": True,
                    "message": "PDF başarıyla yüklendi ancak parçalanacak içerik bulunamadı veya yükleme başarısız oldu.",
                    "chunks": []
                }

            # İYİLEŞTİRME: Document Listesi'ni API için uygun bir JSON Listesi'ne çevirme
            chunk_data = []
            for chunk in chunks:
                chunk_data.append({
                    "content": chunk.page_content,
                    "metadata": chunk.metadata,
                    "length": len(chunk.page_content)
                })

            return {
                "success": True,
                "message": f"PDF başarıyla işlendi ve {len(chunk_data)} parçaya ayrıldı.",
                "total_chunks": len(chunk_data),
                "chunks": chunk_data  # İşlenen ve parçalanan metinlerin listesi
            }


        except FileNotFoundError:
            return {
                "success": False,
                "message": f"Hata: Belirtilen yolda PDF dosyası bulunamadı: {pdf_path}"
            }
        except Exception as e:
            # Beklenmeyen hataları yakalama
            print(f"PDF işlenirken beklenmedik bir hata oluştu: {e}")
            return {
                "success": False,
                "message": f"PDF işlenirken beklenmedik bir hata oluştu. Detay: {type(e).__name__} - {str(e)}"
            }

    # Not: Eski parse_pdf metodu (sadece yükleme yapan) artık bu serviste gerekli olmayabilir.
    # Ancak yine de kullanmak isterseniz aşağıdaki gibi güncelleyebilirsiniz:
    # async def api_parse_pdf_legacy(self, pdf_path: str) -> Dict[str, Any]:
    #     try:
    #         parsed_documents: List[Document] = await self.pdf_processor.parse_pdf(pdf_path=pdf_path)
    #         # Document Listesi'ni API için uygun JSON Listesi'ne çevirme burada da yapılmalıdır.
    #         return {"success": True, "message": "PDF başarıyla yüklendi (Parçalanmadı).", "documents": [d.dict() for d in parsed_documents]}
    #     except Exception as e:
    #         return {"success": False, "message": f"Hata: {str(e)}"}
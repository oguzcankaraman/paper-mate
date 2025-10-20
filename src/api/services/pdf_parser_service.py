from langchain_core.documents import Document
from src.pdf_processing.pdf_parser import PdfProcessor


class PdfParserService:
    def __init__(self):
        self.pdfPross = PdfProcessor()
        print("PdfParserService başlatıldı")

    async def api_parse_pdf(self, pdf_path: str) -> dict:
        try:
            parse_message: Document = await self.pdfPross.pdf_parser(pdf_path=pdf_path)
            return{
                    "success": True,
                    "parse_message": " pdf_path başarıyla alındı: "+  parse_message

            }
        except Exception as e:
            return {
                    "success": False,
                    "parse_message": "Hata alındı, kodu: " + str(e)

            }


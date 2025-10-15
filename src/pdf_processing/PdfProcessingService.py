from typing import List

from langchain_core.documents import Document

from pdf_parser import pdf_parser
from text_processor import splitter


class PdfProcessingService:
    def __init__(self):
        pass


    @staticmethod
    def parser(pdf_path)-> List[Document]:
        docs = pdf_parser(pdf_path)
        return docs

    @staticmethod
    def spliter(documents:List[Document])-> List[Document]:
        text = splitter(documents)
        return text

    def pdf_processor(self, pdf_path)-> List[Document]:
        docs = self.parser(pdf_path)
        text = self.spliter(docs)
        return text

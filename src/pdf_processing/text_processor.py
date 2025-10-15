from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.pdf_processing.pdf_parser import pdf_parser


def splitter(documents:List[Document])-> List[Document]:

    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
    )
    texts = text_splitter.split_documents(documents)

    return texts





if __name__ == "__main__":
    pdf_path = input("📄 PDF dosya yolunu girin: ").strip().strip('"')
    docs = pdf_parser(pdf_path)

    tester = splitter(docs)
    for i,text in enumerate(tester):
        print(f"\n--- {i + 1} ---")
        print(tester[i])






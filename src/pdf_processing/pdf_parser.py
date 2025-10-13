import pprint
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("C:/Users/goktu/OneDrive/Masaüstü/pdf_sample_file_50KB.pdf")

docs = loader.load()

for i ,doc in enumerate(docs):
    print(f"--- Sayfa {i + 1} ---")
    print(doc.page_content)
    pprint.pprint(doc.metadata)
    print()







from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


import os


# === Settings ===
PDF_PATH = "data/scotia.pdf"  # 📝 Make sure this PDF exists
CHROMA_DIR = "db"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_and_split_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Optional: tune the chunk size
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    return chunks

def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    vectordb.persist()
    print(f"✅ Vector store built and saved to '{CHROMA_DIR}'")

if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        print(f"❌ PDF not found at: {PDF_PATH}")
    else:
        chunks = load_and_split_pdf(PDF_PATH)
        build_vectorstore(chunks)

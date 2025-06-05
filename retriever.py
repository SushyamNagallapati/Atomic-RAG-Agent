from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# Settings
CHROMA_DIR = "db"  # folder to store your vector DB
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load ChromaDB index
embedding_function = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_function)

def get_relevant_documents(query: str, k: int = 3):
    """
    Retrieves top-k relevant chunks from the vector store.
    """
    return vectordb.similarity_search(query, k=k)

"""Embed chunks and store them in a local Chroma vector database.

Chroma is an embedded vector DB (no server). The index is persisted under
data/vectorstore so we don't re-embed on every run.
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import settings, VECTORSTORE_DIR
from app.ingest.loader import load_corpus
from app.ingest.chunker import chunk_pages

COLLECTION = "rbi_corpus"

def get_embeddings() -> HuggingFaceEmbeddings:
    """The local embedding model (load offline; see app.config)."""
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)

def get_vectorstore() -> Chroma:
    """Open the persisted Chroma index (reused by the retriever in step 5)."""
    return Chroma(
        collection_name=COLLECTION,
        embedding_function=get_embeddings(),
        persist_directory=str(VECTORSTORE_DIR)
    )

def build_index(chunks: list[Document]) -> Chroma:
    """Embed chunks and persist them to the Chroma index"""
    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=COLLECTION,
        persist_directory=str(VECTORSTORE_DIR)
    )

if __name__ == "__main__":
    chunks = chunk_pages(load_corpus())
    print(f"embedding {len(chunks)} chunks ...")
    vs = build_index(chunks)
    print("index built. total vectors:", vs._collection.count())
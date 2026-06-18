"""Split loaded pages into overlapping chunks for retrieval.

Each chunk is a LangChain Document carrying its source + page in metadata, so a
retrieved chunk can always be cited precisely.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.ingest.loader import LoadedPage, load_corpus

def chunk_pages(pages: list[LoadedPage]) -> list[Document]:
    """Split each page into overlapping chunks, preserving citation metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )

    docs: list[Document] = []
    for p in pages:
        for j, piece in enumerate(splitter.split_text(p.text)):
            docs.append(
                Document(
                    page_content=piece,
                    metadata={
                        "source": p.source,
                        "filename": p.filename,
                        "page" : p.page,
                        "chunk": j,
                    }
                )
            )
    return docs

if __name__ == "__main__":
    chunks = chunk_pages(load_corpus())
    print(f"made {len(chunks)} chunks")
    if chunks:
        c = chunks[0]
        print(f"sample -> {c.metadata} | {c.page_content[:120]!r}")
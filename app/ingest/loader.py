"""Load raw documents (RBI PDFs) from data/corpus into page-level records.

Each page keeps metadata (clean title + page number) so that retrieved chunks
can be traced back to an exact, citable source — non-negotiable for a
compliance tool.
"""

from dataclasses import dataclass

from pypdf import PdfReader

from app.config import CORPUS_DIR

# Map technical filenames -> clean citation titles
TITLES = {
    "rbi-digital-lending-directions-2025.pdf": "RBI (Digital Lending) Directions, 2025",
    "rbi-kyc-master-direction-2025.pdf": "RBI KYC Master Direction, 2016 (2025 update)",
}


@dataclass
class LoadedPage:
    source: str     # clean title for citations
    filename: str   # actual filename
    page: int       # 1-based page number
    text: str


def load_corpus() -> list[LoadedPage]:
    """Read every PDF in data/corpus and return one LoadedPage per non-empty page."""
    pages: list[LoadedPage] = []

    for path in sorted(CORPUS_DIR.glob("*.pdf")):
        reader = PdfReader(path)
        title = TITLES.get(path.name, path.stem)

        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                continue  # skip blank / image-only pages
            pages.append(
                LoadedPage(
                    source=title,
                    filename=path.name,
                    page=i,
                    text=text,
                )
            )

    return pages


if __name__ == "__main__":
    pages = load_corpus()
    print(f"loaded {len(pages)} pages from {CORPUS_DIR}")
    if pages:
        first = pages[0]
        print(f"sample -> {first.source} | p.{first.page} | {first.text[:120]!r}")

"""Ingest pipeline: turn raw RBI PDFs into a searchable index.

    loader.py      read PDFs from data/corpus -> plain text + metadata
    chunker.py     split long documents into retrievable chunks
    embed_store.py embed chunks and store them in the vector DB (Chroma)

Run order:  loader -> chunker -> embed_store.  Built in Week 2-3.
"""

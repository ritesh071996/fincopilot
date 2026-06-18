"""Throwaway check that local embeddings work offline. Delete after Step 1."""

import os

# Load the model from local cache only (avoids the torch+SSL segfault on Windows).
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from langchain_huggingface import HuggingFaceEmbeddings

emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vec = emb.embed_query("What is a Lending Service Provider?")
print("vector length:", len(vec))
print("first 5 numbers:", vec[:5])

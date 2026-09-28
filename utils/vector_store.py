import faiss
import numpy as np


def create_index(embeddings):
    """Create a FAISS IndexFlatL2 index and store embedding vectors."""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.asarray(embeddings, dtype="float32"))
    return index


def search(index, query_embedding, k=3):
    """Return the top-k nearest vectors using squared L2 distance."""
    distances, indices = index.search(
        np.asarray(query_embedding, dtype="float32"),
        k
    )
    return distances, indices

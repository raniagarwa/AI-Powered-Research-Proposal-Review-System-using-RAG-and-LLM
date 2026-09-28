from sentence_transformers import SentenceTransformer

# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embeddings(chunks):
    """
    Convert a list of text chunks into embeddings.
    """

    embeddings =model.encode(
                             chunks,
                             normalize_embeddings=True
    )

    return embeddings
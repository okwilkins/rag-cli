import logging
import sys

from ollama import Client
from qdrant_client import QdrantClient, models


def run_rag(
    ollama_url: str,
    qdrant_url: str,
    collection_name: str,
    top_k: int,
    min_similarity: float,
    query: str,
):
    """Runs the RAG model."""

    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)

    logger.info("Connecting to Ollama")
    ollama_client = Client(host=ollama_url)
    logger.info("Connected to Ollama")

    logger.info("Connecting to vector database")
    qdrant_client = QdrantClient(url=qdrant_url)
    logger.info("Connected to vector database")

    logger.info("Embedding query")
    query_embedding = ollama_client.embeddings(
        model="nomic-embed-text:v1.5",
        prompt=query,
    )
    logger.info("Query embedded")

    logger.info("Searching for similar vectors")
    similar_points = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding["embedding"],
        search_params=models.SearchParams(exact=False),
        score_threshold=min_similarity,
        limit=top_k,
    )

    for point in similar_points:
        print(point)


if __name__ == "__main__":
    run_rag(
        ollama_url="http://localhost:11434",
        qdrant_url="http://localhost:6333",
        collection_name="nomic-embed-text-v1.5",
        top_k=5,
        min_similarity=0.5,
        query="Shiveegovi",
    )

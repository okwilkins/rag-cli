import logging
import sys

from ollama import Client
from qdrant_client import QdrantClient, models


def run_rag(
    ollama_embedding_url: str,
    ollama_chat_url: str,
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

    logger.info("Connecting to Ollama embedding service")
    ollama_embedding_client = Client(host=ollama_embedding_url)
    logger.info("Connected to Ollama embedding service")

    logger.info("Connecting to Ollama chat service")
    ollama_chat_client = Client(host=ollama_chat_url)
    logger.info("Connected to Ollama chat service")

    logger.info("Connecting to vector database")
    qdrant_client = QdrantClient(url=qdrant_url)
    logger.info("Connected to vector database")

    logger.info("Embedding query")
    query_embedding = ollama_embedding_client.embeddings(
        model="nomic-embed-text:v1.5",
        prompt=query,
    )
    logger.info("Query embedded")

    logger.info(f"Searching for similar vectors with parameters: {collection_name=}, {top_k=}, {min_similarity=}")
    similar_points = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding["embedding"],
        search_params=models.SearchParams(exact=True),
        score_threshold=min_similarity,
        limit=top_k,
    )

    logger.info(f"Similar vectors found: {len(similar_points)}")

    text_payloads: list[str] = []

    for similar_point in similar_points:
        if similar_point.payload is None:
            continue

        if 'title' in similar_point.payload and 'extract' in similar_point.payload:
            text_payloads.append( f"Title: {similar_point.payload['title']}\n{similar_point.payload['extract']}\n")
    
    prompt_injection = "\n\n".join(text_payloads)

    logger.info("Injecting similar points into the prompt and generating the response")
    prompt_intro = (
        "You are a helpful AI assistant. You will be provided a prompt and information associated with it. "
        "You need to provide the answer to the question in the prompt.\n"
        "Associated information:\n\n"
    )
    prompt = f"{prompt_intro}\n\n{prompt_injection}"
    response = ollama_chat_client.chat(
        model="phi3:3.8b",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": query,
            }
        ],
    )
    logger.info("Response generated")

    sys.stdout.write(response["message"]["content"])  # type: ignore

import logging
import sys
import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


def run_vector_store(qdrant_url: str, collection_name: str, embedding: list[float], data: dict[str, Any]):
    """Store embeddings in the vector store."""

    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)

    logger.info("Connecting to vector database")
    client = QdrantClient(url=qdrant_url)
    logger.info("Connected to vector database")

    logger.info("Upserting vector")
    point = PointStruct(
        id=uuid.uuid4().hex,
        vector=embedding,
        payload=data,
    )

    client.upsert(collection_name=collection_name, points=[point])
    logger.info("Vector upserted")
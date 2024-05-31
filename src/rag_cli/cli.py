import argparse
import json
import re
import sys
from typing import Any


def list_of_floats(arg: str) -> list[float]:
    """Parses a list of floats."""
    try:
        arg = arg.replace("\n", "")
        pattern = r"[\[\{\<](.*?)[\]\}\>]"
        match = re.match(pattern, arg)

        if match is not None:
            arg = match.group(1)
        else:
            raise argparse.ArgumentTypeError("List must be a list of floats in the form [0.1, 0.2, ...]")
        return [float(x.strip()) for x in arg.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError("List must be a list of floats in the form [0.1, 0.2, ...]")
    

def json_dict(arg: str) -> dict[str, Any]:
    """Parses a JSON dictionary."""
    try:
        return json.loads(arg.replace("\n", "").strip())
    except json.JSONDecodeError:
        raise argparse.ArgumentTypeError("Data must be a valid JSON object")


def cli() -> argparse.Namespace:
    """Command line interface."""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        dest="command",
    )

    embedder_parser = subparsers.add_parser(
        "embed",
        help="Embeds text.",
    )

    embedder_parser.add_argument(
        "--ollama-url",
        help="The URL of the Ollama server.",
        type=str,
    )

    # Add optional stdin argument
    embedder_parser.add_argument(
        '--file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='Input file to embed (default: stdin)'
    )

    vector_store_parser = subparsers.add_parser(
        "vector-store",
        help="Stores a vector in the vector database.",
    )

    vector_store_parser.add_argument(
        "--qdrant-url",
        help="The URL of the Qdrant server.",
        type=str,
    )

    vector_store_parser.add_argument(
        "--collection-name",
        help="The name of the collection.",
        type=str,
    )

    vector_store_parser.add_argument(
        "--data",
        help="The data to store with the vector. Can be any JSON-serializable data.",
        type=json_dict,
        default={},
    )

    vector_store_parser.add_argument(
        "embedding",
        help="File with embedding to store. Must be a list of floats in the form [0.1, 0.2, ...] (default: stdin)",
        type=argparse.FileType('r'),
        nargs="?",
        default=sys.stdin,
    )

    rag_parser = subparsers.add_parser(
        "rag",
        help="Runs the RAG system.",
    )

    rag_parser.add_argument(
        "--ollama-embedding-url",
        help="The URL of the Ollama embedding server.",
        type=str,
    )

    rag_parser.add_argument(
        "--ollama-chat-url",
        help="The URL of the Ollama chat server.",
        type=str,
    )

    rag_parser.add_argument(
        "--qdrant-url",
        help="The URL of the Qdrant server.",
        type=str,
    )

    rag_parser.add_argument(
        "--collection-name",
        help="The name of the collection.",
        type=str,
    )

    rag_parser.add_argument(
        "--top-k",
        help="The number of similar vectors to return.",
        type=int,
        default=5,
    )

    rag_parser.add_argument(
        "--min-similarity",
        help="The minimum similarity to return.",
        type=float,
        default=0.5,
    )

    # Add optional stdin argument
    rag_parser.add_argument(
        '--file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='Input file to chat with (default: stdin)'
    )

    return parser.parse_args()

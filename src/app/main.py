import argparse
import logging
import sys
import json
from ollama import Client


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

    embedder_parser.add_argument(
        "--text",
        help="The text to embed.",
        type=str,
    )

    embedder_parser.add_argument(
        "--file",
        help="The file with text to embed.",
        type=str,
    )

    return parser.parse_args()


def run_embedder(text: str, ollama_url: str):
    """Runs the embedder."""
    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)

    logger.info("Connecting to Ollama")
    client = Client(host=ollama_url)
    logger.info("Connected to Ollama")

    logger.info(f"Embedding text")
    embeddings = client.embeddings(
        model="nomic-embed-text:v1.5",
        prompt=text,
    )
    embeddings["text"] = text
    logger.info("Text embedded")

    sys.stdout.write(json.dumps(embeddings)
)


def main():
    args = cli()

    if args.command in ["embed"]:
        run_embedder(
            text=args.text,
            ollama_url=args.ollama_url,
        )


if __name__ == "__main__":
    main()

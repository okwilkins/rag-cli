import argparse
import logging
import sys
import json
from typing import Optional
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


def run_embedder(ollama_url: str, text: Optional[str] = None, file: Optional[str] = None):
    """Runs the embedder."""
    if text is None and file is None:
        raise ValueError("Either text or file must be provided.")

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

    if text is None and file is not None:
        with open(file, "r") as f:
            text = f.read()

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
            file=args.file,
            ollama_url=args.ollama_url,
        )


if __name__ == "__main__":
    main()

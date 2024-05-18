<p align="center">
  <img height="100" src="https://github.com/okwilkins/rag-cli/raw/main/docs/images/logo.png" alt="RAG CLI">
</p>

<p align="center">
    <b>A project to show good CLI practices with a fully fledged RAG system.</b>
</p>

<p align=center>
    <a href="https://pypi.org/project/rag-cli/"><img src="https://img.shields.io/pypi/pyversions/rag-cli" alt="Python version"></a>
    <a href="https://pypi.org/project/rag-cli/"><img src="https://img.shields.io/pypi/v/rag-cli" alt="PyPI version"></a>
    <a href="https://github.com/okwilkins/rag-cli/raw/main/LICENSE"><img src="https://img.shields.io/badge/License-GNU%20GPL-success" alt="GNU GPL"></a>
</p>

# RAG CLI

## Installation

```bash
pip install rag-cli
```

## Features

- CLI tooling for RAG
- Embedder (Ollama)
- Vector store (Qdrant)

## Usage

### Docker

If you don't have a running instance of [Qdrant](https://qdrant.tech/) or [Ollama](https://ollama.com/), you can use the provided docker-compose file to start one.
  
```bash
docker-compose up --build -d
```

This will start Ollama on `http://localhost:11434` and Qdrant on `http://localhost:6333`.

#### Development

This project uses a dev container, which is the easiest way to set up a consistent development environment. Dev containers provide all the necessary tools, dependencies, and configuration, so you can focus on coding right away.

##### Using Dev Containers

This project uses a dev container for a consistent development environment. To get started:

1. Open the project in Visual Studio Code.
2. On Windows/Linux, press `Ctrl+Shift+P` and run the command `Remote-Containers: Reopen in Container`. On Mac, press `Cmd+Shift+P` and run the same command.
3. VS Code will build and start the dev container, providing access to the project's codebase and dependencies.

Other editors may have similar functionality but this project is optimised for Visual Studio Code.

### Embedder

Before running this command, make sure you have a running instance of [Ollama](https://ollama.com/) and the nomic-embed-text:v1.5 model is available:

```bash
ollama pull nomic-embed-text:v1.5
```

```bash
rag-cli embed --ollama-url http://localhost:11434 --file <INPUT_FILE>
```

You can alternatively use stdin to pass the text:

```bash
cat <INPUT_FILE> | rag-cli embed --ollama-url http://localhost:11434
```

### Vector store

```bash
rag-cli vector-store \
--qdrant-url http://localhost:6333 \
--collection-name <COLLECTION_NAME> \
--data '{<JSON_DATA>}'
--embedding <EMBEDDING_FILE>
```

You can alternatively use stdin to pass embeddings:

```bash
cat <INPUT_FILE> | \
rag-cli vector-store \
--qdrant-url http://localhost:6333 \
--collection-name <COLLECTION_NAME> \
--data '{<JSON_DATA>}'
```

### End-to-end Pipeline

Here is an example of an end-to-end pipeline. It takes the following steps:

- Get a random Wikipedia article
- Embed the article
- Store the embedding in Qdrant

Before running the pipeline make sure you have the following installed:

```bash
sudo apt-get update && sudo apt-get install parallel jq curl
```

Also make sure that the `data/articles` and `data/embeddings` directories exist:

```bash
mkdir -p data/articles data/embeddings
```

Then run the pipeline:

```bash
bash scripts/run_pipeline.sh
```

#### Parallel Pipeline

The script `scripts/run_pipeline.sh` can be run in parallel with [GNU Parallel](https://www.gnu.org/software/parallel/) to speed up the process.

```bash
parallel -j 5 -n0 bash scripts/run_pipeline.sh ::: {0..10}
```

## Examples

### Get 10 Random Wikipedia Articles

```bash
parallel -n0 -j 10 '
curl -L -s "https://en.wikipedia.org/api/rest_v1/page/random/summary" | \
jq -r ".title, .description, .extract" | \
tee data/articles/$(cat /proc/sys/kernel/random/uuid).txt
' ::: {0..10}
```

### Run Embedder On All Articles

```bash
parallel '
rag-cli embed --ollama-url http://localhost:11434 --file {1} 2>> output.log | \
jq ".embedding" | \
tee data/embeddings/$(basename {1} .txt) 1> /dev/null
' ::: $(find data/articles/*.txt)
```

### Store All Embeddings In Qdrant

```bash
parallel rag-cli vector-store --qdrant-url http://localhost:6333 --collection-name nomic-embed-text-v1.5 2>> output.log ::: $(find data/embeddings/*)
```

### End-to-end Pipeline For A Single Article

```bash
curl -L -s "https://en.wikipedia.org/api/rest_v1/page/random/summary" | \
jq -r ".title, .description, .extract" | \
rag-cli embed --ollama-url http://localhost:11434 | \
jq ".embedding" | \
rag-cli vector-store --qdrant-url http://localhost:6333 --collection-name nomic-embed-text-v1.5
```

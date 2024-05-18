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

## Commands

```bash
sudo apt-get update && sudo apt-get install parallel jq curl
```

```bash
mkdir -p data/articles data/embeddings
```

### Get Wikipedia articles

```bash
parallel -n0 -j 10 '
curl -L -s "https://en.wikipedia.org/api/rest_v1/page/random/summary" | \
jq -r ".title, .description, .extract" | \
tee data/articles/$(cat /proc/sys/kernel/random/uuid).txt 1> /dev/null
' ::: {0..10}
```

### Run embeder

```bash
parallel '
rag-cli embed --ollama-url http://localhost:11434 --file {1} 2>> output.log | \
jq ".embedding" | \
tee data/embeddings/$(basename {1} .txt) 1> /dev/null
' ::: $(find data/articles/*.txt)
```

### Vector store

```bash
parallel rag-cli vector-store --qdrant-url http://localhost:6333 --collection-name nomic-embed-text-v1.5 2>> output.log ::: $(find data/embeddings/*)
```

### Complete pipeline for single article

```bash
curl -L -s "https://en.wikipedia.org/api/rest_v1/page/random/summary" | \
jq -r ".title, .description, .extract" | \
rag-cli embed --ollama-url http://localhost:11434 2>> output.log | \
jq ".embedding" | \
rag-cli vector-store --qdrant-url http://localhost:6333 --collection-name nomic-embed-text-v1.5 2>> output.log
```

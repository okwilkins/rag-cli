# Python GNU Parallel

## Commands

### Get Wikipedia articles

```bash
parallel -j 10 '
curl -L -s "https://en.wikipedia.org/api/rest_v1/page/random/summary" | \
jq -r ".title, .description, .extract" | \
tee data/articles/{}.$(cat /proc/sys/kernel/random/uuid).txt 1> /dev/null
' ::: {0..100}
```

### Run embeder

```bash
parallel '
python ./src/app/main.py embed --ollama-url http://llm_backend:11434 --file {1} 2>> output.log | \
jq ".embedding" | \
tee data/embeddings/$(basename {1} .txt) 1> /dev/null
' ::: $(find data/articles/*.txt)
```

### Vector store

```bash
parallel python ./src/app/main.py vector-store --qdrant-url http://vector_db:6333 --collection-name nomic-embed-text-v1.5 2>> output.log ::: $(find data/embeddings/*)
```

### Complete pipeline for single article

```bash
curl -L -s "https://en.wikipedia.org/api/rest_v1/page/random/summary" | \
jq -r ".title, .description, .extract" | \
python ./src/app/main.py embed --ollama-url http://llm_backend:11434 2>> output.log | \
jq ".embedding" | \
python ./src/app/main.py vector-store --qdrant-url http://vector_db:6333 --collection-name nomic-embed-text-v1.5 2>> output.log
```

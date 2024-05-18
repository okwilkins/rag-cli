#!/bin/bash
# qdrant_startup.sh

./qdrant > logs.log & sleep 1

while ! curl -H "Accept: application/json" --connect-timeout 2 -s -D - "http://localhost:6333" -o /dev/null 2>/dev/null | head -n1 | grep 200 > /dev/null; do
  echo "Qdrant is not up yet. Waiting for 1 second."
  sleep 1
done

echo "Qdrant is up and running! Creating a collection."
curl -s -X PUT 'http://localhost:6333/collections/nomic-embed-text-v1.5' \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vectors": {
      "size": 768,
      "distance": "Cosine"
    }
  }'

tail -f logs.log
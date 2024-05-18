wikipedia_data=$(curl -L -s "https://en.wikipedia.org/api/rest_v1/page/random/summary")
text_to_embed=$(jq -r ".title, .description, .extract" <(echo $wikipedia_data))


embedding_data=$(
    echo $text_to_embed | \
    python ./src/app/main.py embed --ollama-url http://llm_backend:11434 2>> output.log

)

payload_data=$(jq "{title: .title, description: .description, extract: .extract}" <(echo $wikipedia_data))

echo $(jq -r ".embedding" <(echo $embedding_data)) | \
python ./src/app/main.py vector-store \
    --qdrant-url http://vector_db:6333 \
    --collection-name nomic-embed-text-v1.5 \
    --data "$payload_data"
    2>> output.log

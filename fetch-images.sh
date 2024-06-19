#!/bin/sh

# Maximum number of concurrent requests (batch size)
max_concurrent_requests=50

# Function to fetch a URL with curl
fetch_image() {
    mbid="$1"
    echo "Fetching image for $mbid"
    curl -sL https://coverartarchive.org/release/"$mbid"/front-250 --output dataset/images/"$mbid".jpg
    echo "Fetched: $mbid.jpg"
}

mkdir -p dataset/images

# Loop through URLs in batches
index=0
jq -r '.id' dataset/dataset.jsonl | while read -r mbid; do
    index=$((index+1))

    fetch_image "$mbid" &

    if [ $((index % max_concurrent_requests)) -eq 0 ]
    then
      echo "Waiting previous $max_concurrent_requests to complete."
      wait
    fi
done

wait

echo "All requests completed."
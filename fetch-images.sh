#!/bin/sh

# Maximum number of concurrent requests (batch size)
max_concurrent_requests=200

# Function to fetch a URL with curl
fetch_image() {
    mbid="$1"
    curl -sL https://coverartarchive.org/release/"$mbid"/front-250 --output dataset/images/"$mbid".jpg
    echo $mbid >> dataset/processed_ids
}

mkdir -p dataset/images

# Loop through URLs in batches
index=0
while read -r mbid; do
    index=$((index+1))

    fetch_image "$mbid" &

    if [ $((index % max_concurrent_requests)) -eq 0 ]
    then
      wait
      echo "Downloaded $index images." 
    fi
done

wait

echo "Downloaded $index images."
echo "All requests completed."

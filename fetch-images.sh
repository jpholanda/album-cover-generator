#!/bin/sh

mkdir -p dataset/images

jq -r '.id' dataset/dataset.jsonl | while read -r mbid; do
  echo "downloading image for $mbid"
  curl -L https://coverartarchive.org/release/"$mbid"/front-250 --output dataset/images/"$mbid".jpg
done
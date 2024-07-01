import json
from generate_hf_dataset import DatasetEntry

if __name__ == "__main__":
    count_by_genre = dict()

    with open('dataset/huggingface/all/dataset.jsonl', 'r') as dataset_file:
        for line in dataset_file:
            data = json.loads(line.strip())
            entry = DatasetEntry(data)
            for genre in entry.genres:
                count_by_genre[genre] = count_by_genre.get(genre, 0) + 1

    for genre, count in count_by_genre.items():
        print(genre, ', ', count)
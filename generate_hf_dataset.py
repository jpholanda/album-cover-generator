import json
import pathlib
import random


class DatasetEntry:
    def __init__(self, json_data):
        self.id = json_data['id']
        self.title = json_data["title"]
        self.type = json_data["type"]
        self.artist = json_data["artist"]
        self.genres = json_data["genres"]
        self.tracklist = json_data["tracklist"]

    def get_caption(self):
        genres_copy = self.genres.copy()
        random.shuffle(genres_copy)
        formatted_genres = ', '.join(genres_copy)
        formatted_tracklist = ', '.join(f'"{track}"' for track in self.tracklist)
        formatted_type = 'release' if self.type is None or self.type == 'Other' else self.type.lower()
        genres_article = 'an' if genres_copy[0][0] in ('a', 'e', 'i', 'o', 'u') else 'a'

        return f'Cover art for {genres_article} {formatted_genres} {formatted_type} titled "{self.title}", by "{self.artist}", including the songs {formatted_tracklist}'.encode('utf-8')


def read_dataset():
    dataset = []

    with open('dataset/dataset.jsonl', 'r') as raw_dataset:
        for line in raw_dataset:
            json_data = json.loads(line.strip())
            entry = DatasetEntry(json_data)
            dataset.append(entry)

    return dataset


def split_dataset(dataset, train_percentage: float):
    random.shuffle(dataset)

    train_dataset = dataset[:int(len(dataset) * train_percentage)]
    test_dataset = dataset[int(len(dataset) * train_percentage):]

    return train_dataset, test_dataset


def persist_dataset(dataset, filepath):
    with open(filepath, 'w') as dataset_file:
        for entry in dataset:
            obj = {
                'file_name': f'{entry.id}.jpg',
                'text': entry.get_caption()
            }
            json.dump(obj, dataset_file)
            dataset_file.write('\n')


def persist_dataset_ids(dataset, filepath):
    with open(filepath, 'w') as dataset_ids_file:
        for entry in dataset:
            dataset_ids_file.write(entry.id)
            dataset_ids_file.write('\n')


def ensure_directory_exists(directory):
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    dataset = read_dataset()

    train_dataset, test_dataset = split_dataset(dataset, train_percentage=0.8)

    ensure_directory_exists('dataset/huggingface/train')
    ensure_directory_exists('dataset/huggingface/test')

    persist_dataset(train_dataset, 'dataset/huggingface/train/metadata.jsonl')
    persist_dataset(test_dataset, 'dataset/huggingface/test/metadata.jsonl')

    persist_dataset_ids(train_dataset, 'dataset/huggingface/train_ids')
    persist_dataset_ids(test_dataset, 'dataset/huggingface/test_ids')

import json
import os
import pathlib
import random
import shutil


class DatasetEntry:
    def __init__(self, json_data):
        self.id = json_data['id']
        self.title = json_data["title"]
        self.type = json_data["type"]
        self.artist = json_data["artist"]
        self.genres = json_data["genres"]
        self.release_date = json_data["date"]

    def get_caption(self):
        genres_copy = self.genres.copy()
        random.shuffle(genres_copy)
        formatted_genres = ', '.join(genres_copy)
        formatted_type = 'release' if self.type is None or self.type == 'Other' else self.type.lower()
        genres_article = 'an' if genres_copy[0][0] in ('a', 'e', 'i', 'o', 'u') else 'a'

        return f'Cover art for {genres_article} {formatted_genres} {formatted_type} titled "{self.title}", by "{self.artist}"'


def read_dataset():
    dataset = []

    with open('dataset/dataset.jsonl', 'r', encoding='utf8') as raw_dataset:
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


def persist_dataset(dataset, split):
    with open(f'dataset/huggingface/{split}/metadata.jsonl', 'w', encoding='utf8') as dataset_file:
        for entry in dataset:
            obj = {
                'file_name': f'{entry.id}.jpg',
                'text': entry.get_caption()
            }
            json.dump(obj, dataset_file, ensure_ascii=False)
            dataset_file.write('\n')


def ensure_directory_exists(directory):
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def copy_image(file_name, split):
    if os.path.exists(f'dataset/huggingface/{split}/{file_name}'):
        return

    if not os.path.exists(f'dataset/images/{file_name}'):
        return

    shutil.copy(f'dataset/images/{file_name}', f'dataset/huggingface/{split}/{file_name}')


def copy_images(dataset, split):
    for entry in dataset:
        copy_image(f'{entry.id}.jpg', split)


if __name__ == '__main__':
    dataset = read_dataset()

    train_dataset, test_dataset = split_dataset(dataset, train_percentage=0.8)

    ensure_directory_exists('dataset/huggingface/train')
    ensure_directory_exists('dataset/huggingface/test')

    persist_dataset(train_dataset, split='train')
    persist_dataset(test_dataset, split='test')

    copy_images(train_dataset, split='train')
    copy_images(test_dataset, split='test')

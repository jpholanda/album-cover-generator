import json
import os
import shutil


def read_dataset_metadata(split):
    file_names = []

    with open(f'dataset/huggingface/{split}/metadata.jsonl', 'r') as metadata_file:
        for line in metadata_file:
            entry = json.loads(line.strip())
            file_names.append(entry['file_name'])

    return file_names


def copy_image(file_name, split):
    if not os.path.exists(f'dataset/huggingface/{split}/{file_name}'):
        if os.path.exists(f'dataset/images/{file_name}'):
            shutil.copy(f'dataset/images/{file_name}', f'dataset/huggingface/{split}/{file_name}')
            print(f'Copied {file_name} to {split} split')
        else:
            print(f'For {split} split: {file_name} is missing')


def copy_images_to_split(split):
    file_names = read_dataset_metadata(split)
    for file_name in file_names:
        copy_image(file_name, split)


if __name__ == '__main__':
    copy_images_to_split('train')
    copy_images_to_split('test')
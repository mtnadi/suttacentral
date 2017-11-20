import json
from pathlib import Path

from tqdm import tqdm


def load_divisions(db, structure_dir: Path):
    print('Loading divisions')
    division_dir = structure_dir / 'division'
    division_files = division_dir.glob('*.json')
    division_objects = []
    divisions_collection = db['divisions']
    text_divisions_collection = db['text_divisions']
    text_division_data_objects = []
    for division_file in tqdm(division_files):
        division_name = '.'.join(division_file.name.split('.')[:-1])
        division_objects.append({'uid': division_name})
        with division_file.open('r', encoding='utf-8') as f:
            division_data = json.load(f)
        division_data = [{'uid': entry.pop('_path').split('/')[-1], **entry, 'division': division_name, 'num': i}
                         for i, entry in enumerate(division_data)]
        text_division_data_objects += division_data

    divisions_collection.import_bulk(division_objects)
    text_divisions_collection.import_bulk(text_division_data_objects)
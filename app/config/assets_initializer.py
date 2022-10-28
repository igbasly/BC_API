import os
import json


def load_manifest(manifest_path: str):
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as manifest_file:
            return json.load(manifest_file)
    else:
        return {}


accepted_files = ['png', 'jpeg', 'gif', 'jpg', 'pdf']

manifest = {}

assets_path = os.path.join('.', 'app', 'assets')
for path in os.listdir(assets_path):
    folder_path = os.path.join(assets_path, path)
    if '.' not in path and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        for file_name in files:
            extension = file_name.split('.')[1] if '.' in file_name else None
            if extension in accepted_files:
                manifest[file_name] = os.path.join(folder_path, file_name)

manifest_path = os.path.join(assets_path, 'manifest.json')
with open(manifest_path, "w", encoding="utf-8") as manifest_file:
    json.dump(manifest, manifest_file)

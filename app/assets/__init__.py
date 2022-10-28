import os
from ..config import load_manifest


manifest_path = os.path.join('app', 'assets', 'manifest.json')

MANIFEST = load_manifest(manifest_path)


def asset_path(asset_name: str):
    if asset_name in MANIFEST:
        return MANIFEST[asset_name]
    else:
        raise NameError(f"Asset '{asset_name}' is not include in manifest")

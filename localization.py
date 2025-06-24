from pathlib import Path
from utils.yaml_loader import load_simple_yaml


def _load_translations():
    translations = {}
    locales_dir = Path(__file__).with_name('locales')
    for file in locales_dir.glob('*.yml'):
        lang = file.stem
        items = load_simple_yaml(str(file))
        for key, value in items.items():
            translations.setdefault(key, {})[lang] = value
    return translations


translations = _load_translations()

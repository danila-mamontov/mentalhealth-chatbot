from pathlib import Path
from utils.yaml_loader import load_simple_yaml

FALLBACK_LANGUAGE = "en"

LANGUAGE_META: dict[str, dict[str, str]] = {
    "en": {"name": "English", "flag": "🇬🇧"},
    "de": {"name": "Deutsch", "flag": "🇩🇪"},
    "ru": {"name": "Русский", "flag": "🇷🇺"},
    "fr": {"name": "Français", "flag": "🇫🇷"},
    "zh": {"name": "中文", "flag": "🇨🇳"},
    "hi": {"name": "हिन्दी", "flag": "🇮🇳"},
    "ar": {"name": "العربية", "flag": "🇦🇪"},
    "uk": {"name": "Українська", "flag": "🇺🇦"},
    "es": {"name": "Español", "flag": "🇪🇸"},
    "it": {"name": "Italiano", "flag": "🇮🇹"},
}


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

def get_available_languages():
    """Return a list of available language codes."""
    return list(LANGUAGE_META.keys())

def get_language_name(code: str) -> str:
    return LANGUAGE_META.get(code, {}).get("name", code)

def get_language_flag(code: str) -> str:
    return LANGUAGE_META.get(code, {}).get("flag", "🏳️")

def normalize_language(code: str | None, available: list[str] | None = None) -> str:
    if not code:
        return FALLBACK_LANGUAGE
    code = code.lower()
    if available is None:
        available = get_available_languages()
    return code if code in available else FALLBACK_LANGUAGE

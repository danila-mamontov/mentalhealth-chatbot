from typing import Any, Dict, List
import codecs
import ast


def load_simple_yaml(path: str) -> Dict[str, Any]:
    """Minimal YAML loader supporting mappings and lists of strings."""
    data: Dict[str, Any] = {}
    with open(path, encoding="utf-8") as f:
        current_key = None
        current_list: List[str] | None = None
        for raw in f:
            line = raw.rstrip("\n")
            if not line or line.lstrip().startswith("#"):
                continue
            if line.startswith("  - "):
                if current_list is None:
                    raise ValueError(f"List item outside of a list in {path}")
                item = line[4:].strip()
                if (item.startswith('"') and item.endswith('"')) or (
                    item.startswith("'") and item.endswith("'")
                ):
                    # use Python parser to handle escapes like \n without
                    # corrupting non-ASCII characters
                    try:
                        item = ast.literal_eval(item)
                    except Exception:
                        item = item[1:-1]
                        item = item.replace("\\n", "\n").replace("\\t", "\t")
                data[current_key].append(item)
            else:
                if current_list is not None:
                    current_key = None
                    current_list = None
                if ':' not in line:
                    continue
                if line.rstrip().endswith(':'):
                    key = line.rstrip()[:-1]
                    rest = ''
                else:
                    key, rest = line.split(':', 1)
                key = key.strip()
                rest = rest.strip()
                if rest == "":
                    data[key] = []
                    current_key = key
                    current_list = data[key]
                else:
                    if rest in {"~", "null"}:
                        data[key] = None
                    else:
                        if (rest.startswith('"') and rest.endswith('"')) or (
                            rest.startswith("'") and rest.endswith("'")
                        ):
                            try:
                                rest = ast.literal_eval(rest)
                            except Exception:
                                rest = rest[1:-1]
                                rest = rest.replace("\\n", "\n").replace("\\t", "\t")
                        data[key] = rest
    return data

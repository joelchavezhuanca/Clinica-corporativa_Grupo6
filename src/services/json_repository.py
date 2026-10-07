import json
from pathlib import Path


class JsonRepository:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.save_all([])

    def load_all(self):
        try:
            with self.path.open("r", encoding="utf-8") as archivo:
                data = json.load(archivo)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def save_all(self, data):
        with self.path.open("w", encoding="utf-8") as archivo:
            json.dump(data, archivo, ensure_ascii=False, indent=2)

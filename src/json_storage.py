import json
import os

from src.abstract_storage import AbstractStorage


class JSONStorage(AbstractStorage):
    def __init__(self, filepath: str = "data/aeroplanes.json"):
        self.filepath = filepath
        dirpath = os.path.dirname(filepath)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load(self) -> list:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, data: list) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_aeroplane(self, aeroplane) -> None:
        data = self._load()
        data.append({
            "icao24": aeroplane.icao24,
            "callsign": aeroplane.callsign,
            "country": aeroplane.country,
            "velocity": aeroplane.velocity,
            "altitude": aeroplane.altitude
        })
        self._save(data)

    def get_aeroplanes(self) -> list:
        return self._load()

    def delete_aeroplane(self, icao24: str) -> None:
        data = self._load()
        data = [item for item in data if item.get("icao24") != icao24]
        self._save(data)

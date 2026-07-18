import os

from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


def test_json_storage_add():
    storage = JSONStorage("test_data.json")
    plane = Aeroplane("abc", "TEST", "US", 100, 5000)
    storage.add_aeroplane(plane)
    data = storage.get_aeroplanes()
    assert len(data) == 1
    assert data[0]["icao24"] == "abc"
    os.remove("test_data.json")


def test_json_storage_delete():
    storage = JSONStorage("test_data.json")
    plane = Aeroplane("abc", "TEST", "US", 100, 5000)
    storage.add_aeroplane(plane)
    storage.delete_aeroplane("abc")
    data = storage.get_aeroplanes()
    assert data == []
    os.remove("test_data.json")


def test_json_storage_load_error(tmp_path):
    test_file = tmp_path / "bad.json"
    test_file.write_text("{invalid json}", encoding="utf-8")
    storage = JSONStorage(str(test_file))
    data = storage._load()
    assert data == []

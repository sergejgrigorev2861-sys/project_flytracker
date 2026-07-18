from unittest.mock import patch

from src.api import APIAdapter


def test_get_country_coordinates():
    with patch("src.api.get") as mock_get:
        mock_get.return_value.json.return_value = [
            {"boundingbox": ["41.6", "83.3", "-141.0", "-52.3"]}
        ]
        api = APIAdapter()
        box = api.get_country_coordinates("Canada")
        assert box == ["41.6", "83.3", "-141.0", "-52.3"]


def test_get_aeroplanes_invalid_country():
    with patch("src.api.get") as mock_get:
        mock_get.return_value.json.return_value = []
        api = APIAdapter()
        api.get_aeroplanes("Invalid")
        assert api.aeroplanes is None


def test_api_adapter_init():
    from src.api import APIAdapter
    api = APIAdapter()
    assert api.openstreetmap_url == "https://nominatim.openstreetmap.org/search"
    assert api.opensky_url == "https://opensky-network.org/api/states/all?"


def test_api_no_coordinates():
    with patch("src.api.get") as mock_get:
        mock_get.return_value.json.return_value = []
        api = APIAdapter()
        api.get_aeroplanes("Invalid")
        assert api.aeroplanes is None


def test_api_empty_response():
    with patch("src.api.get") as mock_get:
        mock_get.return_value.json.return_value = []
        api = APIAdapter()
        api.get_aeroplanes("Invalid")
        assert api.aeroplanes is None


def test_api_get_aeroplanes_success():
    with patch("src.api.get") as mock_get:
        # Мокаем ответ Nominatim
        mock_get.return_value.json.side_effect = [
            [{"boundingbox": ["41.6", "83.3", "-141.0", "-52.3"]}],
            {"states": [["abc", "TEST", "US", 0, 0, 0, 0, 5000, False, 100, 0, 0, None, 0, "0", False, 0]]}
        ]
        api = APIAdapter()
        api.get_aeroplanes("Canada")
        assert api.aeroplanes is not None
        assert "states" in api.aeroplanes

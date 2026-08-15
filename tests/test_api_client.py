from unittest.mock import patch, Mock
from src.api.api_client import APIClient


class TestAPIClient:
    """Тесты для класса APIClient."""

    @patch('src.api.api_client.requests.get')
    def test_get_country_coordinates_success(self, mock_get):
        """Тест: успешное получение координат страны."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"lat": "39.7837304", "lon": "-100.445882"}
        ]
        mock_get.return_value = mock_response

        result = APIClient.get_country_coordinates("USA")
        assert result == (39.7837304, -100.445882)

        # Проверяем, что запрос был с правильными параметрами
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["q"] == "USA"
        assert kwargs["params"]["format"] == "json"

    @patch('src.api.api_client.requests.get')
    def test_get_country_coordinates_not_found(self, mock_get):
        """Тест: страна не найдена (пустой ответ)."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = APIClient.get_country_coordinates("UnknownCountry")
        assert result is None

    @patch('src.api.api_client.requests.get')
    def test_get_country_coordinates_request_error(self, mock_get):
        """Тест: ошибка при запросе к API."""
        # Используем requests.exceptions.RequestException
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Connection error")
        result = APIClient.get_country_coordinates("USA")
        assert result is None

    @patch('src.api.api_client.requests.get')
    def test_get_states_by_bbox_success(self, mock_get):
        """Тест: успешное получение списка самолётов."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "states": [
                ["abc123", "AAL123", "USA", 1, 2, 3, 4, 5, 6],
                ["def456", "UAL456", "USA", 1, 2, 3, 4, 5, 6]
            ]
        }
        mock_get.return_value = mock_response

        result = APIClient.get_states_by_bbox(0, 0, 10, 10)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0][0] == "abc123"

    @patch('src.api.api_client.requests.get')
    def test_get_states_by_bbox_empty(self, mock_get):
        """Тест: пустой ответ от OpenSky."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = APIClient.get_states_by_bbox(0, 0, 10, 10)
        assert result == []

    @patch('src.api.api_client.requests.get')
    def test_get_states_by_bbox_none(self, mock_get):
        """Тест: API вернул None."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"states": None}
        mock_get.return_value = mock_response

        result = APIClient.get_states_by_bbox(0, 0, 10, 10)
        assert result == []

    @patch('src.api.api_client.requests.get')
    def test_get_states_by_bbox_request_error(self, mock_get):
        """Тест: ошибка при запросе к OpenSky."""
        mock_get.side_effect = Exception("API Error")
        result = APIClient.get_states_by_bbox(0, 0, 10, 10)
        assert result == []

    @patch('src.api.api_client.requests.get')
    def test_get_states_by_bbox_http_error(self, mock_get):
        """Тест: HTTP ошибка (404, 500 и т.д.)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_get.return_value = mock_response

        result = APIClient.get_states_by_bbox(0, 0, 10, 10)
        assert result == []

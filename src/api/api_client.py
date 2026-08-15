import requests

from src.config import config


class APIClient:
    """Клиент для работы с API OpenSky и Nominatim."""

    @staticmethod
    def _get_headers() -> dict:
        """
        Возвращает заголовки для запросов к API.

        Returns:
            Словарь с заголовками.
        """
        return {
            "User-Agent": "FlyRadar/1.0 (https://github.com/yourusername/fly_radar; your-email@example.com)"
        }

    @staticmethod
    def get_country_coordinates(country_name: str) -> tuple[float, float] | None:
        """
        Получает координаты страны через Nominatim API.
        """
        headers = {
            "User-Agent": "FlyRadarApp/1.0 (your_email@example.com)"
        }
        params = {
            "q": country_name,
            "format": "json",
            "limit": 1,
        }
        try:
            response = requests.get(
                config.NOMINATIM_URL,
                params=params,
                headers=headers,
                timeout=15
            )
            # Если ответ 403, пробуем с другим User-Agent
            if response.status_code == 403:
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                response = requests.get(
                    config.NOMINATIM_URL,
                    params=params,
                    headers=headers,
                    timeout=10
                )
            response.raise_for_status()
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                print(f"📍 {country_name}: {lat}, {lon}")
                return lat, lon
            print(f"⚠️ Страна '{country_name}' не найдена.")
            return None
        except requests.RequestException as e:
            print(f"❌ Ошибка при запросе к Nominatim: {e}")
            return None

    @staticmethod
    def get_states_by_bbox(lat_min: float, lon_min: float, lat_max: float, lon_max: float) -> list:
        """
        Получает данные о самолётах в заданном прямоугольнике через OpenSky API.

        Args:
            lat_min: Минимальная широта.
            lon_min: Минимальная долгота.
            lat_max: Максимальная широта.
            lon_max: Максимальная долгота.

        Returns:
            Список самолётов в формате OpenSky.
        """
        params = {
            "lamin": lat_min,
            "lomin": lon_min,
            "lamax": lat_max,
            "lomax": lon_max,
        }
        try:
            response = requests.get(config.OPENSKY_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            states = data.get("states")
            if states is None:
                print(f"⚠️ API вернул None для координат {lat_min}, {lon_min}")
                return []
            print(f"🛩️ Найдено самолётов: {len(states)}")
            return states
        except Exception as e:
            print(f"❌ Ошибка при запросе к OpenSky: {e}")
            return []

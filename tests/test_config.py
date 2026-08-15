import os
from unittest.mock import patch

from src.config import Config


class TestConfig:
    """Тесты для класса Config."""

    @staticmethod
    def _create_config_with_env(env_vars):
        """Создаёт новый экземпляр Config с подменой окружения."""
        with patch.dict(os.environ, env_vars, clear=True):
            # Пересоздаём класс, чтобы он заново прочитал окружение
            return Config()

    def test_default_values(self):
        """Тест: значения по умолчанию (без переменных окружения)."""
        test_config = self._create_config_with_env({})
        assert test_config.DB_HOST == "localhost"
        assert test_config.DB_PORT == "5432"
        assert test_config.DB_NAME == "fly_radar"
        assert test_config.DB_USER == "postgres"
        assert test_config.DB_PASSWORD == ""  # ✅ Пустой пароль
        assert test_config.OPENSKY_URL == "https://opensky-network.org/api/states/all"
        assert test_config.NOMINATIM_URL == "https://nominatim.openstreetmap.org/search"
        # Проверяем, что COUNTRIES по умолчанию загружается из .env
        assert "USA" in test_config.COUNTRIES

    def test_config_from_env(self):
        """Тест: загрузка переменных из окружения."""
        env_vars = {
            "DB_HOST": "test_host",
            "DB_PORT": "9999",
            "DB_NAME": "test_db",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_pass",
            "OPENSKY_URL": "test_opensky",
            "NOMINATIM_URL": "test_nominatim",
            "COUNTRIES": "USA,Canada,UK"
        }
        test_config = self._create_config_with_env(env_vars)
        assert test_config.DB_HOST == "test_host"
        assert test_config.DB_PORT == "9999"
        assert test_config.DB_NAME == "test_db"
        assert test_config.DB_USER == "test_user"
        assert test_config.DB_PASSWORD == "test_pass"
        assert test_config.OPENSKY_URL == "test_opensky"
        assert test_config.NOMINATIM_URL == "test_nominatim"
        assert test_config.COUNTRIES == ["USA", "Canada", "UK"]

    def test_db_url_property(self):
        """Тест: формирование строки подключения к БД."""
        env_vars = {
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_NAME": "fly_radar",
            "DB_USER": "postgres",
            "DB_PASSWORD": "12345"
        }
        test_config = self._create_config_with_env(env_vars)
        expected_url = "host=localhost port=5432 dbname=fly_radar user=postgres password=12345"
        assert test_config.db_url == expected_url

    def test_db_url_with_empty_password(self):
        """Тест: строка подключения с пустым паролем."""
        env_vars = {
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_NAME": "fly_radar",
            "DB_USER": "postgres",
            "DB_PASSWORD": ""
        }
        test_config = self._create_config_with_env(env_vars)
        expected_url = "host=localhost port=5432 dbname=fly_radar user=postgres password="
        assert test_config.db_url == expected_url

    def test_countries_parsing(self):
        """Тест: парсинг списка стран из строки."""
        test_cases = [
            ("USA,Canada,UK", ["USA", "Canada", "UK"]),
            ("USA, Canada, UK", ["USA", "Canada", "UK"]),
            ("", []),
            ("Germany, France ,  Spain", ["Germany", "France", "Spain"]),
        ]
        for input_str, expected in test_cases:
            env_vars = {"COUNTRIES": input_str}
            test_config = self._create_config_with_env(env_vars)
            assert test_config.COUNTRIES == expected

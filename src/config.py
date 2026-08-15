import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс для хранения конфигурации приложения."""

    def __init__(self):
        """Инициализирует конфигурацию из переменных окружения."""
        # PostgreSQL
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "5432")
        self.DB_NAME = os.getenv("DB_NAME", "fly_radar")
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "")

        # API
        self.OPENSKY_URL = os.getenv("OPENSKY_URL", "https://opensky-network.org/api/states/all")
        self.NOMINATIM_URL = os.getenv("NOMINATIM_URL", "https://nominatim.openstreetmap.org/search")

        # Страны для анализа
        countries_raw = os.getenv("COUNTRIES", "USA,Germany,United Kingdom,United Arab Emirates")
        self.COUNTRIES = [c.strip() for c in countries_raw.split(",") if c.strip()]

    @property
    def db_url(self) -> str:
        """Возвращает строку подключения к PostgreSQL."""
        return (
            f"host={self.DB_HOST} "
            f"port={self.DB_PORT} "
            f"dbname={self.DB_NAME} "
            f"user={self.DB_USER} "
            f"password={self.DB_PASSWORD}"
        )


# Создаём экземпляр для использования в приложении
config = Config()

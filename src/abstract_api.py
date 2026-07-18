from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    @abstractmethod
    def get_country_coordinates(self, country: str):  # pragma: no cover
        """Получает географические координаты страны."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str):  # pragma: no cover
        """Получает информацию о самолётах над страной."""
        pass

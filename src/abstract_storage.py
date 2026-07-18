from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def add_aeroplane(self, aeroplane) -> None:  # pragma: no cover
        pass

    @abstractmethod
    def get_aeroplanes(self) -> list:  # pragma: no cover
        pass

    @abstractmethod
    def delete_aeroplane(self, icao24: str) -> None:  # pragma: no cover
        pass

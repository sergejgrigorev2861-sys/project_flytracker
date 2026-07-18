from typing import Any, Dict, List


class Aeroplane:
    def __init__(
        self,
        icao24: str,
        callsign: str,
        country: str,
        velocity: float,
        altitude: float
    ) -> None:
        self._icao24 = icao24
        self._callsign = callsign.strip() if callsign else "Unknown"
        self._country = country or "Unknown"
        self._velocity = velocity or 0.0
        self._altitude = altitude or 0.0

    @property
    def icao24(self) -> str:
        return self._icao24

    @property
    def callsign(self) -> str:
        return self._callsign

    @property
    def country(self) -> str:
        return self._country

    @property
    def velocity(self) -> float:
        return self._velocity

    @property
    def altitude(self) -> float:
        return self._altitude

    @classmethod
    def from_dict(cls, data: List[Any]) -> "Aeroplane":
        return cls(
            icao24=data[0],
            callsign=data[1],
            country=data[2],
            velocity=data[9] or 0.0,
            altitude=data[7] or 0.0
        )

    @staticmethod
    def cast_to_object_list(states_data: Dict[str, Any]) -> List["Aeroplane"]:
        if not states_data or "states" not in states_data:
            return []
        return [
            Aeroplane.from_dict(state) for state in states_data["states"]]

    def __lt__(self, other: "Aeroplane") -> bool:
        return self.altitude < other.altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        return self.altitude > other.altitude

    def __eq__(self, other: "Aeroplane") -> bool:
        return self.altitude == other.altitude

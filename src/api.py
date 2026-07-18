from requests import get

from src.abstract_api import AbstractAPI


class APIAdapter(AbstractAPI):
    def __init__(self) -> None:
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.opensky_url = 'https://opensky-network.org/api/states/all?'
        self.aeroplanes = None

    def get_country_coordinates(self, country: str):
        headers_nominatim = {'User-Agent': 'flight-tracker/1.0'}
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
        data = response.json()
        if not data:
            return None
        return data[0].get('boundingbox')

    def get_aeroplanes(self, country: str) -> None:
        geo_coordinates = self.get_country_coordinates(country)
        if not geo_coordinates:
            self.aeroplanes = None
            return

        params = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }
        response = get(url=self.opensky_url, params=params)
        self.aeroplanes = response.json()

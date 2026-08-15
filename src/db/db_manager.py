from src.db.db_connector import DBConnector


class DBManager:
    """Класс для аналитических запросов к базе данных."""

    def __init__(self, db: DBConnector):
        self.db = db

    def get_countries_and_aeroplanes_count(self) -> list:
        """
        Получает список всех стран и количество самолётов в их воздушных пространствах.
        """
        query = """
        SELECT c.name, COUNT(a.id)
        FROM countries c
        LEFT JOIN aeroplanes a ON c.id = a.country_id
        GROUP BY c.name
        ORDER BY c.name;
        """
        return self.db.execute_query(query)

    def get_all_aeroplanes(self) -> list:
        """
        Получает список всех воздушных судов.
        """
        query = """
        SELECT icao24, callsign, c.name as country, a.latitude, a.longitude, a.altitude, a.speed, a.timestamp
        FROM aeroplanes a
        LEFT JOIN countries c ON a.country_id = c.id
        ORDER BY timestamp DESC;
        """
        return self.db.execute_query(query)

    def get_avg_speed(self) -> float:
        """
        Получает среднюю скорость по самолётам.
        """
        query = "SELECT AVG(speed) FROM aeroplanes WHERE speed IS NOT NULL;"
        result = self.db.execute_query(query)
        return result[0][0] if result and result[0][0] else 0.0

    def get_aeroplanes_with_higher_speed(self) -> list:
        """
        Получает список всех самолётов, у которых скорость выше средней.
        """
        avg_speed = self.get_avg_speed()
        query = """
        SELECT icao24, callsign, c.name as country, speed
        FROM aeroplanes a
        LEFT JOIN countries c ON a.country_id = c.id
        WHERE speed > %s
        ORDER BY speed DESC;
        """
        return self.db.execute_query(query, (avg_speed,))

    def get_aeroplanes_with_keyword(self, keyword: str) -> list:
        """
        Получает список всех самолётов, в позывном которых содержатся переданные символы.
        """
        query = """
        SELECT icao24, callsign, c.name as country, speed, altitude
        FROM aeroplanes a
        LEFT JOIN countries c ON a.country_id = c.id
        WHERE callsign ILIKE %s
        ORDER BY callsign;
        """
        return self.db.execute_query(query, (f"%{keyword}%",))

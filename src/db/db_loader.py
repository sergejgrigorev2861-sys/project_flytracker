from datetime import datetime

from src.db.db_connector import DBConnector


class DBLoader:
    """Класс для загрузки данных в PostgreSQL."""

    def __init__(self, db: DBConnector):
        self.db = db

    def clear_tables(self) -> None:
        """Очищает таблицы перед загрузкой новых данных."""
        try:
            self.db.execute_query("TRUNCATE TABLE aeroplanes CASCADE;")
            self.db.execute_query("TRUNCATE TABLE countries CASCADE;")
            print("✅ Таблицы очищены.")
        except Exception as e:
            print(f"⚠️ Ошибка при очистке таблиц: {e}")

    def save_country(self, name: str, latitude: float, longitude: float) -> int:
        # Сначала проверяем, есть ли страна
        check_query = "SELECT id FROM countries WHERE name = %s;"
        check_result = self.db.execute_query(check_query, (name,))
        print(f"🔍 check_result для {name}: {check_result}")  # ОТЛАДКА
        if check_result:
            return check_result[0][0]

        # Если нет — вставляем
        insert_query = """
        INSERT INTO countries (name, latitude, longitude)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        result = self.db.execute_query(insert_query, (name, latitude, longitude))
        print(f"🔍 insert_result для {name}: {result}")  # ОТЛАДКА
        return result[0][0] if result else None

    def save_aeroplanes(self, country_id: int, states: list) -> None:
        """
        Сохраняет список самолётов в БД.

        Args:
            country_id: ID страны.
            states: Список самолётов из OpenSky API.
        """
        if not states:
            print("⚠️ Нет данных о самолётах для сохранения.")
            return

        query = """
        INSERT INTO aeroplanes (icao24, callsign, country_id, latitude, longitude, altitude, speed, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        params_list = []
        for state in states:
            # OpenSky возвращает: icao24, callsign, country, time, longitude, latitude, altitude, velocity, ...
            icao24 = state[0] if state[0] else ''
            callsign = state[1].strip() if state[1] else None
            latitude = state[5] if state[5] is not None else None
            longitude = state[4] if state[4] is not None else None
            altitude = state[7] if state[7] is not None else None
            speed = state[9] if state[9] is not None else None
            timestamp = datetime.now()

            params_list.append((
                icao24,
                callsign,
                country_id,
                latitude,
                longitude,
                altitude,
                speed,
                timestamp
            ))

        try:
            self.db.execute_many(query, params_list)
            print(f"✅ Сохранено {len(params_list)} самолётов в БД.")
        except Exception as e:
            print(f"❌ Ошибка при сохранении самолётов: {e}")

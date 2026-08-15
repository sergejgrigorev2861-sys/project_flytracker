from src.db.db_connector import DBConnector


class DBCreator:
    """Класс для создания таблиц в PostgreSQL."""

    @staticmethod
    def create_tables(db: DBConnector) -> None:
        """
        Создаёт таблицы countries и aeroplanes, если они не существуют.
        """
        # Таблица стран
        query_countries = """
        CREATE TABLE IF NOT EXISTS countries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            latitude DOUBLE PRECISION NOT NULL,
            longitude DOUBLE PRECISION NOT NULL
        );
        """

        # Таблица самолётов
        query_aeroplanes = """
        CREATE TABLE IF NOT EXISTS aeroplanes (
            id SERIAL PRIMARY KEY,
            icao24 VARCHAR(10) NOT NULL,
            callsign VARCHAR(20),
            country_id INTEGER REFERENCES countries(id) ON DELETE CASCADE,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            altitude DOUBLE PRECISION,
            speed DOUBLE PRECISION,
            timestamp TIMESTAMP DEFAULT NOW()
        );
        """

        try:
            db.execute_query(query_countries)
            db.execute_query(query_aeroplanes)
            print("✅ Таблицы успешно созданы (или уже существуют).")
        except Exception as e:
            print(f"❌ Ошибка при создании таблиц: {e}")

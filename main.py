from src.config import config
from src.db.db_connector import DBConnector
from src.db.db_creator import DBCreator
from src.db.db_loader import DBLoader
from src.api.api_client import APIClient
from src.db.db_manager import DBManager


def main():
    """Основная функция приложения."""
    print("🛫 Загрузка данных о самолётах в PostgreSQL...")

    with DBConnector() as db:
        # 1. Удаляем старую таблицу aeroplanes
        try:
            db.execute_query("DROP TABLE IF EXISTS aeroplanes CASCADE;")
            print("✅ Старая таблица aeroplanes удалена.")
        except Exception as e:
            print(f"⚠️ Ошибка при удалении таблицы: {e}")

        # 2. Создаём таблицы заново с DOUBLE PRECISION
        DBCreator.create_tables(db)

        # 3. Очищаем таблицы
        loader = DBLoader(db)
        loader.clear_tables()

        # 4. Загружаем данные по странам
        countries = config.COUNTRIES
        for country_name in countries:
            coords = APIClient.get_country_coordinates(country_name)
            if not coords:
                continue
            lat, lon = coords
            country_id = loader.save_country(country_name, lat, lon)
            if not country_id:
                continue
            print(f"✅ Страна сохранена с ID: {country_id}")

            states = APIClient.get_states_by_bbox(lat - 10, lon - 10, lat + 10, lon + 10)
            loader.save_aeroplanes(country_id, states)

        # 5. Статистика
        result = db.execute_query("""
            SELECT c.name, COUNT(a.id)
            FROM countries c
            LEFT JOIN aeroplanes a ON c.id = a.country_id
            GROUP BY c.name
            ORDER BY c.name;
        """)
        print("\n📊 Статистика по странам:")
        for row in result:
            print(f"  {row[0]}: {row[1]} самолётов")

        # 6. Аналитические запросы
        print("\n📊 Аналитические данные:")
        manager = DBManager(db)

        # 6.1 Страны и количество самолётов
        print("\n📍 Страны и количество самолётов:")
        for row in manager.get_countries_and_aeroplanes_count():
            print(f"  {row[0]}: {row[1]}")

        # 6.2 Все самолёты (первые 5)
        print("\n✈️ Самолёты (первые 5):")
        for row in manager.get_all_aeroplanes()[:5]:
            print(f"  {row}")

        # 6.3 Средняя скорость
        avg_speed = manager.get_avg_speed()
        print(f"\n📊 Средняя скорость: {avg_speed:.2f} узлов")

        # 6.4 Самолёты со скоростью выше средней
        print("\n🚀 Самолёты со скоростью выше средней:")
        for row in manager.get_aeroplanes_with_higher_speed()[:5]:
            print(f"  {row}")

        # 6.5 Поиск по ключевому слову (например, 'AAL' для American Airlines)
        keyword = "AAL"
        print(f"\n🔍 Самолёты с позывным, содержащим '{keyword}':")
        for row in manager.get_aeroplanes_with_keyword(keyword)[:5]:
            print(f"  {row}")


if __name__ == "__main__":
    main()

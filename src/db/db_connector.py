import psycopg2
from psycopg2 import OperationalError

from src.config import config


class DBConnector:
    """Класс для управления подключением к PostgreSQL."""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        """Устанавливает соединение с базой данных."""
        try:
            self.connection = psycopg2.connect(config.db_url)
            self.cursor = self.connection.cursor()
            print("✅ Подключение к PostgreSQL установлено.")
        except OperationalError as e:
            raise ConnectionError(f"Ошибка подключения к БД: {e}")

    def disconnect(self) -> None:
        """Закрывает соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("🔌 Соединение с БД закрыто.")

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Выполняет SQL-запрос и возвращает результат.
        """
        if not self.connection:
            raise RuntimeError("Нет активного подключения. Вызовите connect() сначала.")

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            # 🔥 ВАЖНО: для SELECT и INSERT ... RETURNING нужно вернуть данные
            if query.strip().upper().startswith("SELECT") or "RETURNING" in query.upper():
                return cursor.fetchall()
            self.connection.commit()
            return []

    def execute_many(self, query: str, params_list: list) -> None:
        """
        Выполняет массовую вставку данных.

        Args:
            query: SQL-запрос.
            params_list: Список кортежей с параметрами.
        """
        if not self.connection:
            raise RuntimeError("Нет активного подключения. Вызовите connect() сначала.")

        with self.connection.cursor() as cursor:
            cursor.executemany(query, params_list)
            self.connection.commit()

    def __enter__(self):
        """Поддержка контекстного менеджера."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения."""
        self.disconnect()

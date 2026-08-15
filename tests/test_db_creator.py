import pytest
from unittest.mock import patch, Mock
from src.db.db_creator import DBCreator
from src.db.db_connector import DBConnector


class TestDBCreator:
    """Тесты для класса DBCreator."""

    @patch('src.db.db_creator.DBConnector')
    def test_create_tables_success(self, mock_db):
        """Тест: успешное создание таблиц."""
        mock_db_instance = Mock()
        mock_db_instance.execute_query.return_value = []
        mock_db.return_value = mock_db_instance

        DBCreator.create_tables(mock_db_instance)

        # Проверяем, что execute_query вызывался 2 раза (для каждой таблицы)
        assert mock_db_instance.execute_query.call_count == 2

    @patch('src.db.db_creator.DBConnector')
    def test_create_tables_error(self, mock_db):
        """Тест: ошибка при создании таблиц."""
        mock_db_instance = Mock()
        mock_db_instance.execute_query.side_effect = Exception("Table creation error")
        mock_db.return_value = mock_db_instance

        # Проверяем, что ошибка логируется, но не выбрасывается дальше
        DBCreator.create_tables(mock_db_instance)

        # Проверяем, что execute_query вызывался хотя бы 1 раз
        assert mock_db_instance.execute_query.call_count >= 1

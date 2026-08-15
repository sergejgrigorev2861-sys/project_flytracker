from unittest.mock import Mock

import pytest

from src.db.db_manager import DBManager


class TestDBManager:
    """Тесты для класса DBManager."""

    @pytest.fixture
    def mock_db(self):
        """Фикстура: мок для DBConnector."""
        mock = Mock()
        return mock

    @pytest.fixture
    def manager(self, mock_db):
        """Фикстура: экземпляр DBManager с мок-БД."""
        return DBManager(mock_db)

    def test_get_countries_and_aeroplanes_count(self, manager, mock_db):
        """Тест: получение списка стран и количества самолётов."""
        mock_db.execute_query.return_value = [("USA", 100), ("UK", 50)]

        result = manager.get_countries_and_aeroplanes_count()

        assert result == [("USA", 100), ("UK", 50)]
        mock_db.execute_query.assert_called_once()

    def test_get_all_aeroplanes(self, manager, mock_db):
        """Тест: получение всех самолётов."""
        mock_db.execute_query.return_value = [
            ("abc123", "AAL123", "USA", 39.0, -100.0, 10000.0, 450.0, None)
        ]

        result = manager.get_all_aeroplanes()

        assert len(result) == 1
        assert result[0][0] == "abc123"
        mock_db.execute_query.assert_called_once()

    def test_get_avg_speed_with_data(self, manager, mock_db):
        """Тест: получение средней скорости (есть данные)."""
        mock_db.execute_query.return_value = [(245.5,)]

        result = manager.get_avg_speed()

        assert result == 245.5
        mock_db.execute_query.assert_called_once_with("SELECT AVG(speed) FROM aeroplanes WHERE speed IS NOT NULL;")

    def test_get_avg_speed_no_data(self, manager, mock_db):
        """Тест: получение средней скорости (нет данных)."""
        mock_db.execute_query.return_value = [(None,)]

        result = manager.get_avg_speed()

        assert result == 0.0

    def test_get_avg_speed_empty_result(self, manager, mock_db):
        """Тест: получение средней скорости (пустой результат)."""
        mock_db.execute_query.return_value = []

        result = manager.get_avg_speed()

        assert result == 0.0

    def test_get_aeroplanes_with_higher_speed(self, manager, mock_db):
        """Тест: получение самолётов со скоростью выше средней."""
        mock_db.execute_query.side_effect = [[(245.5,)], [("abc123", "AAL123", "USA", 450.0)]]

        result = manager.get_aeroplanes_with_higher_speed()

        assert len(result) == 1
        assert result[0][0] == "abc123"
        assert mock_db.execute_query.call_count == 2

    def test_get_aeroplanes_with_keyword(self, manager, mock_db):
        """Тест: поиск самолётов по ключевому слову."""
        mock_db.execute_query.return_value = [
            ("abc123", "AAL123", "USA", 450.0, 10000.0)
        ]

        result = manager.get_aeroplanes_with_keyword("AAL")

        assert len(result) == 1
        assert result[0][1] == "AAL123"
        # Проверяем, что запрос содержит ILIKE
        call_args = mock_db.execute_query.call_args[0][0]
        assert "ILIKE" in call_args.upper()
        # Проверяем, что параметры переданы правильно
        call_params = mock_db.execute_query.call_args[0][1]
        assert call_params == ("%AAL%",)

    def test_get_aeroplanes_with_keyword_empty(self, manager, mock_db):
        """Тест: поиск по ключевому слову (нет результатов)."""
        mock_db.execute_query.return_value = []

        result = manager.get_aeroplanes_with_keyword("XXXXX")

        assert result == []

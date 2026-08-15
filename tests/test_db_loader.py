import pytest
from unittest.mock import patch, Mock
from src.db.db_loader import DBLoader
from src.db.db_connector import DBConnector


class TestDBLoader:
    """Тесты для класса DBLoader."""

    @pytest.fixture
    def mock_db(self):
        """Фикстура: мок для DBConnector."""
        mock = Mock()
        mock.execute_query.return_value = [(1,)]
        return mock

    @pytest.fixture
    def loader(self, mock_db):
        """Фикстура: экземпляр DBLoader с мок-БД."""
        return DBLoader(mock_db)

    def test_clear_tables_success(self, loader, mock_db):
        """Тест: успешная очистка таблиц."""
        loader.clear_tables()
        assert mock_db.execute_query.call_count == 2

    def test_clear_tables_error(self, loader, mock_db):
        """Тест: ошибка при очистке таблиц."""
        mock_db.execute_query.side_effect = Exception("Truncate error")
        loader.clear_tables()

    def test_save_country_new(self, loader, mock_db):
        """Тест: сохранение новой страны."""
        mock_db.execute_query.side_effect = [[], [(1,)]]
        country_id = loader.save_country("TestCountry", 10.0, 20.0)
        assert country_id == 1

    def test_save_country_exists(self, loader, mock_db):
        """Тест: сохранение существующей страны."""
        mock_db.execute_query.return_value = [(5,)]
        country_id = loader.save_country("ExistingCountry", 10.0, 20.0)
        assert country_id == 5

    def test_save_country_with_returning(self, loader, mock_db):
        """Тест: сохранение страны без RETURNING (запасной вариант)."""
        mock_db.execute_query.side_effect = [[], []]
        country_id = loader.save_country("TestCountry", 10.0, 20.0)
        assert country_id is None

    def test_save_aeroplanes_empty(self, loader, mock_db):
        """Тест: сохранение пустого списка самолётов."""
        loader.save_aeroplanes(1, [])
        mock_db.execute_many.assert_not_called()

    def test_save_aeroplanes_success(self, loader, mock_db):
        """Тест: успешное сохранение самолётов."""
        states = [
            ["abc123", "AAL123", "USA", 123456, 123456, 39.0, -100.0, 10000.0, 450.0, 250.0, 0, 0],
            ["def456", "UAL456", "USA", 123456, 123456, 40.0, -101.0, 11000.0, 460.0, 260.0, 0, 0]
        ]
        loader.save_aeroplanes(1, states)
        mock_db.execute_many.assert_called_once()
        args, kwargs = mock_db.execute_many.call_args
        params_list = args[1]
        assert len(params_list) == 2
        assert params_list[0][0] == "abc123"
        assert params_list[0][1] == "AAL123"

    def test_save_aeroplanes_with_null_values(self, loader, mock_db):
        """Тест: сохранение самолётов с NULL значениями."""
        states = [
            [None, None, None, None, None, None, None, None, None, None, None, None],
            ["def456", "  UAL456  ", "USA", 123456, 123456, 40.0, -101.0, 11000.0, 460.0, 260.0, 0, 0]
        ]
        loader.save_aeroplanes(1, states)
        args, kwargs = mock_db.execute_many.call_args
        params_list = args[1]
        assert len(params_list) == 2
        assert params_list[0][0] == ''  # icao24 для None
        assert params_list[1][1] == "UAL456"  # callsign (обрезаны пробелы)

    def test_save_aeroplanes_error(self, loader, mock_db):
        """Тест: ошибка при сохранении самолётов."""
        states = [["abc123", "AAL123", "USA", 123456, 123456, 39.0, -100.0, 10000.0, 450.0, 250.0, 0, 0]]
        mock_db.execute_many.side_effect = Exception("Insert error")
        loader.save_aeroplanes(1, states)

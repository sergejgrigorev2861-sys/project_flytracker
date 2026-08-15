from unittest.mock import MagicMock, Mock, patch

import pytest

from src.db.db_connector import DBConnector


class TestDBConnector:
    """Тесты для класса DBConnector."""

    @patch('src.db.db_connector.psycopg2.connect')
    def test_connect_success(self, mock_connect):
        """Тест: успешное подключение к БД."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DBConnector()
        db.connect()

        assert db.connection is not None
        assert db.cursor is not None

    @patch('src.db.db_connector.psycopg2.connect')
    def test_connect_failure(self, mock_connect):
        """Тест: ошибка подключения к БД."""
        from psycopg2 import OperationalError
        mock_connect.side_effect = OperationalError("Connection failed")
        db = DBConnector()
        with pytest.raises(ConnectionError, match="Ошибка подключения к БД"):
            db.connect()

    def test_disconnect(self):
        """Тест: закрытие соединения."""
        db = DBConnector()
        db.connection = Mock()
        db.cursor = Mock()
        db.disconnect()
        db.cursor.close.assert_called_once()
        db.connection.close.assert_called_once()

    def test_execute_query_without_connection(self):
        """Тест: выполнение запроса без подключения."""
        db = DBConnector()
        with pytest.raises(RuntimeError, match="Нет активного подключения"):
            db.execute_query("SELECT 1")

    @patch('src.db.db_connector.psycopg2.connect')
    def test_execute_query_select(self, mock_connect):
        """Тест: выполнение SELECT запроса."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1,)]

        # Создаём контекстный менеджер
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)

        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DBConnector()
        db.connect()
        result = db.execute_query("SELECT 1")

        assert result == [(1,)]
        mock_cursor.execute.assert_called_once()

    @patch('src.db.db_connector.psycopg2.connect')
    def test_execute_query_insert(self, mock_connect):
        """Тест: выполнение INSERT запроса."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)

        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DBConnector()
        db.connect()
        result = db.execute_query("INSERT INTO test VALUES (1)")

        assert result == []
        mock_cursor.execute.assert_called_once()
        mock_connection.commit.assert_called_once()

    @patch('src.db.db_connector.psycopg2.connect')
    def test_execute_many(self, mock_connect):
        """Тест: массовая вставка данных."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)

        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DBConnector()
        db.connect()
        db.execute_many("INSERT INTO test VALUES (%s)", [(1,), (2,)])

        mock_cursor.executemany.assert_called_once()
        mock_connection.commit.assert_called_once()

    @patch('src.db.db_connector.psycopg2.connect')
    def test_context_manager(self, mock_connect):
        """Тест: контекстный менеджер (with)."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        with DBConnector() as db:
            assert db.connection is not None

        mock_connection.close.assert_called_once()

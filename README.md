# ✈️ Трекер самолётов

Приложение для получения информации о самолётах, находящихся в воздушном пространстве выбранной страны, с использованием API OpenSky Network и Nominatim.

## 📋 Описание

Программа:
- Получает координаты страны через Nominatim API
- Запрашивает данные о самолётах через OpenSky API
- Сохраняет информацию в JSON-файл
- Показывает топ-N самолётов по высоте полёта

## 🛠️ Технологии

- Python 3.10+
- Poetry
- requests
- pytest / pytest-cov
- flake8 / isort

## 📦 Установка

```
git clone <url-репозитория>
cd project_flytracker
poetry install
```
## 🚀 Запуск
```
poetry run python main.py
```
## 🧪 Тесты
```
poetry run pytest -v
poetry run pytest --cov=src --cov-report=term
Покрытие тестами
100%
```
## 📁 Структура проекта
```
project_flytracker/
├── data/                  # JSON-файлы с самолётами
├── src/
│   ├── abstract_api.py    # абстрактный класс для API
│   ├── api.py             # работа с Nominatim и OpenSky
│   ├── aeroplane.py       # класс самолёта
│   ├── abstract_storage.py # абстрактный класс для хранения
│   └── json_storage.py    # сохранение в JSON
├── tests/                 # тесты
├── main.py                # взаимодействие с пользователем
├── pyproject.toml
└── README.md
```
## Пример работы
```
=== Трекер самолётов ===
Введите название страны: Canada
✅ Найдено самолётов: 1364
Введите количество самолётов для топа по высоте: 5
1. MYNNS | United Kingdom | Высота: 14325.6 м | Скорость: 234.1 м/с
2. EJA487 | United States | Высота: 13716.0 м | Скорость: 218.2 м/с
```
## Лицензия
MIT

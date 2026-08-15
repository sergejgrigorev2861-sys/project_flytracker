# ✈️ FlyRadar — Трекер самолётов

Приложение для получения информации о самолётах, находящихся в воздушном пространстве выбранных стран, с использованием API OpenSky Network и Nominatim. Данные сохраняются в **PostgreSQL** для последующего анализа.

---

## 📋 Описание

Программа:
- Получает координаты стран через **Nominatim API**
- Запрашивает данные о самолётах через **OpenSky API**
- Сохраняет информацию в **PostgreSQL** (таблицы `countries` и `aeroplanes`)
- Предоставляет аналитические запросы через класс **`DBManager`**

---

## 🛠️ Технологии

| Компонент | Инструмент |
|-----------|------------|
| Язык | Python 3.10+ |
| Управление зависимостями | Poetry |
| HTTP-запросы | requests |
| База данных | PostgreSQL + psycopg2-binary |
| Тестирование | pytest / pytest-cov |
| Линтинг | flake8 / isort |

---

## 📦 Установка и настройка

### 1. Клонируйте репозиторий
```
git clone <url-репозитория>
cd project_flytracker
```
### 2. Установите зависимости через Poetry
```
poetry install
```
### 3. Настройте базу данных
```
Создайте файл .env в корне проекта (на основе .env.example):

env
# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fly_radar
DB_USER=postgres
DB_PASSWORD=your_password

# API
OPENSKY_URL=https://opensky-network.org/api/states/all
NOMINATIM_URL=https://nominatim.openstreetmap.org/search

# Страны для анализа (через запятую)
COUNTRIES=USA,Germany,United Kingdom,United Arab Emirates
```
### 4. Создайте базу данных
```
В pgAdmin или через терминал создайте базу данных с именем fly_radar.
```

🚀 Запуск
```
poetry run python main.py

Программа:

Подключится к PostgreSQL

Создаст таблицы (если их нет)

Очистит старые данные

Загрузит новые данные по странам из .env

Выведет аналитику
```

🧪 Тесты
```
# Запуск всех тестов
poetry run pytest -v

# Запуск с покрытием
poetry run pytest --cov=src --cov-report=term
✅ Покрытие тестами: 98% (40 тестов)
```

📁 Структура проекта
```
project_flytracker/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── api_client.py       # работа с Nominatim и OpenSky
│   ├── db/
│   │   ├── __init__.py
│   │   ├── db_connector.py     # подключение к PostgreSQL
│   │   ├── db_creator.py       # создание таблиц
│   │   ├── db_loader.py        # загрузка данных
│   │   └── db_manager.py       # аналитические запросы
│   ├── __init__.py
│   └── config.py               # настройки из .env
├── tests/                      # тесты (40 шт.)
├── .env                        # переменные окружения
├── .flake8
├── .gitignore
├── main.py                     # точка входа
├── poetry.lock
├── pyproject.toml
└── README.md
```
📊 Пример работы
```
Загрузка данных

🛫 Загрузка данных о самолётах в PostgreSQL...
✅ Подключение к PostgreSQL установлено.
✅ Таблицы успешно созданы.
✅ Таблицы очищены.
📍 USA: 39.7837304, -100.445882
✅ Страна сохранена с ID: 1
🛩️ Найдено самолётов: 675
✅ Сохранено 675 самолётов в БД.
📍 Germany: 51.1638175, 10.4478313
...
Аналитика через DBManager
text
📊 Аналитические данные:

📍 Страны и количество самолётов:
  Germany: 2325
  United Arab Emirates: 95
  United Kingdom: 1173
  USA: 709

📊 Средняя скорость: 155.63 узлов

🚀 Самолёты со скоростью выше средней:
  ('781fb2', 'CCA852', 'Germany', 288.77)
  ('781fb2', 'CCA852', 'United Kingdom', 288.33)
  ...

🔍 Самолёты с позывным, содержащим 'AAL':
  ('ac7216', 'AAL1012', 'USA', 0.0, None)
  ('ab5383', 'AAL1032', 'USA', 224.58, 10668.0)
  ...
```
📌 Методы DBManager
```
Метод (описание)
get_countries_and_aeroplanes_count()	Список стран и количество самолётов
get_all_aeroplanes()	Список всех воздушных судов
get_avg_speed()	Средняя скорость по всем самолётам
get_aeroplanes_with_higher_speed()	Самолёты со скоростью выше средней
get_aeroplanes_with_keyword(keyword)	Поиск по позывному (например, AAL)
```
📄 Лицензия
MIT
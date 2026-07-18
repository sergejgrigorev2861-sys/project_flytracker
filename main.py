from src.api import APIAdapter
from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


def user_interaction():
    api = APIAdapter()
    storage = JSONStorage()

    print("\n=== Трекер самолётов ===")
    country = input("Введите название страны: ").strip()

    api.get_aeroplanes(country)
    if api.aeroplanes is None:
        print("❌ Страна не найдена или ошибка API.")
        return

    aeroplanes = Aeroplane.cast_to_object_list(api.aeroplanes)
    print(f"✅ Найдено самолётов: {len(aeroplanes)}")

    if not aeroplanes:
        print("Нет данных о самолётах.")
        return

    # Сохраняем в JSON
    for plane in aeroplanes:
        storage.add_aeroplane(plane)

    # Топ N по высоте
    try:
        top_n = int(input("Введите количество самолётов для топа по высоте: "))
        sorted_planes = sorted(aeroplanes, key=lambda x: x.altitude, reverse=True)
        for i, p in enumerate(sorted_planes[:top_n], 1):
            print(f"{i}. {p.callsign} | {p.country} | Высота: {p.altitude:.1f} м | Скорость: {p.velocity:.1f} м/с")
    except ValueError:
        print("Некорректный ввод.")


if __name__ == "__main__":
    user_interaction()
    
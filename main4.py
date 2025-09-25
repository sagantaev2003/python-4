import requests
import json
import random

API_BASE = "https://rickandmortyapi.com/api"

# переменные для опыта и истории
xp = 0
history = []

# сохранить историю
def save_history():
    with open("history.txt", "w", encoding="utf-8") as f:
        for h in history:
            f.write(h + "\n")
    print("📂 История сохранена в history.txt")

# поиск персонажа по имени
def find_character():
    global xp
    name = input("Введите имя персонажа: ")
    params = {"name": name}
    response = requests.get(f"{API_BASE}/character", params=params)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            char = data["results"][0]
            print()
            print("Имя:", char["name"])
            print("Статус:", char["status"])
            print("Вид:", char["species"])
            print("Локация:", char["location"]["name"])
            print("Эпизодов:", len(char["episode"]))

            xp += 10
            history.append(f"Найден персонаж: {char['name']}")

            save = input("Добавить в энциклопедию? (y/n): ")
            if save.lower() == "y":
                save_to_encyclopedia(char)
        else:
            print("❌ Персонаж не найден")
    else:
        print("Ошибка запроса:", response.status_code)

# поиск эпизод по номеру
def find_episode():
    global xp
    num = input("Введите номер эпизода: ")
    response = requests.get(f"{API_BASE}/episode/{num}")
    if response.status_code == 200:
        ep = response.json()
        print("Название:", ep["name"])
        print("Дата выхода:", ep["air_date"])
        print("Код эпизода:", ep["episode"])
        print("Персонажи (первые 5):")
        for c in ep["characters"][:5]:
            cdata = requests.get(c).json()
            print("-", cdata["name"])

        xp += 15
        history.append(f"Просмотрен эпизод: {ep['name']}")
    else:
        print("❌ Эпизод не найден")

# поиск локация по имени
def find_location():
    global xp
    name = input("Введите название локации: ")
    params = {"name": name}
    response = requests.get(f"{API_BASE}/location", params=params)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            loc = data["results"][0]
            print("Название:", loc["name"])
            print("Тип:", loc["type"])
            print("Измерение:", loc["dimension"])
            print("Жителей:", len(loc["residents"]))

            xp += 10
            history.append(f"Найдена локация: {loc['name']}")
        else:
            print("❌ Локация не найдена")
    else:
        print("Ошибка:", response.status_code)

# случайный персонаж
def random_character():
    global xp
    rid = random.randint(1, 826)
    response = requests.get(f"{API_BASE}/character/{rid}")
    if response.status_code == 200:
        char = response.json()
        print("🎲 Случайный персонаж!")
        print("Имя:", char["name"])
        print("Статус:", char["status"])
        print("Вид:", char["species"])
        print("Локация:", char["location"]["name"])

        xp += 5
        history.append(f"Случайный персонаж: {char['name']}")
    else:
        print("Ошибка:", response.status_code)

# список все эпизоды
def list_episodes():
    global xp
    url = f"{API_BASE}/episode"
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for ep in data["results"]:
                print(f"{ep['id']}. {ep['name']} ({ep['episode']})")
            url = data["info"]["next"]
        else:
            print("Ошибка при загрузке эпизодов")
            break

    xp += 20
    history.append("Просмотрен список эпизодов")

# сохранить .json
def save_to_encyclopedia(char):
    entry = {
        "name": char["name"],
        "status": char["status"],
        "species": char["species"],
        "location": char["location"]["name"],
        "episodes_count": len(char["episode"])
    }

    try:
        with open("encyclopedia.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open("encyclopedia.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ Сохранено в encyclopedia.json")

# главное меню
def main():
    global xp, history
    while True:
        print("\nМеню:")
        print("1 – Найти персонажа")
        print("2 – Найти эпизод")
        print("3 – Найти локацию")
        print("4 – Случайный персонаж")
        print("5 – Список всех эпизодов")
        print("6 – Выход")
        print()
        choice = input("Ваш выбор: ")

        if choice == "1":
            find_character()
        elif choice == "2":
            find_episode()
        elif choice == "3":
            find_location()
        elif choice == "4":
            random_character()
        elif choice == "5":
            list_episodes()
        elif choice == "6":
            print("\n🎉 Спасибо за игру!")
            print(f"Ваш опыт: {xp} XP")
            print("История действий:")
            for h in history:
                print("-", h)
            save_history()  # history.txt
            break
        else:
            print("❌ Неверный ввод")

if __name__ == "__main__":
    main()

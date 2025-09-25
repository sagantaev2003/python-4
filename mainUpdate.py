import requests
import json
import random
import datetime

API_BASE = "https://rickandmortyapi.com/api"

# переменные опыт и история
xp = 0
history = []

# сохранить история
def save_history():
    with open("history.txt", "w", encoding="utf-8") as f:
        for h in history:
            f.write(h + "\n")
    print("📂 История сохранена в history.txt")

# поиск персонаж
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

            rate = input("Оцените персонажа от 1 до 5 (или Enter для пропуска): ")
            if rate.isdigit() and 1 <= int(rate) <= 5:
                save_to_encyclopedia(char, rating=int(rate))
        else:
            print("❌ Персонаж не найден")
    else:
        print("Ошибка запроса:", response.status_code)

# поиск эпизод
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

# поиск локация
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

            if loc["residents"]:
                print("\nСписок жителей:")
                for url in loc["residents"]:
                    cdata = requests.get(url).json()
                    print("-", cdata["name"])
            else:
                print("В этой локации нет жителей.")

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

# список эпизодов
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

# сохранить в энциклопедию .json
def save_to_encyclopedia(char, rating=None):
    entry = {
        "name": char["name"],
        "status": char["status"],
        "species": char["species"],
        "location": char["location"]["name"],
        "episodes_count": len(char["episode"]),
    }
    if rating:
        entry["rating"] = rating

    try:
        with open("encyclopedia.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open("encyclopedia.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ Сохранено в encyclopedia.json")

# сравнение персонаж
def compare_characters_infinite():
    global xp, history
    print("\n⚔️ Турнир персонажей (бесконечный)! Выбирай любимого персонажа.")
    print("Чтобы выйти из турнира, введите 0.\n")

    # случайный фаворит
    current_fav_id = random.randint(1, 826)
    response = requests.get(f"{API_BASE}/character/{current_fav_id}")
    if response.status_code != 200:
        print("Ошибка загрузки персонажа")
        return
    current_fav = response.json()

    while True:
        # новый соперник
        challenger_id = random.randint(1, 826)
        response = requests.get(f"{API_BASE}/character/{challenger_id}")
        if response.status_code != 200:
            print("Ошибка загрузки персонажа")
            continue
        challenger = response.json()

        print(f"\nТекущий фаворит: {current_fav['name']} ({current_fav['species']}, {current_fav['status']})")
        print(f"Соперник: {challenger['name']} ({challenger['species']}, {challenger['status']})")
        choice = input("Кого выбираете? (1 — фаворит / 2 — соперник / 0 — выйти): ")

        if choice == "1":
            print(f"✅ Вы оставили {current_fav['name']}")
            history.append(f"Выбран фаворит: {current_fav['name']}")
        elif choice == "2":
            current_fav = challenger
            print(f"✅ Теперь фаворит: {current_fav['name']}")
            history.append(f"Выбран фаворит: {current_fav['name']}")
        elif choice == "0":
            print(f"\n🏆 Финальный фаворит: {current_fav['name']}!")
            history.append(f"Финальный фаворит турнира: {current_fav['name']}")
            xp += 20
            break
        else:
            print("❌ Неверный ввод, попробуйте снова")
            continue

        xp += 5  

# фильтр персонаж
def filter_characters():
    global xp
    print("\nФильтры:")
    print("1 – Только живые")
    print("2 – Только мёртвые")
    print("3 – Только инопланетяне")
    choice = input("Ваш выбор: ")

    params = {}
    if choice == "1":
        params["status"] = "alive"
    elif choice == "2":
        params["status"] = "dead"
    elif choice == "3":
        params["species"] = "alien"
    else:
        print("❌ Неверный выбор")
        return

    response = requests.get(f"{API_BASE}/character", params=params)
    if response.status_code == 200:
        data = response.json()
        for char in data["results"]:
            print("-", char["name"], f"({char['status']}, {char['species']})")
        xp += 15
        history.append("Использован фильтр персонажей")
    else:
        print("Ошибка фильтрации")

# поиск эпизодов по сезон
def find_episodes_by_season():
    global xp
    season = input("Введите сезон (например, S01, S02): ").upper()
    url = f"{API_BASE}/episode"
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print("Ошибка загрузки эпизодов")
            break
        data = response.json()
        for ep in data["results"]:
            if ep["episode"].startswith(season):
                print(f"{ep['id']}. {ep['name']} ({ep['episode']})")
        url = data["info"]["next"]

    xp += 20
    history.append(f"Поиск эпизодов по сезону {season}")

# случайный квест
def random_quest():
    global xp, history
    rid = random.randint(1, 826)
    response = requests.get(f"{API_BASE}/character/{rid}")
    if response.status_code == 200:
        char = response.json()

        print("\n🕹 Случайный квест!")
        print("Угадай персонажа по подсказкам:")
        print("Статус:", char["status"])
        print("Вид:", char["species"])
        print("Локация:", char["location"]["name"])

        guess = input("Кто это? ").strip()
        if guess.lower() == char["name"].lower():
            print("✅ Верно! Это был", char["name"])
            xp += 30
            history.append(f"Угадан персонаж в квесте: {char['name']}")
        else:
            print("❌ Неверно. Это был", char["name"])
            history.append(f"Провален квест (был {char['name']})")
    else:
        print("Ошибка при загрузке квеста")

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
        print("6 – Сравнение персонажей")
        print("7 – Фильтр персонажей")
        print("8 – Поиск эпизодов по сезону")
        print("9 – Случайный квест")
        print("0 – Выход")
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
            compare_characters_infinite()
        elif choice == "7":
            filter_characters()
        elif choice == "8":
            find_episodes_by_season()
        elif choice == "9":
            random_quest()
        elif choice == "0":
            print("\n🎉 Спасибо за игру!")
            print(f"Ваш опыт: {xp} XP")
            print("История действий:")
            for h in history:
                print("-", h)

            # сохранить история txt
            with open("history.txt", "w", encoding="utf-8") as f:
                for h in history:
                    f.write(h + "\n")

            # сохранить история .json
            history_with_time = []
            for h in history:
                history_with_time.append({
                    "action": h,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(history_with_time, f, ensure_ascii=False, indent=2)

            print("✅ История сохранена в history.txt и history.json")
            break
        else:
            print("❌ Неверный ввод")

if __name__ == "__main__":
    main()

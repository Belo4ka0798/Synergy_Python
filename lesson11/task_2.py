import collections

# База данных питомцев
pets = {
    1: {
        "Мухтар": {
            "Вид питомца": "Собака",
            "Возраст питомца": 9,
            "Имя владельца": "Павел"
        }
    },
    2: {
        "Kaa": {
            "Вид питомца": "желторотый питон",
            "Возраст питомца": 19,
            "Имя владельца": "Саша"
        }
    }
}


def get_suffix(age):
    if age % 10 == 1 and age != 11:
        return "год"
    elif 2 <= age % 10 <= 4 and (age < 10 or age > 20):
        return "года"
    else:
        return "лет"


def get_pet(ID):
    return pets[ID] if ID in pets else False


def pets_list():
    if not pets:
        print("В базе данных нет питомцев")
        return

    print("\n--- Список всех питомцев ---")
    for pet_id in pets:
        pet_data = get_pet(pet_id)
        pet_name = list(pet_data.keys())[0]
        pet_info = pet_data[pet_name]
        age_suffix = get_suffix(pet_info["Возраст питомца"])

        print(f'ID: {pet_id}, {pet_info["Вид питомца"]} "{pet_name}", '
              f'Возраст: {pet_info["Возраст питомца"]} {age_suffix}, '
              f'Владелец: {pet_info["Имя владельца"]}')
    print("---------------------------")


def create():
    # Получаем последний ID и увеличиваем на 1
    if pets:
        last = collections.deque(pets, maxlen=1)[0]
        new_id = last + 1
    else:
        new_id = 1

    # Запрашиваем информацию о питомце
    print(f"\nДобавление питомца с ID {new_id}:")
    pet_name = input("Введите кличку питомца: ")
    pet_type = input("Введите вид питомца: ")

    while True:
        try:
            pet_age = int(input("Введите возраст питомца: "))
            if pet_age < 0:
                print("Возраст не может быть отрицательным!")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число для возраста!")

    owner_name = input("Введите имя владельца: ")

    # Добавляем питомца в базу
    pets[new_id] = {
        pet_name: {
            "Вид питомца": pet_type,
            "Возраст питомца": pet_age,
            "Имя владельца": owner_name
        }
    }

    print(f"Питомец {pet_name} успешно добавлен с ID {new_id}")


def read():
    try:
        pet_id = int(input("Введите ID питомца для просмотра: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return

    pet_data = get_pet(pet_id)

    if not pet_data:
        print(f"Ошибка: Питомец с ID {pet_id} не найден!")
        return

    pet_name = list(pet_data.keys())[0]
    pet_info = pet_data[pet_name]
    age_suffix = get_suffix(pet_info["Возраст питомца"])

    print(f'Это {pet_info["Вид питомца"]} по кличке "{pet_name}". '
          f'Возраст питомца: {pet_info["Возраст питомца"]} {age_suffix}. '
          f'Имя владельца: {pet_info["Имя владельца"]}')


def update():
    try:
        pet_id = int(input("Введите ID питомца для обновления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return

    pet_data = get_pet(pet_id)

    if not pet_data:
        print(f"Ошибка: Питомец с ID {pet_id} не найден!")
        return

    current_pet_name = list(pet_data.keys())[0]
    pet_info = pet_data[current_pet_name]

    print(f"\nТекущая информация о питомце (ID: {pet_id}):")
    print(f"Кличка: {current_pet_name}")
    print(f"Вид: {pet_info['Вид питомца']}")
    print(f"Возраст: {pet_info['Возраст питомца']}")
    print(f"Владелец: {pet_info['Имя владельца']}")

    print("\nВведите новые данные (оставьте пустым, если не нужно менять):")

    new_pet_name = input(f"Новая кличка [{current_pet_name}]: ").strip()
    new_pet_type = input(f"Новый вид [{pet_info['Вид питомца']}]: ").strip()

    new_pet_age = input(f"Новый возраст [{pet_info['Возраст питомца']}]: ").strip()
    new_owner_name = input(f"Новый владелец [{pet_info['Имя владельца']}]: ").strip()

    # Обновляем данные
    if new_pet_name and new_pet_name != current_pet_name:
        pet_data[new_pet_name] = pet_info
        del pet_data[current_pet_name]
        current_pet_name = new_pet_name

    if new_pet_type:
        pet_info["Вид питомца"] = new_pet_type

    if new_pet_age:
        try:
            pet_info["Возраст питомца"] = int(new_pet_age)
        except ValueError:
            print("Ошибка: Возраст должен быть числом! Возраст не изменен.")

    if new_owner_name:
        pet_info["Имя владельца"] = new_owner_name

    print(f"Информация о питомце с ID {pet_id} успешно обновлена")


def delete():
    try:
        pet_id = int(input("Введите ID питомца для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return

    pet_data = get_pet(pet_id)

    if not pet_data:
        print(f"Ошибка: Питомец с ID {pet_id} не найден!")
        return

    pet_name = list(pet_data.keys())[0]
    del pets[pet_id]
    print(f"Питомец {pet_name} с ID {pet_id} успешно удален")


def main():
    print("=== Система управления ветеринарной клиникой ===")
    print("Доступные команды: create, read, update, delete, list, stop")

    command = ""
    while command != "stop":
        command = input("\nВведите команду: ").strip().lower()

        if command == "create":
            create()
        elif command == "read":
            read()
        elif command == "update":
            update()
        elif command == "delete":
            delete()
        elif command == "list":
            pets_list()
        elif command == "stop":
            print("Работа программы завершена. До свидания!")
        else:
            print("Неизвестная команда! Доступные команды: create, read, update, delete, list, stop")


# Запуск программы
if __name__ == "__main__":
    main()
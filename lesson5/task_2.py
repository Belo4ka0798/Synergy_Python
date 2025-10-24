# Ввод слова
word = input("Введите слово из маленьких латинских букв: ")

# Определяем гласные буквы
vowels = "aeiou"
vowels_list = ['a', 'e', 'i', 'o', 'u']

# Счетчики
total_vowels = 0
total_consonants = 0
vowels_count = {vowel: 0 for vowel in vowels_list}  # Словарь для подсчета каждой гласной

# Анализируем каждую букву в слове
for letter in word:
    if letter in vowels:
        total_vowels += 1
        vowels_count[letter] += 1
    else:
        total_consonants += 1

# Вывод результатов
print(f"Общее количество гласных: {total_vowels}")
print(f"Общее количество согласных: {total_consonants}")

# Вывод количества каждой гласной буквы
print("\nКоличество каждой гласной буквы:")
for vowel in vowels_list:
    count = vowels_count[vowel]
    print(f"{vowel}: {count}")
    if count == 0:
        print(f"{vowel}: False")
import matplotlib.pyplot as plt
from collections import Counter
import math

def preprocess_text(text):
    """
    Преобразует текст: удаляет пробелы, знаки препинания, переводит в нижний регистр,
    оставляя только буквы русского алфавита.
    """
    allowed_chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    text = text.lower()
    clean_text = ''.join([char for char in text if char in allowed_chars])
    return clean_text


def calculate_entropy_k(text, k):
    """
    Вычисляет энтропию Hk(T) для заданного k.
    """
    n = len(text)

    # Проверка, на возможность создания k-граммы
    if n < k:
        return 'Невозможно построить такую k-грамму'

    # Разбиение текста на k-граммы
    k_grams = [text[i:i + k] for i in range(n - k + 1)]

    # Подсчет частоты встречаемости k-грамм
    k_gram_counts = Counter(k_grams)
    total_k_grams = sum(k_gram_counts.values())

    # Вычисление энтропии Hk
    entropy = -sum((count / total_k_grams) * math.log2(count / total_k_grams) for count in k_gram_counts.values())
    return entropy


def plot_entropy_ratios(entropies):
    """
    Строит график зависимости Hk(T)/k от k.
    """
    ks = list(range(1, len(entropies) + 1))
    ratios = [entropies[k - 1] / k for k in ks]

    plt.figure(figsize=(8, 6))
    plt.plot(ks, ratios, marker='o', linestyle='-', color='b')
    plt.title("Зависимость Hk(T)/k от k")
    plt.xlabel("k")
    plt.ylabel("Hk(T)/k")
    plt.xticks(ks)
    plt.yticks(ratios)
    plt.grid(True)
    plt.show()

text = input("Введите текст: ")

clean_text = preprocess_text(text)
print(clean_text)
print()

max_k = int(input("Введите k: "))
entropies = []
for k in range(1, max_k + 1):
    entropy_k = calculate_entropy_k(clean_text, k)
    entropies.append(entropy_k)
    print(f"H{k}(T) = {entropy_k:.4f}")
    print()
    print(f"H{k}(T)/k = {entropy_k/k:.4f}")
    print()

plot_entropy_ratios(entropies)

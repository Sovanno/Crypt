from math import isqrt
from itertools import combinations
from sympy import primerange, isprime

def gcd_extended(a, b):
    """
    Расширенный алгоритм Евклида для нахождения gcd и обратного элемента.
    Возвращает gcd(a, b), x, y такие, что gcd(a, b) = ax + by.
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def trial_division_with_gcd(n):
    """
    Факторизация числа n с,
    где вычисляется НОД между n и произведениями троек простых чисел.
    """
    # Генерация списка простых чисел до sqrt(n)
    primes = list(primerange(2, isqrt(n) + 1))

    # Проверка делимости n на произведение троек простых чисел
    for triple in combinations(primes, 3):  # Перебираем тройки простых чисел
        product = triple[0] * triple[1] * triple[2]
        divisor, _, _ = gcd_extended(n, product)  # Находим НОД
        if 1 < divisor < n and isprime(n // divisor) and isprime(divisor):  # Нашли делитель
            return divisor, n // divisor
    raise ValueError("Не удалось найти множители с использованием заданного метода.")


def modular_exponentiation(base, exp, mod):
    """
    Бинарный алгоритм возведения в степень по модулю.
    Вычисляет (base^exp) % mod.
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:  # Если степень нечетная
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result


def calculate_private_key(e, p, q):
    """
    Вычисляет закрытый ключ d для RSA.
    """
    phi_n = (p - 1) * (q - 1)
    _, d, _ = gcd_extended(e, phi_n)
    d = d % phi_n
    if d < 0:
        d += phi_n
    return d


def decrypt(private_key, n, ciphertext):
    """
    Расшифровывает текст с использованием закрытого ключа.
    """
    decrypt_alphabet = {
        10: 'а', 11: 'б', 12: 'в', 13: 'г', 14: 'д', 15: 'е', 16: 'ж', 17: 'з', 18: 'и', 19: 'й', 20: 'к', 21: 'л',
        22: 'м', 23: 'н', 24: 'о', 25: 'п', 26: 'р', 27: 'с', 28: 'т', 29: 'у', 30: 'ф', 31: 'х', 32: 'ц', 33: 'ч',
        34: 'ш', 35: 'щ', 36: 'ъ', 37: 'ы', 38: 'ь', 39: 'э', 40: 'ю', 41: 'я', 99: ' '
    }
    d = private_key
    n = n
    ciphertext = ciphertext.split()
    blocks = ''.join([str(modular_exponentiation(int(i), d, n)) for i in ciphertext])
    print(f"Расшифрованное сообщение: {blocks}")
    return True

# Данные задачи
e = 251
n = 77173
ciphertext = 37325
private_key_d = ()
p = int
q = int
while True:
    f = int(input(f"Выберите действие: 1)Факторизация 2) Вычислекние закрытого ключа 3) Расшифровка"))

    if f == 1:
        n = int(input(f"Введите n"))
        # Шаг 1: Факторизация n
        print("Факторизация числа n методом пробного деления...")
        p, q = trial_division_with_gcd(n)
        print(f"Найдено: p = {p}, q = {q}")

    elif f == 2:
        e = int(input(f"Введите e:"))
        # Шаг 2: Вычисление закрытого ключа
        print("Вычисление закрытого ключа...")
        d = calculate_private_key(e, p, q)
        print(f"Закрытый ключ: d = {d}")

    elif f == 3:
        ciphertext = input(f"Введите зашифрованный текст:")
        # Шаг 3: Расшифрование сообщения
        print("Расшифрование сообщения...")
        plaintext = decrypt(d, n, ciphertext)

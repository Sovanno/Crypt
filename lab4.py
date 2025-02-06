import random
from sympy import isprime
p = 197
q = 349

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


def generate_keys(p, q):
    """
    Генерирует пару открытого и закрытого ключей (e, n) и (d, n) для RSA.
    """
    if not (isprime(p) and isprime(q)):
        raise ValueError("p и q должны быть простыми числами.")
    if p == q:
        raise ValueError("p и q должны быть разными.")

    # Вычисляем n и φ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Выбираем e (1 < e < φ(n)), взаимно простое с φ(n)
    e = random.randrange(2, phi_n)
    g, _, _ = gcd_extended(e, phi_n)
    while g != 1:
        e = random.randrange(2, phi_n)
        g, _, _ = gcd_extended(e, phi_n)

    # Вычисляем d, обратное к e по модулю φ(n)
    _, d, _ = gcd_extended(e, phi_n)
    d = d % phi_n
    if d < 0:
        d += phi_n

    return (e, n), (d, n)

def add_e_key(e, p, q):
    """
        Добавляет пару открытого и закрытого ключей (e, n) и (d, n) для RSA.
    """
    # Вычисляем n и φ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    g, _, _ = gcd_extended(e, phi_n)
    if g != 1:
        raise ValueError("e и (p - 1) * (q - 1) должны быть взаимно простыми.")

    # Вычисляем d, обратное к e по модулю φ(n)
    _, d, _ = gcd_extended(e, phi_n)
    d = d % phi_n
    if d < 0:
        d += phi_n

    return (e, n), (d, n)

def split_into_blocks(text, n):
    m = []
    while len(text) > 0:
        block = text[:len(str(n))]
        if (int(block) > n):
            block = text[:len(str(n)) - 1]
        if (int(text[:len(block) + 1]) % 10 == 0) and len(text[:len(block) + 1]) > 2:
            block = text[:len(block) - 1]
        text = text[len(block):]
        m.append(int(block))
    return m

def encrypt(public_key, plaintext):
    """
    Шифрует текст с использованием открытого ключа.
    """
    plaintext = plaintext.lower()
    e, n = public_key
    encrypt_alphabet = {
        'а': 10, 'б': 11, 'в': 12, 'г': 13, 'д': 14, 'е': 15, 'ж': 16, 'з': 17, 'и': 18, 'й': 19, 'к': 20, 'л': 21,
        'м': 22, 'н': 23, 'о': 24, 'п': 25, 'р': 26, 'с': 27, 'т': 28, 'у': 29, 'ф': 30, 'х': 31, 'ц': 32, 'ч': 33,
        'ш': 34, 'щ': 35, 'ъ': 36, 'ы': 37, 'ь': 38, 'э': 39, 'ю': 40, 'я': 41, ' ': 99
    }
    plaintext_ints = "".join(map(str, [encrypt_alphabet[char] for char in plaintext]))  # Преобразуем символы в числа
    blocks = split_into_blocks(plaintext_ints, n) # Делим на блоки
    print(blocks)
    ciphertext = [modular_exponentiation(int(pt), e, n) for pt in blocks]
    return ciphertext


def decrypt(private_key, ciphertext):
    """
    Расшифровывает текст с использованием закрытого ключа.
    """
    decrypt_alphabet = {
        10: 'а', 11: 'б', 12: 'в', 13: 'г', 14: 'д', 15: 'е', 16: 'ж', 17: 'з', 18: 'и', 19: 'й', 20: 'к', 21: 'л',
        22: 'м', 23: 'н', 24: 'о', 25: 'п', 26: 'р', 27: 'с', 28: 'т', 29: 'у', 30: 'ф', 31: 'х', 32: 'ц', 33: 'ч',
        34: 'ш', 35: 'щ', 36: 'ъ', 37: 'ы', 38: 'ь', 39: 'э', 40: 'ю', 41: 'я', 99: ' '
    }
    d, n = private_key
    ciphertext = ciphertext.split()
    blocks = ''.join([str(modular_exponentiation(int(i), d, n)) for i in ciphertext])
    decr = []
    while len(blocks) > 0:
        decr.append(decrypt_alphabet[int(blocks[:2])])
        blocks = blocks[2:]
    plaintext = ''.join(decr)
    return plaintext

print("RSA: Генерация ключей, шифрование и расшифрование.")
f = True

# Генерация трех пар ключей
keys = []
for i in range(3):
    public_key, private_key = generate_keys(p, q)
    keys.append((public_key, private_key))
    print(f"Пара ключей {i + 1}:")
    print(f"  Открытый ключ: {public_key}")
    print(f"  Закрытый ключ: {private_key}")


while f == True:

    choi = int(input(f"1) Добавить ключ 2) Зашифровать 3) Расшифровать"))

    if choi == 1:
        flag = int(input('Вы хотите добавить ещё один ключ:Да(0)/Нет(1)'))
        while flag == 0:
            try:
                e = int(input('Введите е:'))
                public_key, private_key = add_e_key(e, p, q)
                keys.append((public_key, private_key))
                print(f"  Открытый ключ: {public_key}")
                print(f"  Закрытый ключ: {private_key}")
                flag = int(input('Вы хотите добавить ещё один ключ:Да(0)/Нет(1)'))
            except:
                print("Ключ не подходит, попробуйте другой")

    elif choi == 2:
        # Пользователь вводит текст для шифрования
        plaintext = input("Введите текст для шифрования: ")
        k = 1
        for p in keys:
            print(f"  Ключи шифрования {k}: {p}")
            k += 1

        # Выбор ключа для шифрования
        key_index = int(input("Выберите номер ключа для шифрования: ")) - 1
        public_key, private_key = keys[key_index]

        # Шифрование
        ciphertext = encrypt(public_key, plaintext)
        with open("result.txt", "a", encoding="utf-8") as file:
            file.write('\n')
            file.write(f'ШИФР-ТЕКСТ (ШТ): {ciphertext}\n')
            file.write(f'КЛЮЧ ОТКРЫТЫЙ: {public_key}\n')
            file.write(f'КЛЮЧ ЗАКРЫТЫЙ: {private_key}\n')

    elif choi == 3:
        ciphertext = input("Введите текст для дешифрования: ")
        k = 1
        for p in keys:
            print(f"  Ключи шифрования {k}: {p}")
            k += 1

        # Выбор ключа для шифрования
        key_index = int(input("Выберите номер ключа для дешифрования: ")) - 1
        public_key, private_key = keys[key_index]

        # Расшифрование
        decrypted_text = decrypt(private_key, ciphertext)
        with open("enc_result.txt", "a", encoding="utf-8") as file:
            file.write('\n')
            file.write(f'РАСШИФР-ТЕКСТ (ШТ): {decrypted_text}\n')
            file.write(f'КЛЮЧ ОТКРЫТЫЙ: {public_key}\n')
            file.write(f'КЛЮЧ ЗАКРЫТЫЙ: {private_key}\n')

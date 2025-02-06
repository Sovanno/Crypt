from collections import Counter

def m_a(t):
    return ord(t) - ord('а')

def search_nod(a, b):
    if a == 0:
        return b, 0, 1
    nod, x1, y1 = search_nod(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return nod, x, y

def inverse_element(a, m):
    nod, x, y = search_nod(a, m)
    if nod != 1:
        return None
    else:
        return x % m

def solve_congruence(a, b, m):
    nod, x, y = search_nod(a, m)
    if b % nod != 0:
        return None
    else:
        x0 = (x * (b // nod)) % m
        solutions = [(x0 + i * (m // nod)) % m for i in range(nod)]
        return solutions

def solve_system_of_congruences(a, b, c, d, m=32):
    if (a - c) < 0:
        solutions_x = solve_congruence(-(a - c), -(b - d), m)
    else:
        solutions_x = solve_congruence(a - c, b - d, m)
    if not solutions_x:
        return None, None
    y = [(b - a * x) % m for x in solutions_x]
    return solutions_x, y

def frequency_analysis(ciphertext):
    counter = Counter(ciphertext)
    most_common = counter.most_common(2)
    return most_common

def guess_plaintext_letters(common_cipher_letters, most):
    common_plaintext_letters_1 = [most[0], most[1]]
    common_plaintext_letters_2 = [most[1], most[0]]
    print(common_plaintext_letters_1)
    print(common_plaintext_letters_2)
    return list(zip(common_plaintext_letters_1, common_cipher_letters)), list(zip(common_plaintext_letters_2, common_cipher_letters))

def affine_decrypt(ciphertext, a, b, m=32):
    inverse_a = inverse_element(a, m)
    if inverse_a is None:
        return None
    plaintext = ''
    for char in ciphertext:
        if char.isalpha():
            x = m_a(char)
            p = (inverse_a * (x - b)) % m
            plaintext += chr(p + ord('а'))
        else:
            plaintext += char
    return plaintext

def brute_force_affine(ciphertext, m=32):
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(f"\n")
    most_common = frequency_analysis(ciphertext)
    Most_letters = 'оеаитнсрвлкмдпуяызъбгчйхжюшцщэф'

    for i in range(len(Most_letters)):
        for j in range(i+1, len(Most_letters)-i):
            letters_1 = guess_plaintext_letters([most_common[0][0], most_common[1][0]], [Most_letters[i], Most_letters[j]])[0]
            letters_2 = guess_plaintext_letters([most_common[0][0], most_common[1][0]], [Most_letters[i], Most_letters[j]])[1]
            a, b = solve_system_of_congruences(m_a(letters_1[0][0]), m_a(letters_1[0][1]), m_a(letters_1[1][0]), m_a(letters_1[1][1]))
            if a is None:
                continue
            for h in range(len(a)):
                plaintext = affine_decrypt(ciphertext, a[h], b[h], m)
                print(f"Попытка: a = {a}, b = {b} -> {plaintext}")
                with open("result.txt", "a", encoding="utf-8") as file:
                    file.write(f"ШИФР-ТЕКСТ (ШТ): {plaintext}\n")
                    file.write(f"КЛЮЧ: {a, b}\n")
                    file.write(f"\n")
                input()
            a, b = solve_system_of_congruences(m_a(letters_2[0][0]), m_a(letters_2[0][1]), m_a(letters_2[1][0]), m_a(letters_2[1][1]))
            print(a, b)
            if a is None:
                continue
            for h in range(len(a)):
                plaintext = affine_decrypt(ciphertext, a[0], b[0], m)
                print(f"Попытка: a = {a}, b = {b} -> {plaintext}")
                with open("result.txt", "a", encoding="utf-8") as file:
                    file.write(f"ШИФР-ТЕКСТ (ШТ): {plaintext}\n")
                    file.write(f"КЛЮЧ: {a, b}\n")
                    file.write(f"\n")
                input()
            cntn = input('Продолжить? (Y/N): ')
            if cntn == 'n' or cntn == 'N':
                break
        if cntn == 'n' or cntn == 'N':
            break

def affine_encrypt(ciphertext, a, b, m=32):
    nod = search_nod(a, m)[0]
    if nod != 1:
        return None
    plaintext = ''
    for char in ciphertext:
        if char.isalpha():
            x = m_a(char)
            c = ((x * a) + b) % m
            plaintext += chr(c + ord('а'))
        else:
            plaintext += char
    return plaintext

Chois = int(input("Выберите действие: (1) Обратный элемента, (2) Решение сравнения вида ax mod m ≡ b, "
                  "(3) Решение системы сравнений вида (ax + y)mod m ≡ b,(cx + y)mod m ≡ d."
                  "(4) Частотный анализ, (5) Выдвижение предположений,"
                  "(6) Расшифровка текста"))

if Chois == 1:
    a = int(input("Введите число a: "))
    m = int(input("Введите модуль m: "))
    inverse = inverse_element(a, m)
    if inverse is None:
        print(f"Обратного элемента для {a} по модулю {m} не существует.")
    else:
        print(f"Обратный элемент для {a} по модулю {m} равен {inverse}.")

elif Chois == 2:
    a = int(input("Введите a: "))
    b = int(input("Введите b: "))
    m = int(input("Введите модуль m: "))
    solutions = solve_congruence(a, b, m)
    if solutions is None:
        print("Решений нет.")
    else:
        print(f"Решения сравнения: {solutions}")

elif Chois == 3:
    a = int(input("Введите a: "))
    b = int(input("Введите b: "))
    c = int(input("Введите c: "))
    d = int(input("Введите d: "))
    m = int(input("Введите модуль m: "))
    solution = solve_system_of_congruences(a, b, c, d, m)
    if solution is not None:
        print(f"Решение системы: x = {solution[0]}, y = {solution[1]}")
    else:
        print("Система неразрешима.")

elif Chois == 4:
    ciphertext = input("Введите шифр-текст: ")
    most_common_letters = frequency_analysis(ciphertext)
    print(f"Две самые частые буквы: {most_common_letters}")

elif Chois == 5:
    most_letters = ['о', 'е']
    cipher_letters = ['м', 'о']
    guesses = guess_plaintext_letters(cipher_letters, most_letters)
    print(f"Предположительные буквы: {guesses}")

elif Chois == 6:
    ciphertext = input("Введите шифр-текст: ")
    brute_force_affine(ciphertext)

elif Chois == 7:
    ciphertext = input("Введите шифр-текст: ")
    a = int(input("Введите a: "))
    b = int(input("Введите b: "))
    print(affine_encrypt(ciphertext, a, b))

elif Chois == 8:
    ciphertext = input("Введите шифр-текст: ")
    a = int(input("Введите a: "))
    b = int(input("Введите b: "))
    print(affine_decrypt(ciphertext, a, b))

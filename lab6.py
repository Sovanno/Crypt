def integer_square_root(m):
    if m < 0:
        raise ValueError("Квадратный корень от отрицательного числа не определен.")
    if m == 0:
        return 0
    x = m
    while True:
        y = (x + m // x) // 2
        if y >= x:
            return x
        x = y

def quadratic_sieve(m, a, b, c):

    def sieve_modulo(m, modul):
        x_filtr = set()
        results = []
        for x in range(modul):
            x2 = x ** 2 % modul
            z = (x2 - m) % modul
            if z < 0:
                z += modul
            lej = (z ** ((modul - 1) / 2)) % modul
            if lej == 1 or lej == 0:
                x_filtr.add(x)

            results.append((x, x2, z))
        print(f"\nРешето для модуля {modul}")
        for x, xm, z in results:
            print(f"x = {x}, x^2mod m = {xm}, Z = {z}")
        return x_filtr

    def find_factors(x, y):
        p = x + y
        q = x - y
        return abs(p), abs(q)

    x_filtr_a = sieve_modulo(m, a)
    x_filtr_b = sieve_modulo(m, b)
    x_filtr_c = sieve_modulo(m, c)

    print('квадратичные вычеты по модулю a' ,x_filtr_a)
    print('квадратичные вычеты по модулю b' ,x_filtr_b)
    print('квадратичные вычеты по модулю c' ,x_filtr_c)

    start_x = integer_square_root(m) + 0
    end_x = (m + 1) // 2

    print(f"\nНаложение решет на диапазон чисел от {start_x} до {end_x}")
    for x in range(start_x, end_x):
        a_z = x % a
        b_z = x % b
        c_z = x % c
        if x == 254: print(a_z, b_z, c_z)
        if a_z in x_filtr_a and b_z in x_filtr_b and c_z in x_filtr_c:
            z = x ** 2 - m
            y = integer_square_root(z)
            if y ** 2 == z:
                print(f"Найдено: x = {x}, y = {y}, z = {z}")
                p, q = find_factors(x, y)
                if p and q:
                    print(f"Делители: p = {p}, q = {q}")
                    return p, q

    print("Не удалось найти делители с использованием метода квадратичного решета.")
    return None, None


def gcd_e(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_e(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def rho_method(m, x0, a, b, num):

    def f(x, a, b):
        return ((a * x ** 2) + (b)) % m

    x1, x2, d = x0, x0, 1
    step = 0
    print(f"Шаг {step}: x = {x1}, y = {x2}, |x1 - x2| = - НОД = -")
    for _ in range(num):
        if 1 < d and d < m:
            break
        x1 = f(x1, a, b)
        x2 = f(f(x2, a, b), a, b)
        d, _, _ = gcd_e(abs(x1 - x2), m)
        step += 1
        print(f"Шаг {step}: x = {x1}, y = {x2}, |x1 - x2| = {abs(x1 - x2)}, НОД = {d}")

    if d == 1 or d == m:
        print(f"При заданных значениях невозможно найти делители")
    else:
        print(f"Делители: p = {d}, q = {m // d}")
    return d, m // d

while True:
    print("Программа факторизации числа m")
    ch = int(input(f"\nВыберите действие: 1)Факторизация методом квадратичного решета 2) Факторизация р-методом "))
    if ch == 1:
        print("\nМетод квадратичного решета")
        m = int(input("Введите число m для факторизации: "))
        a = int(input("Введите модуль a: "))
        b = int(input("Введите модуль b: "))
        c = int(input("Введите модуль c: "))

        quadratic_sieve(m, a, b, c)

    elif ch == 2:
        print("\nρ-метод")
        m = int(input("Введите число m для факторизации: "))
        x0 = int(input("Введите начальный член последовательности x0: "))
        print("a * x^2 + b")
        a = int(input("Введите коэффицент a при x^2: "))
        b = int(input("Введите коэффицент b: "))
        num = int(input("Введите количество итераций для метода: "))
        rho_method(m, x0, a, b, num)

    else:
        break

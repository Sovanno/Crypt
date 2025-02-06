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

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

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


def baby_step_giant_step(a, b, p, N):
    """
    Метод «шаг младенца – шаг великана» для поиска дискретного логарифма.
    Найти x, такое что a^x ≡ b (mod p).
    """
    k = integer_square_root(p) + 1
    print(f'k = {k}')
    baby_steps = {}
    for i in range(1, N+1):
        baby_step_value = modular_exponentiation(a, i*k, p)
        baby_steps[baby_step_value] = i

    giant_steps = {}
    for j in range(1, N+1):
        giant_step_value = (b * modular_exponentiation(a, j, p)) % p
        giant_steps[giant_step_value] = j

    for val, ind in baby_steps.items():
        print(f'n = {ind}, yn = {val}, zn = {get_key(giant_steps, ind)}')

    x = None
    x_answ = set()
    for val, ind in baby_steps.items():
        if val in giant_steps.keys():
            x = ind * k - giant_steps[val]
            x_answ.add(x)
            print(f'i = {ind} ; j = {giant_steps[val]}')
            print(f"Значение x = {x}")
            #return x
    if x == None:
        print('Решения нет')

    return x_answ
while True:
    print("Введите значения для вычисления дискретного логарифма:")
    a = int(input("Основание a: "))
    b = int(input("Число b: "))
    p = int(input("Модуль p: "))
    N = int(input("Количество итераций N: "))

    x = baby_step_giant_step(a, b, p, N)

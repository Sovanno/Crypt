def caesar_encrypt(text, key):
    encrypted_text = ''
    for char in text:
        if 'а' <= char <= 'я':
            encrypted_text += chr((ord(char) - 1072 + key) % 32 + 1072)
        elif 'А' <= char <= 'Я':
            encrypted_text += chr((ord(char) - 1052 + key) % 32 + 1052)
        elif char == 'ё':
            encrypted_text += chr((ord('е') - 1072 + key) % 32 + 1072)
        elif char == 'Ё':
            encrypted_text += chr((ord('Е') - 1052 + key) % 32 + 1052)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)

def brute_force_decrypt(text):
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write('')

    for key in range(1, 33):
        decrypted_text = caesar_decrypt(text, key)
        print(f'Ключ: {key} - Расшифрованный текст: {decrypted_text}')

    text1 = input("Введите Автора и название произведения: ").lower()
    key = int(input("Введите подошедший ключ (от 1 до 32): "))
    author_encr = caesar_encrypt(text1, key)

    with open("result.txt", "a", encoding="utf-8") as file:
        file.write('\n')
        file.write(f'ШИФР-ТЕКСТ (ШТ): {text}\n')
        file.write(f'РАСШИФРОВАННЫЙ ТЕКСТ (ОТ): {caesar_decrypt(text, key)}\n')
        file.write(f'КЛЮЧ: {key}\n')
        file.write(f'АВТОР И ПРОИЗВЕДЕНИЕ (ОТ): {text1}\n')
        file.write(f'ЗАШИФРОВАННЫЕ ФАМИЛИЯ И НАЗВАНИЕ (ШТ): {author_encr}\n')

action = input("Выберите действие (шифрование-1/расшифрование-2/поиск ключа-3): ").strip()
text = input("Введите текст: ")

if action == '1':
    key = int(input("Введите ключ (от 1 до 32): "))
    encrypted_text = caesar_encrypt(text, key)
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(f"ШИФР-ТЕКСТ (ШТ): {encrypted_text}\n")
        file.write(f"КЛЮЧ: {key}\n")
    print("Текст зашифрован и записан в result.txt")

elif action == '2':
    key = int(input("Введите ключ (от 1 до 32): "))
    decrypted_text = caesar_decrypt(text, key)
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(f"ОРИГИНАЛЬНЫЙ-ТЕКСТ (ОТ): {decrypted_text}\n")
        file.write(f"КЛЮЧ: {key}\n")
    print("Текст зашифрован и записан в result.txt")

elif action == '3':
    brute_force_decrypt(text)
    print("Текст зашифрован и записан в result.txt")

else:
    print("Некорректное действие. Попробуйте снова.")

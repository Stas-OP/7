import numpy as np

def to_lower_case(text):
    return text.lower()

def remove_spaces(text):
    return text.replace(" ", "")

def generate_key_table(key):
    key = remove_spaces(to_lower_case(key))
    key = key.replace('j', 'i')
    key = ''.join(dict.fromkeys(key))  # Remove duplicate letters

    alphabet = "abcdefghiklmnopqrstuvwxyz"  # 'j' is excluded
    key_table = [c for c in key if c in alphabet]

    for char in alphabet:
        if char not in key_table:
            key_table.append(char)

    key_table = np.array(key_table).reshape(5, 5)
    return key_table

def search(key_table, a, b):
    if a == 'j':
        a = 'i'
    if b == 'j':
        b = 'i'

    p1 = p2 = None
    for i in range(5):
        for j in range(5):
            if key_table[i, j] == a:
                p1 = (i, j)
            elif key_table[i, j] == b:
                p2 = (i, j)
    return p1, p2

def prepare_text(text):
    text = remove_spaces(to_lower_case(text))
    text = text.replace('j', 'i')
    
    # Add filler 'x' between double letters
    i = 0
    while i < len(text)-1:
        if text[i] == text[i+1]:
            text = text[:i+1] + 'x' + text[i+1:]
        i += 2
    
    # Make the length even by adding 'z' if needed
    if len(text) % 2 != 0:
        text += 'z'
        
    return text

def encrypt(text: str, key: str) -> str:
    text = prepare_text(text)
    key_table = generate_key_table(key)
    encrypted = []

    for i in range(0, len(text), 2):
        p1, p2 = search(key_table, text[i], text[i+1])

        if p1[0] == p2[0]:  # Same row
            encrypted.append(key_table[p1[0], (p1[1]+1)%5])
            encrypted.append(key_table[p2[0], (p2[1]+1)%5])
        elif p1[1] == p2[1]:  # Same column
            encrypted.append(key_table[(p1[0]+1)%5, p1[1]])
            encrypted.append(key_table[(p2[0]+1)%5, p2[1]])
        else:  # Rectangle rule
            encrypted.append(key_table[p1[0], p2[1]])
            encrypted.append(key_table[p2[0], p1[1]])

    return ''.join(encrypted)

def decrypt(cipher_text: str, key: str) -> str:
    cipher_text = remove_spaces(to_lower_case(cipher_text))
    key_table = generate_key_table(key)
    decrypted = []

    for i in range(0, len(cipher_text), 2):
        p1, p2 = search(key_table, cipher_text[i], cipher_text[i+1])

        if p1[0] == p2[0]:  # Same row
            decrypted.append(key_table[p1[0], (p1[1]-1)%5])
            decrypted.append(key_table[p2[0], (p2[1]-1)%5])
        elif p1[1] == p2[1]:  # Same column
            decrypted.append(key_table[(p1[0]-1)%5, p1[1]])
            decrypted.append(key_table[(p2[0]-1)%5, p2[1]])
        else:  # Rectangle rule
            decrypted.append(key_table[p1[0], p2[1]])
            decrypted.append(key_table[p2[0], p1[1]])

    return ''.join(decrypted) 
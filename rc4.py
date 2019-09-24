import binascii

def array_S_T(key):
    S = []
    T = []
    for indice in range(256):
        S.append(indice)
        T.append(ord(key[indice % len(key)]))
    return(S, T)

def change_position(array, index_i, element_i, index_j, element_j):
    array[index_i] = element_j
    array[index_j] = element_i

    return array

def initial_permutation(array_S, array_T): 
    j = 0
    for i in range(256):
        j = (j + array_S[i] + array_T[i]) % 256
        array_S = change_position(array_S, i, array_S[i], j, array_S[j])
    return array_S

def get_random_element(permutate_array):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + permutate_array[i]) % 256
        permutate_array[i], permutate_array[j] = permutate_array[j], permutate_array[i]
        yield permutate_array[(permutate_array[i] + permutate_array[j]) % 256]

def run_rc4(permutate_array, text):
    cipher_text = []
    random_char = get_random_element(permutate_array)
    for char in text:
        byte = ord(char)
        cipher_byte = byte ^ random_char.__next__()
        cipher_text.append(chr(cipher_byte))
    return binascii.hexlify(''.join(cipher_text).encode())

def decrypt_message(text, key):
    S,T = array_S_T(key)
    S = initial_permutation(S, T)
    text = binascii.unhexlify(text[2:-1]).decode('utf-8')
    array_copy = list(S)
    natural_value = repr(run_rc4(array_copy, text))
    text_de = binascii.unhexlify(natural_value[2:-1])
    return text_de.decode('utf-8')

def encrypt_message(text, key):
    S,T = array_S_T(key)
    S = initial_permutation(S, T)
    array_copy = list(S)
    return repr(run_rc4(array_copy, text))

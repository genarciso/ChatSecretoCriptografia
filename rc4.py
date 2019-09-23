import textwrap
import readline
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

def get_k(permutate_array):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + permutate_array[i]) % 256
        permutate_array[i], permutate_array[j] = permutate_array[j], permutate_array[i]
        yield permutate_array[(permutate_array[i] + permutate_array[j]) % 256]

def run_rc4(permutate_array, text):
    cipher_text = []
    random_char = get_k(permutate_array)
    for char in text:
        byte = ord(char)
        cipher_byte = byte ^ random_char.__next__()
        cipher_text.append(chr(cipher_byte))
    print(''.join(cipher_text).encode())
    return binascii.hexlify(''.join(cipher_text).encode())

def loop_user_query(k):
    """Raises EOFError when the user uses an EOT escape sequence (i.e. ^D)."""
    quotes = "'\""
    text = input('Enter plain or cipher text: ')
    if text[0] == text[-1] and text[0] in quotes:
        # Unescape presumed ciphertext.
        print ('Unescaping ciphertext...')
        text = binascii.unhexlify(text[1:-1]).decode('utf-8')
        k_copy = list(k)
        j = repr(run_rc4(k_copy, text))
        print ('Your RC4 text is:', j)
        text_de = binascii.unhexlify(j[2:-1])
        print (text_de.decode('utf-8'))
    else: 
        k_copy = list(k)
        print ('Your RC4 text is:', repr(run_rc4(k_copy, text)))

def print_prologue():
    title = 'RC4 Utility'
    print ('=' * len(title))
    print (title)
    print ('=' * len(title))
    explanation = """The output values are valid Python strings. They may
contain escape characters of the form \\xhh to avoid confusing your terminal
emulator. Only the first 256 characters of the encryption key are used."""
    for line in textwrap.wrap(explanation, width=79):
        print (line)

def main():
    print_prologue()

    key = input('Enter an encryption key: ')
    S,T = array_S_T(key)
    S = initial_permutation(S, T)

    try:
        loop_user_query(S)
    except EOFError:
        print ('Have a pleasant day!')

if __name__ == "__main__":
    main()
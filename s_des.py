# Shifts
def left_shift(bits):
	return bits[1:] + bits[0]

def left_two_shift(bits):
	return left_shift(left_shift(bits))

# Expand
def expand_eight(bits):
	e8 = [4,1,2,3,2,3,4,1]
	final_permutate = ""

	for i in e8:
		final_permutate += bits[i-1]

	return final_permutate

# Permutate
def permutate(bits, per):
	final_permutate = ""

	for i in per:
		final_permutate += bits[i-1]

	return final_permutate

def permutate_ten(bits):
	p10 = [3,5,2,7,4,10,1,9,8,6]

	return permutate(bits, p10)

def permutate_eight(bits):
	p8 = [6,3,7,4,8,5,10,9]
	
	return permutate(bits, p8)

# Permutate or Expand decision
def p_four(bits):
	p4 = [2,4,3,1]

	return permutate(bits, p4)

def p_ten(bits):
	return permutate_ten(bits)
	
def p_eight(bits):
	if len(bits) < 8:
		return expand_eight(bits)
	else:
		return permutate_eight(bits)

# Keys generating
def generate_keys(bits):
	final_bits = p_ten(bits)

	left = left_shift(final_bits[:5])
	right = left_shift(final_bits[5:])

	k1 = p_eight("{}{}".format(left, right))

	left = left_two_shift(left)
	right = left_two_shift(right)

	k2 = p_eight("{}{}".format(left, right))

	return (k1, k2)

# IP or IP-1
def ip(bits, IP):
	
	final_permutate = ""

	for i in IP:
		final_permutate += bits[i-1]
	
	return final_permutate

# IP or IP-1 inverse

def ip_inverse(bits, IP):
	final = ""

	for i in range(1,9):
		index = IP.index(i)
		final += bits[index]

	return final

# XOR
def xor(left, right):
	final = ""
	for i in range(len(left)):
		if(left[i] != right[i]):
			final += "1"
		else:
			final += "0"

	return final

# S
def S(bits, matriz):
	linha = int(bits[0] + bits[3], 2)
	coluna = int(bits[1] + bits[2], 2)

	final = bin(matriz[linha][coluna])[-2:]
	final = final.replace("b","0")

	return final

def S0(bits):
	matriz = [[1,0,3,2], [3,2,1,0], [0,2,1,3], [3,1,3,2]]

	return S(bits, matriz)

def S1(bits):
	matriz = [[1,1,2,3], [2,0,1,3], [3,0,1,0], [2,1,0,3]]

	return S(bits, matriz)

# Complex function F
def F(bits, key):
	final = p_eight(bits)
	final = xor(final, key)
	
	left_xor = S0(final[:4])
	right_xor = S1(final[4:])

	final = p_four(left_xor + right_xor)

	return final

# Switch
def switch(left, right):
	return (right, left)

# Encrypt
def s_des_encrypt(bits, key):
	## Pré ....
	#key = "1010000010"

	IP = [2,6,3,1,4,8,5,7]
	IP_inverse = [4,1,3,5,7,2,8,6]

	K1, K2 = generate_keys(key)
	
	final_bits = ip(bits, IP)

	left_bits = final_bits[:4]
	right_bits = final_bits[4:]
	
	## Primeira parte
	p_4 = F(right_bits, K1)
	left_bits = xor(left_bits, p_4)
	
	## Segunda parte
	left_bits, right_bits = switch(left_bits, right_bits)
	p_4 = F(right_bits, K2)
	left_bits = xor(left_bits, p_4)

	final_bits = ip("{}{}".format(left_bits, right_bits), IP_inverse)

	return final_bits

# Decrypt
def s_des_decrypt(bits, key):
	## Pré
	#key = "1010000010"

	IP = [2,6,3,1,4,8,5,7]
	IP_inverse = [4,1,3,5,7,2,8,6]

	K1, K2 = generate_keys(key)

	final_bits = ip_inverse(bits, IP_inverse)

	left_bits = final_bits[:4]
	right_bits = final_bits[4:]

	## Primeira parte
	left_bits = xor(left_bits,F(right_bits, K2))

	## Segunda parte
	left_bits, right_bits = switch(left_bits, right_bits)

	left_bits = xor(left_bits, F(right_bits, K1))
	
	final_bits = ip_inverse("{}{}".format(left_bits,right_bits), IP)

	return final_bits

def bits_8(bits):
	while(len(bits) < 8):
 		bits = '0'+bits
	return bits

def encrypt_message(message, key):
	final_text = ""
	for char in message:
		char_8_bits = bits_8(bin(ord(char))[2:])
		char_cripto = s_des_encrypt(char_8_bits, key)
		final_text += chr(int(char_cripto, 2))

	return final_text

def decrypt_message(message, key):
	texto_decifrado = ""
	for letra in message:
		letra_8_bits = bits_8(bin(ord(letra))[2:])
		letra_decrypt = s_des_decrypt(letra_8_bits, key)
		texto_decifrado += chr(int(letra_decrypt, 2))

	return texto_decifrado

def main():
	key = '1010000010'
	#Encriptar texto
	texto = "Tentativa de esconder uma mensagem!"
	
	texto_encriptado = encrypt_message(texto, key)
	print(texto_encriptado)

	texto_decifrado = decrypt_message(texto_encriptado, key)

	print(texto_decifrado)

def main2():
	for i in range(1,9):
		print(i)

if __name__ == '__main__':
	main()


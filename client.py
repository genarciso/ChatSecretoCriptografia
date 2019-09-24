# Python program to implement client side of chat room. 
import socket 
import select 
import sys 

# import s-des, diffie_hellman
import s_des as sd
import rc4 as rc4
import diffie_hellman as df

def transform_binary(key):
    return sd.bits_10(bin(key)[2:])

def decode_encrypt(message, which):    
    decrypted_message = ''
    
    print('----------------------------- Decifrando -----------------------------')
    
    if("s-des" in which): # s-des
        print('Entrou no s-des')
        decrypted_message = sd.decrypt_message(message, transform_binary(key))
    elif("rc4" in which):
        print('Entrou no rc4')
        decrypted_message = rc4.decrypt_message(message, str(key))
    else: # Mensagem em claro
        print('Entrou no else')
        decrypted_message = message
    
    
    print('* Mensagem decifrada: {}'.format(decrypted_message))
    print('-----------------------------------------------------------------------')
    
    return decrypted_message


def encode_decrypt(message, which):
    encrypted_message = ''
    
    print('----------------------------- Encriptando -----------------------------')
    print(which)
    
    if("s-des" in which):
        print('Entrou no s-des')
        encrypted_message = sd.encrypt_message(message, transform_binary(key))
    elif("rc4" in which):
        print('Entrou no rc4')
        encrypted_message = rc4.encrypt_message(message, str(key))
    else: # Mensagem em claro
        print('Entrou no else')
        encrypted_message = message
    
    print('* Mensagem encriptada: {}'.format(encrypted_message))
    
    print('-----------------------------------------------------------------------')
    return encrypted_message


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print("Correct usage: script, IP address, port number")
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
message = ""

which_alg = "none"
next_alg = "none"
my_private_key = 0
my_public_key = 0
dest_public_key = 0
key = 0
expecting_public_key = False

while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 

    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048)
            # ToDo: decifrar a mensagem antes de imprimir
            message = decode_encrypt(message.decode(), which_alg)
            if not(expecting_public_key):
                if( ("\crypt" in str(message)) ):
                    # Mudança de algoritmo
                    next_alg = message.split(' ')[1].lower()
                    # Gerando as chaves privada e pública
                    my_private_key = df.generate_x()
                    my_public_key = df.generate_y(int(my_private_key))
                    # Avisa que está esperando a chave pública do outro
                    expecting_public_key = True
                    # Envia a minha chave pública
                    server.send(encode_decrypt(str(my_public_key),which_alg).encode())
                else:
                    print("+ Recebeu: {}".format(message.replace('\n', '')))
            else: # Pegando a chave pública do outro
                dest_public_key = message
                key = df.diffie_hellman(int(my_private_key), int(dest_public_key))
                expecting_public_key = False
                which_alg = next_alg
                next_alg = "none"
                print(which_alg)
        else: 
            # Pegando a mensagem do terminal
            message = sys.stdin.readline()
            server.send( encode_decrypt(message, which_alg).encode() )
            if( ("\crypt" in str(message)) ):
                
                # Mudança de algoritmo
                next_alg = message.split(' ')[1].lower()
                # Gerando as chaves privada e pública
                my_private_key = df.generate_x()
                my_public_key = df.generate_y(int(my_private_key))
                # Avisa que está esperando a chave pública do outro
                expecting_public_key = True
                # Envia a minha chave pública
                server.send(encode_decrypt(str(my_public_key),which_alg).encode())
            
            # End if
        # End if
    # End for
# End while
server.close() 
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
    
    if("s-des" in which): # s-des
        decrypted_message = sd.decrypt_message(message, transform_binary(key))
    elif("rc4" in which):
        decrypted_message = rc4.decrypt_message(message, str(key))
    else: # Mensagem em claro
        decrypted_message = message
    
    return decrypted_message


def encode_decrypt(message, which):
    encrypted_message = ''

    if("s-des" in which):
        encrypted_message = sd.encrypt_message(message, transform_binary(key))
    elif("rc4" in which):
        encrypted_message = rc4.encrypt_message(message, str(key))
    else: # Mensagem em claro
        encrypted_message = message
    
    return encrypted_message


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print("Uso correto: script, endereço IP, número da porta")
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


while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 

    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        expecting_public_key = False
        if socks == server: 
            message = socks.recv(2048)
            
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
                print("*** OBS: A partir de agora as mensagens estão utilizando a cifragem {}".format(which_alg))
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
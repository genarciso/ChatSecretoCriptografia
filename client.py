# Python program to implement client side of chat room. 
import socket 
import select 
import sys 

# import s-des, diffie_hellman
import s_des as sd
import diffie_hellman as df

def decode_encrypt(message, which):    
    if(which == "s-des"): # s-des
        return sd.decrypt_message(message, my_private_key)
    elif(which == "rc4"):
        return rc4.decrypt_message(message, my_private_key)
    else: # Mensagem em claro
        return message


def encode_decrypt(message, which):
    if(which == "s-des"):
        return sd.encrypt_message(message, dest_public_key)
    elif(which == "rc4"):
        return rc4.encrypt_message(message, dest_public_key)
    else: # Mensagem em claro
        return message


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
my_private_key = ""
my_public_key = ""
dest_public_key = ""
key = ""
expecting_public_key = False

while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 
    
    """ There are two possible input situations. Either the 
        user wants to give  manual input to send to other people, 
        or the server is sending a message  to be printed on the 
        screen. Select returns from sockets_list, the stream that 
        is reader for input. So for example, if the server wants 
        to send a message, then the if condition will hold true 
        below.If the user wants to send a message, the else 
        condition will evaluate as true
    """
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
                    my_public_key = df.generate_y(my_private_key)
                    # Avisa que está esperando a chave pública do outro
                    expecting_public_key = True
                    # Envia a minha chave pública
                    server.send(encode_decrypt(str(my_public_key),which_alg).encode())
                else:
                    print("- Recebeu: {}".format(message))
            else: # Pegando a chave pública do outro
                dest_public_key = message
                key = df.diffie_hellman(my_private_key, dest_public_key)
                expecting_public_key = False
                which_alg = next_alg
                next_alg = "none"
        else: 
            # Pegando a mensagem do terminal
            message = sys.stdin.readline()
            #print(type(message))
            # Encriptando a mensagem e enviando
            sys.stdout.write("+ Enviou: {}".format(message)) 
            sys.stdout.flush() 
            server.send( encode_decrypt(message, which_alg).encode() )
server.close() 
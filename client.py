# Python program to implement client side of chat room. 
import socket 
import select 
import sys 

# import s-des, diffie_hellman
import s_des as sd
import diffie_hellman as df

def decode_encrypt(message, which):
    if(which == "none"): # None
        return message
    elif(which == "s-des"): # s-des
        return sd.decrypt_message(message, my_private_key)
    elif(which == "rc4"):
        return rc4.decrypt_message(message, my_private_key)


def encode_decrypt(message, which):
    if(which == "none"):
        return message
    elif(which == "s-des"):
        return sd.encrypt_message(message, dest_public_key)
    elif(which == "rc4"):
        return rc4.encrypt_message(message, dest_public_key)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print "Correct usage: script, IP address, port number"
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
message = ""

which_alg = "none"
my_private_key = ""
my_public_key = ""
dest_public_key = ""
key = ""

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
            print decode_decrypt(message)
        else: 
            message = sys.stdin.readline()
            #ToDo: encriptar a mensagem antes de enviar
            server.send(message) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message) 
            sys.stdout.flush() 
server.close() 
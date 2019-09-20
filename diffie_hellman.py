import random

def generate_q():
    return 353

def generate_alpha():
    return 3

def generate_x():
    x = random.randint(0,generate_q()-1)
    return x

def generate_y(x):
    y = (generate_alpha()**x)%generate_q()
    return y

def diffie_hellman(x, y): # return k
    k = (y**x) % generate_q()
    return k

import random

def generate_q():
    return 353

def generate_alpha():
    return 3

def generate_x(q):
    x = random.randint(0,q-1)
    return x

def generate_y(q, alpha, x):
    y = (alpha**x)%q
    return y

def diffie_hellman(q, x, y): # return k
    k = (y**x) % q
    return k

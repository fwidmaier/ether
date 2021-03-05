import random

def gen_pass(length):
    passw = str()
    for c in range(0,length):
        ll = random.randint(40,126)
        passw += chr(ll)
    return passw

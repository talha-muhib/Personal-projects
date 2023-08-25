import random
import math
import sys

def is_prime(num):
    if(num < 2):
        return False
    for i in range(2, round(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def gen_prime(min_val, max_val):
    num = random.randint(min_val, max_val)
    while(not is_prime(num)):
        num = random.randint(min_val, max_val)
    return num

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Multiplicative inverse doesn't exist")

def main():
    if len(sys.argv) < 4:
        raise Exception("No message passed in")

    #Change these ranges as you wish and see what happens
    p, q = gen_prime(1000, 9000), gen_prime(1000, 9000)
    while q == p:
        q = gen_prime(1000, 9000)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randint(3, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n - 1)
    d = mod_inverse(e, phi_n)

    print(f"Public key: {e}")
    #print(f"Private key: {d}") #If you wish to see the private key then uncomment this line
    print(f"N = {n}")
    print(f"ϕ(N) = {phi_n}")

    #Encode the message as ASCII codes (the ord function converts to ASCII)
    message = " ".join(s for s in sys.argv[1:])
    encoded = [ord(c) for c in message]
    ciphertext = [pow(c, e, n) for c in encoded]
    print(f"Ciphertext: {ciphertext}")

    encoded = [pow(c, d, n) for c in ciphertext]
    message = "".join(chr(c) for c in encoded) #chr converts from ASCII back to readable characters
    print(f"After decrypting: {message}")

main()
import rsa
import sys

#Generate public and secret keys, each with 1024 bytes
"""
pk, sk = rsa.newkeys(1024)
"""

#Open 2 files and save our 2 keys into those files (PEM = Privacy Enhanced Mail)
"""
with open("public_key.pem", "wb") as f:
    f.write(pk.save_pkcs1("PEM"))
with open("private_key.pem", "wb") as f:
    f.write(sk.save_pkcs1("PEM"))
"""

"""
Since my keys are saved to my files I can comment out the code above.
If you wish to generate random keys I'll let you figure that out.
Now I can just read from my PEM files and store the values in variables.
Ideally the private key should be kept secret, but for this example I'm showing you.
"""
with open("public_key.pem", "rb") as f:
    pk = rsa.PublicKey.load_pkcs1(f.read())
with open("private_key.pem", "rb") as f:
    sk = rsa.PrivateKey.load_pkcs1(f.read())

#Main function
def main():
    if len(sys.argv) < 2:
        raise Exception("No valid message given")
    
    #Generate our message from command line arguments
    message = " ".join(s for s in sys.argv[1:])

    #Encrypt the message
    encrypt = rsa.encrypt(message.encode(), pk)
    print(f"Encrypting:\n{encrypt}\n")

    #Decrypt the message
    decrypt = rsa.decrypt(encrypt, sk)
    print(f"Decrypting:\n{decrypt}\n")

    #We can also do signatures
    signature = rsa.sign(message.encode(), sk, "SHA-256") #Sign with the SHA-256 algorithm
    print(f"Signature:\n{signature}\n")

    #Verify the signature with the public key
    verify = rsa.verify(message.encode(), signature, pk)
    print(f"Verify:\n{verify}")

    #Play with the message/key contents and see how verification can fail

#Calling main
main()
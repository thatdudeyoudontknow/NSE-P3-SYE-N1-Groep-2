from base64 import b64decode
from Crypto.Cipher import AES

def ECB_decrypt(ciphertext, key):

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    print(plaintext)
    return plaintext


# Laat deze asserts onaangetast & onderaan je code!
ciphertext = b64decode('86ueC+xlCMwpjrosuZ+pKCPWXgOeNJqL0VI3qB59SSY=')
key = b'SECRETSAREHIDDEN'
assert ECB_decrypt(ciphertext, key)[:28] == \
    b64decode('SGFzdCBkdSBldHdhcyBaZWl0IGZ1ciBtaWNoPw==')

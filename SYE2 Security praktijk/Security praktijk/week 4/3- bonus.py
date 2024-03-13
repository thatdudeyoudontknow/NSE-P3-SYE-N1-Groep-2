# from base64 import b64decode
# from Crypto.Cipher import AES

# def ECB_decrypt_from_file(filename, key, output_filename):
#     """
#     Accepts a filename and a key, reads the ciphertext from the file,
#     decrypts it, and writes the resulting plaintext to another file.

#     Parameters
#     ----------
#     filename : str
#         name of the file to read the ciphertext from
#     key : bytes
#         key to be used in decryption
#     output_filename : str
#         name of the file to write the plaintext to

#     Returns
#     -------
#     None
#     """

#     # Read the ciphertext from the file
#     with open(filename, 'rb') as f:
#         ciphertext = f.read()

#     # Decrypt the ciphertext
#     cipher = AES.new(key, AES.MODE_ECB)
#     plaintext = cipher.decrypt(b64decode(ciphertext))

#     # Write the plaintext to another file
#     with open(output_filename, 'w') as f:
#         f.write(plaintext.decode('utf-8'))

# # Use the function
# ECB_decrypt_from_file('file3.txt', b'SECRETSAREHIDDEN', 'output.txt')

from Crypto.Cipher import AES
from base64 import b64encode

def ECB_encrypt(plaintext, key):
    """Accepts a plaintext in byte-form,
    as well as a 16-byte key, and returns 
    the corresponding ciphertext.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be encrypted
    key : bytes
        key to be used in encryption

    Returns
    -------
    bytes
        encrypted ciphertext
    """
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

# Voorbeeld gebruik van de ECB_encrypt functie:
plaintext = b"Hello, this is a secret message!"  # Voorbeeld plaintext
key = b'SECRETSAREHIDDEN'  # Dezelfde sleutel als in de decryptiefunctie

# Encrypteer de plaintext
ciphertext = ECB_encrypt(plaintext, key)

# Print de ciphertext in base64 gecodeerd formaat
print(b64encode(ciphertext))

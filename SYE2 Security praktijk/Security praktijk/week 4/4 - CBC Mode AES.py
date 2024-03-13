from base64 import b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

from pyfiglet import Figlet
from colorama import Fore, init

def print_big_and_green(text):
    init(autoreset=True)  # Initialize colorama
    f = Figlet(font='slant')  # Choose a font
    print(Fore.GREEN + f.renderText(text))  # Print the text in green

def fixed_length_xor(block, xor_with):
    # XOR each byte of the block with the corresponding byte of xor_with
    return bytes([a ^ b for a, b in zip(block, xor_with)])

def ECB_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)

def CBC_decrypt(ciphertext, key, IV):
    # split the ciphertext into blocks
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    # create a list to store the plaintext blocks
    plaintext_blocks = []
    # loop through the blocks
    for i in range(len(blocks)):
        # decrypt the block
        decrypted = ECB_decrypt(blocks[i], key)
        # if it is the first block
        if i == 0:
            # xor the decrypted block with the IV
            plaintext_blocks.append(fixed_length_xor(decrypted, IV))
        else:
            # xor the decrypted block with the previous ciphertext block
            plaintext_blocks.append(fixed_length_xor(decrypted, blocks[i-1]))
    # join the blocks together
    plaintext = b''.join(plaintext_blocks)
    return plaintext





# Laat dit blok code onaangetast & onderaan je code!
a_ciphertext = b64decode('e8Fa/QnddxdVd4dsL7pHbnuZvRa4OwkGXKUvLPoc8ew=')
a_key = b'SECRETSAREHIDDEN'
a_IV = b'WE KNOW THE GAME'

def clear_screen():
    print("\033c", end="")

def main():
    clear_screen()
    plaintext = CBC_decrypt(a_ciphertext, a_key, a_IV)
    print (plaintext)
    #plaintext = unpad(plaintext, AES.block_size)
    print_big_and_green(plaintext.decode()) 
    # assert plaintext[:18] == b64decode('eW91IGtub3cgdGhlIHJ1bGVz')
    # print_big_and_green(plaintext.decode()) 

if __name__ == "__main__":
     main()
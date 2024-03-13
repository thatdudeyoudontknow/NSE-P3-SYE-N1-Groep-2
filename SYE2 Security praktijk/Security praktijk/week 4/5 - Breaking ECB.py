from base64 import b64decode
#from Crypto.Cipher import AES
from Cryptodome.Cipher import AES
from secrets import token_bytes
from Cryptodome.Util.Padding import pad

def pkcs7_pad(plaintext, blocksize):
    """Appends the plaintext with n bytes,
    making it an even multiple of blocksize.
    Byte used for appending is byteform of n.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be appended
    blocksize : int
        blocksize to conform to

    Returns
    -------
    plaintext : bytes
        plaintext appended with n bytes
    """

    # Determine how many bytes to append
    n = blocksize - len(plaintext)%blocksize
    # Append n*(byteform of n) to plaintext
    # n is in a list as bytes() expects iterable
    plaintext += (n*bytes([n]))
    return plaintext

def ECB_oracle(plaintext, key):
    """Appends a top-secret identifier to the plaintext
    and encrypts it under AES-ECB using the provided key.

    Parameters
    ----------
    plaintext : bytes
        plaintext to be encrypted
    key : bytes
        16-byte key to be used in decryption

    Returns
    -------
    ciphertext : bytes
        encrypted plaintext
    """
    plaintext += b64decode('U2F5IG5hIG5hIG5hCk9uIGEgZGFyayBkZXNlcnRlZCB3YXksIHNheSBuYSBuYSBuYQpUaGVyZSdzIGEgbGlnaHQgZm9yIHlvdSB0aGF0IHdhaXRzLCBpdCdzIG5hIG5hIG5hClNheSBuYSBuYSBuYSwgc2F5IG5hIG5hIG5hCllvdSdyZSBub3QgYWxvbmUsIHNvIHN0YW5kIHVwLCBuYSBuYSBuYQpCZSBhIGhlcm8sIGJlIHRoZSByYWluYm93LCBhbmQgc2luZyBuYSBuYSBuYQpTYXkgbmEgbmEgbmE=')
    plaintext = pkcs7_pad(plaintext, len(key))
    cipher = cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

# Genereer een willekeurige key

key = token_bytes(16)

#####################################
###  schrijf hieronder jouw code  ###
### verander code hierboven niet! ###
#####################################

def find_block_length():
    """Finds the block length used by the ECB oracle.

    Returns
    -------
    blocksize : integer
        blocksize used by ECB oracle
    """
# make a for loop and add a byte to the plaintext each time until the length of the ciphertext changes
    plaintext = b''
    ciphertext = ECB_oracle(plaintext, key)
    blocksize = 0
    for i in range(1, 100):
        plaintext += b'A'
        new_ciphertext = ECB_oracle(plaintext, key)
        #print (plaintext, len(new_ciphertext))
        if len(new_ciphertext) != len(ciphertext):
            blocksize = len(new_ciphertext) - len(ciphertext)
            break
        #print (new_ciphertext)    
        #print (i)
    return blocksize

# def get_target_ciphertext(blocksize):
#     padding = b'A' * (blocksize - 1)
#     target_ciphertext = ECB_oracle(padding, key)
#     return target_ciphertext

def get_target_ciphertext(blocksize):
    padding = b'A' * (blocksize - 1)  # Create a padding of blocksize - 1 bytes
    target_ciphertext = ECB_oracle(padding, key)
    return target_ciphertext


def clear_screen():
    print("\033c", end="")

def main():
    clear_screen()
    blocksize = find_block_length()
    target_ciphertext = get_target_ciphertext(blocksize)

    # Print column numbers
    print('   |', ' | '.join(f'{i:02}' for i in range(1, 17)), '|')

    # Print the ciphertext in chunks of 16 bytes
    for i in range(0, len(target_ciphertext), 16):
        chunk = target_ciphertext[i:i+16]
        hex_chunk = ' | '.join(f'{byte:02x}' for byte in chunk)
        # Print row number and chunk
        print(f'{i//16 + 1:02} |', hex_chunk, '|')

if __name__ == "__main__":
    main()
    
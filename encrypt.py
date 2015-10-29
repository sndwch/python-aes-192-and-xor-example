from Crypto.Cipher import AES
import base64
import os
from itertools import cycle, izip


def encrypt(text, key):
    iv = os.urandom(16)
    b = base64.encodestring(text)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    ciphertext = iv + cipher.encrypt(b)

    cyphered = ''.join(chr(ord(c) ^ ord(k)) for c, k in izip(ciphertext, cycle(key)))

    return cyphered


def decrypt(text, key):
    message = ''.join(chr(ord(c) ^ ord(k)) for c, k in izip(text, cycle(key)))

    iv = message[:AES.block_size]
    message = message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CFB, str(iv))
    decrypted = cipher.decrypt(message)

    return base64.decodestring(decrypted)


if __name__ == "__main__":
    key = "1234567890abcdef" #16 bytes
    text = "your_awesome_secret_text_here"

    encrypted = encrypt(text, key)
    decrypted = decrypt(encrypted, key)

    if text == decrypted:
        print "Round trip encryption worked."
    else:
        print "Something happened."

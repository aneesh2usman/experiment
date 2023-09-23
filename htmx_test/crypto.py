from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad
import base64
from django.conf import settings
def generate_key_and_salt(password, salt_length=16):
    salt = get_random_bytes(salt_length)
    key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)
    return key, salt

def encrypt(plaintext, password=settings.ENCRYPTED_PASSWORD,no_encrypt=True):
    if no_encrypt:
        return plaintext
    key, salt = generate_key_and_salt(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(salt + cipher.iv + ciphertext).decode()

def decrypt(ciphertext, password=settings.ENCRYPTED_PASSWORD,no_encrypt=True):
    if no_encrypt:
        return ciphertext
    ciphertext = base64.b64decode(ciphertext.encode())
    salt = ciphertext[:16]
    iv = ciphertext[16:32]
    ciphertext = ciphertext[32:]
    key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode()
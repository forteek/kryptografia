from block_encryption import *
from rich import print

if __name__ == '__main__':
    print('Enter name of file to encrypt: ')
    filename = input()
    with open(filename, 'r') as f:
        message = f.read()
    print('Enter name of file to save encrypted message to: ')
    filename = input()
    print('Enter key: ')
    key = input()
    encrypter = ECB(key)
    with open(filename, 'w') as f:
        f.write(encrypter.encrypt(message).hex())
    print('Enter name of file to decrypt: ')
    filename = input()
    with open(filename, 'r') as f:
        message = f.read()
    print('Enter name of file to save decrypted message to: ')
    filename = input()
    print('Enter key: ')
    key = input()
    with open(filename, 'w') as f:
        f.write(encrypter.decrypt(bytes.fromhex(message)).decode())
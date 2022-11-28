from block_encryption import *
from rich import print

if __name__ == '__main__':
    print('Enter name of file to encrypt: ')
    filename = input()
    with open(filename, 'r') as f:
        message = f.read()
    print('Enter name of file to save encrypted message to: ')
    filename = input()
    with open(filename, 'w') as f:

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class ECB:
    def __init__(self, key, block_size=16):
        self.key = key.encode('utf-8')
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.block_size = block_size

    def encrypt(self, plaintext):
        return self.cipher.encrypt(pad(plaintext.encode('utf-8'), self.block_size))

    def decrypt(self, ciphertext):
        return unpad(self.cipher.decrypt(ciphertext), self.block_size)


class CBC:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, plaintext):
        ciphertext = b''
        prev = self.iv
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i+16]
            block = bytes([block[j] ^ prev[j] for j in range(16)])
            block = self.cipher.encrypt(block)
            ciphertext += block
            prev = block
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        prev = self.iv
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            block = self.cipher.decrypt(block)
            block = bytes([block[j] ^ prev[j] for j in range(16)])
            plaintext += block
            prev = ciphertext[i:i+16]
        return plaintext


class CFB:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, plaintext):
        ciphertext = b''
        prev = self.iv
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i+16]
            prev = self.cipher.encrypt(prev)
            block = bytes([block[j] ^ prev[j] for j in range(16)])
            ciphertext += block
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        prev = self.iv
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            prev = self.cipher.encrypt(prev)
            block = bytes([block[j] ^ prev[j] for j in range(16)])
            plaintext += block
        return plaintext
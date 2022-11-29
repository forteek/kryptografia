from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time

mode_names = {
    1: "ECB",
    2: "CBC",
    3: "CFB",
    5: "OFB",
    6: "CTR",
    7: "OPENPGP",
    8: "CCM",
    9: "EAX",
    10: "SIV",
    11: "GCM",
    12: "OCB"
}

if __name__ == '__main__':
    key = b'1234567890123456'
    iv = b'1234567890123456'
    for filename in ['maly', 'sredni', 'duzy']:
        with open(filename, 'r') as f:
            message = f.read()

        non_iv_modes = [AES.MODE_ECB, AES.MODE_CTR]
        for mode in non_iv_modes:
            start_time = time.time()
            cipher = AES.new(key, mode)
            ciphertext = cipher.encrypt(message.encode('utf-8'))
            print(f'Encryption time for {filename} file in {mode_names[mode]} mode: {time.time() - start_time}')
            start_time = time.time()
            cipher = AES.new(key, mode)
            plaintext = cipher.decrypt(ciphertext)
            print(f'Decryption time for {filename} file in {mode_names[mode]} mode: {time.time() - start_time}')
        iv_modes = [AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB, AES.MODE_OPENPGP,
                    AES.MODE_EAX, AES.MODE_GCM]
        for mode in iv_modes:
            start_time = time.time()
            cipher = AES.new(key, mode, iv)
            ciphertext = cipher.encrypt(message.encode('utf-8'))
            print(f'Encryption time for {filename} file in {mode_names[mode]} mode: {time.time() - start_time}')
            start_time = time.time()
            cipher = AES.new(key, mode, iv)
            plaintext = cipher.decrypt(ciphertext)
            print(f'Decryption time for {filename} file in {mode_names[mode]} mode: {time.time() - start_time}')
        nonce_modes = [AES.MODE_CCM, AES.MODE_OCB]
        for mode in nonce_modes:
            start_time = time.time()
            cipher = AES.new(key, mode, nonce=b'1234567890')
            ciphertext = cipher.encrypt(message.encode('utf-8'))
            print(f'Encryption time for {filename} file in {mode} mode: {time.time() - start_time}')
            start_time = time.time()
            cipher = AES.new(key, mode, nonce=b'1234567890')
            plaintext = cipher.decrypt(ciphertext)
            print(f'Decryption time for {filename} file in {mode} mode: {time.time() - start_time}')

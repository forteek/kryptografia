class BitsEncrypter:
    @staticmethod
    def encrypt(key, message) -> str:
        if len(message) > len(key):
            raise ValueError('Key is too short.')

        return ''.join([str(int(key_char) ^ int(message_char)) for key_char, message_char in zip(key, message)])

    @staticmethod
    def decrypt(key, message) -> str:
        return BitsEncrypter.encrypt(key, message)

class TextEncrypter:
    @staticmethod
    def encrypt(key, message) -> str:
        bits = ''.join([bin(ord(char))[2:].zfill(8) for char in message])
        result_bits = BitsEncrypter.encrypt(key, bits)

        return ''.join([chr(int(result_bits[i:i+8], 2)) for i in range(0, len(result_bits), 8)])

    @staticmethod
    def decrypt(key, message) -> str:
        return TextEncrypter.encrypt(key, message)


class AsciiEncrypter:
    @staticmethod
    def encrypt(key, message) -> str:
        return ''.join([chr(ord(key_char) ^ ord(message_char)) for key_char, message_char in zip(key, message)])

    @staticmethod
    def decrypt(key, message) -> str:
        return AsciiEncrypter.encrypt(key, message)


class ElectronicCodeBookEncrypter(BitsEncrypter):
    @staticmethod
    def encrypt(key, message) -> str:
        block_size = len(key)
        blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]
        result_blocks = [super().encrypt(key, block) for block in blocks]

        return ''.join(result_blocks)

    @staticmethod
    def decrypt(key, message) -> str:
        block_size = len(key)
        blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]
        result_blocks = [super().decrypt(key, block) for block in blocks]

        return ''.join(result_blocks)


class CipherBlockChainingEncrypter(BitsEncrypter):
    @staticmethod
    def encrypt(key, message) -> str:
        block_size = len(key)
        blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]

        result = ''
        previous_block = key
        for block in blocks:
            result += super().encrypt(previous_block, block)
            previous_block = result[-block_size:]

        return result

    @staticmethod
    def decrypt(key, message) -> str:
        block_size = len(key)
        blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]

        result = ''
        previous_block = key
        for block in blocks:
            result += super().decrypt(previous_block, block)
            previous_block = block

        return result


class OutputFeedbackEncrypter(BitsEncrypter):
    @staticmethod
    def encrypt(key, message) -> str:
        block_size = len(key)
        blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]

        result = ''
        previous_block = key
        for block in blocks:
            encrypted_block = super().encrypt(previous_block, previous_block)
            result += super().encrypt(encrypted_block, block)
            previous_block = encrypted_block

        return result

    @staticmethod
    def decrypt(key, message) -> str:
        block_size = len(key)
        blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]

        result = ''
        previous_block = key
        for block in blocks:
            encrypted_block = super().encrypt(previous_block, previous_block)
            result += super().encrypt(encrypted_block, block)
            previous_block = encrypted_block

        return result



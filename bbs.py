from typing import Generator
from math import gcd
import re
from env import DEBUG


def are_coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1


class BbsGenerator:
    @staticmethod
    def generate(modulus: int, length: int, seed: int) -> Generator[int, None, None]:
        if not are_coprime(modulus, seed):
            raise AttributeError("Seed and modulus must be coprime.")

        number = seed
        for _ in range(length):
            number = (number ** 2) % modulus
            yield number % 2

class FipsTester:
    @staticmethod
    def single_bits_test(sequence: str) -> bool:
        if DEBUG:
            print(str(len(['1' for x in sequence if x == '1'])) + ' jedynek')

        return 9725 < len(['1' for x in sequence if x == '1']) < 10275

    @staticmethod
    def series_test(sequence: str) -> bool:
        return FipsTester._char_series_test(sequence, '0') and FipsTester._char_series_test(sequence, '1')

    @staticmethod
    def _char_series_test(sequence: str, char: str) -> bool:
        subsequences = re.findall(r"(" + char + r"+)", sequence)
        subsequences_counts = {x: 0 for x in range(1, 7)}

        for subsequence in subsequences:
            index = len(subsequence)
            index = index if index < 7 else 6

            subsequences_counts[index] += 1

        if DEBUG:
            print(f'Wystąpienia {char}: {subsequences_counts}')

        return 2315 < subsequences_counts[1] < 2685 and \
               1114 < subsequences_counts[2] < 1386 and \
               527 < subsequences_counts[3] < 723 and \
               240 < subsequences_counts[4] < 384 and \
               103 < subsequences_counts[5] < 209 and \
               103 < subsequences_counts[6] < 209

    @staticmethod
    def long_series_test(sequence: str) -> bool:
        long_sequences = re.findall(r"(1{26,}|0{26,})", sequence)

        if DEBUG:
            print(str(len(long_sequences)) + ' długich ciągów')

        return len(long_sequences) == 0

    @staticmethod
    def poker_test(sequence: str) -> bool:
        subsequences = [sequence[i:i+4] for i in range(0, len(sequence), 4)]
        frequencies = {x: 0 for x in range(16)}
        for subsequence in subsequences:
            frequencies[int(subsequence, 2)] += 1

        sum = 0
        for frequency in frequencies.values():
            sum += frequency ** 2

        result = 16/5000 * sum - 5000

        if DEBUG:
            print('Wynik testu pokerowego to ' + str(result))

        return 2.16 < result < 46.17

from rich import print as rprint
import sys
from bbs import FipsTester, BbsGenerator
from encryption import BitsEncrypter, TextEncrypter, AsciiEncrypter


def test_sequence(seq: str) -> None:
    rprint('[bold blue]Test suite[/bold blue]')
    rprint('[white dim]Single bits test'.ljust(100, '.') + '[/white dim]', FipsTester.single_bits_test(seq))
    rprint('[white dim]Series test'.ljust(100, '.') + '[/white dim]', FipsTester.series_test(seq))
    rprint('[white dim]Long series test'.ljust(100, '.') + '[/white dim]', FipsTester.long_series_test(seq))
    rprint('[white dim]Poker test'.ljust(100, '.') + '[/white dim]', FipsTester.poker_test(seq))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            seq = f.read().strip()
            if len(seq) > 20000:
                rprint('[bold yellow]Warning:[/bold yellow] Sequence is too long. It will be truncated to 20000 bits.\n')
                seq = seq[:20000]
            elif len(seq) < 20000:
                rprint('[bold red]Error:[/bold red] Sequence is too short. It needs to be 20000 bits long.')
                exit(1)
    else:
        seq = ''.join([str(x) for x in BbsGenerator.generate(1200000003730000000273, 20000, 5667298754)])

    rprint(f"[bold blue]Sequence:[/bold blue]")
    print(seq, '\n')

    rprint('Press [bold red]Enter[/bold red] to start tests.')
    input()

    test_sequence(seq)

    rprint('\nPress [bold red]Enter[/bold red] to start encryption.')
    input()

    message = input('Enter message to encrypt: ')
    chars = set(message)
    if chars == {'0', '1'} or chars == {'0'} or chars == {'1'}:
        encrypter = BitsEncrypter
    else:
        encrypter = TextEncrypter

    key = BbsGenerator.generate(1200000003730000000273, 20000, 5667298754)
    key = ''.join([str(x) for x in key])

    rprint(f'\nMessage prior to encryption: [bold blue]{message}[/bold blue]')
    encrypted = encrypter.encrypt(key, message)
    rprint(f'Message after encryption:    [bold blue]{encrypted}[/bold blue]')
    decrypted = encrypter.decrypt(key, encrypted)
    rprint(f'Message after decryption:    [bold blue]{decrypted}[/bold blue]')
    exit(0)
    rprint('\nPress [bold red]Enter[/bold red] to start tests on multiple instances.')
    input()

    bbs_seeds = [
        (1200000003730000000273, 5667298754),
        (1200000003730000000273, 2921799738),
        (1200000003730000000273, 5861968144),
    ]

    for modulus, seed in bbs_seeds:
        seq = ''.join([str(x) for x in BbsGenerator.generate(modulus, 20000, seed)])

        rprint(f"[bold blue]Sequence:[/bold blue]")
        print(seq, '\n')

        test_sequence(seq)

        rprint('\nPress [bold red]Enter[/bold red] to continue.')
        input()

    rprint('\nPress [bold red]Enter[/bold red] to start tests on a random encrypted value.')
    input()

    modulus, seed = bbs_seeds[0]
    key = ''.join([str(x) for x in BbsGenerator.generate(modulus, 20000, seed)])
    modulus, seed = bbs_seeds[1]
    message = ''.join([str(x) for x in BbsGenerator.generate(modulus, 20000, seed)])

    encrypted = BitsEncrypter.encrypt(key, message)

    rprint(f"[bold blue]Sequence:[/bold blue]")
    print(encrypted, '\n')

    test_sequence(encrypted)

    rprint('\nPress [bold red]Enter[/bold red] to start generating a 1 million bits long sequence.')
    input()

    modulus, seed = bbs_seeds[2]
    seq = ''.join([str(x) for x in BbsGenerator.generate(modulus, 1_000_000, seed)])

    with open('mpi/result', 'w') as file:
        file.write(seq)

    rprint('Sequence saved to [bold blue]result[/bold blue] file.')

    rprint('\nPress [bold red]Enter[/bold red] to exit.')
    input()

from dataclasses import dataclass
from mpi4py import MPI
from rich import print
import argparse


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--handlers', type=int, default=10)
    parser.add_argument('--hospital_rooms', type=int, default=10)

    return parser.parse_args()


@dataclass
class Message:
    clock: int
    value: str


@dataclass
class IncomingMessage(Message):
    sender: int


class CommMember:
    def __init__(self, comm: MPI.Comm):
        self._comm = comm
        self._rank = comm.Get_rank()
        self._size = comm.Get_size()

        self._lamport_clock = 0
        self._other_clocks = {i: 0 for i in range(self._size) if i != self._rank}

    def _log(self, message: str, color: str = 'brightwhite'):
        print(f'[white dim]#[blue]{self._rank}[/blue] >[blue]{self._lamport_clock}[/blue] - [/white dim]'
              f'[{color}]{message}[/{color}]')

    def _tick(self):
        self._lamport_clock += 1

    def _send(self, message: str, destination: int, tag: int = 0):
        self._comm.send(
            Message(self._lamport_clock, message),
            destination,
            tag
        )


class Veteran(CommMember):
    def __init__(self, comm: MPI.Comm):
        super().__init__(comm)

        self._log(f'Właśnie powstałem. Nienawidzę moich wrogów.')


if __name__ == '__main__':
    args = handle_args()

    handler_count = args.handlers
    hospital_room_count = args.hospital_rooms

    comm = MPI.COMM_WORLD
    Veteran(comm)

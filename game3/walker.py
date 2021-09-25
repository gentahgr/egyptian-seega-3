# -*- coding: utf-8
"""
Game Board Walker

"""

from .game3 import Game3


class Walker(object):

    def __init__(self, game, ptr):
        self._game = game
        self._history = []
        self.update(ptr)

    def update(self, pt):
        self._ptr = pt
        self._nexts = self._game.board(pt)["next"]

    def forward(self, pt):
        self._history.append(self._ptr)
        self.update(pt)

    def backward(self):
        if self._history:
            pt = self._history.pop()
            self.update(pt)

    def attr(self, pt):
        return self._game[pt]

    def print_board1(self, pt):
        board, turn = pt
        prop = self._game.board(pt)
        print("{}|{}|{}|turn: {turn}\n{}|{}|{}|Flags: {flags}\n{}|{}|{}|Next: {next}".format(
            *board, turn=turn, flags=prop["flags"], next=len(prop["next"])))

    def print_board(self):
        print("Current")
        self.print_board1(self._ptr)

        for i, n in enumerate(self._nexts):
            print(f"==Case {i}")
            self.print_board1(n)

    def print_history(self):
        for i, b in enumerate(self._history):
            print(f"Step: {i}")
            self.print_board1(b)

    def main_loop(self):
        while True:
            self.print_board()
            cmd = input("[{}] Command(q(uit),p(rev),h(istory),Number)".format(len(self._history)))
            cmd = cmd.strip().lower()
            if cmd.startswith('q'):
                break
            elif cmd.startswith('p'):
                self.backward()
            elif cmd.startswith('h'):
                self.print_history()
            else:
                try:
                    n = int(cmd)
                    if 0 <= n < len(self._nexts):
                        self.forward(self._nexts[n])
                    else:
                        print("f{n} is not a valid index.")

                except ValueError:
                    print(f"{cmd} is not a number.")
                    pass


def main():
    g = Game3()

    init_b = (Game3.G_P1, Game3.G_P1, Game3.G_P1,
              Game3.G_Empty, Game3.G_Empty, Game3.G_Empty,
              Game3.G_P2, Game3.G_P2, Game3.G_P2)

    init_t = Game3.G_P1
    g.analyze(init_b, init_t)
    Walker(g, (init_b, init_t)).main_loop()


if __name__ == '__main__':
    main()

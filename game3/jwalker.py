# -*- coding: utf-8
"""
Game Board Walker for Jupyter notebook

"""
from .game3 import Game3
from IPython.display import HTML, SVG


class W(object):

    disp_icon = {
        Game3.G_P1: "O",
        Game3.G_P2: "X",
        Game3.G_Empty: "",

    }

    @classmethod
    def new(cls):
        g = Game3()

        init_b = (Game3.G_P1, Game3.G_P1, Game3.G_P1,
                  Game3.G_Empty, Game3.G_Empty, Game3.G_Empty,
                  Game3.G_P2, Game3.G_P2, Game3.G_P2)

        init_t = Game3.G_P1
        g.analyze(init_b, init_t)
        return cls(g, (init_b, init_t))

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

    def top(self):
        if self._history:
            pt = self._history[0]
            self._history = []
            self.update(pt)

    def b2d(self, b):
        if hasattr(b, '__iter__'):
            return (self.disp_icon[i] for i in b)
        else:
            return self.disp_icon[b]

    def print_board1(self, pt, title):
        board, turn = pt
        prop = self._game.board(pt)
        return ('<div float="left"><table><caption>{title}</caption>'
                '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'
                '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'
                '<tr><td>{}</td><td>{}</td><td>{}</td></tr><table>'
                'turn: {turn}, f: {flags}, n: {next}</div>'.format(
                 *self.b2d(board), title=title, turn=self.b2d(turn),
                 flags=prop["flags"], next=len(prop["next"])))

    def print_board(self):
        return HTML(self.print_board1(self._ptr, "Current"))

    def print_next_boards(self):
        r = [self.print_board1(n, f"Case {i}") for i, n in enumerate(self._nexts)]

        return HTML("".join(r))

    def print_history(self):
        r = [self.print_board1(b, f"Step: {i}") for i, b in enumerate(self._history)]
        return HTML("".join(r))

    # Command
    @property
    def pc(self):
        return self.print_board()

    @property
    def pn(self):
        return self.print_next_boards()

    @property
    def ph(self):
        return self.print_history()

    def f(self, n):
        if 0 <= n < len(self._nexts):
            self.forward(self._nexts[n])
        else:
            raise ValueError(f"{n} is not a valid index.")
        return self

    @property
    def b(self):
        self.backward()
        return self

    @property
    def t(self):
        self.top()
        return self

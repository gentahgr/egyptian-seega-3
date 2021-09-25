# -*- coding: utf-8
"""
Generate graph for game map

"""

from .game3 import Game3


class Game2Graph(object):

    disp_icon = {
        Game3.G_P1: "O",
        Game3.G_P2: "X",
        Game3.G_Empty: "-",

    }

    def __init__(self, g):
        self._game = g  # type: Game3

    def mklabel(self, pt):
        board, turn = pt
        border = 3 if turn == Game3.G_P1 else 1
        return ('<<table>'
                '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'
                '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'
                '<tr><td>{}</td><td>{}</td><td>{}</td></tr></table>>'
                ''.format(*self.b2d(board)))

    @staticmethod
    def mk_nodeid(pt):
        board, turn = pt
        return 'B{}{}{}{}{}{}{}{}{}_{}'.format(*board, turn)

    def b2d(self, b):
        if hasattr(b, '__iter__'):
            return (self.disp_icon[i] for i in b)
        else:
            return self.disp_icon[b]

    def mkattr(self, pt):
        prop = self._game.board(pt)
        flags = prop["flags"]
        if (1, 'win') in flags:
            return [("shape", "doublecircle"), ("style", "filled"), ("fillcolor", "yellow")]
        elif (2, 'win') in flags:
            return [("shape", "doublecircle")]
        elif (1, 'start') in flags or (2, 'start') in flags:
            return [("shape", "circle")]
        else:
            return [("shape", "box")]

    def dump_nodes(self, fp):
        """

        :param file fp: output stream
        :return: None
        """

        for p in self._game._game_table:
            print("{id} [label={label},{attr}];".format(
                id=self.mk_nodeid(p),
                label=self.mklabel(p),
                attr=",".join(f"{k}={v}" for k, v in self.mkattr(p))
            ), file=fp)

    def dump_edges(self, fp):
        for p in self._game._game_table:
            src = self.mk_nodeid(p)
            for n in self._game._game_table[p]["next"]:
                dst = self.mk_nodeid(n)
                print(f"{src} -> {dst};", file=fp)

    def generate_dot(self, filename):

        with open(filename, "w") as fp:
            print("""
digraph graph_name {
  graph [
    charset = "UTF-8";
    label = "Game",
    labelloc = "t",
    labeljust = "c",
  ];
                """, file=fp)
            self.dump_nodes(fp)
            self.dump_edges(fp)
            print("}", file=fp)


def main():
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "game.dot"

    g = Game3()

    init_b = (Game3.G_P1, Game3.G_P1, Game3.G_P1,
              Game3.G_Empty, Game3.G_Empty, Game3.G_Empty,
              Game3.G_P2, Game3.G_P2, Game3.G_P2)

    init_t = Game3.G_P1
    g.analyze(init_b, init_t)
    Game2Graph(g).generate_dot(filename)


if __name__ == '__main__':
    main()

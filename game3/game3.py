# -*- coding: utf-8


class Game3(object):
    """
    Egyptian Seega (3 rows)

    +-+-+-+
    |1|1|1|
    +-+-+-+
    |0|0|0|
    +-+-+-+
    |2|2|2|
    +-+-+-+
    0 : Empty
    1 : Player_1
    2 : Player_2

    Player 1 and 2 move their stones turn by turn.

    Board address
    +-+-+-+
    |0|1|2|
    +-+-+-+
    |3|4|5|
    +-+-+-+
    |6|7|8|
    +-+-+-+

    """

    # Game cell state
    G_Empty, G_P1, G_P2 = range(3)

    player_name = {
        G_P1: "Player 1",
        G_P2: "Player 2"
    }

    B_fin, B_win, B_lose = "fin", "win", "lose"

    # next position
    adjacent_cells = {
        0: (1, 3, 4),
        1: (0, 2, 3, 4, 5),
        2: (1, 4, 5),
        3: (0, 1, 4, 6, 7),
        4: (0, 1, 2, 3, 5, 6, 7, 8),
        5: (1, 2, 4, 7, 8),
        6: (3, 4, 7),
        7: (3, 4, 5, 6, 8),
        8: (4, 5, 7)
    }

    winner_pattern = {
        # stone patten : [excluded player]

        # Horizontal
        (1, 1, 1, 0, 0, 0, 0, 0, 0): (G_P1,),
        (0, 0, 0, 1, 1, 1, 0, 0, 0): tuple(),
        (0, 0, 0, 0, 0, 0, 1, 1, 1): (G_P2,),

        # Vertical
        (1, 0, 0, 1, 0, 0, 1, 0, 0): tuple(),
        (0, 1, 0, 0, 1, 0, 0, 1, 0): tuple(),
        (0, 0, 1, 0, 0, 1, 0, 0, 1): tuple(),

        # Cross
        (1, 0, 0, 0, 1, 0, 0, 0, 1): tuple(),
        (0, 0, 1, 0, 1, 0, 1, 0, 0): tuple()
    }

    def __init__(self):

        # init data area

        self._proc_q = []
        self._game_table = {}
        self._turn = self.G_P1
        self._start = None

    def next_turn(self, t):
        if t == self.G_P1:
            return self.G_P2
        elif t == self.G_P2:
            return self.G_P1

        raise ValueError("Turn must be in {}".format((self.G_P1, self.G_P2)))

    @staticmethod
    def swap_boad_pos(prev, pos1, pos2):
        """

        :param tuple prev: Previous board state
        :param int pos1: index to the first stone
        :param int pos2: index to the second stone
        :return: new board state with the 2 position of stones swapped
        """
        replace_table = {pos1: prev[pos2], pos2: prev[pos1]}
        return tuple((replace_table[i] if i in replace_table else n) for i, n in enumerate(prev))

    def next_states(self, prev_board, turn):

        # find stone position
        stones = [i for i in range(9) if prev_board[i] == turn]
        for s in stones:
            for candidate in self.adjacent_cells[s]:
                if prev_board[candidate] == self.G_Empty:
                    # The position is available
                    yield self.swap_boad_pos(prev_board, s, candidate)

    def add_queue(self, state):
        """

        :param tuple state:
        :return:
        """
        self._proc_q.append(state)

    def check_winner(self, board):
        """

        :param tuple(int, int, int, int, int, int, int, int, int) board:
        :return:
        """
        result = set()

        for turn in (self.G_P1, self.G_P2):
            player_stone_pos = tuple(1 if n == turn else 0 for n in board)
            if player_stone_pos in self.winner_pattern:
                if turn not in self.winner_pattern[player_stone_pos]:
                    result.add((turn, self.B_fin))

        return result

    def generate_board_transition(self):
        """
        Process game step

        1. Take 1 board status from queue
        2. Populate the stateus in game table
        3. Search possible next position
        4. Push next board state to queue if it does not exist.

        :return:
        """

        while self._proc_q:

            # 1. Take 1 board status from queue
            board, turn = self._proc_q.pop()

            # print(f"Processing {board} for {turn}")

            if (board, turn) in self._game_table:
                # same position can be pushed to the queue
                # print(f"Skip {(board, turn)}")
                continue

            # 2. Populate the stateus in game table
            attr = {
                "next": [],
                "flags": self.check_winner(board)
            }
            self._game_table[(board, turn)] = attr

            # skip next pattern if this pattern is already in fin case
            if len(attr["flags"]) > 0:
                print(f"Final pattern{(board, turn)}")
                continue

            # 3. Search possible next position
            next_t = self.next_turn(turn)
            for nb in self.next_states(board, turn):
                next_state = (nb, next_t)
                attr["next"].append(next_state)

                # 4. Push next board state to queue if it does not exist.
                if next_state not in self._game_table:
                    self.add_queue(next_state)

    def scan_win(self):
        update = False
        for state in self._game_table:
            board, turn = state
            n_states = self._game_table[state]["next"]
            flags = self._game_table[state]["flags"]
            
            if (turn, self.B_win) in flags:
                continue

            # Win check
            keys = ((turn, self.B_fin), (turn, self.B_win))
            if any(any(True for k in keys if k in self._game_table[n]["flags"]) for n in n_states):

                print(f"Win {board}, {turn}")
                flags.add((turn, self.B_win))
                update = True

            # Lose check
            if (turn, self.B_lose) in flags:
                continue

            n_turn = self.next_turn(turn)
            n_keys = ((n_turn, self.B_fin), (n_turn, self.B_win))

            if len(n_states) > 0 and all(any(True for k in n_keys if k in self._game_table[n]["flags"]) for n in n_states):

                print(f"Lose {board}, {turn}")
                flags.add((n_turn, self.B_win))
                flags.add((turn, self.B_lose))
                update = True

        return update

    def mark_start(self):
        s = self._game_table[self._start]
        b, t = self._start
        s["flags"].add((t, "start"))

    def board(self, b):
        return self._game_table[b]

    @property
    def start_node(self):
        return self._start

    def analyze(self, initial_board, initial_turn=G_P1):
        self._start = (initial_board, initial_turn)
        self.add_queue(self._start)
        self.generate_board_transition()

        while self.scan_win():
            # print("Scanning winner pattern")
            pass

        self.mark_start()

    def main(self):

        # push initial state to queue
        initial_board = (self.G_P1, self.G_P1, self.G_P1,
                         self.G_Empty, self.G_Empty, self.G_Empty,
                         self.G_P2, self.G_P2, self.G_P2)

        self.analyze(initial_board)

        # print result
        print("state_count: ", len(self._game_table))
        for s in sorted(self._game_table):
            v = self._game_table[s]
            print("DUMP: {} : next {} cases, {}".format(s, len(v["next"]), v["flags"]))


if __name__ == '__main__':
    Game3().main()

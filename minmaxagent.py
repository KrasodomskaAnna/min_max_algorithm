from exceptions import AgentException


class MinMaxAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token
        self.max = 1000

    def minmax(self, connect4, is_max, depth):
        if len(connect4.possible_drops()) == 0:
            return 0

        if depth == 0:
            return 0

        for i in connect4.possible_drops():
            connect4.drop_token(i)
            if connect4.wins == connect4.get_oponent():
                connect4.take_token(i)
                return self.max if is_max else -self.max
            connect4.take_token(i)

        best = -self.max if is_max else self.max
        for i in connect4.possible_drops():
            connect4.drop_token(i)
            second = self.minmax(connect4, not is_max, depth-1)
            best = (best if best >= second else second) if is_max else (best if best <= second else second)
            connect4.take_token(i)
            if best == (self.max if is_max else -self.max):
                return best

        return best

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')

        max_depth = 5

        best_move = connect4.possible_drops()[0]
        connect4.drop_token(best_move)
        best_score = self.minmax(connect4, False, max_depth)
        connect4.take_token(best_move)
        for i in connect4.possible_drops():
            if i == best_move:
                continue

            connect4.drop_token(i)
            score = self.minmax(connect4, False, max_depth)
            connect4.take_token(i)

            if score > best_score:
                best_score = score
                best_move = i

        return best_move

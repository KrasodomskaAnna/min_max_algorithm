from exceptions import AgentException


class AlphaBetaAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token
        self.max = 1000
        self.init_alfa = -1000
        self.init_betha = 1000

    def minmax(self, connect4, is_max, depth, alfa, betha):
        if len(connect4.possible_drops()) == 0:
            return 0

        if depth == 0:
            return 0

        if alfa >= betha:
            return

        for i in connect4.possible_drops():
            connect4.drop_token(i)
            if connect4.wins == connect4.get_oponent():
                connect4.take_token(i)
                return self.max if is_max else -self.max
            connect4.take_token(i)

        best = -self.max if is_max else self.max
        for i in connect4.possible_drops():
            connect4.drop_token(i)
            second = self.minmax(connect4, not is_max, depth-1, alfa, betha)

            # przyznawanie punktów centrum
            center_column = connect4.center_column()
            my_tokens = center_column.count(self.my_token)
            op_tokens = center_column.count('x' if self.my_token == 'o' else 'o')
            if my_tokens > op_tokens:
                second += (my_tokens-op_tokens)*2
            elif my_tokens < op_tokens:
                second -= (my_tokens - op_tokens)*2
            elif my_tokens == 0 and op_tokens == 0:
                second += connect4.get_size()[1]*3

            # przyznawanie punktów iter_fours (czwórki)
            iter_fours = connect4.iter_fours()
            for four in iter_fours:
                my_tokens = four.count(self.my_token)
                op_tokens = four.count('x' if self.my_token == 'o' else 'o')
                if op_tokens > 0 and my_tokens > 0:
                    second -= 1
                elif op_tokens > 0:
                    second -= op_tokens*2
                elif my_tokens > 0:
                    second += my_tokens*2
                else:
                    second += four.count('_')

            best = (best if best >= second else second) if is_max else (best if best <= second else second)
            connect4.take_token(i)
            if is_max:
                alfa = best if best <= alfa else alfa
            else:
                betha = best if best >= betha else betha
            if best == (self.max if is_max else -self.max):
                return best

        return best

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')

        max_depth = 5

        best_move = connect4.possible_drops()[0]
        connect4.drop_token(best_move)
        best_score = self.minmax(connect4, False, max_depth, self.init_alfa, self.init_betha)
        connect4.take_token(best_move)
        for i in connect4.possible_drops():
            if i == best_move:
                continue

            connect4.drop_token(i)
            score = self.minmax(connect4, False, max_depth, self.init_alfa, self.init_betha)
            connect4.take_token(i)

            if score > best_score:
                best_score = score
                best_move = i

        return best_move

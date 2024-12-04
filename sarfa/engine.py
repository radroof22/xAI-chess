import chess
import chess.engine
from collections import defaultdict

class Engine:
    def __init__(self, engine_path: str):
        """
        Params
        - engine_path: str (expecting path to the 'stockfish_15_x64_avx2' file)
        """
        self.engine_path = engine_path
        self.chess_engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)

    def q_values(self, board, candidate_actions, multipv=3, runtime=5.0) -> tuple[dict[str, float], str]:
        """
        Compute the q-values Q(s,a) for a given board
        """

        options = self.chess_engine.analyse(board, chess.engine.Limit(time=runtime), multipv=multipv)
        
        score_per_move = defaultdict(int)

        for option in options:
            is_white_move = option['score'].turn
            score = option['score'].white() if is_white_move else option['score'].black()
            
            curr_action = str(option["pv"][0])
            if option['score'].is_mate():
                score = 40 if '+' in str(score) else -40
            else:
                score = round(score.cp/100.0, 2)
            
            score_per_move[curr_action] = score

        q_vals = {}
        optimal_action = None
        best_q_val = float('-inf')
        for valid_move in candidate_actions:
            q_vals[str(valid_move)] = score_per_move[str(valid_move)]

            # track the optimal action according
            # to the max Q-value
            if q_vals[str(valid_move)] > best_q_val:
                best_q_val = q_vals[str(valid_move)]
                optimal_action = str(valid_move)
            
        return q_vals, optimal_action
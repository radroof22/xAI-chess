import chess
from .engine import Engine
from .core import computeSaliencyUsingSarfa

class SarfaBaseline:
    def __init__(self, engine: Engine, original_board: chess.Board, runtime: float=2.0):
        self.engine = engine
        self.runtime = runtime

        self.original_board = original_board
        self.original_board_actions = set(self.original_board.legal_moves) 

        # calculate the q-values for the original board
        self.q_vals_original_board, _ = self.engine.q_values(self.original_board, self.original_board_actions, runtime=runtime)

    def compute(self, perturbed_board: chess.Board, action: chess.Move | None = None) -> float:

        # action space shared by the original board
        # and the original board
        common_actions: set[chess.Move] = self.original_board_actions & set(perturbed_board.legal_moves)

        # was the action you ran posssible in these boards
        if action and action not in common_actions:
            return 0

        # only keep the keys which are in the common set 
        # of legal actions
        q_vals_original_board_common: dict[str, float] = {move: q_val for move, q_val in self.q_vals_original_board.items() if chess.Move.from_uci(move) in common_actions}
        # final optimal action by max q-value
        optimal_move_original_board: str = max(q_vals_original_board_common, key=q_vals_original_board_common.get)

        q_vals_perturbed_board, _ = self.engine.q_values(perturbed_board, common_actions, runtime=runtime)
        
        # overrride optimal action if provided
        if (action != None):
            optimal_move_original_board = action

        saliency, _, _, _, _, _ = computeSaliencyUsingSarfa(
            optimal_move_original_board, 
            q_vals_original_board_common, q_vals_perturbed_board)

        return saliency



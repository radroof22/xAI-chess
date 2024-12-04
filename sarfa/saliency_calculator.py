import chess
from .engine import Engine
from .core import computeSaliencyUsingSarfa

class SarfaBaseline:
    def __init__(self, engine: Engine, original_board: chess.Board):
        self.engine = engine

        self.original_board_actions = set(original_board.legal_moves) 
        self.original_board = original_board

    def compute(self, perturbed_board: chess.Board, action: chess.Move | None = None, runtime: float=2.0) -> float:

        # action space shared by the original board
        # and the original board
        common_actions = self.original_board_actions & set(perturbed_board.legal_moves)

        # was the action you ran posssible in these boards
        if action and action not in common_actions:
            return 0

        q_vals_original_board, optimal_move_original_board = self.engine.q_values(self.original_board, common_actions, runtime=runtime)

        q_vals_perturbed_board, _ = self.engine.q_values(perturbed_board, common_actions, runtime=runtime)

        saliency, _, _, _, _, _ = computeSaliencyUsingSarfa(
            optimal_move_original_board, 
            q_vals_original_board, q_vals_perturbed_board)

        return saliency



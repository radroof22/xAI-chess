from dataclasses import dataclass

import chess
from .engine import Engine
from .core import computeSaliencyUsingSarfa

EPSILON = 1e-9

@dataclass()
class SarfaComputeResult:
    saliency: float
    dP: float
    optimal_move: str # on the original board
    optimal_move_q_val: float

class SarfaBaseline:
    def __init__(self, engine: Engine, original_board: chess.Board, runtime: float=2.0):
        self.engine = engine
        self.runtime = runtime

        self.original_board = original_board
        self.original_board_actions = set(self.original_board.legal_moves) 

        # calculate the q-values for the original board
        self.q_vals_original_board, _ = self.engine.q_values(self.original_board, self.original_board_actions, multipv=len(self.original_board_actions),runtime=runtime)

    def compute(self, perturbed_board: chess.Board, action: chess.Move | None = None, allow_defense: bool = False) -> SarfaComputeResult:

        # BASE CASES
        # Case 1: Perturbed piece puts it into check
        if perturbed_board.was_into_check():
            return SarfaComputeResult(
                saliency=0,
                dP=EPSILON,
                optimal_move=action,
                optimal_move_q_val=float("inf")
            )
        
        # Case 2: if the original move is illegal in this perturbed state
        if action and not perturbed_board.is_legal(action):
            return SarfaComputeResult(
                saliency=1,
                dP=EPSILON,
                optimal_move=action,
                optimal_move_q_val=0
            )

        # action space shared by the original board
        # and the original board
        perturbed_board_actions = set(perturbed_board.legal_moves)
        common_actions: set[chess.Move] = self.original_board_actions & perturbed_board_actions

        

        # was the action you ran posssible in these boards
        if action and action not in common_actions or len(common_actions) < 1:
            return SarfaComputeResult(
                saliency=1,
                dP=EPSILON,
                optimal_move=action,
                optimal_move_q_val=0
            )
        
        # only keep the keys which are in the common set 
        # of legal actions
        q_vals_original_board_common: dict[str, float] = {move: q_val for move, q_val in self.q_vals_original_board.items() if chess.Move.from_uci(move) in common_actions}
        # final optimal action by max q-value
        optimal_move_original_board: str = max(q_vals_original_board_common, key=q_vals_original_board_common.get)

        q_vals_perturbed_board, _ = self.engine.q_values(perturbed_board, common_actions, multipv=len(perturbed_board_actions), runtime=self.runtime)

        
        # overrride optimal action if provided
        if (action != None):
            optimal_move_original_board = str(action)
        # print(common_actions)
        # print(optimal_move_original_board)
        # print(q_vals_original_board_common)
        # print(q_vals_perturbed_board)
        saliency, dP, _, _, _, _ = computeSaliencyUsingSarfa(
            optimal_move_original_board, 
            q_vals_original_board_common, q_vals_perturbed_board,
            allow_defense_check=allow_defense)

        return SarfaComputeResult(
            saliency=saliency,
            dP=dP,
            optimal_move=optimal_move_original_board,
            optimal_move_q_val = max(q_vals_original_board_common.values())
        )
    
    def compute_q_values(self, perturbed_board: chess.Board) -> tuple[dict[str, float], dict[str, float], str]:

        # action space shared by the original board
        # and the original board
        common_actions: set[chess.Move] = self.original_board_actions & set(perturbed_board.legal_moves)
        
        # only keep the keys which are in the common set 
        # of legal actions
        q_vals_original_board_common: dict[str, float] = {move: q_val for move, q_val in self.q_vals_original_board.items() if chess.Move.from_uci(move) in common_actions}
        # final optimal action by max q-value
        optimal_move_original_board: str = max(q_vals_original_board_common, key=q_vals_original_board_common.get)

        q_vals_perturbed_board, _ = self.engine.q_values(perturbed_board, common_actions, runtime=self.runtime)

        return q_vals_original_board_common, q_vals_perturbed_board, optimal_move_original_board



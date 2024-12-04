import chess
from .utils import get_pos_obj, get_all_pos
from typing import Generator
class RemovalPerturber:
    def __init__(self, board: chess.Board):
        self.board = board
        
    def perturb_position(self, position_str: str) -> chess.Board | None:
        position = get_pos_obj(position_str)
        
        piece = self.board.piece_at(position)
        # don't remove it if its a king
        if not piece or piece == chess.Piece(chess.KING, chess.WHITE) or piece == chess.Piece(chess.KING, chess.BLACK):
            return None

        perturbed_board = self.board.copy()
        perturbed_board.remove_piece_at(position)

        # if the perturbation leads to a check
        # this is an irrelevant comparison so ignore it
        if perturbed_board.was_into_check():
            return None
        
        return perturbed_board
        
    def process(self) -> Generator[tuple[chess.Board, str], None, None]:
        """
        Generator that iterates over all board positions and yields perturbed instances.
        Each yield contains the perturbed board and the position string that was perturbed.
        """
        for position_str in get_all_pos():
            perturbed_board = self.perturb_position(position_str)
            if perturbed_board:
                yield perturbed_board, position_str

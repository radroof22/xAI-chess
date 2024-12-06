import chess
from .utils import get_pos_obj, get_all_pos
from typing import Generator

class Perturber:
    def __init__(self, board: chess.Board):
        self.board = board

    def perturb_position(self, position_str: str) -> chess.Board | None:
        raise NotImplementedError("Need to implement perturb position function.")

    def process(self) -> Generator[tuple[chess.Board, str], None, None]:
        """
        Generator that iterates over all board positions and yields perturbed instances.
        Each yield contains the perturbed board and the position string that was perturbed.
        """
        for position_str in get_all_pos():
            perturbed_board = self.perturb_position(position_str)
            if perturbed_board:
                yield perturbed_board, position_str
        
class RemovalPerturber(Perturber):
        
    def perturb_position(self, position_str: str) -> chess.Board | None:
        position = get_pos_obj(position_str)
        
        piece = self.board.piece_at(position)
        # don't remove it if its a king
        if not piece or piece == chess.Piece(chess.KING, chess.WHITE) or piece == chess.Piece(chess.KING, chess.BLACK):
            return None

        perturbed_board = self.board.copy()
        perturbed_board.remove_piece_at(position)
        
        return perturbed_board
        

class AddPerturber(Perturber):
        
    def perturb_position(self, position_str: str) -> chess.Board | None:
        position = get_pos_obj(position_str)
        piece = self.board.piece_at(position)
        perturbed_board = None

        # can add a piece only if the space is empty
        if not piece:
            perturbed_board = self.board.copy()
            # add pawn same color as current move
            new_piece = chess.Piece(chess.PAWN, chess.WHITE) if self.board.turn else chess.Piece(chess.PAWN, chess.BLACK)
            perturbed_board.set_piece_at(position, new_piece)

        return perturbed_board
        
from chess import Board, Move
import numpy as np
import cv2
from utils import pos_to_index_mapping
import svg_custom.svg_custom as svg_custom 
import cairosvg


class BoardVisualization():
    DRAWING_FILE = "svg_custom/board"
    def __init__(self, board: Board):
        self.board : Board = board

    def only_board(self) -> "displayable":
        """
        Displays only the board for of the FEN without
        any extra visualizations.
        """
        return self.board

    def get_heatmap(self, position_to_saliency: dict[str, float]) -> np.array:
        # Heatmap of saliency icons
        heatmap = np.zeros((8, 8))
        for position in position_to_saliency:
            row, col = pos_to_index_mapping(position)
            heatmap[row, col] = position_to_saliency[position]

        heatmap = np.flipud(heatmap)

        return heatmap

    def _draw_saliency_boxes(self, heatmap: np.array):
        # original board as a numpy array
        board_array = cv2.imread(f"{self.DRAWING_FILE}.png")

        threshold = (100/256)*np.max(heatmap) # percentage threshold. Saliency values above this threshold won't be mapped onto board

        # Create bounding boxes with saliency colours for every square on chess board
        for i in range(0, 8, 1):
            for j in range(0, 8, 1):
                ii = 45*i+20
                jj = 45*j+20
                value_of_square =  heatmap[i, j]
                if value_of_square < threshold:
                    continue
                for box_i in range(ii, ii+44, 1):
                    for box_j in range(jj, jj+44, 1):
                        if box_i > ii+4 and box_i < ii+40 and box_j > jj+4 and box_j < jj+40:
                            continue
                        board_array[box_i, box_j, 0] = 256 - 0.8*256*heatmap[i, j]/(np.max(heatmap) + 1e-10)
                        board_array[box_i, box_j, 1] = 256 - 0.84*256*heatmap[i, j]/(np.max(heatmap) + 1e-10)
                        board_array[box_i, box_j, 2] = 256 - 0.19*256*heatmap[i, j]/(np.max(heatmap) + 1e-10)
        cv2.imwrite(f"{self.DRAWING_FILE}.png", board_array)

    def show_heatmap(self, position_to_saliency: dict[str, float], best_move: Move) -> str:
        """
        Generates heatmap for saliency evaluation of the best move

        Returns path (string) to SVG image with correct drawings.

        ```bash
        board_path = Visualizer.show_heatmap(...)
        display(Image(board_path))
        ```
        """
        heatmap = self.get_heatmap(position_to_saliency)

        # draw svg with arrow best_move
        arrows = []
        if best_move:
            arrows = [svg_custom.Arrow(tail =  best_move.from_square, head = best_move.to_square, color = '#e6e600')]
        svg = svg_custom.board(self.board, arrows = arrows)

        with open(f"{self.DRAWING_FILE}.svg", 'w+') as f:
            f.write(svg)
        cairosvg.svg2png(url=f"{self.DRAWING_FILE}.svg", write_to=f"{self.DRAWING_FILE}.png")

        self._draw_saliency_boxes(heatmap)

        return f"{self.DRAWING_FILE}.png"

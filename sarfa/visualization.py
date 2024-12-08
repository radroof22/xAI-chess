from chess import Board, Move
import numpy as np
import cv2
from .utils import pos_to_index_mapping
import svg_custom.svg_custom as svg_custom 
import cairosvg
import matplotlib.pyplot as plt
import chess
from PIL import Image as PILImage

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

    def _add_labels(self, board_array: np.array):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        color = (255, 255, 255)  # White text

        # Add column labels (a to h) towards the center of each square
        for j, label in enumerate("abcdefgh"):
            position = (45 * j + 37, 395)  # Adjusted to center the label in the square
            cv2.putText(board_array, label, position, font, font_scale, color, thickness)

        # Add row labels (1 to 8) slightly lower than before
        for i, label in enumerate("87654321"):
            position = (5, 45 * i + 47)  # Slightly lower text for rows
            cv2.putText(board_array, label, position, font, font_scale, color, thickness)

    def _draw_saliency_boxes(self, heatmap: np.array):
        # original board as a numpy array
        board_array = cv2.imread(f"{self.DRAWING_FILE}.png")
        self._add_labels(board_array)
        if not heatmap.any():
            cv2.imwrite(f"{self.DRAWING_FILE}.png", board_array)
            return

        threshold = (10/256)*np.max(heatmap) # percentage threshold. Saliency values above this threshold won't be mapped onto board

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

class OffenseDefenseBoardVisualization():
    DRAWING_FILE = "svg_custom/board"
    def __init__(self, board: Board):
        self.board : Board = board

    def only_board(self) -> "displayable":
        """
        Displays only the board for of the FEN without
        any extra visualizations.
        """
        return self.board

    def get_heatmap(self, position_to_saliency: dict[str, tuple[str, float]]) -> tuple[np.array, np.array]:
        # Heatmap of saliency icons
        heatmap = np.zeros((8, 8))
        # +1=offense, -1=defense
        offense_defense_heatmap = np.zeros((8, 8))
        for position in position_to_saliency:
            row, col = pos_to_index_mapping(position)
            heatmap[row, col] = position_to_saliency[position][1]
            if (position_to_saliency[position][0] == 'defensive'):
                offense_defense_heatmap[row, col] = -1
            else:
                offense_defense_heatmap[row, col] = 1

        heatmap = np.flipud(heatmap)
        offense_defense_heatmap = np.flipud(offense_defense_heatmap)

        return heatmap, offense_defense_heatmap

    def _draw_saliency_boxes(self, heatmap: np.array, offense_defense_heatmap:np.array):
        # original board as a numpy array
        board_array = cv2.imread(f"{self.DRAWING_FILE}.png")

        defensive_threshold = (100/256)*np.max(heatmap[offense_defense_heatmap == -1]) # percentage threshold. Saliency values above this threshold won't be mapped onto board
        defensive_max = np.max(heatmap[offense_defense_heatmap == -1])

        offensive_threshold = (100/256)*np.max(heatmap[offense_defense_heatmap == 1]) # percentage threshold. Saliency values above this threshold won't be mapped onto board
        offensive_max = np.max(heatmap[offense_defense_heatmap == 1])

        # Create bounding boxes with saliency colours for every square on chess board
        for i in range(0, 8, 1):
            for j in range(0, 8, 1):
                ii = 45*i+20
                jj = 45*j+20
                value_of_square =  heatmap[i, j]

                if (int(offense_defense_heatmap[i, j]) == 1 and value_of_square < offensive_threshold):
                    continue
                elif (int(offense_defense_heatmap[i, j]) == -1 and value_of_square < defensive_threshold):
                    continue

                for box_i in range(ii, ii+44, 1):
                    for box_j in range(jj, jj+44, 1):
                        if box_i > ii+4 and box_i < ii+40 and box_j > jj+4 and box_j < jj+40:
                            continue
                        # offensive
                        if (int(offense_defense_heatmap[i, j]) == 1):
                            board_array[box_i, box_j, 0] = 256 - 0.8*256*heatmap[i, j]/(offensive_max + 1e-10)
                            board_array[box_i, box_j, 1] = 256 - 0.84*256*heatmap[i, j]/(offensive_max + 1e-10)
                            board_array[box_i, box_j, 2] = 256 - 0.19*256*heatmap[i, j]/(offensive_max + 1e-10)
                        elif ((int(offense_defense_heatmap[i, j]) == -1)):
                            # defensive
                            board_array[box_i, box_j, 0] = 256 - 0.19*256*heatmap[i, j]/(defensive_max + 1e-10)
                            board_array[box_i, box_j, 1] = 256 - 0.84*256*heatmap[i, j]/(defensive_max + 1e-10)
                            board_array[box_i, box_j, 2] = 256 - 0.8*256*heatmap[i, j]/(defensive_max + 1e-10)

        cv2.imwrite(f"{self.DRAWING_FILE}.png", board_array)

    def show_heatmap(self, position_to_saliency: dict[str, tuple[str, float]], best_move: Move) -> str:
        """
        Generates heatmap for saliency evaluation of the best move

        Returns path (string) to SVG image with correct drawings.

        ```bash
        board_path = Visualizer.show_heatmap(...)
        display(Image(board_path))
        ```
        """
        heatmap, offense_defense_heatmap = self.get_heatmap(position_to_saliency)

        # draw svg with arrow best_move
        arrows = []
        if best_move:
            arrows = [svg_custom.Arrow(tail =  best_move.from_square, head = best_move.to_square, color = '#e6e600')]
        svg = svg_custom.board(self.board, arrows = arrows)

        with open(f"{self.DRAWING_FILE}.svg", 'w+') as f:
            f.write(svg)
        cairosvg.svg2png(url=f"{self.DRAWING_FILE}.svg", write_to=f"{self.DRAWING_FILE}.png")

        self._draw_saliency_boxes(heatmap, offense_defense_heatmap)

        return f"{self.DRAWING_FILE}.png"

class PairsBoardVisualization():
    DRAWING_FILE = "svg_custom/board"
    def __init__(self, board: Board):
        self.board : Board = board

    def only_board(self) -> "displayable":
        """
        Displays only the board for of the FEN without
        any extra visualizations.
        """
        return self.board

    def get_heatmap(self, important_groups: list[list[str]]) -> np.array:
        # Heatmap of saliency icons
        heatmap = np.zeros((8, 8))
        heatmap[:, :] = -1
        for i, group in enumerate(important_groups):
            for position in group:
                row, col = pos_to_index_mapping(position)
                heatmap[row, col] = i

        heatmap = np.flipud(heatmap)

        return heatmap

    def _draw_saliency_boxes(self, heatmap: np.array):
        # define group colors with RGB
        colors = [(255, 0, 0), (255, 153, 51), (255, 255, 51), (153, 255, 51), (51, 255, 255), (0,0,255), (127,0,255), (255,0,255), (128, 128, 128)]

        # original board as a numpy array
        board_array = cv2.imread(f"{self.DRAWING_FILE}.png")

        threshold = 0

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

                        board_array[box_i, box_j, 0] = colors[int(heatmap[i, j])][2]
                        board_array[box_i, box_j, 1] = colors[int(heatmap[i, j])][1]
                        board_array[box_i, box_j, 2] = colors[int(heatmap[i, j])][0]

        cv2.imwrite(f"{self.DRAWING_FILE}.png", board_array)

    def show_heatmap(self, important_groups: list[list[str]], best_move: Move) -> str:
        """
        Generates heatmap for saliency evaluation of the best move

        Returns path (string) to SVG image with correct drawings.

        ```bash
        board_path = Visualizer.show_heatmap(...)
        display(Image(board_path))
        ```
        """
        heatmap = self.get_heatmap(important_groups)

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

class ProgressionVisualizer:
    def __init__(self, saliency_timestep, moves_taken: list[chess.Move]):
        self.boards = [st[1] for st in saliency_timestep]
        self.saliency_map = [st[0] for st in saliency_timestep]
        self.moves_taken = moves_taken
        self.depth = len(moves_taken)

    def show(self) -> plt.Figure:
        # Create a grid of subplots (1 row, `depth` columns)
        fig, axes = plt.subplots(1, self.depth, figsize=(5 * self.depth, 5))  # Adjust the size as needed

        # Loop through indices 1 through `depth`
        for step in range(self.depth):  # 1 through `depth` inclusive
            board_visualization = BoardVisualization(self.boards[step])
            path = board_visualization.show_heatmap(self.saliency_map[step], self.moves_taken[step])
            img = PILImage.open(path)
            
            # Display the image in the corresponding subplot
            axes[step].imshow(img)
            axes[step].axis('off')  # Turn off axis
            axes[step].set_title(f"Timestep {step}", fontsize=12)

        # Adjust layout and show the grid
        plt.tight_layout()
        return fig
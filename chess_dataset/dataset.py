import json

def load_dataset(prefix="./"):
    with open(prefix+"chess_dataset/chess_saliency_dataset_v1.json", "rb") as f:
        raw_data = json.load(f)

    return ChessPuzzleDataset(raw_data)

class ChessPuzzleDataset:
    def __init__(self, puzzles_data):
        """
        Initialize the dataset with the puzzles data.
        :param puzzles_data: JSON data containing puzzles.
        """
        self.length = puzzles_data.get('length', 0)
        self.puzzles = self._parse_puzzles(puzzles_data.get('puzzles', []))

    def _parse_puzzles(self, puzzles):
        """
        Parse the list of puzzles to extract relevant data.
        :param puzzles: List of puzzles from the JSON.
        :return: List of parsed puzzles.
        """
        parsed_puzzles = []
        for puzzle in puzzles:
            parsed_puzzles.append({
                'fen': puzzle.get('fen'),
                'responseMoves': puzzle.get('responseMoves', []),
                'saliencyGroundTruth': puzzle.get('saliencyGroundTruth', []),
                'solution': puzzle.get('solution', []),
            })
        return parsed_puzzles
    
    def get_puzzle(self, index):
        """
        Get a specific puzzle by index.
        :param index: Index of the puzzle.
        :return: Puzzle dictionary.
        """
        if index < 0 or index >= self.length:
            raise IndexError("Puzzle index out of range.")
        return self.puzzles[index]
    
    def get_fen(self, index):
        """
        Get the FEN (board state) of a specific puzzle.
        :param index: Index of the puzzle.
        :return: FEN string.
        """
        return self.get_puzzle(index)['fen']
    
    def get_response_moves(self, index):
        """
        Get the response moves of a specific puzzle.
        :param index: Index of the puzzle.
        :return: List of response moves.
        """
        return self.get_puzzle(index)['responseMoves']
    
    def get_saliency_ground_truth(self, index):
        """
        Get the saliency ground truth of a specific puzzle.
        :param index: Index of the puzzle.
        :return: List of saliency ground truth squares.
        """
        return self.get_puzzle(index)['saliencyGroundTruth']
    
    def get_solution(self, index):
        """
        Get the solution moves of a specific puzzle.
        :param index: Index of the puzzle.
        :return: List of solution moves.
        """
        return self.get_puzzle(index)['solution']
    
    def get_all_puzzles(self):
        """
        Get all puzzles in the dataset.
        :return: List of all puzzles.
        """
        return self.puzzles
    
    def __len__(self):
        """
        Return the number of puzzles in the dataset.
        :return: Number of puzzles.
        """
        return self.length
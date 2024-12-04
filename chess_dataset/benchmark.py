from typing import Callable, Dict, List

import numpy as np
from sklearn.metrics import roc_curve, auc

import chess

from .dataset import load_dataset

class SafraBenchmark:

    def __init__(self, saliency_algorithm: Callable[[str], Dict[str, int]]):
        self.dataset = load_dataset()
        self.saliency_algorithm: Callable[[str], Dict[str, int]] = saliency_algorithm

        self.ground_truth_array = np.array([])
        self.predicted_values_array = np.array([])
        self.index_to_position_strs = []
        
        self._run_test()

    def _run_test(self):
        """
        Takes the saliency_algorithm and runs it on the test dataset 
        """

        for i in range(len(self.dataset)):
            print(i)
            if (i == 2):
                break

            fen = self.dataset.get_fen(i)

            # use the ground truth action provided from the dataset
            board = chess.Board(fen)
            action_ground_truth: chess.Move = board.parse_san(self.dataset.get_solution(i)[0])

            saliency_predicted: Dict[str, float] = self.saliency_algorithm(fen, action_ground_truth)

            saliency_ground_truths: List[str] = self.dataset.get_saliency_ground_truth(i)

            # Sanity check
            for val in saliency_ground_truths:
                if val not in saliency_predicted:
                    raise ValueError("There is a saliency value that exists in the dataset ground truth which wasn't tested by the algorithm")
            
            ground_truth_array, predicted_values_array, index_to_position_str = self.get_aligned_arrays(saliency_ground_truths, saliency_predicted)

            self.ground_truth_array = np.concatenate((self.ground_truth_array, ground_truth_array))
            self.predicted_values_array = np.concatenate((self.predicted_values_array, predicted_values_array))
            self.index_to_position_strs.append(index_to_position_str)

    

    def get_aligned_arrays(self, ground_truth, predicted_values):
        """
        This function takes a list of ground_truth keys and a predicted_values dictionary,
        aligning the values to generate two NumPy arrays: one for ground truth and one for predicted values.
        The ground truth values are set to 1 for keys present in predicted_values.

        Returns:
            - ground_truth_array: A NumPy array with values 1 or 0 based on presence in predicted_values.
            - predicted_values_array: A NumPy array with float values from the predicted_values dictionary.
            index_to_position_str: dictionary mapping index to the corresponding position as a string
        """
        # Combine ground_truth and predicted keys to get all possible keys
        all_positions = set(ground_truth).union(predicted_values.keys())
        
        # Initialize lists for the aligned values
        ground_truth_array = []
        predicted_values_array = []
        index_to_position_str = {}
        
        # Iterate over all possible keys (the union of ground_truth and predicted_keys)
        for i, pos in enumerate(all_positions):
            # Ground truth array: 1 if key is in ground_truth, 0 otherwise
            ground_truth_array.append(1 if pos in ground_truth else 0)
            
            # Predicted values array: value from predicted_values or 0 if key not found
            predicted_values_array.append(predicted_values.get(pos, 0))
            index_to_position_str[i] = pos
        
        # Convert to NumPy arrays
        ground_truth_array = np.array(ground_truth_array)
        predicted_values_array = np.array(predicted_values_array)
        
        # scale the predicted score between 0-1
        min_val = np.min(predicted_values_array)
        max_val = np.max(predicted_values_array)
        predicted_values_array = (predicted_values_array-min_val) / (max_val-min_val)
        return ground_truth_array, predicted_values_array, index_to_position_str
        

    def accuracy(self):
        """
        This function compares different ways to combine two sets of values, delta_p and K,
        and calculates the harmonic mean, arithmetic mean, geometric mean, and minimum as scalars.

        Returns:
            dict: A dictionary containing the computed results for harmonic mean, average, geometric mean, and minimum.
        """
        # Ensure using numpy arrays
        individual_accuracies = 1 - np.abs(self.predicted_values_array - self.ground_truth_array)  # absolute difference
        harmonic_mean_scalar = np.mean(individual_accuracies)  # Get scalar value by averaging over all values

        # Return the results in a dictionary as scalars
        return {
            'accuracy - harmonic_mean': harmonic_mean_scalar
        }


    
    def roc_curve(self) -> tuple[np.array, np.array]:
        fpr, tpr, thresholds = roc_curve(self.ground_truth_array, self.predicted_values_array)

        return fpr, tpr
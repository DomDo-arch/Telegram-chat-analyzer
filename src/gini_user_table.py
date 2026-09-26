from make_table_from_chat import make_table
import numpy as np	
from collections import Counter
from pandas import DataFrame

def gini(x):
    # Convert to a NumPy array and sort in ascending order
    x = np.asarray(x, dtype=np.float64)
    sorted_x = np.sort(x)
    n = len(x)
    
    # Check for zero mean to avoid division by zero
    if np.sum(sorted_x) == 0:
        return 0.0
        
    # Relative mean absolute difference formula
    # G = sum_i (2i - n - 1) * x_i / (n * sum_i x_i)
    index = np.arange(1, n + 1)
    return (np.sum((2 * index - n - 1) * sorted_x)) / (n * np.sum(sorted_x))
   
if __name__ == "__main__":
	
	input_txt = "group_chat.json"
	df = make_table(input_txt)
	
	print(df)
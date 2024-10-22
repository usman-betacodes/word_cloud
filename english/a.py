import numpy as np

def calculate_percentile(data, percentile):
    return np.percentile(data, percentile)

# Example usage
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
percentile_value = 90
result = calculate_percentile(data, percentile_value)
print(f"The {percentile_value}th percentile is: {result}")

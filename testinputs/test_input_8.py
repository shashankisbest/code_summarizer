import numpy as np

def calculate_statistics(data):
    """Calculate mean, median, std deviation."""
    arr = np.array(data)
    return {
        'mean': np.mean(arr),
        'median': np.median(arr),
        'std': np.std(arr),
        'min': np.min(arr),
        'max': np.max(arr)
    }

def remove_outliers(data, threshold=2):
    """Remove outliers using z-score method."""
    arr = np.array(data)
    mean = np.mean(arr)
    std = np.std(arr)
    z_scores = np.abs((arr - mean) / std)
    return arr[z_scores < threshold]

data = [1, 2, 3, 4, 5, 100, 4, 3, 2]
stats = calculate_statistics(data)
print(stats)

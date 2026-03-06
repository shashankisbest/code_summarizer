import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_dataset(filepath):
    """Load CSV dataset into DataFrame"""
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print("File not found")
        return None

def preprocess_data(df):
    """Clean and prepare data for analysis"""
    # Remove missing values
    df = df.dropna()
    
    # Normalize numerical columns
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = (df[col] - df[col].mean()) / df[col].std()
    
    return df

class DataAnalyzer:
    """Performs statistical analysis on datasets"""
    
    def __init__(self, data):
        self.data = data
    
    def calculate_statistics(self):
        """Calculate basic statistics"""
        return self.data.describe()
    
    def find_correlations(self):
        """Find correlations between variables"""
        return self.data.corr()
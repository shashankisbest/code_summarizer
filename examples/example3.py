import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def split_data(df, target_column):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y

def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

class ModelEvaluator:
    
    def __init__(self, model):
        self.model = model

    def evaluate(self, X_test, y_test):
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        return mse
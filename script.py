# -*- coding: utf-8 -*-
"""D24CSA003_MLOps_Major.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jEXQOgpXiO2BWtIw7T8_tN-2hgvCVisV

#Question 1: Data Structure and Processing Pipeline

## a: Create a data processing class that implements:

Conversion of data to pandas DataFrame with proper column names
"""

# Required Libraries
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import mlflow
import mlflow.sklearn
import joblib

# Data Processor Class
class IrisDataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.data = load_iris()
        self.df = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def prepare_data(self):
        # Convert to DataFrame
        self.df = pd.DataFrame(self.data.data, columns=self.data.feature_names)
        self.df['target'] = self.data.target

        # Feature scaling
        self.df[self.data.feature_names] = self.scaler.fit_transform(self.df[self.data.feature_names])

        # Train-test split
        X = self.df[self.data.feature_names]
        y = self.df['target']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        return self.X_train, self.X_test, self.y_train, self.y_test , df

    def get_feature_stats(self):
        return self.df.describe()

class IrisExperiment:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.models = {
            'Logistic Regression': LogisticRegression(),
            'Random Forest': RandomForestClassifier()
        }
        self.results = {}

    def run_experiment(self):
        for model_name, model in self.models.items():
            # Start a new MLflow run for each model
            with mlflow.start_run(nested = True):
                model.fit(self.data_processor.X_train, self.data_processor.y_train)
                y_pred = model.predict(self.data_processor.X_test)

                # Record metrics
                accuracy = accuracy_score(self.data_processor.y_test, y_pred)
                precision = precision_score(self.data_processor.y_test, y_pred, average='macro')
                recall = recall_score(self.data_processor.y_test, y_pred, average='macro')

                # Log metrics to MLflow
                mlflow.log_param("Model", model_name)
                mlflow.log_metric("Accuracy", accuracy)
                mlflow.log_metric("Precision", precision)
                mlflow.log_metric("Recall", recall)

                # Store results
                self.results[model_name] = {'Accuracy': accuracy, 'Precision': precision, 'Recall': recall}

            # End the MLflow run automatically when the 'with' block exits

    def log_results(self):
        for model_name, metrics in self.results.items():
            print(f"Results for {model_name}:")
            for metric, value in metrics.items():
                print(f"{metric}: {value}")

# Model Optimizer Class
class IrisModelOptimizer:
    def __init__(self, experiment):
        self.experiment = experiment

    def quantize_model(self, model):
        # Quantize by reducing precision of coefficients (simple example for logistic regression)
        model.coef_ = np.round(model.coef_, decimals=2)
        return model

    def run_tests(self):
        for model_name, model in self.experiment.models.items():
            # Test model quantization for Logistic Regression only
            if model_name == 'Logistic Regression':
                quantized_model = self.quantize_model(model)
                print(f"Quantized Model Coefficients for {model_name}: {quantized_model.coef_}")

# Main Code Execution
def main():
    # Initialize processor
    processor = IrisDataProcessor()
    X_train, X_test, y_train, y_test, df = processor.prepare_data()

    print("Feature Statistics:")
    print(processor.get_feature_stats())
    print("\nDataFrame:")
    print(df.head())

    # Run experiments
    experiment = IrisExperiment(processor)
    experiment.run_experiment()
    experiment.log_results()

    # Optimize and test
    optimizer = IrisModelOptimizer(experiment)
    optimizer.run_tests()

if __name__ == "__main__":
    main()
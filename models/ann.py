from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from matplotlib import pyplot as plt
import os
from datetime import datetime
import numpy as np

from utils.preprocess_data import X_col, y_col

class ANN:
    def __init__(self):
        self.model = Sequential()
        # Define the model layers
        self.model.add(Dense(64, input_dim=7, activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(1, activation='linear'))
        
        # Compile the model
        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    def summary(self):
        # Display the model summary
        return self.model.summary()
    
    def fit(self, X, y, epochs:int = 100, batch_size:int = 32, validation_ratio:float = 0.2):
        # Train the model
        history = self.model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=validation_ratio)
        return history

    def test(self, X_test, y_test, save_path="metrics/ann"):
        # Calculate mean squared error and mean absolute error
        test_metrics = self.model.evaluate(X_test, y_test, verbose=0)
        mse = test_metrics[0]
        mae = test_metrics[1]
        print(f"Test MSE: {mse}, Test MAE: {mae}")
        
        # Generate predictions
        y_pred = self.model.predict(X_test)
        
        # Plot actual vs predicted values
        plt.figure(figsize=(10, 6))
        plt.plot(np.array(y_test), label='Actual Values', color='b')
        plt.plot(y_pred.reshape(-1), label='Predicted Values', color='r')
        plt.xlabel('Samples')
        plt.ylabel('Values')
        plt.title(f"Actual vs Predicted Values\nMSE: {mse:.4f}, MAE: {mae:.4f}")
        plt.legend()

        # Create directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        plot_path = os.path.join(save_path, f'ann_{np.round(mse,1)}_{datetime.now().timestamp()}.png')

        # Save the plot
        plt.savefig(plot_path)
        print(f"Plot saved at {plot_path}")
        
        return mse

    def fit_and_evaluate(self, train_data, test_data):
        history = self.model.fit(self, train_data[X_col], train_data[y_col], epochs=100, batch_size=32, validation_ratio=0.2)

        mse = self.model.test(test_data[X_col], test_data[y_col])

        return history, mse
    


    def save_model(self, path=f"models/ann_model.keras"):
        # Save the model using Keras's save method
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save(path)
        print(f"Model saved to {path}")


class old_ann_model(ANN):
    def __init__(self, model_path: str = "models/ann_model.keras"):
        # Check if the model file exists
        if os.path.exists(model_path):
            self.model = load_model(model_path)
            print("Loaded model from", model_path)
        else:
            super().__init__()  # Initialize a new model if file does not exist
            print("Model file not found. Initialized a new model.")
   
    
    def evaluate(self, test_data):
        mse = self.model.test(test_data[X_col], test_data[y_col])
        return mse
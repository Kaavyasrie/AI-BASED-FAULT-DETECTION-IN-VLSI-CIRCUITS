# train.py
import pandas as pd
import pickle
from model import VerilogFaultPredictor
from dataset import generate_dataset

# Generate the dataset
dataset = generate_dataset()

# Save the dataset
dataset.to_csv('verilog_fault_dataset.csv', index=False)
print(f"Dataset with {len(dataset)} samples generated and saved to 'verilog_fault_dataset.csv'")

# Load the dataset
data = pd.read_csv('verilog_fault_dataset.csv')

# Train the model
predictor = VerilogFaultPredictor()
predictor.fit(data)

# Save the model
with open('fault_predictor.pkl', 'wb') as f:
    pickle.dump(predictor, f)

print("Model trained and saved to 'fault_predictor.pkl'")
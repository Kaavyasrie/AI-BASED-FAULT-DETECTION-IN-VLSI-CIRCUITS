# app.py
from flask import Flask, request, render_template  # Use render_template
import pickle
import os
from model import VerilogFaultPredictor
from charset_normalizer import detect  # For Verilog file encoding

app = Flask(__name__)

# Load the model
try:
    with open('fault_predictor.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Error: fault_predictor.pkl not found. Run train.py first.")
    model = None

@app.route('/', methods=['GET', 'POST'])
def index():
    predictions = []
    error = None  # Add error handling for Verilog file decoding
    if request.method == 'POST':
        code = ""
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and (file.filename.endswith('.v') or file.filename.endswith('.sv')):
                # Read the file as bytes and detect encoding
                file_bytes = file.read()
                detected = detect(file_bytes)
                encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
                try:
                    code = file_bytes.decode(encoding, errors='replace')
                except UnicodeDecodeError as e:
                    error = f"Failed to decode the Verilog file using {encoding}. Please ensure it's a valid text file."
        if not code and 'code' in request.form:
            code = request.form['code']
        
        if code and model and not error:
            predictions = model.predict(code)

    return render_template('index.html', predictions=predictions, error=error)

if __name__ == "__main__":
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True) 
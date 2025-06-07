# AI-Based Fault Prediction in Combinational Circuits

## Overview

**FaultAI** is a web-based system designed to predict faults in combinational circuits from Verilog RTL code, enhancing the reliability of hardware designs. It automates fault detection for constructs like logic operations (`&`, `|`, `^`), non-blocking assignments (`<=`), and register declarations (`reg`), addressing the limitations of manual verification. The system uses a Random Forest model trained on a dataset of 2000 Verilog snippets, covering 20 fault types (e.g., path delay, stuck-at, bridging faults). FaultAI provides detailed outputs, including fault descriptions, severity scores (1–10), occurrence probabilities (5–20%), and code fix suggestions, displayed through an intuitive web interface.

### Key Features
- **Fault Prediction**: Identifies 20 unique fault types in Verilog RTL code.
- **Detailed Outputs**: Provides fault descriptions, severity, occurrence, and fix suggestions.
- **User-Friendly Interface**: Web-based platform using Flask (backend) and React with Tailwind CSS (frontend).
- **High Accuracy**: Achieves 95% fault detection accuracy with response times under 2 seconds.
- **Scalability**: Handles diverse Verilog designs with a lightweight Random Forest model.

## Prerequisites

- **Python 3.12**: For backend scripts and Flask server.
- **Node.js and npm**: For React frontend development.
- **VS Code with Live Server**: For running the frontend.
- **Git**: For cloning the repository.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Kaavyasrie/AI-BASED-FAULT-DETECTION-IN-VLSI-CIRCUITS.git
   ```

2. **Set Up the Backend**:
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Generate the dataset (if not already present):
     ```bash
     python dataset/dataset.py
     ```
     This creates `verilog_fault_dataset.csv` in the `dataset/` folder.

3. **Train the Model**:
   - Train the Random Forest model for fault prediction:
     ```bash
     python backend/fault_prediction_model.py
     ```
     This generates `fault_model.pkl` and `vectorizer.pkl`.

4. **Set Up the Frontend**:
   - Navigate to the frontend directory and install dependencies:
     ```bash
     cd frontend
     npm install
     ```

## Usage

1. **Start the Backend Server**:
   - Run the Flask server to handle Verilog file uploads and fault predictions:
     ```bash
     cd backend
     python server.py
     ```
     The server runs on `http://localhost:5000`.

2. **Run the Frontend**:
   - Open `frontend/index.html` in VS Code.
   - Use the Live Server extension to launch the web interface (default: `http://localhost:5500`).

3. **Upload Verilog Files**:
   - Use the web interface to upload Verilog files (e.g., from `test_files/`).
   - Example files include `and_fault.v`, `or_fault.v`, etc., which trigger faults like:
     - `and_fault.v`: Path delay fault (Severity: 5, Occurrence: 10%)
     - `or_fault.v`: Path delay fault (Severity: 5, Occurrence: 10%)

4. **View Results**:
   - The interface displays three blocks per fault:
     - **Block 1**: Fault description (e.g., “PATH DELAY FAULT (AND OPERATIONS MAY CAUSE PATH DELAYS) FAULT MAY OCCUR IN LINE 5 DUE TO assign y = a & b;”).
     - **Block 2**: Severity and occurrence (e.g., “SEVERITY: 5\nFAULT OCCURRING CHANCES PERCENTAGE: 10.00%”).
     - **Block 3**: Fix suggestion (e.g., “Add timing buffers to stabilize AND operation paths.”).

## Dataset

- **File**: `verilog_fault_dataset.csv`
- **Size**: 2000 samples
- **Columns**:
  - `code`: Verilog snippet (e.g., `assign y = a & b;`).
  - `fault_type`: Fault type (e.g., Path delay fault).
  - `severity`: 1–10 scale (e.g., 5 for `&`).
  - `occurrence`: Percentage (e.g., 10% for `&`).
- Generated using `dataset.py`, covering 20 fault types like path delay, stuck-at, and bridging faults.

## Evaluation

- **Accuracy**: 95% fault detection accuracy on a test set of 400 snippets.
- **Speed**: Predictions in under 2 seconds.
- **Usability**: Tested with 15 users, rated highly for ease of use.

## Troubleshooting

- **Only “Potential blocking assignment” Fault Detected**:
  - Ensure you’re using the updated `fault_prediction_model.py`, which fixes parsing to prioritize symbols like `&` over `=`.
  - Verify `verilog_fault_dataset.csv` is in the `dataset/` folder.

- **Frontend Not Loading**:
  - Ensure Live Server is running and `npm install` was executed in the `frontend/` directory.

## Future Work

- Expand the dataset to include SystemVerilog constructs.
- Integrate with synthesis tools for end-to-end verification.
- Develop a mobile app for broader accessibility.

## References

- K. Ojha, “AI-Augmented Fault Detection and Diagnosis in VLSI Circuits: A Step toward Intelligent Chip Design,” *Journal of Artificial Intelligence and Machine Learning: Neural Networks*, Oct. 2024. [Link](https://hmjournals.com/index.php/JAIMLNN/article/view/497)
- M. Moness et al., “Automated Design Error Debugging of Digital VLSI Circuits,” *Journal of Electronic Testing*, Aug. 2022. [Link](https://link.springer.com/article/10.1007/s10836-022-06020-z)
- Anoop S, Ajeesh S, Deebu U S, “Deep Learning-Powered Fault Detection in Digital VLSI Circuits: Advancements and Applications,” *International Journal of Creative Research Thoughts (IJCRT)*, Dec. 2023.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributor

- [Kaavyasrie V T] ((https://github.com/Kaavyasrie))


# dataset.py
import random
import pandas as pd

# Fault dictionary with fault types, severity, and occurrence percentages
# Simplified keys to single tokens where possible
FAULT_DICT = {
    '&': {'fault': 'Path delay fault (AND operations may cause path delays)', 'severity': 5, 'occurrence': 10},
    '|': {'fault': 'Path delay fault (OR operations may cause path delays)', 'severity': 5, 'occurrence': 10},
    '^': {'fault': 'Path delay fault (XOR operations may cause path delays)', 'severity': 5, 'occurrence': 10},
    '~': {'fault': 'Stuck-at fault (Inverter may cause stuck-at faults)', 'severity': 7, 'occurrence': 15},
    '=': {'fault': 'Bridging fault (Assignment may cause bridging faults)', 'severity': 6, 'occurrence': 12},
    '<=': {'fault': 'Bridging fault (Non-blocking assignment may cause bridging faults)', 'severity': 6, 'occurrence': 12},
    'always_posedge': {'fault': 'Clock skew fault (Edge-triggered always block may cause clock skew)', 'severity': 8, 'occurrence': 20},
    'always_comb': {'fault': 'Combinational loop fault (Level-sensitive always block may cause combinational loops)', 'severity': 9, 'occurrence': 18},
    'if': {'fault': 'Stuck-at fault (Conditional statements may cause stuck-at faults)', 'severity': 7, 'occurrence': 15},
    'case': {'fault': 'Stuck-at fault (Case statements may cause stuck-at faults)', 'severity': 7, 'occurrence': 15},
    'assign': {'fault': 'Bridging fault (Continuous assignment may cause bridging faults)', 'severity': 6, 'occurrence': 12},
    'wire': {'fault': 'Open fault (Wire declaration may lead to open circuits)', 'severity': 4, 'occurrence': 8},
    'reg': {'fault': 'Stuck-at fault (Register declaration may cause stuck-at faults)', 'severity': 7, 'occurrence': 15},
    '`include': {'fault': 'Missing file fault (Include directive may cause missing file issues)', 'severity': 3, 'occurrence': 5},
    '`define': {'fault': 'Macro expansion fault (Macro definition may cause expansion issues)', 'severity': 3, 'occurrence': 5},
    'fork': {'fault': 'Race condition fault (Fork-join may cause race conditions)', 'severity': 8, 'occurrence': 20},
    'join': {'fault': 'Race condition fault (Fork-join may cause race conditions)', 'severity': 8, 'occurrence': 20},
    '#': {'fault': 'Delay fault (Delay specification may cause timing issues)', 'severity': 6, 'occurrence': 12},
    'wait': {'fault': 'Livelock fault (Wait statement may cause livelock)', 'severity': 9, 'occurrence': 18},
    'force': {'fault': 'Contention fault (Force statement may cause signal contention)', 'severity': 7, 'occurrence': 15}
}

# Function to generate random Verilog code snippets (more realistic)
def generate_code_snippet(fault_key=None):
    variables = ['a', 'b', 'c', 'd', 'clk', 'rst']
    # Map fault keys to snippets
    snippets = {
        '&': f"assign y = {random.choice(variables)} & {random.choice(variables)} & {random.choice(variables)};",
        '|': f"assign y = {random.choice(variables)} | {random.choice(variables)};",
        '^': f"assign y = {random.choice(variables)} ^ {random.choice(variables)};",
        '~': f"assign y = ~{random.choice(variables)};",
        '<=': f"always @(posedge {random.choice(['clk', 'rst'])}) q <= {random.choice(variables)};",
        'always_posedge': f"always @(posedge {random.choice(['clk', 'rst'])}) begin\n    q <= {random.choice(variables)};\nend",
        'always_comb': f"always @(*) begin\n    y = {random.choice(variables)} & {random.choice(variables)};\nend",
        'if': f"always @(*) begin\n    if ({random.choice(variables)} == 1)\n        y = {random.choice(variables)};\nend",
        'case': f"always @(*) begin\n    case ({random.choice(variables)})\n        0: y = 1;\n        default: y = 0;\n    endcase\nend",
        'assign': f"assign y = {random.choice(variables)} + {random.choice(variables)};",
        'wire': f"wire [3:0] {random.choice(variables)};",
        'reg': f"reg [3:0] {random.choice(variables)};",
        '`include': "`include \"file.v\"",
        '`define': "`define SIZE 8",
        'fork': f"fork\n    #5 {random.choice(variables)} = 1;\n    #5 {random.choice(variables)} = 0;\njoin",
        'join': f"fork\n    #5 {random.choice(variables)} = 1;\n    #5 {random.choice(variables)} = 0;\njoin",
        '#': f"assign #5 y = {random.choice(variables)};",
        'wait': f"wait ({random.choice(variables)} == 1);",
        'force': f"force {random.choice(variables)} = 1;"
    }
    
    # If a specific fault key is provided, return the corresponding snippet
    if fault_key:
        return snippets.get(fault_key, f"assign y = {random.choice(variables)};")
    
    # Otherwise, choose a random snippet
    return random.choice(list(snippets.values()))

# Function to detect the primary fault in a code snippet
def inject_fault(code):
    for key in FAULT_DICT:
        if key in code:
            return {
                'fault_type': FAULT_DICT[key]['fault'],
                'severity': FAULT_DICT[key]['severity'],
                'occurrence': FAULT_DICT[key]['occurrence']
            }
    return {'fault_type': 'No fault detected', 'severity': 1, 'occurrence': 1}

# Generate a balanced dataset with ~2000 samples
def generate_dataset(num_samples=2000):
    data = []
    fault_keys = list(FAULT_DICT.keys())
    samples_per_fault = num_samples // len(fault_keys)  # Distribute samples evenly

    for key in fault_keys:
        for _ in range(samples_per_fault):
            code = generate_code_snippet(key)
            fault = inject_fault(code)
            data.append({
                'code': code,
                'fault_type': fault['fault_type'],
                'severity': fault['severity'],
                'occurrence': fault['occurrence']
            })

    # Fill remaining samples with random snippets
    while len(data) < num_samples:
        code = generate_code_snippet()
        fault = inject_fault(code)
        data.append({
            'code': code,
            'fault_type': fault['fault_type'],
            'severity': fault['severity'],
            'occurrence': fault['occurrence']
        })

    return pd.DataFrame(data)

# Only generate the dataset if this script is run directly
if __name__ == "__main__":
    dataset = generate_dataset()
    dataset.to_csv('verilog_fault_dataset.csv', index=False)
    print(f"Dataset with {len(dataset)} samples generated and saved to 'verilog_fault_dataset.csv'")
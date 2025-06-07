import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from dataset import FAULT_DICT

class VerilogFaultPredictor:
    def __init__(self):
        self.fault_classifier = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight='balanced'
        )
        self.label_encoder = LabelEncoder()
        self.feature_columns = None

    def is_module_line(self, line):
        """Strictly filter any module/endmodule line"""
        line_clean = line.strip().lower()
        return 'module' in line_clean or 'endmodule' in line_clean

    def preprocess_line(self, line):
        """Extract features from a line of Verilog code"""
        features = {}
        for symbol in FAULT_DICT.keys():
            if symbol in ['always_posedge', 'always_comb']:
                # Special handling for always blocks
                if symbol == 'always_posedge' and 'always @(posedge' in line:
                    features[symbol] = 1
                elif symbol == 'always_comb' and 'always @(*)' in line:
                    features[symbol] = 1
                else:
                    features[symbol] = 0
            else:
                features[symbol] = line.count(symbol)
        return features

    def fit(self, data):
        """Train the model on the dataset"""
        X = []
        y = []

        for _, row in data.iterrows():
            code = row['code']
            lines = code.split('\n')

            for line in lines:
                if self.is_module_line(line):
                    continue

                features = self.preprocess_line(line)
                # Use the fault type from the dataset
                fault_type = row['fault_type']

                X.append(features)
                y.append(fault_type)

        X_df = pd.DataFrame(X)
        self.feature_columns = X_df.columns
        self.label_encoder.fit(y)
        y_encoded = self.label_encoder.transform(y)
        self.fault_classifier.fit(X_df, y_encoded)

    def predict(self, code):
        """Predict all valid faults, excluding module lines"""
        lines = code.split('\n')
        predictions = []
        seen_faults = set()

        for i, line in enumerate(lines, 1):
            if self.is_module_line(line):
                continue

            features = self.preprocess_line(line)
            features_df = pd.DataFrame([features])

            for col in self.feature_columns:
                if col not in features_df:
                    features_df[col] = 0
            features_df = features_df[self.feature_columns]

            fault_pred = self.fault_classifier.predict(features_df)
            fault_type = self.label_encoder.inverse_transform(fault_pred)[0]

            if fault_type != 'No fault detected' and fault_type not in seen_faults:
                fault_info = next(
                    (v for k, v in FAULT_DICT.items() if v['fault'] == fault_type),
                    {'severity': 0.0, 'occurrence': 0}
                )

                predictions.append({
                    'line': i,
                    'code': line.strip(),
                    'fault': fault_type,
                    'severity': float(fault_info['severity']),
                    'occurrence': int(fault_info['occurrence'])
                })
                seen_faults.add(fault_type)

        # Sort all faults by severity, return the complete list (frontend decides top N)
        predictions.sort(key=lambda x: x['severity'], reverse=True)
        return predictions
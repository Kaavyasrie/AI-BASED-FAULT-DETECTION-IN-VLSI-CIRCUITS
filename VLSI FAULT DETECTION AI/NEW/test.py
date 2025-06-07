import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report

# Load the test dataset
test_data = pd.read_csv('test_data.csv')

# Load the preprocessor (TF-IDF vectorizer) and label encoder
vectorizer = joblib.load('tfidf_vectorizer.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Preprocess the test data
X_test = vectorizer.transform(test_data['code'])

# Target variable: 'fault_type'
y_test = test_data['fault_type']
y_test_encoded = label_encoder.transform(y_test)

# Load the trained model
model = joblib.load('fault_predictor_model.pkl')

# Make predictions on the test set
y_pred_encoded = model.predict(X_test)
y_pred = label_encoder.inverse_transform(y_pred_encoded)

# Evaluate the model
accuracy = accuracy_score(y_test_encoded, y_pred_encoded)
print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))
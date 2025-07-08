from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the selected model (Random Forest, in this case)
model = joblib.load(r'C:\Users\sathv\OneDrive\Desktop\GTDPP\best_random_forest (2).pkl')

# Define the list of features in the correct order
FEATURE_NAMES = [
    'Patient Age', "Genes in mother's side", 'Inherited from father', 'Maternal gene',
    'Paternal gene', 'Status', 'Respiratory Rate (breaths/min)', 'Heart Rate (rates/min',
    'Follow-up', 'Gender', 'Birth asphyxia', 'Autopsy shows birth defect (if applicable)',
     'Folic acid details (peri-conceptional)', 'H/O serious maternal illness',
    'H/O radiation exposure (x-ray)', 'H/O substance abuse', 'Assisted conception IVF/ART',
    'History of anomalies in previous pregnancies', 'No. of previous abortion', 'Birth defects',
    'Blood test result', 'Disorder Subclass', 'Symptom Count', 'Total Blood Cell Count',
    'Combined_disorder'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    form_data = request.form
    input_features = []

    for feature in FEATURE_NAMES:
        value = form_data.get(feature)

        # Handle missing or empty values
        if value is None or value.strip() == "":
            input_features.append(0)  # Default fallback value
            continue

        try:
            # Try converting to float first (use float if even categorical data is encoded numerically)
            input_features.append(float(value))
        except ValueError:
            try:
                input_features.append(int(value))
            except ValueError:
                input_features.append(0)  # Fallback if neither works

    # Make prediction using the model
    prediction = model.predict([input_features])[0]

    # Return results
    if prediction == 0:
        severity = "No Transmission"
    elif prediction == 1:
        severity = "Light transmission"
    elif prediction == 2:
        severity = "Total Transmission"
    else:
        severity = "Unknown"
    return render_template('result.html', prediction=severity, request_form=form_data)



if __name__ == '__main__':
    app.run(debug=True)
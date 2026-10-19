"""Definitions for the three medical tabular datasets.

Each entry describes the input form shown to the user. Only the values the model
actually uses are asked for, so the forms stay short.
"""

TABULAR_TASKS = {
    "heart": {
        "title": "Heart disease",
        "short": "Assess heart disease risk from age, blood pressure, cholesterol and heart tests.",
        "description": "Enter your routine clinical measurements. The model estimates how likely "
                       "heart disease is, based on patterns in the Cleveland heart disease study.",
        "file": "heart.csv",
        "target": "target",
        "positive_label": "heart disease",
        "info_key": "Heart disease",
        "source": "UCI Heart Disease (Cleveland), 303 patients",
        "select_top_k": None,
        "fields": {
            "age": {"label": "Age", "unit": "years", "min": 18, "max": 100, "step": 1, "default": 55},
            "sex": {"label": "Sex", "options": [[1, "Male"], [0, "Female"]], "default": 1},
            "cp": {"label": "Chest pain type", "options": [
                [0, "Typical angina"], [1, "Atypical angina"],
                [2, "Non-anginal pain"], [3, "Asymptomatic"]], "default": 0,
                "help": "The type of chest discomfort you experience, if any."},
            "trestbps": {"label": "Resting blood pressure", "unit": "mm Hg", "min": 80, "max": 220,
                         "step": 1, "default": 130, "help": "Measured while you are at rest."},
            "chol": {"label": "Serum cholesterol", "unit": "mg/dL", "min": 100, "max": 600,
                     "step": 1, "default": 240, "help": "From a blood test."},
            "fbs": {"label": "Fasting blood sugar above 120 mg/dL", "options": [[0, "No"], [1, "Yes"]],
                    "default": 0, "help": "From a fasting blood test."},
            "restecg": {"label": "Resting ECG result", "options": [
                [0, "Normal"], [1, "ST-T wave abnormality"],
                [2, "Left ventricular hypertrophy"]], "default": 0},
            "thalach": {"label": "Maximum heart rate reached", "unit": "bpm", "min": 60, "max": 220,
                        "step": 1, "default": 150, "help": "Highest heart rate during exercise testing."},
            "exang": {"label": "Chest pain brought on by exercise", "options": [[0, "No"], [1, "Yes"]],
                      "default": 0},
            "oldpeak": {"label": "ST depression during exercise", "unit": "mm", "min": 0, "max": 7,
                        "step": 0.1, "default": 1.0, "help": "From the exercise ECG."},
            "slope": {"label": "Slope of peak exercise ST segment", "options": [
                [0, "Upsloping"], [1, "Flat"], [2, "Downsloping"]], "default": 1},
            "ca": {"label": "Major vessels coloured by fluoroscopy", "options": [
                [0, "0"], [1, "1"], [2, "2"], [3, "3"], [4, "4"]], "default": 0,
                "help": "Number of major heart vessels visible on the scan."},
            "thal": {"label": "Thalassaemia test result", "options": [
                [0, "Code 0"], [1, "Code 1"], [2, "Code 2"], [3, "Code 3"]], "default": 2,
                "help": "Result code from the thalassaemia blood test, as recorded in the dataset."},
        },
    },
    "diabetes": {
        "title": "Diabetes",
        "short": "Estimate diabetes risk from glucose, insulin, BMI and family history.",
        "description": "Enter your blood test and body measurements. The model estimates how likely "
                       "type 2 diabetes is, based on the Pima Indians Diabetes study.",
        "file": "diabetes.csv",
        "target": "Outcome",
        "positive_label": "diabetes",
        "info_key": "Diabetes",
        "source": "UCI Pima Indians Diabetes, 768 patients",
        "zero_is_missing": ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"],
        "select_top_k": None,
        "fields": {
            "Pregnancies": {"label": "Number of pregnancies", "min": 0, "max": 20, "step": 1,
                            "default": 1},
            "Glucose": {"label": "Plasma glucose (2-hour test)", "unit": "mg/dL", "min": 40, "max": 300,
                        "step": 1, "default": 120, "help": "From an oral glucose tolerance test."},
            "BloodPressure": {"label": "Diastolic blood pressure", "unit": "mm Hg", "min": 30,
                              "max": 150, "step": 1, "default": 70},
            "SkinThickness": {"label": "Triceps skin fold thickness", "unit": "mm", "min": 5,
                              "max": 100, "step": 1, "default": 20},
            "Insulin": {"label": "2-hour serum insulin", "unit": "µU/mL", "min": 10, "max": 900,
                        "step": 1, "default": 80},
            "BMI": {"label": "Body mass index (BMI)", "unit": "kg/m²", "min": 10, "max": 70,
                    "step": 0.1, "default": 28.0},
            "DiabetesPedigreeFunction": {"label": "Family history score", "min": 0.05, "max": 2.5,
                                         "step": 0.001, "default": 0.45,
                                         "help": "A score reflecting diabetes in close relatives."},
            "Age": {"label": "Age", "unit": "years", "min": 18, "max": 100, "step": 1, "default": 35},
        },
    },
    "breast": {
        "title": "Breast cancer",
        "short": "Assess whether a breast tumour is likely malignant from lab measurements.",
        "description": "Enter measurements from a fine-needle aspiration (FNA) lab report. The model "
                       "estimates how likely the tumour is malignant. Only the 8 most informative "
                       "measurements are requested.",
        "file": "breast_cancer.csv",
        "target": "target",
        "positive_label": "malignant breast tumour",
        "info_key": "Breast cancer",
        "source": "UCI Breast Cancer Wisconsin (Diagnostic), 569 samples",
        "select_top_k": 8,
        "fields": {},   # generated from the data at training time
    },
    "kidney": {
        "title": "Chronic kidney disease",
        "short": "Assess kidney disease risk from urine tests, blood tests and medical history.",
        "description": "Enter your urine and blood test results and your medical history. The model estimates "
                       "how likely chronic kidney disease is, based on the UCI Chronic Kidney Disease study.",
        "file": "kidney.csv",
        "target": "target",
        "positive_label": "chronic kidney disease",
        "info_key": "Chronic kidney disease",
        "source": "UCI Chronic Kidney Disease (Kaggle/UCI copy), 400 patients",
        "select_top_k": None,
        "fields": {
            "age": {"label": "Age", "unit": "years", "min": 2, "max": 90, "step": 1, "default": 50, "group": "Personal and blood pressure", "help": ""},
            "bp": {"label": "Blood pressure (diastolic)", "unit": "mm Hg", "min": 50, "max": 180, "step": 1, "default": 80, "group": "Personal and blood pressure", "help": "The bottom number of your blood pressure reading."},
            "sg": {"label": "Urine specific gravity", "options": [[1.005, "1.005"], [1.01, "1.010"], [1.015, "1.015"], [1.02, "1.020"], [1.025, "1.025"]], "default": 1.02, "group": "Urine tests", "help": "Measures how concentrated the urine is."},
            "al": {"label": "Urine albumin level", "options": [[0, "0 (none)"], [1, "1"], [2, "2"], [3, "3"], [4, "4"], [5, "5 (very high)"]], "default": 0, "group": "Urine tests", "help": "Protein-type leak into the urine. Higher means more albumin."},
            "su": {"label": "Urine sugar level", "options": [[0, "0 (none)"], [1, "1"], [2, "2"], [3, "3"], [4, "4"], [5, "5 (very high)"]], "default": 0, "group": "Urine tests", "help": "Sugar found in the urine."},
            "rbc": {"label": "Red blood cells in urine", "options": [[0, "Normal"], [1, "Abnormal"]], "default": 0, "group": "Urine tests", "help": "From the urine microscopy."},
            "pc": {"label": "Pus cells in urine", "options": [[0, "Normal"], [1, "Abnormal"]], "default": 0, "group": "Urine tests", "help": "From the urine microscopy."},
            "pcc": {"label": "Pus cell clumps in urine", "options": [[0, "Not present"], [1, "Present"]], "default": 0, "group": "Urine tests", "help": "Clusters of pus cells seen under the microscope."},
            "ba": {"label": "Bacteria in urine", "options": [[0, "Not present"], [1, "Present"]], "default": 0, "group": "Urine tests", "help": "Bacteria seen under the microscope."},
            "bgr": {"label": "Random blood glucose", "unit": "mg/dL", "min": 20, "max": 500, "step": 1, "default": 120, "group": "Blood tests", "help": "Blood sugar measured at any time of day."},
            "bu": {"label": "Blood urea", "unit": "mg/dL", "min": 1, "max": 400, "step": 0.5, "default": 35, "group": "Blood tests", "help": "A waste product measured in a blood test."},
            "sc": {"label": "Serum creatinine", "unit": "mg/dL", "min": 0.4, "max": 80, "step": 0.1, "default": 1.2, "group": "Blood tests", "help": "A key kidney function marker from a blood test."},
            "sod": {"label": "Blood sodium", "unit": "mEq/L", "min": 4, "max": 165, "step": 0.5, "default": 137, "group": "Blood tests", "help": ""},
            "pot": {"label": "Blood potassium", "unit": "mEq/L", "min": 2, "max": 50, "step": 0.1, "default": 4.5, "group": "Blood tests", "help": ""},
            "hemo": {"label": "Haemoglobin", "unit": "g/dL", "min": 3, "max": 18, "step": 0.1, "default": 13.0, "group": "Blood tests", "help": "Measured in a full blood count."},
            "pcv": {"label": "Packed cell volume (haematocrit)", "unit": "%", "min": 9, "max": 60, "step": 1, "default": 40, "group": "Blood tests", "help": "Share of blood made of red cells."},
            "wc": {"label": "White blood cell count", "unit": "cells/cumm", "min": 2000, "max": 30000, "step": 100, "default": 8000, "group": "Blood tests", "help": "From a full blood count."},
            "rc": {"label": "Red blood cell count", "unit": "million/cumm", "min": 2, "max": 9, "step": 0.1, "default": 4.8, "group": "Blood tests", "help": "From a full blood count."},
            "htn": {"label": "Hypertension (high blood pressure)", "options": [[0, "No"], [1, "Yes"]], "default": 0, "group": "Medical history and symptoms", "help": "Diagnosed by a doctor."},
            "dm": {"label": "Diabetes mellitus", "options": [[0, "No"], [1, "Yes"]], "default": 0, "group": "Medical history and symptoms", "help": "Diagnosed by a doctor."},
            "cad": {"label": "Coronary artery disease", "options": [[0, "No"], [1, "Yes"]], "default": 0, "group": "Medical history and symptoms", "help": "Diagnosed by a doctor."},
            "ane": {"label": "Anaemia", "options": [[0, "No"], [1, "Yes"]], "default": 0, "group": "Medical history and symptoms", "help": "Diagnosed or measured as low haemoglobin."},
            "pe": {"label": "Swelling in legs (pedal oedema)", "options": [[0, "No"], [1, "Yes"]], "default": 0, "group": "Medical history and symptoms", "help": "Visible swelling of the feet or ankles."},
            "appet": {"label": "Appetite", "options": [[0, "Good"], [1, "Poor"]], "default": 0, "group": "Medical history and symptoms", "help": "Recent appetite."},
        },
    },
    "liver": {
        "title": "Liver disease",
        "short": "Estimate liver disease risk from liver function blood tests.",
        "description": "Enter your liver function blood test results. The model estimates how likely liver disease "
                       "is, based on the Indian Liver Patient Dataset.",
        "file": "liver.csv",
        "target": "target",
        "positive_label": "liver disease",
        "info_key": "Liver disease",
        "source": "UCI ILPD (Indian Liver Patient Dataset), 583 patients",
        "select_top_k": None,
        "fields": {
            "Age": {"label": "Age", "unit": "years", "min": 4, "max": 90, "step": 1, "default": 45, "group": "Personal", "help": ""},
            "Gender": {"label": "Sex", "options": [[1, "Male"], [0, "Female"]], "default": 1, "group": "Personal", "help": ""},
            "TB": {"label": "Total bilirubin", "unit": "mg/dL", "min": 0.4, "max": 75, "step": 0.1, "default": 1.0, "group": "Liver blood tests", "help": "Bilirubin is a yellow pigment the liver clears."},
            "DB": {"label": "Direct bilirubin", "unit": "mg/dL", "min": 0.1, "max": 20, "step": 0.1, "default": 0.2, "group": "Liver blood tests", "help": ""},
            "Alkphos": {"label": "Alkaline phosphatase", "unit": "IU/L", "min": 60, "max": 2200, "step": 1, "default": 200, "group": "Liver blood tests", "help": ""},
            "Sgpt": {"label": "ALT (SGPT)", "unit": "IU/L", "min": 10, "max": 2000, "step": 1, "default": 30, "group": "Liver blood tests", "help": "Alanine aminotransferase, a liver enzyme."},
            "Sgot": {"label": "AST (SGOT)", "unit": "IU/L", "min": 10, "max": 5000, "step": 1, "default": 40, "group": "Liver blood tests", "help": "Aspartate aminotransferase, a liver enzyme."},
            "TP": {"label": "Total protein", "unit": "g/dL", "min": 2.5, "max": 10, "step": 0.1, "default": 6.8, "group": "Liver blood tests", "help": ""},
            "ALB": {"label": "Albumin", "unit": "g/dL", "min": 0.9, "max": 6, "step": 0.1, "default": 3.5, "group": "Liver blood tests", "help": ""},
            "AG_Ratio": {"label": "Albumin and globulin ratio", "unit": "", "min": 0.3, "max": 3, "step": 0.01, "default": 1.0, "group": "Liver blood tests", "help": ""},
        },
    },
}


def friendly_breast_label(column: str) -> str:
    """'worst concave points' -> 'Worst concave points'."""
    text = column.replace("_", " ").strip()
    return text[:1].upper() + text[1:]


def breast_help(column: str) -> str:
    if column.startswith("worst"):
        return "Largest (worst) value measured across the cell nuclei in the sample."
    if column.startswith("mean"):
        return "Average value measured across the cell nuclei in the sample."
    if "error" in column:
        return "Variation (standard error) of the measurement across the sample."
    return "Measurement from the fine-needle aspiration lab report."

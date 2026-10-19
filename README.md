# Disease Prediction

A web application that estimates disease likelihood from symptoms or clinical measurements.
Each check asks only for the information its model needs.

| Check | Input | Data | Best model (selected by CV ROC-AUC) |
|---|---|---|---|
| Symptom checker | Symptoms (min. 3) | 132 symptoms, 41 conditions | SVM |
| Heart disease | 13 clinical measurements | UCI Heart Disease (Cleveland), 303 patients | Logistic Regression |
| Diabetes | 8 blood-test and body measurements | UCI Pima Indians Diabetes, 768 patients | Logistic Regression |
| Breast cancer | 8 lab measurements from a fine-needle aspiration | UCI Breast Cancer Wisconsin, 569 samples | Logistic Regression |
| Kidney disease | 24 urine, blood and history inputs | UCI Chronic Kidney Disease, 400 patients | SVM |
| Liver disease | 10 liver function blood test inputs | UCI ILPD, 583 patients | Random Forest |
| Blood pressure | Systolic and diastolic pressure | ACC/AHA 2017 guideline (rule-based, not trained) | n/a |

Each task trains four algorithms: Support Vector Machine, Logistic Regression, Random Forest and XGBoost.
Models are compared on a held-out test set, and the **Model comparison** page shows every result.

> **Educational use only.** These models are not clinically validated and must not be used for medical decisions.

## Project structure
```text
Disease_Prediction_Project/
├── app.py                    # Flask web app and API routes
├── src/
│   ├── data.py               # symptom data loading and cleaning
│   ├── tabular.py            # input definitions for heart, diabetes and breast cancer
│   ├── train.py              # trains and compares all four algorithms for each task
│   ├── predictor.py          # loads trained models and validates inputs
│   └── disease_info.py       # plain-language information about each condition
├── templates/                # home, symptom checker, disease check, model comparison
├── static/
│   ├── css/style.css
│   └── js/                   # common.js, symptoms.js, disease.js
├── data/                     # datasets (see data/SOURCES.md)
├── models/                   # trained models and metadata (created by training)
├── reports/                  # comparison tables (created by training)
├── notebooks/                # original exploratory notebook
├── tests/test_app.py         # smoke tests
├── requirements.txt
└── README.md
```

## Pages
- **Patient assessment** (home): symptoms, personal details, blood tests and heart tests in one form.
- **Disease checks**: a separate form for each condition (blood pressure, diabetes, heart, kidney, liver, breast cancer, symptom checker).
- **Model comparison**: accuracy and other metrics for every model.
- **About**: datasets, developer and contact details.

Every result shows the disease information: what it is, how it occurs, precautions to take, foods to eat, and foods and habits to avoid.

## Setup and run
1. Extract the ZIP and open the `Disease_Prediction_Project` folder in VS Code or a terminal.
2. (Optional) create a virtual environment:
   - Windows PowerShell: `python -m venv .venv` then `.venv\Scripts\Activate.ps1`
3. Install packages: `python -m pip install -r requirements.txt`
4. (Only if the data folder changed) rebuild the kidney and liver files: `python -m src.prepare_extra`
5. Train all models (about 1 to 2 minutes; the app also trains automatically if models are missing):
   `python -m src.train`
   To train one task only: `python -m src.train heart`
6. Start the app: `python app.py`
7. Open http://127.0.0.1:5000
8. (Optional) run the tests: `python -m pytest -q`

## API
| Method | Route | Body | Returns |
|---|---|---|---|
| POST | `/api/symptoms/predict` | `{"symptoms": ["itching", ...]}` | top 3 conditions with probabilities and information |
| POST | `/api/predict/heart`, `/diabetes`, `/breast` | `{"values": {"age": 55, ...}}` | probability, risk level, explanation and information |

Invalid or missing inputs return HTTP 400 with a list of readable error messages.

## How the risk estimate works
- The model outputs the probability that the condition is present.
- Below 30% is a lower likelihood, 30 to 60% is moderate, and 60% or above is higher.
- Results are estimates from patterns in past study data. They are not a diagnosis.

## Limitations
- The datasets are small, come from specific study populations, and may not represent other people.
- Sensitivity (recall) is shown because missing a true case is often more harmful than a false alarm in screening.
- Breast cancer uses 8 of 30 available measurements, chosen by a random forest on training data only.
- None of the models has been validated in a clinical setting.

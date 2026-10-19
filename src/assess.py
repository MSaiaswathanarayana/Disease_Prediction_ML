"""Combined patient assessment.

One form collects symptoms, personal details, blood test results and heart test results.
Each input is passed to the model that needs it:
  - symptoms            -> symptom checker (41 conditions)
  - heart fields        -> heart disease model (Cleveland data)
  - blood + personal    -> diabetes model (Pima data)
Standard clinical thresholds are applied to blood results to flag values that need attention.
"""
from src.disease_info import get_disease_info
from src.predictor import MIN_SYMPTOMS, get_predictor


def _num(name, label, unit, lo, hi, step, default, help_text=""):
    return {"name": name, "label": label, "unit": unit, "type": "number", "min": lo, "max": hi,
            "step": step, "default": default, "help": help_text}


def _sel(name, label, options, default, help_text=""):
    return {"name": name, "label": label, "unit": "", "type": "select", "options": options,
            "default": default, "help": help_text}


SECTIONS = [
    {
        "id": "personal",
        "title": "Personal details",
        "intro": "Basic information about you.",
        "fields": [
            _num("age", "Age", "years", 18, 100, 1, 45),
            _sel("sex", "Sex", [[1, "Male"], [0, "Female"]], 1),
            _num("pregnancies", "Number of pregnancies", "", 0, 20, 1, 0,
                 "Enter 0 if not applicable."),
        ],
    },
    {
        "id": "blood",
        "title": "Blood test results",
        "intro": "From a routine blood test, a glucose tolerance test and a blood pressure reading.",
        "fields": [
            _num("systolic_bp", "Systolic blood pressure", "mm Hg", 80, 220, 1, 120,
                 "The top number of your blood pressure reading."),
            _num("diastolic_bp", "Diastolic blood pressure", "mm Hg", 30, 150, 1, 80,
                 "The bottom number of your blood pressure reading."),
            _num("cholesterol", "Total cholesterol", "mg/dL", 100, 600, 1, 200,
                 "From a fasting lipid panel."),
            _num("fasting_glucose", "Fasting blood glucose", "mg/dL", 50, 400, 1, 95,
                 "Measured after at least 8 hours without food."),
            _num("glucose_2h", "2-hour glucose (glucose tolerance test)", "mg/dL", 40, 300, 1, 120,
                 "Measured 2 hours after a 75 g glucose drink."),
            _num("insulin_2h", "2-hour serum insulin", "µU/mL", 10, 900, 1, 80,
                 "Measured during the glucose tolerance test."),
            _num("bmi", "Body mass index (BMI)", "kg/m²", 10, 70, 0.1, 26.0,
                 "Weight in kg divided by height in metres squared."),
            _num("skin_thickness", "Triceps skin fold thickness", "mm", 5, 100, 1, 20,
                 "Measured with skin-fold calipers."),
            _num("pedigree", "Family history of diabetes score", "", 0.05, 2.5, 0.001, 0.45,
                 "Diabetes pedigree score based on diabetes in close relatives."),
        ],
    },
    {
        "id": "heart",
        "title": "Heart test results",
        "intro": "From an ECG and an exercise stress test.",
        "fields": [
            _sel("cp", "Chest pain type",
                 [[0, "Typical angina"], [1, "Atypical angina"], [2, "Non-anginal pain"], [3, "Asymptomatic"]],
                 3, "Choose Asymptomatic if you have no chest discomfort."),
            _sel("restecg", "Resting ECG result",
                 [[0, "Normal"], [1, "ST-T wave abnormality"], [2, "Left ventricular hypertrophy"]], 0),
            _num("thalach", "Maximum heart rate during exercise", "bpm", 60, 220, 1, 150),
            _sel("exang", "Chest pain brought on by exercise", [[0, "No"], [1, "Yes"]], 0),
            _num("oldpeak", "ST depression during exercise", "mm", 0, 7, 0.1, 1.0),
            _sel("slope", "Slope of peak exercise ST segment",
                 [[0, "Upsloping"], [1, "Flat"], [2, "Downsloping"]], 1),
            _sel("ca", "Major vessels coloured by fluoroscopy",
                 [[0, "0"], [1, "1"], [2, "2"], [3, "3"], [4, "4"]], 0),
            _sel("thal", "Thalassaemia test result",
                 [[0, "Code 0"], [1, "Code 1"], [2, "Code 2"], [3, "Code 3"]], 2,
                 "Result code from the thalassaemia test, as recorded in the heart dataset."),
        ],
    },
]


def _all_fields():
    for section in SECTIONS:
        yield from section["fields"]


def parse_values(values):
    """Return (clean_numbers, errors). Every field is required and must be in range."""
    clean, errors = {}, []
    for f in _all_fields():
        raw = values.get(f["name"])
        if raw is None or str(raw).strip() == "":
            errors.append(f"{f['label']} is required.")
            continue
        try:
            number = float(raw)
        except (TypeError, ValueError):
            errors.append(f"{f['label']} must be a number.")
            continue
        if f["type"] == "select":
            if number not in [float(o[0]) for o in f["options"]]:
                errors.append(f"{f['label']} has an invalid choice.")
                continue
        elif not (f["min"] <= number <= f["max"]):
            errors.append(f"{f['label']} should be between {f['min']:g} and {f['max']:g}.")
            continue
        clean[f["name"]] = number
    return clean, errors


def _heart_inputs(v):
    return {
        "age": v["age"], "sex": v["sex"], "cp": v["cp"],
        "trestbps": v["systolic_bp"], "chol": v["cholesterol"],
        "fbs": 1 if v["fasting_glucose"] > 120 else 0,
        "restecg": v["restecg"], "thalach": v["thalach"], "exang": v["exang"],
        "oldpeak": v["oldpeak"], "slope": v["slope"], "ca": v["ca"], "thal": v["thal"],
    }


def _diabetes_inputs(v):
    return {
        "Pregnancies": v["pregnancies"], "Glucose": v["glucose_2h"],
        "BloodPressure": v["diastolic_bp"], "SkinThickness": v["skin_thickness"],
        "Insulin": v["insulin_2h"], "BMI": v["bmi"],
        "DiabetesPedigreeFunction": v["pedigree"], "Age": v["age"],
    }


STATUS_LABEL = {"normal": "Normal", "borderline": "Borderline", "high": "High"}


def _flag(test, value, status, message):
    return {"test": test, "value": value, "status": status,
            "label": STATUS_LABEL[status], "message": message}


def blood_flags(v):
    """Flag blood and blood-pressure results against standard clinical thresholds."""
    flags = []

    fg = v["fasting_glucose"]
    if fg >= 126:
        flags.append(_flag("Fasting glucose", f"{fg:g} mg/dL", "high",
                           "In the diabetes range (126 mg/dL or higher)."))
    elif fg >= 100:
        flags.append(_flag("Fasting glucose", f"{fg:g} mg/dL", "borderline",
                           "In the prediabetes range (100 to 125 mg/dL)."))
    else:
        flags.append(_flag("Fasting glucose", f"{fg:g} mg/dL", "normal",
                           "Within the normal range (below 100 mg/dL)."))

    g2 = v["glucose_2h"]
    if g2 >= 200:
        flags.append(_flag("2-hour glucose", f"{g2:g} mg/dL", "high",
                           "In the diabetes range (200 mg/dL or higher)."))
    elif g2 >= 140:
        flags.append(_flag("2-hour glucose", f"{g2:g} mg/dL", "borderline",
                           "In the impaired glucose tolerance range (140 to 199 mg/dL)."))
    else:
        flags.append(_flag("2-hour glucose", f"{g2:g} mg/dL", "normal",
                           "Within the normal range (below 140 mg/dL)."))

    chol = v["cholesterol"]
    if chol >= 240:
        flags.append(_flag("Total cholesterol", f"{chol:g} mg/dL", "high",
                           "High (240 mg/dL or more)."))
    elif chol >= 200:
        flags.append(_flag("Total cholesterol", f"{chol:g} mg/dL", "borderline",
                           "Borderline high (200 to 239 mg/dL)."))
    else:
        flags.append(_flag("Total cholesterol", f"{chol:g} mg/dL", "normal",
                           "Desirable (below 200 mg/dL)."))

    sys_bp, dia_bp = v["systolic_bp"], v["diastolic_bp"]
    bp_value = f"{sys_bp:g}/{dia_bp:g} mm Hg"
    if sys_bp >= 140 or dia_bp >= 90:
        flags.append(_flag("Blood pressure", bp_value, "high",
                           "High (140/90 mm Hg or higher)."))
    elif sys_bp >= 130 or dia_bp >= 80:
        flags.append(_flag("Blood pressure", bp_value, "borderline",
                           "Raised (130/80 mm Hg or higher)."))
    else:
        flags.append(_flag("Blood pressure", bp_value, "normal",
                           "Normal (below 130/80 mm Hg)."))

    bmi = v["bmi"]
    if bmi >= 30:
        flags.append(_flag("Body mass index", f"{bmi:.1f} kg/m²", "high", "In the obesity range (30 or higher)."))
    elif bmi >= 25:
        flags.append(_flag("Body mass index", f"{bmi:.1f} kg/m²", "borderline", "Overweight (25 to 29.9)."))
    elif bmi < 18.5:
        flags.append(_flag("Body mass index", f"{bmi:.1f} kg/m²", "borderline", "Underweight (below 18.5)."))
    else:
        flags.append(_flag("Body mass index", f"{bmi:.1f} kg/m²", "normal", "Healthy range (18.5 to 24.9)."))
    return flags


def overall_summary(heart, diabetes, flags):
    high_flag = any(f["status"] == "high" for f in flags)
    borderline_flag = any(f["status"] == "borderline" for f in flags)
    if heart["risk_level"] == "Higher" or diabetes["risk_level"] == "Higher" or high_flag:
        return {"tone": "high", "title": "Some results need medical attention.",
                "text": "One or more results are in a higher-risk range. Please arrange to see a doctor soon to discuss them."}
    if heart["risk_level"] == "Moderate" or diabetes["risk_level"] == "Moderate" or borderline_flag:
        return {"tone": "moderate", "title": "Some results are borderline.",
                "text": "Discuss these results with your doctor at your next visit. Ask about lifestyle changes or repeat tests."}
    return {"tone": "low", "title": "Results are mostly in the lower-risk range.",
            "text": "Keep up healthy habits and continue routine check-ups. This is still an estimate, not a diagnosis."}


def run_assessment(payload):
    """Return (result, errors). Result is None when the input is incomplete or invalid."""
    symptoms = payload.get("symptoms", [])
    values = payload.get("values", {})
    if not isinstance(symptoms, list) or not isinstance(values, dict):
        return None, ["Please send symptoms as a list and the form values as an object."]

    symptoms = [str(s) for s in symptoms if str(s).strip()]
    errors = []
    symptom_model = get_predictor("symptoms")
    symptom_results, used = symptom_model.predict(symptoms)
    if len(used) < MIN_SYMPTOMS:
        errors.append(f"Please select at least {MIN_SYMPTOMS} symptoms.")

    clean, value_errors = parse_values(values)
    errors.extend(value_errors)
    if errors:
        return None, errors

    heart_result, heart_err = get_predictor("heart").predict(_heart_inputs(clean))
    diabetes_result, diabetes_err = get_predictor("diabetes").predict(_diabetes_inputs(clean))
    if heart_err or diabetes_err:
        return None, heart_err + diabetes_err

    labels = symptom_model.meta["symptom_labels"]
    for item in symptom_results:
        item["info"] = get_disease_info(item["disease"])

    heart_result.update(title="Heart disease", info=get_disease_info("Heart disease"))
    diabetes_result.update(
        title="Diabetes", info=get_disease_info("Diabetes"),
        note=("This estimate comes from a model trained on adult women of Pima Indian heritage. "
              "Treat it with extra caution for other groups.") if clean["sex"] == 0 else
             ("This estimate comes from a model trained on adult women of Pima Indian heritage. "
              "Treat it with extra caution for men.")
    )
    flags = blood_flags(clean)
    return {
        "summary": overall_summary(heart_result, diabetes_result, flags),
        "symptoms": {"results": symptom_results, "symptoms_used": [labels[k] for k in used]},
        "heart": heart_result,
        "diabetes": diabetes_result,
        "flags": flags,
    }, []

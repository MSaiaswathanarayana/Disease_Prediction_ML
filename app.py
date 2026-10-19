"""Disease Prediction web application.

Run:  python app.py   then open http://127.0.0.1:5000
"""
from flask import Flask, abort, jsonify, render_template, request

from src.assess import SECTIONS, run_assessment
from src.bp import classify_bp
from src.disease_info import get_disease_info
from src.predictor import ALL_TASKS, MIN_SYMPTOMS, get_predictor, load_meta
from src.tabular import TABULAR_TASKS as TABULAR_DEFS

app = Flask(__name__)
TABULAR_TASKS = list(TABULAR_DEFS)
DEVELOPER = {"name": "M SAIASWATHANARAYANA", "email": "msaswath2006@gmail.com"}

METRIC_COLUMNS_TABULAR = ["Model", "CV ROC-AUC (train)", "Accuracy", "Sensitivity (recall)",
                          "Specificity", "Precision", "F1-score", "Test ROC-AUC"]
PERCENT_COLUMNS = {"Accuracy", "Sensitivity (recall)", "Specificity", "Precision", "F1-score"}
METRIC_COLUMNS_SYMPTOMS = ["Model", "Accuracy", "Macro Precision", "Macro Recall", "Macro F1-score"]


def _format_row(row, columns):
    """Format metric values for display: percentages for rates, three decimals for AUC."""
    out = {}
    for c in columns:
        v = row.get(c)
        if isinstance(v, float) and (c in PERCENT_COLUMNS or c.startswith("Macro")):
            out[c] = f"{v * 100:.1f}%"
        elif isinstance(v, float) and "AUC" in c:
            out[c] = f"{v:.3f}"
        else:
            out[c] = v
    return out


def dataset_details():
    """Plain-language details of every dataset and model, shown on the About page."""
    s = load_meta("symptoms")
    rows = [{
        "name": "Symptom checker", "source": s["source"],
        "records": f"{s['n_train']:,} training / {s['n_test']} test",
        "detail": f"{len(s['features'])} symptoms, {len(s['classes'])} conditions",
        "model": s["best_model"], "metric": f"Macro F1 {s['best_macro_f1'] * 100:.1f}%",
        "used_in": "Symptom checker and patient assessment",
    }]
    used = {"heart": "Patient assessment and heart check", "diabetes": "Patient assessment and diabetes check",
            "kidney": "Kidney (urine and blood) check", "liver": "Liver check",
            "breast": "Breast cancer check"}
    for key in TABULAR_TASKS:
        m = load_meta(key)
        rows.append({
            "name": m["title"], "source": m["source"],
            "records": f"{m['n_train']} training / {m['n_test']} test",
            "detail": f"{len(m['features'])} inputs, predicts {m['positive_label']}",
            "model": m["best_model"], "metric": f"Test ROC-AUC {m['best_test_auc']:.3f}",
            "used_in": used.get(key, "Disease check"),
        })
    return rows


@app.route("/")
def assess_page():
    symptoms = get_predictor("symptoms").symptoms
    return render_template("assess.html", sections=SECTIONS, symptoms=symptoms, min_symptoms=MIN_SYMPTOMS)


@app.post("/api/assess")
def api_assess():
    payload = request.get_json(silent=True) or {}
    result, errors = run_assessment(payload)
    if errors:
        return jsonify(error=" ".join(errors), errors=errors), 400
    return jsonify(result)


@app.route("/about")
def about_page():
    return render_template("about.html", datasets=dataset_details(), developer=DEVELOPER)


@app.route("/checks")
def checks_page():
    cards = [
        {"title": "Blood pressure", "href": "/bp", "inputs": "3 inputs",
         "short": "Classify a blood pressure reading and see what it means, with next steps."},
        {"title": "Diabetes", "href": "/predict/diabetes", "inputs": f"{len(TABULAR_DEFS['diabetes']['fields'])} inputs",
         "short": "Estimate diabetes risk from glucose, insulin, BMI and family history."},
        {"title": "Heart disease", "href": "/predict/heart", "inputs": f"{len(TABULAR_DEFS['heart']['fields'])} inputs",
         "short": "Estimate heart disease risk from ECG, exercise and blood test results."},
        {"title": "Kidney disease (urine test)", "href": "/predict/kidney", "inputs": f"{len(TABULAR_DEFS['kidney']['fields'])} inputs",
         "short": "Estimate chronic kidney disease risk from urine tests, blood tests and history."},
        {"title": "Liver disease", "href": "/predict/liver", "inputs": f"{len(TABULAR_DEFS['liver']['fields'])} inputs",
         "short": "Estimate liver disease risk from liver function blood tests."},
        {"title": "Breast cancer", "href": "/predict/breast", "inputs": f"{len(TABULAR_DEFS['breast']['fields']) or 8} inputs",
         "short": "Estimate whether a breast tumour is likely malignant from lab measurements."},
        {"title": "Symptom checker", "href": "/symptoms", "inputs": "Symptoms (min. 3)",
         "short": "Choose your symptoms to see the conditions they most closely resemble."},
    ]
    return render_template("checks.html", cards=cards)


@app.route("/bp")
def bp_page():
    return render_template("bp.html")


@app.post("/api/bp")
def api_bp():
    payload = request.get_json(silent=True) or {}
    try:
        sys_bp = float(payload.get("systolic"))
        dia_bp = float(payload.get("diastolic"))
    except (TypeError, ValueError):
        return jsonify(error="Please enter both blood pressure numbers."), 400
    errors = []
    if not (70 <= sys_bp <= 260):
        errors.append("Systolic pressure should be between 70 and 260 mm Hg.")
    if not (40 <= dia_bp <= 160):
        errors.append("Diastolic pressure should be between 40 and 160 mm Hg.")
    if sys_bp <= dia_bp:
        errors.append("Systolic pressure should be higher than diastolic pressure.")
    if errors:
        return jsonify(error=" ".join(errors), errors=errors), 400
    result, _ = classify_bp(sys_bp, dia_bp, bool(payload.get("on_medication")))
    result["systolic"], result["diastolic"] = sys_bp, dia_bp
    return jsonify(result)


@app.route("/symptoms")
def symptoms_page():
    predictor = get_predictor("symptoms")
    return render_template("symptoms.html", symptoms=predictor.symptoms, min_symptoms=MIN_SYMPTOMS)


@app.route("/predict/<key>")
def predict_page(key):
    if key not in TABULAR_TASKS:
        abort(404)
    meta = load_meta(key)
    spec = {
        "key": key,
        "title": meta["title"],
        "description": meta["description"],
        "positive_label": meta["positive_label"],
        "features": meta["features"],
        "best_model": meta["best_model"],
        "accuracy": round(meta["best_accuracy"] * 100, 1),
    }
    return render_template("disease.html", spec=spec)


@app.route("/models")
def models_page():
    tasks = []
    for key in ALL_TASKS:
        meta = load_meta(key)
        if key == "symptoms":
            columns = METRIC_COLUMNS_SYMPTOMS
            n = None
        else:
            columns = METRIC_COLUMNS_TABULAR
            n = meta["n_samples"]
        rows = [_format_row(r, columns) for r in meta["metrics"]]
        tasks.append({"title": meta.get("title", "Symptom checker"), "source": meta["source"],
                      "n_samples": n, "best_model": meta["best_model"], "columns": columns,
                      "rows": rows})
    return render_template("models.html", tasks=tasks)


@app.post("/api/symptoms/predict")
def predict_symptoms():
    payload = request.get_json(silent=True) or {}
    selected = payload.get("symptoms", [])
    if not isinstance(selected, list):
        return jsonify(error="Please send the symptoms as a list."), 400

    predictor = get_predictor("symptoms")
    results, used = predictor.predict([str(s) for s in selected])
    if len(used) < MIN_SYMPTOMS:
        return jsonify(error=f"Please select at least {MIN_SYMPTOMS} symptoms."), 400

    for item in results:
        item["info"] = get_disease_info(item["disease"])
    labels = {f: predictor.meta["symptom_labels"][f] for f in used}
    return jsonify(results=results, symptoms_used=[labels[k] for k in used])


@app.post("/api/predict/<key>")
def predict_tabular(key):
    if key not in TABULAR_TASKS:
        return jsonify(error="Unknown prediction type."), 404
    payload = request.get_json(silent=True) or {}
    values = payload.get("values", {})
    if not isinstance(values, dict):
        return jsonify(error="Please send the values as an object."), 400

    predictor = get_predictor(key)
    result, errors = predictor.predict(values)
    if errors:
        return jsonify(error=" ".join(errors), errors=errors), 400
    result["info"] = get_disease_info(predictor.meta["info_key"])
    return jsonify(result)


if __name__ == "__main__":
    for key in ALL_TASKS:
        load_meta(key)  # trains any missing models before the server starts
    app.run(debug=False, host="127.0.0.1", port=5000)

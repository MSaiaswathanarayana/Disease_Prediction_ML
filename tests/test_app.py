"""Smoke tests. Run from the project root:  python -m pytest -q"""
import pytest

from app import app

FULL_VALUES = {
    "age": 63, "sex": 1, "pregnancies": 0,
    "systolic_bp": 145, "diastolic_bp": 72, "cholesterol": 233, "fasting_glucose": 130,
    "glucose_2h": 150, "insulin_2h": 80, "bmi": 33.6, "skin_thickness": 35, "pedigree": 0.627,
    "cp": 3, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1,
}
SYMPTOMS = ["itching", "skin_rash", "nodal_skin_eruptions"]


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_pages_load(client):
    for path in ["/", "/checks", "/bp", "/symptoms", "/predict/breast", "/predict/kidney", "/predict/liver", "/models", "/about"]:
        assert client.get(path).status_code == 200, path


def test_about_page_has_developer_and_email(client):
    html = client.get("/about").get_data(as_text=True)
    assert "M SAIASWATHANARAYANA" in html
    assert "msaswath2006@gmail.com" in html


def test_unknown_task_is_404(client):
    assert client.get("/predict/unknown").status_code == 404


def test_assessment_full_case(client):
    r = client.post("/api/assess", json={"symptoms": SYMPTOMS, "values": FULL_VALUES})
    body = r.get_json()
    assert r.status_code == 200
    assert body["symptoms"]["results"][0]["disease"] == "Fungal infection"
    assert 0 <= body["heart"]["probability"] <= 100
    assert 0 <= body["diabetes"]["probability"] <= 100
    assert body["summary"]["tone"] in {"low", "moderate", "high"}
    flag_tests = {f["test"] for f in body["flags"]}
    assert {"Fasting glucose", "Blood pressure", "Total cholesterol"} <= flag_tests


def test_assessment_needs_three_symptoms(client):
    r = client.post("/api/assess", json={"symptoms": SYMPTOMS[:2], "values": FULL_VALUES})
    assert r.status_code == 400
    assert "at least 3 symptoms" in r.get_json()["error"]


def test_assessment_missing_field_reported(client):
    values = dict(FULL_VALUES)
    del values["cholesterol"]
    r = client.post("/api/assess", json={"symptoms": SYMPTOMS, "values": values})
    assert r.status_code == 400
    assert any("Total cholesterol is required" in e for e in r.get_json()["errors"])


def test_assessment_out_of_range_rejected(client):
    values = dict(FULL_VALUES, fasting_glucose=9999)
    r = client.post("/api/assess", json={"symptoms": SYMPTOMS, "values": values})
    assert r.status_code == 400


def test_symptom_api_still_works(client):
    r = client.post("/api/symptoms/predict", json={"symptoms": SYMPTOMS})
    assert r.get_json()["results"][0]["disease"] == "Fungal infection"


def test_breast_api_validates_missing(client):
    r = client.post("/api/predict/breast", json={"values": {}})
    assert r.status_code == 400


KIDNEY_DEFAULTS = {}


def test_kidney_and_liver_predict_with_defaults(client):
    from src.predictor import get_predictor
    for key in ["kidney", "liver"]:
        predictor = get_predictor(key)
        values = {f["name"]: f["default"] for f in predictor.meta["features"]}
        r = client.post(f"/api/predict/{key}", json={"values": values})
        assert r.status_code == 200, key
        body = r.get_json()
        assert 0 <= body["probability"] <= 100
        assert body["info"]["precautions"]


def test_bp_classification(client):
    cases = {(118, 76): "Normal", (125, 78): "Elevated", (135, 85): "Stage 1 hypertension",
             (150, 95): "Stage 2 hypertension", (190, 125): "Hypertensive crisis"}
    for (sys_bp, dia_bp), expected in cases.items():
        r = client.post("/api/bp", json={"systolic": sys_bp, "diastolic": dia_bp})
        assert r.get_json()["category"] == expected, (sys_bp, dia_bp)


def test_bp_rejects_inverted_numbers(client):
    r = client.post("/api/bp", json={"systolic": 80, "diastolic": 90})
    assert r.status_code == 400


def test_every_predictable_condition_has_information():
    import json
    from src.data import MODEL_DIR
    from src.disease_info import DEFAULT_INFO, get_disease_info
    from src.tabular import TABULAR_TASKS
    symptom_classes = json.loads((MODEL_DIR / "symptoms_meta.json").read_text())["classes"]
    names = set(symptom_classes) | {v["info_key"] for v in TABULAR_TASKS.values()}
    for name in names:
        info = get_disease_info(name)
        assert info is not DEFAULT_INFO, name
        for key in ["about", "how_it_occurs", "precautions", "diet_follow", "diet_avoid"]:
            assert info[key], (name, key)

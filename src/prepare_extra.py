"""Convert the raw kidney (CKD) and liver (ILPD) files into numeric CSVs used by the app.

Run once from the project root:  python -m src.prepare_extra
Raw files are kept in data/raw/ so the conversion can be checked.
"""
import numpy as np
import pandas as pd

from src.data import DATA_DIR

BINARY_TEXT = {
    "rbc": {"normal": 0, "abnormal": 1}, "pc": {"normal": 0, "abnormal": 1},
    "pcc": {"notpresent": 0, "present": 1}, "ba": {"notpresent": 0, "present": 1},
    "htn": {"no": 0, "yes": 1}, "dm": {"no": 0, "yes": 1}, "cad": {"no": 0, "yes": 1},
    "pe": {"no": 0, "yes": 1}, "ane": {"no": 0, "yes": 1}, "appet": {"good": 0, "poor": 1},
}
NUMERIC_COLS = ["age", "bp", "sg", "al", "su", "bgr", "bu", "sc", "sod", "pot",
                "hemo", "pcv", "wc", "rc"]


def prepare_kidney():
    raw = pd.read_csv(DATA_DIR / "raw" / "kidney_disease_raw.csv")
    df = raw.drop(columns=["id"])
    df = df.apply(lambda s: s.map(lambda v: v.strip() if isinstance(v, str) else v))
    df = df.replace("?", np.nan)
    for col in NUMERIC_COLS + ["pcv", "wc", "rc"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col, mapping in BINARY_TEXT.items():
        df[col] = df[col].map(mapping)
    df["target"] = df["classification"].map({"ckd": 1, "notckd": 0})
    df = df.drop(columns=["classification"])
    out = DATA_DIR / "kidney.csv"
    df.to_csv(out, index=False)
    print(f"kidney.csv: {df.shape}, positive (CKD) = {int(df['target'].sum())}, "
          f"missing values = {int(df.isna().sum().sum())}")
    return out


def prepare_liver():
    raw = pd.read_csv(DATA_DIR / "raw" / "ilpd_liver_raw.csv")
    raw.columns = ["Age", "Gender", "TB", "DB", "Alkphos", "Sgpt", "Sgot", "TP", "ALB",
                   "AG_Ratio", "Selector"]
    df = pd.DataFrame({
        "Age": raw["Age"],
        "Gender": raw["Gender"].map({"Male": 1, "Female": 0}),
        "TB": raw["TB"], "DB": raw["DB"], "Alkphos": raw["Alkphos"],
        "Sgpt": raw["Sgpt"], "Sgot": raw["Sgot"], "TP": raw["TP"], "ALB": raw["ALB"],
        "AG_Ratio": raw["AG_Ratio"],
        "target": raw["Selector"].map({"A": 1, "B": 0}),   # A = liver disease, B = no liver disease
    })
    out = DATA_DIR / "liver.csv"
    df.to_csv(out, index=False)
    print(f"liver.csv: {df.shape}, positive (liver disease) = {int(df['target'].sum())}, "
          f"missing values = {int(df.isna().sum().sum())}")
    return out


if __name__ == "__main__":
    prepare_kidney()
    prepare_liver()

"""Blood pressure category check based on the ACC/AHA 2017 guideline.

This is a rule-based check, not a trained model. It classifies a reading and explains what it means.
"""
from src.disease_info import get_disease_info


def classify_bp(systolic: float, diastolic: float, on_medication: bool = False):
    if systolic > 180 or diastolic > 120:
        category, level = "Hypertensive crisis", "Higher"
        meaning = ("This reading is very high. If you have chest pain, breathlessness, weakness, confusion, "
                   "vision changes or severe headache, call emergency services now.")
        steps = ["Seek medical care the same day, even if you feel well.",
                 "Do not stop or change prescribed medicines without advice.",
                 "Rest quietly and recheck after 5 minutes seated, if you can."]
    elif systolic >= 140 or diastolic >= 90:
        category, level = "Stage 2 hypertension", "Higher"
        meaning = "Blood pressure is high at this reading (140/90 mm Hg or above)."
        steps = ["See a doctor soon to confirm the reading and discuss treatment.",
                 "Take prescribed medicines every day.",
                 "Cut down salt, lose excess weight and be more active."]
    elif systolic >= 130 or diastolic >= 80:
        category, level = "Stage 1 hypertension", "Moderate"
        meaning = "Blood pressure is raised (130/80 mm Hg or above)."
        steps = ["Recheck your blood pressure over several days and discuss it with your doctor.",
                 "Reduce salt and processed foods, and aim for 150 minutes of activity a week.",
                 "Limit alcohol and stop smoking."]
    elif systolic >= 120:
        category, level = "Elevated", "Moderate"
        meaning = "Blood pressure is slightly raised (120 to 129 systolic, below 80 diastolic)."
        steps = ["Lifestyle changes can often bring this down.",
                 "Keep active, eat more vegetables and reduce salt.",
                 "Recheck at your next routine check-up."]
    else:
        category, level = "Normal", "Lower"
        meaning = "Blood pressure is in the normal range (below 120/80 mm Hg)."
        steps = ["Keep up healthy habits and check your blood pressure periodically.",
                 "Continue regular physical activity and a balanced diet."]

    notes = []
    if on_medication and level != "Lower":
        notes.append("You already take blood pressure medicine. Discuss with your doctor whether your "
                     "current treatment is working, rather than changing it yourself.")
    return {
        "category": category,
        "risk_level": level,
        "meaning": meaning,
        "steps": steps,
        "notes": notes,
        "info": get_disease_info("Hypertension"),
    }, None

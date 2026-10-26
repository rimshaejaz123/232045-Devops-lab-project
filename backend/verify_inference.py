"""Independent check: load the bundle and predict the sample row (no Flask involved)."""
import json
from pathlib import Path

import joblib
import pandas as pd

here = Path(__file__).parent
bundle = joblib.load(here / "models" / "model_bundle.joblib")
payload = json.loads((here / "test_payload.json").read_text())
X = pd.DataFrame([payload], columns=bundle["numeric_features"] + bundle["categorical_features"])
pred = bundle["pipeline"].predict(X)[0]
print("Prediction:", bundle["classes"][int(pred)])

import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

DEFAULT_MODEL = Path(__file__).parent / "models" / "model_bundle.joblib"


def create_app(model_path=None):
    app = Flask(__name__)
    CORS(app)
    path = Path(model_path or os.environ.get("MODEL_PATH", DEFAULT_MODEL))
    bundle = joblib.load(path) if path.exists() else None

    @app.get("/health")
    def health():
        return jsonify(status="ok", model_loaded=bundle is not None)

    @app.post("/predict")
    def predict():
        if bundle is None:
            return jsonify(error="Model bundle not found. Run backend/train_model.py first."), 503
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="Body must be a JSON object."), 400

        num, cat = bundle["numeric_features"], bundle["categorical_features"]
        expected = num + cat
        missing = [k for k in expected if k not in data]
        unknown = [k for k in data if k not in expected]
        if missing or unknown:
            return jsonify(error="Payload keys do not match the expected features.",
                           missing=missing, unexpected=unknown), 400

        row = {}
        for k in num:
            try:
                row[k] = float(data[k])
            except (TypeError, ValueError):
                return jsonify(error=f"'{k}' must be a number."), 400
        for k in cat:
            row[k] = str(data[k])

        X = pd.DataFrame([row], columns=expected)
        probs = bundle["pipeline"].predict_proba(X)[0]
        best = int(probs.argmax())
        return jsonify(
            prediction=bundle["classes"][best],
            confidence=round(float(probs[best]), 4),
            probabilities={c: round(float(p), 4) for c, p in zip(bundle["classes"], probs)},
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

# Network Attack Classifier - ML Full-Stack CI/CD Lab
UNSW-NB15 MLP model -> Flask API (`backend/`) -> Angular UI (`frontend/`) -> GitHub Pages via GitHub Actions.

## Run locally
```bash
python -m venv .venv && .venv\Scripts\activate        # Windows (Mac/Linux: source .venv/bin/activate)
pip install -r backend/requirements.txt
python backend/train_model.py       # creates model_bundle.joblib, sample_inputs.csv, test_payload.json
python backend/verify_inference.py
python backend/app.py               # terminal 1 -> http://127.0.0.1:5000/health

cd frontend && npm install && npm start   # terminal 2 -> http://localhost:4200
```

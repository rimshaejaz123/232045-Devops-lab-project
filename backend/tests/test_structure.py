from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    ".gitignore",
    ".github/workflows/pages.yml",
    "backend/app.py",
    "backend/train_model.py",
    "backend/requirements.txt",
    "backend/models/model_bundle.joblib",
    "backend/test_payload.json",
    "data/sample_inputs.csv",
    "frontend/package.json",
    "frontend/proxy.conf.json",
    "frontend/src/app/app.component.ts",
]


def test_required_files_exist():
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    assert not missing, f"Missing files: {missing}"

"""Train the UNSW-NB15 MLP exactly like Devops_lab.ipynb (23 numeric + 3 categorical)
and export everything needed for inference into backend/models/model_bundle.joblib."""
import json
from pathlib import Path

import joblib
from datasets import load_dataset
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT / "backend" / "models" / "model_bundle.joblib"

# 23 features chosen by IG + RF + RFE in the notebook
NUMERIC = [
    "Dintpkt", "Sintpkt", "Sjit", "ackdat", "ct_dst_sport_ltm", "ct_dst_src_ltm",
    "ct_src_dport_ltm", "ct_srv_dst", "ct_srv_src", "ct_state_ttl", "dbytes", "djit",
    "dload", "dloss", "dmeansz", "dur", "rate", "sbytes", "sload", "smeansz",
    "sttl", "synack", "tcprtt",
]
CATEGORICAL = ["proto", "service", "state"]
EXCLUDED = ["Analysis", "Backdoor", "Shellcode", "Worms"]  # dropped as in the paper


def build_pipeline() -> Pipeline:
    pre = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")),
                          ("scaler", StandardScaler())]), NUMERIC),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                          ("encoder", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL),
    ])
    mlp = MLPClassifier(hidden_layer_sizes=(128, 128), activation="relu", solver="adam",
                        learning_rate_init=0.0003, batch_size=64, max_iter=300,
                        early_stopping=True, validation_fraction=0.1,
                        n_iter_no_change=30, random_state=42)
    return Pipeline([("preprocessing", pre), ("model", mlp)])


def make_bundle(pipe: Pipeline, classes, metrics=None) -> dict:
    cats = pipe.named_steps["preprocessing"].named_transformers_["cat"] \
               .named_steps["encoder"].categories_
    return {
        "pipeline": pipe,
        "classes": [str(c) for c in classes],
        "numeric_features": NUMERIC,
        "categorical_features": CATEGORICAL,
        "categories": {c: [str(v) for v in cs] for c, cs in zip(CATEGORICAL, cats)},
        "metrics": metrics or {},
    }


def main():
    ds = load_dataset("lacg030175/UNSW-NB15", "temporal")
    train = ds["train"].to_pandas().drop_duplicates()
    test = ds["test"].to_pandas()
    train = train[~train["attack_cat"].isin(EXCLUDED)]
    test = test[~test["attack_cat"].isin(EXCLUDED)]

    feats = NUMERIC + CATEGORICAL
    le = LabelEncoder()
    y_train = le.fit_transform(train["attack_cat"])
    y_test = le.transform(test["attack_cat"])

    pipe = build_pipeline()
    print("Training MLP ...")
    pipe.fit(train[feats], y_train)

    pred = pipe.predict(test[feats])
    metrics = {"accuracy": round(accuracy_score(y_test, pred), 4),
               "weighted_f1": round(f1_score(y_test, pred, average="weighted"), 4),
               "macro_f1": round(f1_score(y_test, pred, average="macro"), 4)}
    print("Metrics:", metrics)

    BUNDLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(make_bundle(pipe, le.classes_, metrics), BUNDLE_PATH)
    print("Saved", BUNDLE_PATH)

    sample = test[feats].iloc[[0]]
    (ROOT / "data").mkdir(exist_ok=True)
    sample.to_csv(ROOT / "data" / "sample_inputs.csv", index=False)
    (ROOT / "backend" / "test_payload.json").write_text(
        json.dumps(json.loads(sample.iloc[0].to_json()), indent=2))
    print("Wrote data/sample_inputs.csv and backend/test_payload.json")


if __name__ == "__main__":
    main()

import os
import json
import joblib
import numpy as np
import pandas as pd

def load_pipeline(model_dir="model"):
    # load model
    model_path = os.path.join(model_dir, "model.pkl")
    feat_path = os.path.join(model_dir, "feature_order.json")
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    model = None
    scaler = None
    feat = None
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
        except Exception:
            model = None
    if os.path.exists(scaler_path):
        try:
            scaler = joblib.load(scaler_path)
        except Exception:
            scaler = None
    if os.path.exists(feat_path):
        with open(feat_path, "r") as f:
            feat = json.load(f).get("features", [])
    return {"model": model, "scaler": scaler, "features": feat}

def predict_from_dict(pipeline, data: dict):
    features = pipeline.get("features") or list(data.keys())
    row = []
    for f in features:
        v = data.get(f)
        # simple casting
        try:
            row.append(float(v) if v not in [None, ""] else np.nan)
        except Exception:
            row.append(np.nan)
    X = pd.DataFrame([row], columns=features)
    if pipeline.get("scaler") is not None:
        X = pd.DataFrame(pipeline["scaler"].transform(X), columns=features)
    model = pipeline.get("model")
    if model is None:
        raise RuntimeError("Model not found in model/ directory.")
    proba = None
    try:
        proba = model.predict_proba(X)[0, 1]
    except Exception:
        proba = float(model.predict(X)[0])
    pred = int(proba >= 0.5) if proba is not None else None
    return {"prediction": pred, "probability": float(proba) if proba is not None else None, "features": features}

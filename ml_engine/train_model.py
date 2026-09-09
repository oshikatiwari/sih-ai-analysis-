import os
import joblib
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_squared_error, r2_score, classification_report, accuracy_score

def train_and_export_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "dataset", "kaggle_dementia_cognitive_game_telemetry.csv")
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    print(f"[*] Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)

    # Feature Engineering
    df["accuracy_speed_ratio"] = df["accuracy"] / (df["response_time_ms"] / 1000.0)
    df["error_rate"] = df["errors"] / (df["attempts"] + 1e-5)
    df["cognitive_efficiency_idx"] = df["completion_rate"] * df["accuracy"]

    # Categorical Encodings
    game_type_le = LabelEncoder()
    df["game_type_encoded"] = game_type_le.fit_transform(df["game_type"])

    lang_le = LabelEncoder()
    df["language_encoded"] = lang_le.fit_transform(df["preferred_language"])

    difficulty_map = {"easy": 0, "medium": 1, "hard": 2}
    df["difficulty_target"] = df["next_adaptive_difficulty"].map(difficulty_map)

    # Feature Columns
    feature_cols = [
        "age",
        "education_level",
        "language_encoded",
        "mmse_score",
        "gds_score",
        "game_type_encoded",
        "accuracy",
        "response_time_ms",
        "attempts",
        "errors",
        "hints_used",
        "completion_rate",
        "accuracy_speed_ratio",
        "error_rate",
        "cognitive_efficiency_idx"
    ]

    X = df[feature_cols]
    y_cps = df["cps_score"]
    y_diff = df["difficulty_target"]
    y_impairment = df["cognitive_impairment_status"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_cps_train, y_cps_test, y_diff_train, y_diff_test, y_imp_train, y_imp_test = train_test_split(
        X_scaled, y_cps, y_diff, y_impairment, test_size=0.2, random_state=42
    )

    print("\n--- 1. Training CPS (Cognitive Performance Score) Regressor ---")
    cps_model = XGBRegressor(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
    cps_model.fit(X_train, y_cps_train)

    y_cps_pred = cps_model.predict(X_test)
    r2 = r2_score(y_cps_test, y_cps_pred)
    mse = mean_squared_error(y_cps_test, y_cps_pred)
    print(f"[+] CPS Model R2 Score: {r2:.4f}")
    print(f"[+] CPS Model MSE: {mse:.4f}")

    print("\n--- 2. Training Hidden Adaptive Difficulty Classifier ---")
    diff_model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42
    )
    diff_model.fit(X_train, y_diff_train)

    y_diff_pred = diff_model.predict(X_test)
    acc = accuracy_score(y_diff_test, y_diff_pred)
    print(f"[+] Hidden Adaptive Difficulty Model Accuracy: {acc * 100:.2f}%")
    print(classification_report(y_diff_test, y_diff_pred, target_names=["Easy", "Medium", "Hard"]))

    print("\n--- 3. Training Clinical Cognitive Impairment Classifier ---")
    imp_model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42
    )
    imp_model.fit(X_train, y_imp_train)
    y_imp_pred = imp_model.predict(X_test)
    imp_acc = accuracy_score(y_imp_test, y_imp_pred)
    print(f"[+] Impairment Classifier Accuracy: {imp_acc * 100:.2f}%")

    # Save artifacts
    joblib.dump(cps_model, os.path.join(models_dir, "cps_regressor.pkl"))
    joblib.dump(diff_model, os.path.join(models_dir, "difficulty_classifier.pkl"))
    joblib.dump(imp_model, os.path.join(models_dir, "impairment_classifier.pkl"))
    joblib.dump(scaler, os.path.join(models_dir, "scaler.pkl"))
    joblib.dump(game_type_le, os.path.join(models_dir, "game_type_encoder.pkl"))
    joblib.dump(lang_le, os.path.join(models_dir, "language_encoder.pkl"))

    meta_info = {
        "model_version": "2.0.0",
        "sih_problem_statement": "SIH26003",
        "supported_languages": ["Hindi", "English", "Mizo", "Khasi", "Assamese"],
        "feature_cols": feature_cols,
        "difficulty_mapping": {"0": "easy", "1": "medium", "2": "hard"},
        "cps_r2_score": round(float(r2), 4),
        "difficulty_accuracy": round(float(acc), 4),
        "impairment_accuracy": round(float(imp_acc), 4),
        "scaler_means": scaler.mean_.tolist(),
        "scaler_scales": scaler.scale_.tolist()
    }

    with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
        json.dump(meta_info, f, indent=4)

    print(f"\n[+] All ML models successfully trained & saved to {models_dir}")

if __name__ == "__main__":
    train_and_export_models()

import os
import joblib
import json
import numpy as np
import pandas as pd

class CPSAnalyzer:
    def __init__(self, models_dir=None):
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        
        self.models_dir = models_dir
        self.cps_model = joblib.load(os.path.join(models_dir, "cps_regressor.pkl"))
        self.diff_model = joblib.load(os.path.join(models_dir, "difficulty_classifier.pkl"))
        self.imp_model = joblib.load(os.path.join(models_dir, "impairment_classifier.pkl"))
        self.scaler = joblib.load(os.path.join(models_dir, "scaler.pkl"))
        self.game_type_le = joblib.load(os.path.join(models_dir, "game_type_encoder.pkl"))

        with open(os.path.join(models_dir, "model_metadata.json"), "r") as f:
            self.metadata = json.load(f)

    def analyze_session(self, telemetry: dict) -> dict:
        """
        Processes game session telemetry and returns:
          - cps_score (0 - 100)
          - next_adaptive_difficulty (HIDDEN from patient: 'easy', 'medium', 'hard')
          - cognitive_risk_level
          - patient_ui_feedback (warm, regional encouragement without difficulty labels)
          - caregiver_dashboard_metrics
        """
        age = telemetry.get("age", 70)
        education_level = telemetry.get("education_level", 2)
        mmse_score = telemetry.get("mmse_score", 22.0)
        gds_score = telemetry.get("gds_score", 4.0)
        game_type = telemetry.get("game_type", "memory_matching")
        accuracy = float(telemetry.get("accuracy", 0.75))
        response_time_ms = int(telemetry.get("response_time_ms", 45000))
        attempts = int(telemetry.get("attempts", 12))
        errors = int(telemetry.get("errors", 3))
        hints_used = int(telemetry.get("hints_used", 1))
        completion_rate = float(telemetry.get("completion_rate", 0.90))

        # Encode categorical & derived features
        try:
            game_type_enc = int(self.game_type_le.transform([game_type])[0])
        except Exception:
            game_type_enc = 0

        accuracy_speed_ratio = accuracy / (response_time_ms / 1000.0)
        error_rate = errors / (attempts + 1e-5)
        cognitive_efficiency_idx = completion_rate * accuracy

        features = [
            age,
            education_level,
            mmse_score,
            gds_score,
            game_type_enc,
            accuracy,
            response_time_ms,
            attempts,
            errors,
            hints_used,
            completion_rate,
            accuracy_speed_ratio,
            error_rate,
            cognitive_efficiency_idx
        ]

        # Scale features
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features_array)

        # AI Model Inference
        predicted_cps = float(self.cps_model.predict(features_scaled)[0])
        predicted_cps = round(np.clip(predicted_cps, 0.0, 100.0), 2)

        predicted_diff_idx = int(self.diff_model.predict(features_scaled)[0])
        diff_map = {0: "easy", 1: "medium", 2: "hard"}
        next_difficulty = diff_map.get(predicted_diff_idx, "easy")

        imp_pred = int(self.imp_model.predict(features_scaled)[0])
        imp_label = "High Risk / Impaired" if imp_pred == 1 else "Normal / Stable"

        # Fatigue & Reaction Stability Metrics for Caregiver
        avg_reaction_per_attempt_ms = round(response_time_ms / max(attempts, 1), 2)
        fatigue_index = round(np.clip((response_time_ms / 60000.0) * (hints_used + 1) * (errors + 1) / 10.0, 0.0, 1.0), 2)

        # Warm Regional Patient UI Feedback (NO Easy/Medium/Hard exposed)
        patient_messages = {
            "easy": {
                "english": "Wonderful effort! You are doing great. Let's enjoy another fun memory activity!",
                "assamese": "অতি সুন্দৰ! আপুনি বহুত ভাল খেলিছে। বলক আন এটি ধুনীয়া স্মৃতি খেল খেলো।",
                "bengali": "দারুণ চেষ্টা! আপনি খুব সুন্দর খেলছেন। চলুন পরবর্তী স্মৃতির খেলা শুরু করি।",
                "manipuri": "য়াম্না ফবা হোৎনবনি! অদোম অসি লাইনা শানবা ঙম্লি।"
            },
            "medium": {
                "english": "Fantastic progress! Your focus is super sharp today. Let's keep exploring!",
                "assamese": "চমৎকার উন্নতি! আপোনাৰ মনোযোগ সঁচাকৈয়ে প্রশংসনীয়।",
                "bengali": "চমৎকার উন্নতি! আপনার মনোযোগ খুব চমৎকার। চলুন এগিয়ে যাই।",
                "manipuri": "মরাং কায়না চাওখৎলে! অদোমগী সীনবা ঙম্বদু য়াম্না ফই।"
            },
            "hard": {
                "english": "Outperforming excellence! You are a master memory explorer today!",
                "assamese": "অসাধাৰণ দক্ষতা! আপুনি আজি সঁচাকৈয়ে এজন মহান স্মৃতি বিজয়ী!",
                "bengali": "অসাধারণ দক্ষতা! আজ আপনি স্মৃতির একজন মহাবীর!",
                "manipuri": "য়াম্না অথোইবা ঙম্বনি! অদোম অসি য়াম্না ফবা শানবা মীওইনি।"
            }
        }

        return {
            "cps_score": predicted_cps,
            "hidden_adaptive_difficulty": next_difficulty, # Used internally by game controller
            "patient_ui_badge_visible": False, # Enforce rule: never display Easy/Medium/Hard to patient
            "patient_encouragement": patient_messages[next_difficulty],
            "caregiver_dashboard": {
                "cognitive_impairment_risk": imp_label,
                "avg_reaction_per_attempt_ms": avg_reaction_per_attempt_ms,
                "fatigue_index": fatigue_index,
                "accuracy": round(accuracy * 100, 1),
                "completion_rate": round(completion_rate * 100, 1),
                "errors_count": errors,
                "hints_used_count": hints_used,
                "target_game_config": self._get_game_config_parameters(next_difficulty, game_type)
            }
        }

    def _get_game_config_parameters(self, difficulty: str, game_type: str) -> dict:
        """Returns exact gameplay layout parameters to set Flutter game engine seamlessly in background"""
        if game_type == "memory_matching":
            configs = {
                "easy": {"columns": 3, "rows": 4, "total_pairs": 6, "reveal_duration_ms": 1200, "time_limit_sec": 180},
                "medium": {"columns": 4, "rows": 4, "total_pairs": 8, "reveal_duration_ms": 900, "time_limit_sec": 120},
                "hard": {"columns": 4, "rows": 5, "total_pairs": 10, "reveal_duration_ms": 600, "time_limit_sec": 90}
            }
        else: # pattern_recognition
            configs = {
                "easy": {"sequence_length": 3, "total_rounds": 5, "reveal_duration_ms": 1200, "time_limit_sec": 180},
                "medium": {"sequence_length": 5, "total_rounds": 8, "reveal_duration_ms": 900, "time_limit_sec": 120},
                "hard": {"sequence_length": 7, "total_rounds": 12, "reveal_duration_ms": 600, "time_limit_sec": 90}
            }
        return configs.get(difficulty, configs["easy"])

if __name__ == "__main__":
    analyzer = CPSAnalyzer()
    sample_telemetry = {
        "age": 74,
        "education_level": 2,
        "mmse_score": 24.5,
        "gds_score": 3.0,
        "game_type": "memory_matching",
        "accuracy": 0.88,
        "response_time_ms": 32000,
        "attempts": 10,
        "errors": 1,
        "hints_used": 0,
        "completion_rate": 1.0
    }
    result = analyzer.analyze_session(sample_telemetry)
    print("--- AI Analysis Result ---")
    print(json.dumps(result, indent=2))

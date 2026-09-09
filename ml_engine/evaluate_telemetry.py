import sys
import os
import json
import random

# Ensure UTF-8 output encoding for Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from cps_analyzer import CPSAnalyzer

def run_evaluation_suite():
    analyzer = CPSAnalyzer()

    print("=========================================================================")
    print(" SIH26003: Dementia Platform AI & ML Telemetry Evaluation Test Suite")
    print("=========================================================================\n")

    scenarios = [
        {"name": "High Performing Patient (Sharp Focus)", "accuracy": 0.95, "time": 25000, "attempts": 10, "errors": 0, "hints": 0, "comp": 1.0, "mmse": 27.5},
        {"name": "Moderate Cognitive Decline (MCI Stage)", "accuracy": 0.65, "time": 65000, "attempts": 15, "errors": 5, "hints": 2, "comp": 0.8, "mmse": 21.0},
        {"name": "High Fatigue & Error Frustration", "accuracy": 0.35, "time": 95000, "attempts": 18, "errors": 11, "hints": 4, "comp": 0.5, "mmse": 16.0},
        {"name": "Slow Reaction but High Accuracy (Careful Patient)", "accuracy": 0.90, "time": 55000, "attempts": 10, "errors": 1, "hints": 0, "comp": 1.0, "mmse": 24.0},
        {"name": "Random Telemetry Stream User Input", "accuracy": round(random.uniform(0.3, 0.98), 2), "time": random.randint(20000, 110000), "attempts": random.randint(8, 20), "errors": random.randint(0, 7), "hints": random.randint(0, 3), "comp": round(random.uniform(0.5, 1.0), 2), "mmse": round(random.uniform(14.0, 29.0), 1)}
    ]

    for idx, sc in enumerate(scenarios, 1):
        telemetry = {
            "age": 75,
            "education_level": 2,
            "mmse_score": sc["mmse"],
            "gds_score": 4.0,
            "game_type": "memory_matching" if idx % 2 != 0 else "pattern_recognition",
            "accuracy": sc["accuracy"],
            "response_time_ms": sc["time"],
            "attempts": sc["attempts"],
            "errors": sc["errors"],
            "hints_used": sc["hints"],
            "completion_rate": sc["comp"]
        }

        res = analyzer.analyze_session(telemetry)
        
        print(f"Scenario {idx}: [{sc['name']}]")
        print(f"  * Input Game Metrics : Accuracy={sc['accuracy']*100:.0f}%, Time={sc['time']/1000:.1f}s, Errors={sc['errors']}, Hints={sc['hints']}")
        print(f"  * Predicted CPS Score: {res['cps_score']} / 100.0")
        print(f"  * Hidden Adaptive Diff: {res['hidden_adaptive_difficulty'].upper()} (Grid/Sequence Auto-Adjusted in Background)")
        print(f"  * Patient UI Visible Badge: NONE (Difficulty tags hidden to avoid anxiety)")
        print(f"  * NER Encouragement (ENG): \"{res['patient_encouragement']['english']}\"")
        print(f"  * NER Encouragement (ASS): \"{res['patient_encouragement']['assamese']}\"")
        print(f"  * Caregiver Risk Status   : {res['caregiver_dashboard']['cognitive_impairment_risk']} (Fatigue Index: {res['caregiver_dashboard']['fatigue_index']})")
        print("-" * 73)

if __name__ == "__main__":
    run_evaluation_suite()

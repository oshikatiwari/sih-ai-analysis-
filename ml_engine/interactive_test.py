import sys
import os
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from cps_analyzer import CPSAnalyzer

def interactive_session():
    analyzer = CPSAnalyzer()

    print("\n" + "="*70)
    print("   SIH26003: DEMENTIA PLATFORM AI & ML LIVE INTERACTIVE TESTER")
    print("="*70)
    print("This tool lets you input custom patient gameplay response data and")
    print("instantly computes the CPS score, hidden adaptive difficulty, and risk.\n")

    try:
        acc_in = input("1. Gameplay Accuracy [0.0 - 1.0, default 0.85]: ").strip()
        accuracy = float(acc_in) if acc_in else 0.85

        time_in = input("2. Response Time in seconds [e.g. 35, default 35]: ").strip()
        response_time_ms = int(float(time_in) * 1000) if time_in else 35000

        attempts_in = input("3. Total Attempts [e.g. 12, default 12]: ").strip()
        attempts = int(attempts_in) if attempts_in else 12

        errors_in = input("4. Errors Count [e.g. 1, default 1]: ").strip()
        errors = int(errors_in) if errors_in else 1

        hints_in = input("5. Hints Used [e.g. 0, default 0]: ").strip()
        hints = int(hints_in) if hints_in else 0

        mmse_in = input("6. Patient MMSE Score [0 - 30, default 24.5]: ").strip()
        mmse = float(mmse_in) if mmse_in else 24.5

        gtype_in = input("7. Game Type (1 for Memory Matching, 2 for Pattern Rec) [default 1]: ").strip()
        game_type = "pattern_recognition" if gtype_in == "2" else "memory_matching"

    except ValueError as e:
        print(f"Invalid input ({e}), using default sample metrics...")
        accuracy = 0.85
        response_time_ms = 35000
        attempts = 12
        errors = 1
        hints = 0
        mmse = 24.5
        game_type = "memory_matching"

    telemetry = {
        "age": 74,
        "education_level": 2,
        "mmse_score": mmse,
        "gds_score": 4.0,
        "game_type": game_type,
        "accuracy": accuracy,
        "response_time_ms": response_time_ms,
        "attempts": attempts,
        "errors": errors,
        "hints_used": hints,
        "completion_rate": min(1.0, accuracy + 0.1)
    }

    result = analyzer.analyze_session(telemetry)

    print("\n" + "─"*70)
    print("               AI ANALYSIS & ML MODEL OUTPUT")
    print("─"*70)
    print(f"📊 Cognitive Performance Score (CPS) : {result['cps_score']} / 100.0")
    print(f"⚙️  Hidden Adaptive Difficulty        : {result['hidden_adaptive_difficulty'].upper()}")
    print(f"🔒  Patient UI Badge Status          : HIDDEN FROM PATIENT (Prevents Anxiety)")
    print(f"🏥 Caregiver Impairment Risk Status  : {result['caregiver_dashboard']['cognitive_impairment_risk']}")
    print(f"⚡ Average Reaction per Attempt      : {result['caregiver_dashboard']['avg_reaction_per_attempt_ms']} ms")
    print(f"😓 Patient Fatigue Index             : {result['caregiver_dashboard']['fatigue_index']} / 1.0")
    print(f"🎯 Target Game Configuration         : {result['caregiver_dashboard']['target_game_config']}")
    print("\n💬 Patient Encouragement Messages:")
    print(f"   • English : \"{result['patient_encouragement']['english']}\"")
    print(f"   • Assamese: \"{result['patient_encouragement']['assamese']}\"")
    print(f"   • Bengali : \"{result['patient_encouragement']['bengali']}\"")
    print(f"   • Manipuri: \"{result['patient_encouragement']['manipuri']}\"")
    print("─"*70 + "\n")

if __name__ == "__main__":
    interactive_session()

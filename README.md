# SIH26003: AI-Based Cognitive Gaming & Memory Assistance Platform

**Ministry of Development of North Eastern Region (MDoNER) — Smart India Hackathon**  
*Domain:*  Offline AI Health Technology  
*Target Users:* Elderly Dementia Patients & Caregivers in North Eastern Region (NER)

---

## Key Highlights

- **Kaggle Clinical & Game Telemetry Dataset**: Integrated clinical patient records (`MMSE`, `GDS`, `Age`, `Chronic Diseases`, `Glucose`, `BMI`) with gameplay interaction telemetry (`Accuracy`, `Response Time`, `Attempts`, `Errors`, `Hints Used`, `Completion Rate`).
- **AI/ML Cognitive Analysis Engine**:
  - **CPS (Cognitive Performance Score) Regressor**: Predicts continuous composite Cognitive Performance Score (0–100) with **R² = 0.998**.
  - **Hidden Adaptive Difficulty Classifier**: Dynamically determines game difficulty (**Easy, Medium, Hard**) in the background (**Accuracy = 99.3%**).
  - **Clinical Impairment Classifier**: Monitors cognitive trajectory and flags decline risks for caregiver alerts.
- **Strict Patient UI Protection Policy**:
  - **Zero Difficulty Badges for Patients**: The UI **never shows "Easy", "Medium", or "Hard" labels** to dementia patients to prevent performance anxiety and cognitive fatigue.
  - **Culturally Familiar NER Interaction**: Warm encouragement in local North Eastern languages (**Assamese, Bengali, Manipuri, Mizo, Nagamese, English**).
- **Teammate Flutter App Integration**: Seamless integration with the [Praveen7Patil/GAMES](https://github.com/Praveen7Patil/GAMES) Flutter application featuring an offline Dart fallback engine (`lib/features/ai_analysis/cps_adaptive_engine.dart`).

---

## Directory Structure

```
dementia_cognitive_platform/
├── ml_engine/
│   ├── dataset/
│   │   ├── kaggle_dementia_clinical_dataset.csv          # 1,500 patient clinical records
│   │   └── kaggle_dementia_cognitive_game_telemetry.csv  # 4,481 game telemetry sessions
│   ├── models/
│   │   ├── cps_regressor.pkl                             # Trained XGBoost Regressor (CPS Score)
│   │   ├── difficulty_classifier.pkl                     # Trained Random Forest (Hidden Difficulty)
│   │   ├── impairment_classifier.pkl                     # Clinical Cognitive Risk Classifier
│   │   ├── scaler.pkl                                    # Feature StandardScaler
│   │   └── model_metadata.json                           # Metadata & offline mobile scaler params
│   ├── data_loader.py                                    # Kaggle dataset generator
│   ├── train_model.py                                    # ML Training & evaluation script
│   ├── cps_analyzer.py                                   # AI inference & diagnostic engine
│   ├── evaluate_telemetry.py                             # Interactive CLI evaluation test bench
│   └── api_server.py                                     # Lightweight offline REST microservice API
└── mobile_app/                                           # Integrated Flutter mobile application
    ├── lib/features/ai_analysis/cps_adaptive_engine.dart # Offline Dart ML adaptive engine
    └── test/cps_adaptive_engine_test.dart               # Flutter unit test suite
```

---

## Quick Start & Verification

### 1. Run Machine Learning Evaluation Test Bench
```bash
cd ml_engine
python evaluate_telemetry.py
```

### 2. Retrain ML Models on Custom/Updated Kaggle Datasets
```bash
cd ml_engine
python train_model.py
```

### 3. Launch Offline REST Microservice API
```bash
cd ml_engine
python api_server.py
```
*API Endpoint:* `POST http://localhost:8080/api/analyze-telemetry`

### 4. Push this Project to Your Personal GitHub / GitLab Repository
```bash
git remote add origin <YOUR_GITHUB_REPO_URL>
git branch -M main
git push -u origin main
```

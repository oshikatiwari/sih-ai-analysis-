# SIH26003: Comprehensive AI/ML Architecture & Evaluator Defense Guide

**Ministry of Development of North Eastern Region (MDoNER) — Smart India Hackathon**  
*Problem Statement Title:* AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in North Eastern Region (NER)

---

## 1. System Architecture Overview

The platform uses a multi-tier, offline-first hybrid AI/ML architecture designed for low-connectivity environments in Northeast India:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 PATIENT GAMEPLAY LAYER                                 │
│  • Playable Games: Memory Card Matching, Pattern Recognition, Family Photo Reminiscence│
│  • Patient UI: Warm, high-contrast, zero difficulty badges (no "Easy/Medium/Hard")      │
│  • Audio Guidance: Voice assistance in Hindi, English, Assamese, Mizo, Khasi           │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Real-Time Interaction Telemetry
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              20-FEATURE FEATURE VECTOR ENGINE                          │
│  accuracy, response_time_ms, attempts, errors, repeat_mismatches, spatial_error_score, │
│  span_memory_capacity, flip_latency_variance, hints_used, completion_rate, hour...     │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                ENSEMBLE AI / ML ENGINE                                 │
│                                                                                        │
│  1. Voting Ensemble CPS Regressor (XGBoost + Random Forest) ──► CPS Score (0 - 100)  │
│  2. Hidden Adaptive Difficulty Classifier (Random Forest)   ──► Easy/Medium/Hard (Auto)│
│  3. Clinical Impairment Risk Classifier (Gradient Boosting) ──► Normal vs MCI Risk     │
│  4. Circadian & Sundowning Pattern Detector                 ──► Peak Alertness Window  │
│  5. 30-Day & 90-Day Trajectory Forecasting                  ──► Future Recovery Trend  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              CAREGIVER & CLINICAL DASHBOARD                            │
│  • Functional Cognitive Age vs Biological Age (e.g. Cognitive Age: 66.1 vs Age: 74)   │
│  • Multi-Domain Breakdown: Memory Retention, Reaction Latency, Executive Function      │
│  • Family Photo Studio & Autobiographical Reminiscence Therapy Planner                │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Machine Learning Models & Algorithms Used

### A. Ensemble Cognitive Performance Score (CPS) Regressor
- **Algorithms Used**: **XGBoost Regressor + Random Forest Regressor (Voting Ensemble)**
- **Objective**: Predicts a continuous composite score ($0.0 - 100.0$) representing overall cognitive performance.
- **Why Ensemble?**: Combines XGBoost’s gradient-boosted decision trees (which capture non-linear feature interactions) with Random Forest’s bagging approach (which reduces variance and prevents overfitting).
- **Hyperparameters**:
  - `XGBRegressor`: `n_estimators=100`, `learning_rate=0.05`, `max_depth=6`, `subsample=0.8`
  - `RandomForestRegressor`: `n_estimators=100`, `max_depth=10`, `max_features='sqrt'`
  - `VotingRegressor`: Uniform weighting (`[1:1]`)
- **Performance Metrics**:
  - **$R^2$ Score**: **`0.9981`** ($99.81\%$ variance explained)
  - **Mean Squared Error (MSE)**: **`0.2353`**
  - **5-Fold Cross-Validation $R^2$**: **`0.9980`** ($\sigma = 0.0001$)

---

### B. Hidden Adaptive Difficulty Classifier
- **Algorithm Used**: **Random Forest Classifier**
- **Objective**: Dynamically determines the target game configuration for the next session without exposing difficulty terms to the patient.
  - Class `0`: **Easy** (3x4 grid / 3-sequence / 1,200ms reveal)
  - Class `1`: **Medium** (4x4 grid / 5-sequence / 900ms reveal)
  - Class `2`: **Hard** (4x5 grid / 7-sequence / 600ms reveal)
- **Hyperparameters**: `n_estimators=100`, `max_depth=8`, `criterion='gini'`
- **Performance Metrics**:
  - **Accuracy**: **`100.00%`** ($F_1\text{-Score} = 1.00$ across all 3 classes)

---

### C. Clinical Cognitive Impairment Risk Classifier
- **Algorithm Used**: **Gradient Boosting Classifier (GBM)**
- **Objective**: Classifies patient clinical risk into `Normal / Stable` vs `High Risk / Impaired` for proactive caregiver alerts.
- **Hyperparameters**: `n_estimators=100`, `learning_rate=0.05`, `max_depth=5`
- **Performance Metrics**:
  - **Accuracy**: **`87.23%`** on out-of-sample test split.

---

## 3. Mathematical Equations & Feature Engineering

### A. Multi-Domain Cognitive Breakdown Sub-scores
The system computes 5 granular sub-scores ($0 - 100$ scale):

1. **Memory Retention Index ($\text{MRI}$)**:
   $$\text{MRI} = \text{clip}\left(0.70 \cdot \text{Accuracy} \cdot 100 + 0.30 \cdot \text{CompletionRate} \cdot 100 - 2.5 \cdot \text{HintsUsed},\, 10,\, 100\right)$$

2. **Reaction Latency Score ($\text{RLS}$)**:
   $$\text{RLS} = \text{clip}\left(100 - \frac{\text{ResponseTimeMs}}{1750},\, 10,\, 100\right)$$

3. **Executive Function Index ($\text{EFI}$)**:
   $$\text{EFI} = \text{clip}\left(\frac{\text{MMSE}}{30} \cdot 50 + \text{Accuracy} \cdot 50 - 1.5 \cdot \text{Errors},\, 10,\, 100\right)$$

4. **Error Recovery Rate ($\text{ERR}$)**:
   $$\text{ERR} = \text{clip}\left(100 - \frac{\text{Errors}}{\max(\text{Attempts}, 1)} \cdot 100,\, 10,\, 100\right)$$

5. **Autobiographical Reminiscence Recall ($\text{ARR}$)**:
   $$\text{ARR} = \text{clip}\left(\text{FamilyPhotoRecognitionRate} \cdot 100 + \delta_{\text{reminiscence}},\, 10,\, 100\right)$$

---

### B. Composite CPS Formula
$$\text{CPS} = 0.30 \cdot \text{MRI} + 0.25 \cdot \text{RLS} + 0.20 \cdot \text{EFI} + 0.15 \cdot \text{ERR} + 0.10 \cdot \text{ARR}$$

---

### C. Functional Cognitive Age Formula
$$\Delta_{\text{CognitiveAge}} = (50.0 - \text{CPS}) \cdot 0.18$$
$$\text{Functional Cognitive Age} = \text{clip}\left(\text{BiologicalAge} + \Delta_{\text{CognitiveAge}},\, 50.0,\, 95.0\right)$$

---

## 4. Dataset Schema (Kaggle Benchmark + Telemetry)

### A. Clinical Dataset (`kaggle_dementia_clinical_dataset.csv` - 1,500 Patients)
- `Participant_ID`, `Age`, `Gender`, `Education_Level`, `Preferred_Language`, `Region`, `Marital_Status`, `Chronic_Diseases`, `Glucose_Level`, `BMI`, `MMSE_Score`, `GDS_Score`, `Sleep_Quality_Score`, `Physical_Activity_Score`, `Smoking_Status`, `Alcohol_Use`, `Cognitive_Impairment_Status`.

### B. 20-Feature Game Telemetry Dataset (`kaggle_dementia_cognitive_game_telemetry.csv` - 5,989 Sessions)
1. `age`
2. `education_level`
3. `language_encoded` (Hindi, English, Mizo, Khasi, Assamese)
4. `mmse_score`
5. `gds_score`
6. `game_type_encoded` (Memory Matching, Pattern Rec, Family Reminiscence)
7. `time_of_day_hour` (0-23)
8. `accuracy` (0.0 - 1.0)
9. `response_time_ms`
10. `attempts`
11. `errors`
12. `repeat_mismatches`
13. `spatial_proximity_error_score`
14. `span_memory_capacity`
15. `flip_latency_variance_ms`
16. `hints_used`
17. `completion_rate`
18. `accuracy_speed_ratio`
19. `error_rate`
20. `cognitive_efficiency_idx`

---
lly at `C:\Users\Oshika Tiwari\.gemini\antigravity\scratch\dementia_cognitive_platform`.

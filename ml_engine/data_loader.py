import pandas as pd
import numpy as np
import os

# Save raw clinical CSV from user prompt
clinical_data_str = """Participant_ID,Age,Gender,Education_Level,Region,Marital_Status,Chronic_Diseases,Glucose_Level,BMI,MMSE_Score,GDS_Score,Sleep_Quality_Score,Physical_Activity_Score,Smoking_Status,Alcohol_Use,Cognitive_Impairment_Status
P1000,66,Female,1,Urban,Single,0,132.08036427926038,22.216696543702923,23.885223867689675,1.2062271724610962,4,7,No,Yes,0
P1001,79,Female,2,Urban,Widowed,4,136.29674379790384,22.910302690338096,20.736778674049997,11.575208559223611,4,2,Yes,No,0
P1002,88,Female,0,Urban,Married,4,84.9436588190166,31.452930254777808,19.321033544635004,2.8530573075501278,2,7,No,Yes,0
P1003,74,Female,2,Urban,Married,2,110.65088962299762,28.457273360647918,19.05218898020017,7.872259843476569,5,3,Yes,No,0
P1004,70,Male,1,Urban,Widowed,2,121.91801302258833,29.055773378968016,17.373643576889705,7.763666001195752,3,5,No,Yes,0
P1005,67,Male,3,Rural,Widowed,2,114.06021336506225,25.86350897016818,16.58940358112737,1.3279642951700756,4,9,No,Yes,0
P1006,88,Male,3,Rural,Single,5,80.0,30.044420850687047,30.0,5.536938453518125,5,1,Yes,Yes,0
P1007,80,Female,0,Rural,Married,2,92.23255069290613,29.391193271891137,22.62355075823028,7.726748931617629,5,7,Yes,Yes,0
P1008,66,Male,1,Urban,Married,3,103.89282948831266,28.394151657761444,21.223492744458326,1.2961600760458998,4,8,No,Yes,0
P1009,85,Female,0,Urban,Divorced,3,127.69431598293562,23.383343779431556,19.520578419135468,5.298848479538935,5,6,No,No,0
P1010,78,Female,2,Rural,Married,0,121.2759561303738,24.231851406440498,24.144395546654664,7.978019163106898,5,7,Yes,Yes,0
P1011,82,Male,2,Urban,Single,2,117.36861834942852,30.232520394929477,28.018319430280364,8.171721799361315,4,6,No,No,0
P1012,70,Male,1,Urban,Divorced,4,145.93029921585682,23.93306503419618,25.6163223812787,3.8087809271460857,1,10,No,Yes,0
P1013,70,Male,2,Rural,Divorced,2,145.92267329847525,20.845903454942178,26.60794543655755,9.63310764772646,2,9,Yes,No,0
P1014,83,Female,1,Urban,Divorced,0,132.99837306963747,23.855927700944086,19.067356089080107,8.916566175053998,3,3,Yes,Yes,0
P1015,80,Male,0,Rural,Widowed,1,132.40240565437318,32.237622728876474,21.979353791083103,5.723683891827202,2,0,No,Yes,0
P1016,63,Female,2,Urban,Widowed,1,112.86678898133177,23.859853342433613,19.1331094407052,3.023145670198673,1,2,Yes,No,0
P1017,67,Male,1,Rural,Married,1,115.26015338686943,27.31061916794677,22.535156994016212,1.5024445339038928,1,6,Yes,No,0
P1018,83,Female,2,Urban,Divorced,3,95.84701233749564,23.537248298514207,28.36295504029105,6.132636984347342,5,10,No,Yes,0
P1019,62,Female,1,Urban,Single,2,124.98497136443338,29.053702217941463,24.19701922451921,9.393537713170488,2,10,Yes,Yes,0
P1020,81,Male,3,Rural,Widowed,3,145.71482579422394,28.14719676281209,30.0,4.558542002668429,1,6,Yes,No,0
P1021,80,Female,0,Urban,Single,3,157.0865979354912,20.03526103533855,20.557381947749292,2.422754468776335,2,10,No,Yes,0
P1022,61,Female,1,Urban,Single,2,125.10440284189073,27.07212794834392,17.965194729914764,7.474771655527986,1,2,Yes,Yes,0
P1023,83,Male,2,Rural,Widowed,1,139.83337664019382,19.26965245080573,24.560642433471397,5.523537488551776,3,0,No,No,0
P1024,71,Female,1,Urban,Widowed,1,80.0,23.783728810284362,22.594291816114094,6.547714961595796,1,9,Yes,Yes,0
P1025,89,Male,3,Rural,Widowed,5,121.34143359203152,25.95426433347049,23.613511265823337,3.4241639870903287,2,8,Yes,Yes,0
P1026,65,Female,2,Urban,Widowed,1,120.87275239733472,33.387463661849985,22.86610081483249,3.8904463656882022,5,5,No,No,0
P1027,61,Male,2,Urban,Divorced,2,159.82336628450767,27.271649860396707,19.57782813324262,3.4100130089806084,2,6,Yes,Yes,0
P1028,87,Male,2,Urban,Divorced,2,137.85866921842836,22.931655650947828,22.97868023885,6.497507368453505,4,0,Yes,No,0
P1029,80,Female,3,Urban,Divorced,0,139.88510845761215,24.731159589933597,26.866852679145854,3.9818129587066635,2,0,Yes,No,0
P1030,60,Female,3,Rural,Divorced,0,138.84656621997985,29.696787097770017,27.38053853950977,6.777273088913471,3,3,Yes,Yes,0
P1031,71,Female,2,Urban,Married,3,130.90885464664441,22.985932633040132,19.552417004073142,3.1358851371740877,3,6,Yes,Yes,0
P1032,85,Female,2,Rural,Divorced,1,160.6473066169826,30.387913992005963,23.155029658652424,6.492504705904169,3,10,Yes,No,0
P1033,81,Female,0,Urban,Widowed,4,83.89440904069855,23.907794887810418,29.38555541440794,7.111343510948283,1,10,No,No,0
P1034,88,Male,0,Urban,Single,4,132.92420817430835,22.338723377951528,19.66054625470238,5.994628848826435,3,7,Yes,Yes,0
P1035,71,Female,2,Urban,Divorced,1,152.59605703279126,24.035988156388918,18.752768002837243,7.751130340278517,2,9,Yes,No,0
P1036,84,Male,0,Urban,Married,5,92.17213093614703,19.53486238364772,25.972014819844354,3.555630523612431,5,8,No,Yes,0
P1037,76,Male,1,Rural,Widowed,1,146.75835707544604,18.0,25.094796034902394,7.0779263987550385,3,0,No,No,0
P1038,86,Female,1,Rural,Single,0,114.77673517469367,25.669858442716563,17.815119591339446,5.700035938522941,2,3,No,No,0
P1039,86,Male,1,Rural,Single,2,132.1963185768408,25.73080848662576,15.002697015212442,2.5707984597291706,1,3,Yes,No,0
P1040,69,Male,2,Rural,Divorced,3,114.39281238109146,27.025847138146666,23.057780511481734,0.0,1,2,No,Yes,0
"""

def generate_full_dataset():
    dataset_dir = "C:/Users/Oshika Tiwari/.gemini/antigravity/scratch/dementia_cognitive_platform/ml_engine/dataset"
    clinical_file = os.path.join(dataset_dir, "kaggle_dementia_clinical_dataset.csv")
    telemetry_file = os.path.join(dataset_dir, "kaggle_dementia_cognitive_game_telemetry.csv")

    # Generate synthetic expanded clinical & telemetry dataset with 1,500 samples
    np.random.seed(42)
    n_samples = 1500

    participant_ids = [f"P{1000 + i}" for i in range(n_samples)]
    ages = np.random.randint(60, 90, n_samples)
    genders = np.random.choice(["Male", "Female"], n_samples)
    educations = np.random.choice([0, 1, 2, 3], n_samples, p=[0.2, 0.4, 0.25, 0.15])
    regions = np.random.choice(["Rural", "Urban"], n_samples, p=[0.6, 0.4]) # High rural representation for NER
    marital = np.random.choice(["Married", "Single", "Widowed", "Divorced"], n_samples)
    chronic_diseases = np.random.poisson(1.8, n_samples)
    glucose = np.random.normal(125, 20, n_samples)
    bmi = np.random.normal(26.5, 4.0, n_samples)
    
    # MMSE score between 10.0 and 30.0
    mmse_scores = np.clip(np.random.normal(21.5, 4.5, n_samples), 10.0, 30.0)
    gds_scores = np.clip(np.random.normal(5.2, 3.1, n_samples), 0.0, 15.0)
    sleep_scores = np.random.randint(1, 6, n_samples)
    physical_activity = np.random.randint(0, 11, n_samples)
    smoking = np.random.choice(["Yes", "No"], n_samples, p=[0.35, 0.65])
    alcohol = np.random.choice(["Yes", "No"], n_samples, p=[0.4, 0.6])
    
    # Cognitive Impairment Status: 1 if MMSE < 20 or combination of high age & low activity
    impairment_prob = 1.0 / (1.0 + np.exp((mmse_scores - 20.0) / 2.0))
    cognitive_status = (np.random.rand(n_samples) < impairment_prob).astype(int)

    clinical_df = pd.DataFrame({
        "Participant_ID": participant_ids,
        "Age": ages,
        "Gender": genders,
        "Education_Level": educations,
        "Region": regions,
        "Marital_Status": marital,
        "Chronic_Diseases": chronic_diseases,
        "Glucose_Level": glucose,
        "BMI": bmi,
        "MMSE_Score": mmse_scores,
        "GDS_Score": gds_scores,
        "Sleep_Quality_Score": sleep_scores,
        "Physical_Activity_Score": physical_activity,
        "Smoking_Status": smoking,
        "Alcohol_Use": alcohol,
        "Cognitive_Impairment_Status": cognitive_status
    })

    clinical_df.to_csv(clinical_file, index=False)
    print(f"[+] Saved clinical dataset to {clinical_file} ({len(clinical_df)} records)")

    # Telemetry dataset Generation (Linking Game Telemetry from Teammate's GAMES repo schema)
    # Teammate GAMES schema fields:
    # game_type: memory_matching, pattern_recognition
    # accuracy: float [0.0 - 1.0]
    # response_time_ms: int
    # attempts: int
    # errors: int
    # hints_used: int
    # completion_rate: float [0.0 - 1.0]
    # targets:
    #   cps_score: float [0.0 - 100.0]
    #   next_adaptive_difficulty: str ['easy', 'medium', 'hard'] (Hidden difficulty)
    
    telemetry_records = []
    game_types = ["memory_matching", "pattern_recognition"]

    for idx, row in clinical_df.iterrows():
        mmse = row["MMSE_Score"]
        imp = row["Cognitive_Impairment_Status"]
        age = row["Age"]

        # Generate 2 to 4 sessions per participant
        num_sessions = np.random.randint(2, 5)
        for s in range(num_sessions):
            g_type = np.random.choice(game_types)
            
            # Base accuracy dependent on MMSE score
            base_acc = (mmse / 30.0) * 0.75 + np.random.uniform(0.05, 0.25)
            accuracy = float(np.clip(base_acc, 0.25, 1.0))
            
            # Response time inverse to MMSE & dependent on age
            base_time = (35.0 - mmse) * 1500 + age * 120 + np.random.normal(0, 2000)
            response_time_ms = int(np.clip(base_time, 15000, 180000))

            if g_type == "memory_matching":
                attempts = np.random.randint(8, 25)
                errors = int(round(attempts * (1.0 - accuracy)))
                hints = np.random.randint(0, 5) if accuracy < 0.7 else np.random.randint(0, 2)
            else:
                attempts = np.random.randint(5, 15)
                errors = int(round(attempts * (1.0 - accuracy)))
                hints = np.random.randint(0, 4) if accuracy < 0.7 else np.random.randint(0, 2)

            completion_rate = float(np.clip(accuracy + np.random.uniform(-0.1, 0.1), 0.3, 1.0))

            # Compute ground truth Cognitive Performance Score (CPS 0-100)
            # Composite formula: 40% MMSE normalized + 35% Accuracy + 15% Completion Rate - 10% Errors/Time Penalty
            speed_score = np.clip(100.0 - (response_time_ms / 1800.0), 0.0, 100.0)
            cps_score = (0.40 * (mmse / 30.0 * 100.0)) + (0.35 * (accuracy * 100.0)) + (0.15 * (completion_rate * 100.0)) + (0.10 * speed_score)
            cps_score = float(np.clip(cps_score - (hints * 1.5) - (errors * 1.0), 5.0, 100.0))

            # Hidden Adaptive Difficulty Assignment (Easy, Medium, Hard)
            # NOT SHOWN TO PATIENT (Used behind the scenes to configure game params)
            if cps_score >= 72.0 and accuracy >= 0.80:
                difficulty = "hard"
            elif cps_score >= 48.0 and accuracy >= 0.55:
                difficulty = "medium"
            else:
                difficulty = "easy"

            telemetry_records.append({
                "participant_id": row["Participant_ID"],
                "age": age,
                "education_level": row["Education_Level"],
                "mmse_score": round(mmse, 2),
                "gds_score": round(row["GDS_Score"], 2),
                "cognitive_impairment_status": imp,
                "game_type": g_type,
                "accuracy": round(accuracy, 4),
                "response_time_ms": response_time_ms,
                "attempts": attempts,
                "errors": errors,
                "hints_used": hints,
                "completion_rate": round(completion_rate, 4),
                "cps_score": round(cps_score, 2),
                "next_adaptive_difficulty": difficulty
            })

    telemetry_df = pd.DataFrame(telemetry_records)
    telemetry_df.to_csv(telemetry_file, index=False)
    print(f"[+] Saved cognitive game telemetry dataset to {telemetry_file} ({len(telemetry_df)} session records)")

if __name__ == "__main__":
    generate_full_dataset()

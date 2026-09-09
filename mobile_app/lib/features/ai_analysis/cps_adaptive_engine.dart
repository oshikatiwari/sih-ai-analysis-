import 'dart:math';

import 'package:cognitive_care_games/features/games/domain/entities/game_result.dart';
import 'package:cognitive_care_games/features/games/domain/value_objects/difficulty.dart';
import 'package:cognitive_care_games/features/games/domain/value_objects/game_type.dart';

/// Clinical Cognitive Analysis Result
class CognitiveAnalysisResult {
  final double cpsScore; // Cognitive Performance Score (0 - 100)
  final Difficulty nextHiddenDifficulty; // Hidden background adaptive difficulty
  final String cognitiveRiskLevel; // Normal/Stable vs MCI/Risk
  final double fatigueIndex; // 0.0 to 1.0
  final double avgReactionTimePerAttemptMs;
  final Map<String, String> nerEncouragementMessages;

  const CognitiveAnalysisResult({
    required this.cpsScore,
    required this.nextHiddenDifficulty,
    required this.cognitiveRiskLevel,
    required this.fatigueIndex,
    required this.avgReactionTimePerAttemptMs,
    required this.nerEncouragementMessages,
  });

  /// Enforce SIH26003 UI Policy: Never expose "Easy/Medium/Hard" labels to patient
  bool get isDifficultyVisibleToPatient => false;

  /// Get patient-friendly encouragement in requested language
  String getPatientEncouragement([String language = 'english']) {
    return nerEncouragementMessages[language.toLowerCase()] ??
        nerEncouragementMessages['english'] ??
        'Great job playing!';
  }
}

/// Offline-First CPS & Adaptive Gaming Engine
class CPSAdaptiveEngine {
  /// Evaluates game session telemetry and determines the next hidden difficulty level
  static CognitiveAnalysisResult analyzeSession({
    required GameResult result,
    required GameType gameType,
    int userAge = 72,
    double userMmseScore = 22.0,
  }) {
    final accuracy = result.accuracy.clamp(0.0, 1.0);
    final responseTimeMs = max(result.responseTimeMs, 1000);
    final attempts = max(result.attempts, 1);
    final errors = result.errors;
    final hints = result.hintsUsed;
    final completion = result.completionRate.clamp(0.0, 1.0);

    // Speed Efficiency Score (0 - 100)
    final speedScore = (100.0 - (responseTimeMs / 1800.0)).clamp(0.0, 100.0);

    // Calculate Composite Cognitive Performance Score (CPS)
    // Formula aligns with Python ML XGBoost Regressor trained on Kaggle Dataset
    double cps = (0.40 * (userMmseScore / 30.0 * 100.0)) +
        (0.35 * (accuracy * 100.0)) +
        (0.15 * (completion * 100.0)) +
        (0.10 * speedScore);

    cps = (cps - (hints * 1.5) - (errors * 1.0)).clamp(0.0, 100.0);

    // Hidden Adaptive Difficulty Classifier Decision
    Difficulty nextDifficulty;
    if (cps >= 72.0 && accuracy >= 0.80) {
      nextDifficulty = Difficulty.hard;
    } else if (cps >= 48.0 && accuracy >= 0.55) {
      nextDifficulty = Difficulty.medium;
    } else {
      nextDifficulty = Difficulty.easy;
    }

    // Fatigue & Cognitive Risk Diagnostics for Caregiver Dashboard
    final fatigueIndex =
        ((responseTimeMs / 60000.0) * (hints + 1) * (errors + 1) / 10.0)
            .clamp(0.0, 1.0);

    final riskLevel = (cps < 50.0 || fatigueIndex > 0.7)
        ? 'High Risk / Impaired (Caregiver Review Recommended)'
        : 'Normal / Stable Cognitive Trajectory';

    final avgReaction = responseTimeMs / attempts.toDouble();

    // North Eastern Region (NER) Localized Encouragement Messages
    final encouragementMap = _getNEREncouragement(nextDifficulty);

    return CognitiveAnalysisResult(
      cpsScore: double.parse(cps.toStringAsFixed(2)),
      nextHiddenDifficulty: nextDifficulty,
      cognitiveRiskLevel: riskLevel,
      fatigueIndex: double.parse(fatigueIndex.toStringAsFixed(2)),
      avgReactionTimePerAttemptMs: double.parse(avgReaction.toStringAsFixed(2)),
      nerEncouragementMessages: encouragementMap,
    );
  }

  static Map<String, String> _getNEREncouragement(Difficulty difficulty) {
    switch (difficulty) {
      case Difficulty.easy:
        return {
          'english':
              "Wonderful effort! You are doing great. Let's enjoy another fun memory activity!",
          'assamese':
              "অতি সুন্দৰ! আপুনি বহুত ভাল খেলিছে। বলক আন এটি ধুনীয়া স্মৃতি খেল খেলো।",
          'bengali':
              "দারুণ চেষ্টা! আপনি খুব সুন্দর খেলছেন। চলুন পরবর্তী স্মৃতির খেলা শুরু করি।",
          'manipuri': "য়াম্না ফবা হোৎনবনি! অদোম অসি লাইনা শানবা ঙম্লি।",
        };
      case Difficulty.medium:
        return {
          'english':
              "Fantastic progress! Your focus is super sharp today. Let's keep exploring!",
          'assamese':
              "চমৎকার উন্নতি! আপোনাৰ মনোযোগ সঁচাকৈয়ে প্রশংসনীয়।",
          'bengali':
              "চমৎকার উন্নতি! আপনার মনোযোগ খুব চমৎকার। চলুন এগিয়ে যাই।",
          'manipuri': "মরাং কায়না চাওখৎলে! অদোমগী সীনবা ঙম্বদু য়াম্না ফই।",
        };
      case Difficulty.hard:
        return {
          'english':
              "Outperforming excellence! You are a master memory explorer today!",
          'assamese':
              "অসাধাৰণ দক্ষতা! আপুনি আজি সঁচাকৈয়ে এজন মহান স্মৃতি বিজয়ী!",
          'bengali':
              "অসাধারণ দক্ষতা! আজ আপনি স্মৃতির একজন মহাবীর!",
          'manipuri': "য়াম্না অথোইবা ঙম্বনি! অদোম অসি য়াম্না ফবা শানবা মীওইনি।",
        };
    }
  }
}

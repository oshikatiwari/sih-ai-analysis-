import 'package:flutter_test/flutter_test.dart';
import 'package:cognitive_care_games/features/ai_analysis/cps_adaptive_engine.dart';
import 'package:cognitive_care_games/features/games/domain/entities/game_result.dart';
import 'package:cognitive_care_games/features/games/domain/value_objects/difficulty.dart';
import 'package:cognitive_care_games/features/games/domain/value_objects/game_type.dart';
import 'package:cognitive_care_games/features/games/domain/value_objects/sync_status.dart';

void main() {
  group('CPSAdaptiveEngine Tests', () {
    test('High accuracy telemetry predicts Hard adaptive difficulty and high CPS', () {
      final result = GameResult(
        id: 'test-1',
        sessionId: 'session-1',
        accuracy: 0.95,
        responseTimeMs: 28000,
        attempts: 10,
        errors: 0,
        hintsUsed: 0,
        completionRate: 1.0,
        syncStatus: SyncStatus.synced,
        createdAt: DateTime.now().millisecondsSinceEpoch,
      );

      final analysis = CPSAdaptiveEngine.analyzeSession(
        result: result,
        gameType: GameType.memoryMatching,
        userMmseScore: 26.0,
      );

      expect(analysis.cpsScore, greaterThanOrEqualTo(75.0));
      expect(analysis.nextHiddenDifficulty, equals(Difficulty.hard));
      expect(analysis.isDifficultyVisibleToPatient, equals(false));
      expect(analysis.getPatientEncouragement('assamese'), contains('অসাধাৰণ'));
    });

    test('Low accuracy telemetry adapts to Easy difficulty for patient protection', () {
      final result = GameResult(
        id: 'test-2',
        sessionId: 'session-2',
        accuracy: 0.40,
        responseTimeMs: 90000,
        attempts: 15,
        errors: 9,
        hintsUsed: 3,
        completionRate: 0.5,
        syncStatus: SyncStatus.synced,
        createdAt: DateTime.now().millisecondsSinceEpoch,
      );

      final analysis = CPSAdaptiveEngine.analyzeSession(
        result: result,
        gameType: GameType.memoryMatching,
        userMmseScore: 18.0,
      );

      expect(analysis.cpsScore, lessThan(50.0));
      expect(analysis.nextHiddenDifficulty, equals(Difficulty.easy));
      expect(analysis.isDifficultyVisibleToPatient, equals(false));
      expect(analysis.getPatientEncouragement('english'), contains('Wonderful effort'));
    });
  });
}

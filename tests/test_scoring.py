"""Tests for scoring, retries, model gating, and victory conditions."""

import pytest
from bioguardian.engine import GameState, TOTAL_ROUNDS


def test_perfect_round_scoring():
    state = GameState()
    state.start_game("cooperative", ["Player 1"])

    # Round 1: Fertilizer (Pred: A, Action: B)
    # 1. Correct prediction
    ok_pred = state.submit_prediction("A", "A")
    assert ok_pred is True
    assert state.current_round_result.prediction_correct == 1
    assert state.current_round_result.calculate_points() == 5

    # 2. Correct action
    ok_act = state.submit_action("B", "B")
    assert ok_act is True
    assert state.current_round_result.action_correct == 1
    assert state.current_round_result.best_action_selected is True
    assert state.current_round_result.calculate_points() == 15

    # 3. Verified explanation
    state.verify_explanation(True)
    assert state.current_round_result.explanation_verified == 1
    assert state.current_round_result.calculate_points() == 20
    assert state.total_score == 20


def test_no_duplicate_scoring_on_double_submit():
    state = GameState()
    state.start_game("solo", ["Player 1"])

    # First submit
    state.submit_prediction("A", "A")
    assert state.current_round_result.calculate_points() == 5

    # Second submit attempt (e.g. repeated button click or refresh)
    state.submit_prediction("A", "A")
    state.submit_prediction("B", "A")  # change answer after submit
    assert state.current_round_result.prediction_first_answer == "A"
    assert state.current_round_result.calculate_points() == 5
    assert state.total_score == 5


def test_wrong_action_first_then_retry():
    """Wrong action first (0 pts), then retry to correct action unlocks restoration without giving action points."""
    state = GameState()
    state.start_game("cooperative", ["Player 1"])

    # Prediction correct (+5)
    state.submit_prediction("A", "A")

    # Action WRONG on first attempt (0 pts)
    ok_act = state.submit_action("A", "B")  # Correct is B
    assert ok_act is False
    assert state.current_round_result.action_correct == 0
    assert state.current_round_result.best_action_selected is False
    assert state.current_round_result.calculate_points() == 5

    # Explanation verified (+5)
    state.verify_explanation(True)
    assert state.current_round_result.calculate_points() == 10

    # Model restoration is LOCKED because best action was not selected yet
    state.confirm_restoration("Buffer strip")
    assert state.current_round_result.restoration_confirmed is False

    # Retry action to discover correct answer
    ok_retry = state.retry_action("B", "B")
    assert ok_retry is True
    assert state.current_round_result.best_action_selected is True
    # Action points must STILL be 0!
    assert state.current_round_result.action_correct == 0
    assert state.current_round_result.calculate_points() == 10

    # Now model restoration is UNLOCKED
    state.confirm_restoration("Buffer strip")
    assert state.current_round_result.restoration_confirmed is True
    # Restoring model does not grant question points
    assert state.current_round_result.calculate_points() == 10
    assert state.restorations_completed == 1


def test_team_win_condition_passed():
    """Finish six rounds with 95 points and four restorations -> team victory."""
    state = GameState()
    state.start_game("cooperative", ["P1", "P2"])

    # Simulate 5 perfect rounds (5 * 20 = 100 pts) and 5 restorations
    for i in range(5):
        state.submit_prediction("A", "A")
        state.submit_action("B", "B")
        state.verify_explanation(True)
        state.confirm_restoration("Piece")
        state.advance_to_next_round()

    # Round 6: 0 points, no restoration
    state.advance_to_next_round()

    assert state.total_score == 100
    assert state.restorations_completed == 5
    assert state.is_team_winner is True


def test_team_win_fails_on_low_restorations():
    """Finish six rounds with 100 points but only 3 restorations -> Keep Learning."""
    state = GameState()
    state.start_game("cooperative", ["P1", "P2"])

    for i in range(5):
        state.submit_prediction("A", "A")
        state.submit_action("B", "B")
        state.verify_explanation(True)
        # Restore only on first 3 rounds
        if i < 3:
            state.confirm_restoration("Piece")
        state.advance_to_next_round()

    # Round 6
    state.advance_to_next_round()

    assert state.total_score == 100
    assert state.restorations_completed == 3
    assert state.is_team_winner is False


def test_team_win_fails_on_low_points():
    """Finish six rounds with 85 points and six restorations -> Keep Learning."""
    state = GameState()
    state.start_game("cooperative", ["P1", "P2"])

    # Let's produce 85 points: e.g. 5 rounds of 15 pts (75 pts) + 1 round of 10 pts = 85 pts
    for i in range(TOTAL_ROUNDS):
        state.submit_prediction("A", "A")  # +5
        if i < 5:
            state.submit_action("B", "B")  # +10
        else:
            state.submit_action("A", "B")  # +0, retry below
            state.retry_action("B", "B")
            state.verify_explanation(True)  # +5
        state.confirm_restoration("Piece")
        state.advance_to_next_round()

    # Total score = 5 * 15 + 10 = 85 pts
    assert state.total_score == 85
    assert state.restorations_completed == 6
    assert state.is_team_winner is False


def test_max_score_and_restorations():
    """All 6 rounds perfect: 120 points and 6 restorations."""
    state = GameState()
    state.start_game("cooperative", ["P1"])

    for i in range(TOTAL_ROUNDS):
        state.submit_prediction("A", "A")
        state.submit_action("B", "B")
        state.verify_explanation(True)
        state.confirm_restoration("Piece")
        state.advance_to_next_round()

    assert state.total_score == 120
    assert state.restorations_completed == 6
    assert state.is_team_winner is True

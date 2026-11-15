"""Acceptance criteria test suite directly mirroring PRD Section 10."""

import pytest
import tempfile
from pathlib import Path
from bioguardian.engine import GameState, TOTAL_ROUNDS
from bioguardian.challenges import load_challenges
from bioguardian.storage import save_game_state, load_game_state, clear_saved_game


def test_ac_01_start_game_with_1_2_4_players():
    """AC 1: Names/defaults appear; round starts with Player 1."""
    # 1 player
    s1 = GameState()
    s1.start_game("solo", ["Aria"])
    assert s1.active_player_name == "Aria"
    assert s1.current_round_number == 1

    # 2 players
    s2 = GameState()
    s2.start_game("cooperative", ["Aria", "Ben"])
    assert s2.active_player_name == "Aria"
    assert s2.current_round_number == 1

    # 4 players
    s4 = GameState()
    s4.start_game("cooperative", ["Aria", "Ben", "Cara", "Dan"])
    assert s4.active_player_name == "Aria"
    assert s4.current_round_number == 1


def test_ac_02_20_points_awarded_for_perfect_round():
    """AC 2: Correct prediction + correct action + verified explanation = 20 points."""
    state = GameState()
    state.start_game("cooperative", ["Player 1"])
    state.submit_prediction("A", "A")
    state.submit_action("B", "B")
    state.verify_explanation(True)
    assert state.current_round_result.round_points == 20
    assert state.total_score == 20


def test_ac_03_wrong_action_first_correct_on_retry():
    """AC 3: Wrong action first, correct on retry -> 0 action points; restoration unlocks on retry."""
    state = GameState()
    state.start_game("cooperative", ["Player 1"])
    state.submit_prediction("A", "A")  # +5
    state.submit_action("C", "B")      # Wrong action: 0 pts
    assert state.current_round_result.action_correct == 0
    assert state.current_round_result.best_action_selected is False
    assert state.current_round_result.round_points == 5

    # Restoration is initially blocked
    state.confirm_restoration("Buffer strip")
    assert state.current_round_result.restoration_confirmed is False

    # Retry with correct answer
    state.retry_action("B", "B")
    assert state.current_round_result.best_action_selected is True
    # Action points must remain 0
    assert state.current_round_result.action_correct == 0
    assert state.current_round_result.round_points == 5

    # Restoration is now unlocked
    state.confirm_restoration("Buffer strip")
    assert state.current_round_result.restoration_confirmed is True


def test_ac_04_no_duplicate_points_on_double_submit_or_refresh():
    """AC 4: Submit twice / refresh after submission -> No duplicate points."""
    state = GameState()
    state.start_game("cooperative", ["Player 1"])
    state.submit_prediction("A", "A")
    state.submit_prediction("A", "A")
    state.submit_prediction("B", "A")
    state.submit_action("B", "B")
    state.submit_action("B", "B")
    state.verify_explanation(True)
    state.verify_explanation(True)
    assert state.current_round_result.round_points == 20


def test_ac_05_mark_model_changed():
    """AC 5: Mark model changed -> Restoration counter increments once; threat tile becomes completed."""
    state = GameState()
    state.start_game("cooperative", ["Player 1"])
    state.submit_action("B", "B")
    assert state.restorations_completed == 0
    assert state.current_round_result.restoration_confirmed is False

    state.confirm_restoration("Buffer piece")
    assert state.restorations_completed == 1
    assert state.current_round_result.restoration_confirmed is True

    # Confirming again does not double count
    state.confirm_restoration("Buffer piece")
    assert state.restorations_completed == 1


def test_ac_06_team_victory_95_points_4_restorations():
    """AC 6: Finish six rounds with 95 points and four restorations -> Team victory."""
    state = GameState()
    state.start_game("cooperative", ["P1"])

    # 4 perfect rounds (80 pts, 4 restorations)
    for _ in range(4):
        state.submit_prediction("A", "A")
        state.submit_action("B", "B")
        state.verify_explanation(True)
        state.confirm_restoration("Piece")
        state.advance_to_next_round()

    # Round 5: 15 pts (prediction + action, no explanation), no restoration
    state.submit_prediction("A", "A")
    state.submit_action("B", "B")
    state.advance_to_next_round()

    # Round 6: 0 pts, no restoration
    state.advance_to_next_round()

    assert state.total_score == 95
    assert state.restorations_completed == 4
    assert state.is_team_winner is True


def test_ac_07_keep_learning_100_points_3_restorations():
    """AC 7: Finish six rounds with 100 points but three restorations -> Keep Learning."""
    state = GameState()
    state.start_game("cooperative", ["P1"])

    # 5 rounds of 20 pts (100 pts), but only 3 restorations
    for i in range(5):
        state.submit_prediction("A", "A")
        state.submit_action("B", "B")
        state.verify_explanation(True)
        if i < 3:
            state.confirm_restoration("Piece")
        state.advance_to_next_round()

    # Round 6: 0 pts
    state.advance_to_next_round()

    assert state.total_score == 100
    assert state.restorations_completed == 3
    assert state.is_team_winner is False


def test_ac_08_keep_learning_85_points_6_restorations():
    """AC 8: Finish six rounds with 85 points and six restorations -> Keep Learning."""
    state = GameState()
    state.start_game("cooperative", ["P1"])

    # 5 rounds of 15 pts (75 pts) + 1 round of 10 pts = 85 pts; all 6 restored
    for i in range(TOTAL_ROUNDS):
        state.submit_prediction("A", "A")  # +5
        if i < 5:
            state.submit_action("B", "B")  # +10
        else:
            state.submit_action("C", "B")  # +0
            state.retry_action("B", "B")   # unlocks restore
            state.verify_explanation(True) # +5
        state.confirm_restoration("Piece")
        state.advance_to_next_round()

    assert state.total_score == 85
    assert state.restorations_completed == 6
    assert state.is_team_winner is False


def test_ac_09_reload_mid_game_preserves_consistent_state():
    """AC 9: Reload mid-game -> Resume at saved screen with consistent score."""
    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = Path(tmpdir) / "state.json"
        state = GameState()
        state.start_game("cooperative", ["Maya", "Leo"])
        state.current_screen = "S06_ACTION"
        state.submit_prediction("A", "A")
        save_game_state(state, save_path)

        # Reload
        reloaded = load_game_state(save_path)
        assert reloaded is not None
        assert reloaded.current_screen == "S06_ACTION"
        assert reloaded.total_score == 5
        assert reloaded.active_player_name == "Maya"
        assert reloaded.round_results[0].prediction_correct == 1


def test_ac_10_restart_game_clean_state():
    """AC 10: Restart game -> Clean new game."""
    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = Path(tmpdir) / "state.json"
        state = GameState()
        state.start_game("cooperative", ["Maya"])
        state.submit_prediction("A", "A")
        save_game_state(state, save_path)

        # Restart
        clear_saved_game(save_path)
        new_state = GameState()
        new_state.start_game("cooperative", ["Maya"])
        assert new_state.total_score == 0
        assert new_state.restorations_completed == 0
        assert new_state.current_round_index == 0


def test_ac_11_core_challenge_data_offline_availability():
    """AC 11: Challenge data is statically packaged locally with zero network dependencies."""
    challenges = load_challenges()
    assert len(challenges) == 6
    for c in challenges:
        assert c.title
        assert len(c.prediction.choices) == 3
        assert len(c.action.choices) == 3
        assert c.physical_instruction
        assert c.science_explanation

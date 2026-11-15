"""Tests for game engine, player rotation, and state management."""

import pytest
from bioguardian.engine import GameState, TOTAL_ROUNDS


def test_start_game_with_different_player_counts():
    # 1 player (Solo)
    state = GameState()
    state.start_game("solo", ["Alex"])
    assert state.mode == "solo"
    assert state.player_names == ["Alex"]
    assert state.active_player_name == "Alex"
    assert state.current_round_index == 0
    assert len(state.round_results) == 6

    # 2 players (Coop)
    state2 = GameState()
    state2.start_game("cooperative", ["Maya", "Leo"])
    assert len(state2.player_names) == 2
    assert state2.active_player_name == "Maya"

    # 4 players (Coop)
    state4 = GameState()
    state4.start_game("cooperative", ["A", "B", "C", "D"])
    assert len(state4.player_names) == 4
    assert state4.active_player_name == "A"


def test_turn_rotation_in_cooperative_mode():
    state = GameState()
    players = ["Maya", "Leo", "Sam"]
    state.start_game("cooperative", players)

    # Round 1
    assert state.active_player_name == "Maya"
    state.advance_to_next_round()

    # Round 2
    assert state.active_player_name == "Leo"
    state.advance_to_next_round()

    # Round 3
    assert state.active_player_name == "Sam"
    state.advance_to_next_round()

    # Round 4 (wraps back to Maya)
    assert state.active_player_name == "Maya"


def test_turn_in_solo_mode():
    state = GameState()
    state.start_game("solo", ["SoloPlayer"])

    for _ in range(5):
        assert state.active_player_name == "SoloPlayer"
        state.advance_to_next_round()
    assert state.active_player_name == "SoloPlayer"


def test_navigation_history():
    state = GameState()
    state.current_screen = "S04_DASHBOARD"
    state.navigate_to("S11_HELP")
    assert state.current_screen == "S11_HELP"
    assert state.previous_screen == "S04_DASHBOARD"
    state.navigate_back()
    assert state.current_screen == "S04_DASHBOARD"

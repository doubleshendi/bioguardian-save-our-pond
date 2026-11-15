"""Tests for storage, persistence, save/resume, and reset."""

import pytest
import tempfile
from pathlib import Path
from bioguardian.engine import GameState
from bioguardian.storage import save_game_state, load_game_state, has_saved_game, clear_saved_game


def test_save_and_load_state():
    with tempfile.TemporaryDirectory() as tmpdir:
        save_file = Path(tmpdir) / "state.json"

        state = GameState()
        state.start_game("cooperative", ["Maya", "Leo"])
        state.submit_prediction("A", "A")
        state.submit_action("B", "B")
        state.confirm_restoration("Buffer strip")

        # Save
        assert save_game_state(state, save_file) is True
        assert save_file.exists()

        # Load
        loaded = load_game_state(save_file)
        assert loaded is not None
        assert loaded.mode == "cooperative"
        assert loaded.player_names == ["Maya", "Leo"]
        assert loaded.current_round_index == 0
        assert loaded.total_score == 15
        assert loaded.restorations_completed == 1
        assert loaded.round_results[0].prediction_correct == 1
        assert loaded.round_results[0].action_correct == 1
        assert loaded.round_results[0].restoration_confirmed is True


def test_has_saved_game_and_clear():
    with tempfile.TemporaryDirectory() as tmpdir:
        save_file = Path(tmpdir) / "state.json"

        assert has_saved_game(save_file) is False

        state = GameState()
        state.start_game("solo", ["Solo"])
        save_game_state(state, save_file)

        assert has_saved_game(save_file) is True

        # Clear
        clear_saved_game(save_file)
        assert has_saved_game(save_file) is False

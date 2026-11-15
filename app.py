"""BioGuardian: Save Our Pond! - Main Streamlit Application."""

import streamlit as st
import sys
from pathlib import Path

# Ensure package is on sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from bioguardian.engine import GameState
from bioguardian.storage import load_game_state, save_game_state
from bioguardian.styles import render_app_header
from bioguardian.views import (
    render_s01_welcome,
    render_s02_setup,
    render_s03_instructions,
    render_s04_dashboard,
    render_s05_predict,
    render_s06_action,
    render_s07_learn,
    render_s08_restore,
    render_s09_round_result,
    render_s10_final_report,
    render_s11_help,
)

st.set_page_config(
    page_title="BioGuardian: Save Our Pond!",
    page_icon="🦆",
    layout="centered",
    initial_sidebar_state="collapsed"
)


def get_game_state() -> GameState:
    """Retrieve or initialize game state from session state or disk."""
    if "game_state" not in st.session_state:
        saved = load_game_state()
        if saved and saved.status == "in_progress":
            st.session_state.game_state = saved
        else:
            st.session_state.game_state = GameState()
    return st.session_state.game_state


def main():
    state = get_game_state()

    # Render header (disclaimer, score, turn, quick help)
    show_nav = state.current_screen not in ["S01_WELCOME"]
    render_app_header(state, show_nav=show_nav)

    # Route screens
    screen = state.current_screen

    if screen == "S01_WELCOME":
        render_s01_welcome(state)
    elif screen == "S02_SETUP":
        render_s02_setup(state)
    elif screen == "S03_INSTRUCTIONS":
        render_s03_instructions(state)
    elif screen == "S04_DASHBOARD":
        render_s04_dashboard(state)
    elif screen == "S05_PREDICT":
        render_s05_predict(state)
    elif screen == "S06_ACTION":
        render_s06_action(state)
    elif screen == "S07_LEARN":
        render_s07_learn(state)
    elif screen == "S08_RESTORE":
        render_s08_restore(state)
    elif screen == "S09_ROUND_RESULT":
        render_s09_round_result(state)
    elif screen == "S10_FINAL_REPORT":
        render_s10_final_report(state)
    elif screen == "S11_HELP":
        render_s11_help(state)
    else:
        state.current_screen = "S01_WELCOME"
        render_s01_welcome(state)


if __name__ == "__main__":
    main()

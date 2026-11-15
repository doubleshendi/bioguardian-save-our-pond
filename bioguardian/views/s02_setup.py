"""S02: Game Setup Screen."""

import streamlit as st
from bioguardian.engine import GameState
from bioguardian.storage import save_game_state


def render_s02_setup(state: GameState):
    st.markdown("<h2>⚙️ Game Setup</h2>", unsafe_allow_html=True)
    st.caption("Configure your team and player roles. All data stays local on this device.")

    mode = st.radio(
        "Select Game Mode:",
        options=["Cooperative Team (1–4 Players)", "Solo Explorer (1 Player)"],
        index=0 if state.mode == "cooperative" else 1,
        help="Cooperative mode pools points into a shared score and rotates the active Decision Maker each round."
    )
    chosen_mode = "cooperative" if "Cooperative" in mode else "solo"

    num_players = 1
    if chosen_mode == "cooperative":
        num_players = st.slider("Number of Players:", min_value=1, max_value=4, value=len(state.player_names) if len(state.player_names) <= 4 else 2)

    st.markdown("#### Player Nicknames")
    st.markdown("<p style='font-size:0.85rem; color:#64748b;'>Use first names or nicknames only (e.g. Leo, Maya, Player 1). No personal data is stored.</p>", unsafe_allow_html=True)

    player_names = []
    cols = st.columns(2) if num_players > 1 else [st.container()]
    for i in range(num_players):
        col = cols[i % len(cols)] if isinstance(cols, list) else cols
        default_name = state.player_names[i] if i < len(state.player_names) else f"Player {i+1}"
        with col:
            name = st.text_input(
                f"Player {i+1} Name:",
                value=default_name,
                key=f"player_name_input_{i}",
                placeholder=f"Player {i+1}"
            )
            player_names.append(name.strip() if name.strip() else f"Player {i+1}")

    st.markdown("<br/>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🌱 Start Conservation Journey", key="setup_start_btn", type="primary", use_container_width=True):
            state.start_game(chosen_mode, player_names)
            save_game_state(state)
            state.navigate_to("S03_INSTRUCTIONS")
            st.rerun()
    with col2:
        if st.button("⬅️ Back", key="setup_back_btn", use_container_width=True):
            state.navigate_to("S01_WELCOME")
            st.rerun()

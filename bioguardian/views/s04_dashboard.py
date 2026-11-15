"""S04: Pond Dashboard Screen."""

import streamlit as st
from bioguardian.engine import GameState, TOTAL_ROUNDS, MAX_TOTAL_POINTS
from bioguardian.challenges import load_challenges
from bioguardian.storage import clear_saved_game, save_game_state


def render_s04_dashboard(state: GameState):
    challenges = load_challenges()

    st.markdown("<h2>🏞️ Pond Habitat Dashboard</h2>", unsafe_allow_html=True)

    # Top progress and scoreboard
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Progress",
            value=f"Round {state.current_round_number} of {TOTAL_ROUNDS}",
            delta=f"{TOTAL_ROUNDS - state.current_round_number} remaining" if state.current_round_number <= TOTAL_ROUNDS else "Complete"
        )
    with col2:
        st.metric(
            label="Team Score",
            value=f"{state.total_score} / {MAX_TOTAL_POINTS} pts",
            help="Target for team victory: 90+ pts"
        )
    with col3:
        st.metric(
            label="Restorations",
            value=f"{state.restorations_completed} / {TOTAL_ROUNDS} pieces",
            help="Target for team victory: 4+ restorations"
        )

    st.markdown("<hr style='margin: 12px 0 16px 0;'/>", unsafe_allow_html=True)
    st.markdown("#### 📋 6 Habitat Scenarios & Physical Model Status")

    # Display 6 challenge status tiles in 2 columns
    col_left, col_right = st.columns(2)
    for idx, challenge in enumerate(challenges):
        col = col_left if idx % 2 == 0 else col_right
        rr = state.round_results[idx]
        is_current = (idx == state.current_round_index and state.status == "in_progress")
        is_completed = rr.restoration_confirmed
        is_past = idx < state.current_round_index

        tile_class = "threat-tile-completed" if is_completed else "threat-tile-warning"
        current_class = "threat-tile-current" if is_current else ""
        status_badge = (
            "<span style='color: #15803d; font-weight: 700;'>✅ Planned / Demonstrated</span>"
            if is_completed else
            "<span style='color: #b45309; font-weight: 700;'>⚠️ Active Threat</span>"
        )

        with col:
            st.markdown(f"""
            <div class="threat-tile {tile_class} {current_class}">
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-size: 1.3rem;'>{challenge.icon} <strong>{challenge.card_code}</strong></span>
                    <span style='font-size: 0.8rem;'>{status_badge}</span>
                </div>
                <div style='font-size: 0.95rem; font-weight: 600; margin: 4px 0;'>{challenge.title}</div>
                <div style='font-size: 0.8rem; opacity: 0.85;'>
                    {'Model Restored' if is_completed else f'Physical Piece: {challenge.threat_marker}'}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Main action button
    if state.status == "in_progress" and state.current_round_index < TOTAL_ROUNDS:
        current_challenge = challenges[state.current_round_index]
        button_text = f"▶️ Begin Round {state.current_round_number}: {current_challenge.title}"
        if st.button(button_text, key="dashboard_begin_round", type="primary", use_container_width=True):
            state.navigate_to("S05_PREDICT")
            save_game_state(state)
            st.rerun()
    elif state.status == "complete" or state.current_round_index >= TOTAL_ROUNDS:
        if st.button("🏆 View Final Team Report", key="dashboard_view_report", type="primary", use_container_width=True):
            state.navigate_to("S10_FINAL_REPORT")
            st.rerun()

    # Reset game with safety confirmation
    st.markdown("<br/><hr style='margin: 16px 0;'/>", unsafe_allow_html=True)
    if not state.show_restart_confirm:
        col_res1, col_res2 = st.columns([1, 1])
        with col_res1:
            if st.button("🔄 Restart Game", key="dashboard_restart_prompt", use_container_width=True):
                state.show_restart_confirm = True
                st.rerun()
        with col_res2:
            if st.button("📖 Rules & Help", key="dashboard_rules_btn", use_container_width=True):
                state.navigate_to("S11_HELP")
                st.rerun()
    else:
        st.warning("⚠️ Are you sure you want to restart? All current scores and restorations will be reset.")
        col_y, col_n = st.columns(2)
        with col_y:
            if st.button("Yes, Reset Game", key="confirm_reset_yes", type="primary", use_container_width=True):
                clear_saved_game()
                state.start_game(state.mode, state.player_names)
                state.show_restart_confirm = False
                state.navigate_to("S01_WELCOME")
                st.rerun()
        with col_n:
            if st.button("Cancel", key="confirm_reset_no", use_container_width=True):
                state.show_restart_confirm = False
                st.rerun()

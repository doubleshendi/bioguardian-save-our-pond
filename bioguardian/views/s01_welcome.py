"""S01: Welcome Screen."""

import streamlit as st
from bioguardian.engine import GameState
from bioguardian.storage import has_saved_game, load_game_state, save_game_state


def render_s01_welcome(state: GameState):
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <div style='font-size: 3.5rem; margin-bottom: 8px;'>🦆 🌿 🌊</div>
        <h1 style='margin: 0; color: #1b4332; font-size: 2.2rem;'>BioGuardian</h1>
        <h3 style='margin: 4px 0 16px 0; color: #2d6a4f; font-weight: 500;'>Save Our Pond!</h3>
        <p style='color: #4b5563; font-size: 1.05rem; max-width: 540px; margin: auto;'>
            An interactive tabletop conservation game for FIRST LEGO League (FLL) teams and young scientists.
            Predict ecosystem impacts, choose conservation actions, explain the science, and physically restore the pond model!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="status-card" style='border-left: 5px solid #0284c7;'>
        <h4 style='margin-top:0;'>🎯 Mission Overview</h4>
        <ul style='margin-bottom:0; padding-left: 20px; color: #334155;'>
            <li><strong>6 Conservation Rounds:</strong> Fertilizer, Invasives, Pollinators, Litter, Shoreline, Sediment.</li>
            <li><strong>Cooperative Play:</strong> 1 to 4 players collaborate and rotate turns.</li>
            <li><strong>Physical Model:</strong> Update the 24" &times; 36" pond habitat with matching pieces.</li>
            <li><strong>Winning Goal:</strong> Score <strong>90+ points</strong> and complete <strong>4+ physical restorations</strong>!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 New Game", key="welcome_new_game", use_container_width=True, type="primary"):
            state.navigate_to("S02_SETUP")
            st.rerun()

    with col2:
        if st.button("📖 How to Play", key="welcome_how_to_play", use_container_width=True):
            state.navigate_to("S03_INSTRUCTIONS")
            st.rerun()

    saved_exists = has_saved_game()
    if saved_exists:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.info("💾 A saved game in progress was found.")
        if st.button("▶️ Resume Saved Game", key="welcome_resume_game", use_container_width=True):
            loaded = load_game_state()
            if loaded:
                for k, v in loaded.__dict__.items():
                    setattr(state, k, v)
                state.current_screen = "S04_DASHBOARD"
                save_game_state(state)
                st.rerun()

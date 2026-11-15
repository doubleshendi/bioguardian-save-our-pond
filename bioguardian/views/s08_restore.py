"""S08: Restore Physical Model Screen (Step 4 of 4)."""

import streamlit as st
from bioguardian.engine import GameState
from bioguardian.challenges import get_challenge_by_round
from bioguardian.storage import save_game_state


def render_s08_restore(state: GameState):
    challenge = get_challenge_by_round(state.current_round_number)
    if not challenge:
        st.error("Challenge not found.")
        return

    rr = state.current_round_result

    st.markdown(f"<div class='step-indicator'>Round {state.current_round_number} of 6 — Step 4 of 4</div>", unsafe_allow_html=True)
    st.markdown(f"<h2>🧩 Modify the Physical Pond Model</h2>", unsafe_allow_html=True)

    # Physical pieces instruction box
    st.markdown(f"""
    <div class="physical-box">
        <h4 style='margin-top:0; color:#581c87;'>🛠️ Tabletop Modification Instructions</h4>
        <div style='margin-bottom: 8px;'>
            <strong>1. Remove Problem Marker:</strong> <span style='background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:4px;'>{challenge.threat_marker}</span>
        </div>
        <div style='margin-bottom: 8px;'>
            <strong>2. Attach Solution Piece:</strong> <span style='background:#dcfce7; color:#166534; padding:2px 8px; border-radius:4px;'>{challenge.solution_piece}</span>
        </div>
        <div style='margin-top: 10px; font-size: 0.95rem; font-style: italic; color: #4c1d95;'>
            &ldquo;{challenge.physical_instruction}&rdquo;
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Educational science caveat banner
    st.markdown("""
    <div class="edu-disclaimer" style='border-left-color: #0284c7; background: #f0f9ff; color: #0369a1;'>
        💡 <strong>Scientific Practice Note:</strong> This physical change demonstrates a <em>planned conservation intervention</em>.
        In real-world ecology, recovery takes time and requires ongoing environmental testing.
    </div>
    """, unsafe_allow_html=True)

    # Model change confirmation
    st.markdown("### Model Confirmation")
    if not rr.restoration_confirmed:
        st.markdown(f"<p style='color:#334155;'>Once the physical model piece has been attached on the tabletop by <strong>{state.active_player_name}</strong> or the team, press the button below:</p>", unsafe_allow_html=True)
        if st.button("✅ I Changed the Model!", key="confirm_model_changed_btn", type="primary", use_container_width=True):
            state.confirm_restoration(challenge.solution_piece)
            save_game_state(state)
            st.rerun()
    else:
        st.success(f"🎉 **Restoration Demonstrated!** Model piece &ldquo;{rr.physical_pieces_changed}&rdquo; recorded. Threat marker is now resolved.")
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("View Round Results ➡️", key="restore_to_results_btn", type="primary", use_container_width=True):
            state.navigate_to("S09_ROUND_RESULT")
            save_game_state(state)
            st.rerun()

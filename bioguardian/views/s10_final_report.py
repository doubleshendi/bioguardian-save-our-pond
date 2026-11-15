"""S10: Final Report & Learning Assessment Screen."""

import streamlit as st
import pandas as pd
from bioguardian.engine import (
    GameState, TOTAL_ROUNDS, MAX_TOTAL_POINTS,
    WIN_POINTS_THRESHOLD, WIN_RESTORATIONS_THRESHOLD
)
from bioguardian.challenges import load_challenges
from bioguardian.storage import clear_saved_game


def render_s10_final_report(state: GameState):
    challenges = load_challenges()
    is_winner = state.is_team_winner
    total_score = state.total_score
    restorations = state.restorations_completed

    st.markdown("<h2>🏆 Final Game Report & Learning Summary</h2>", unsafe_allow_html=True)

    # Victory or Keep Learning Banner
    if is_winner:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #166534, #15803d); color: white; border-radius: 12px; padding: 22px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3rem; margin-bottom: 8px;'>🌟 🦆 🌿</div>
            <h2 style='color: white; margin: 0 0 6px 0;'>Team Victory! Pond Habitat Stewards</h2>
            <p style='font-size: 1.15rem; margin: 0 0 12px 0;'>
                Congratulations! You met both conservation criteria: <strong>{total_score}/{MAX_TOTAL_POINTS} points</strong> (target &ge; {WIN_POINTS_THRESHOLD}) and <strong>{restorations}/{TOTAL_ROUNDS} physical restorations</strong> (target &ge; {WIN_RESTORATIONS_THRESHOLD})!
            </p>
            <p style='font-size: 0.9rem; opacity: 0.9; margin: 0;'>
                You demonstrated deep scientific understanding of freshwater runoff, invasive management, pollinator resources, and erosion control.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        reasons = []
        if total_score < WIN_POINTS_THRESHOLD:
            reasons.append(f"Score was {total_score} pts (needed {WIN_POINTS_THRESHOLD}+ pts)")
        if restorations < WIN_RESTORATIONS_THRESHOLD:
            reasons.append(f"Completed {restorations} restorations (needed {WIN_RESTORATIONS_THRESHOLD}+ restorations)")
        reason_str = " and ".join(reasons)

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #b45309, #d97706); color: white; border-radius: 12px; padding: 22px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3rem; margin-bottom: 8px;'>🌱 📖 💡</div>
            <h2 style='color: white; margin: 0 0 6px 0;'>Keep Learning! Pond Care in Progress</h2>
            <p style='font-size: 1.1rem; margin: 0 0 10px 0;'>
                Good collaborative effort! You achieved <strong>{total_score}/{MAX_TOTAL_POINTS} points</strong> and <strong>{restorations}/{TOTAL_ROUNDS} restorations</strong>.
            </p>
            <p style='font-size: 0.95rem; background: rgba(0,0,0,0.15); padding: 8px; border-radius: 6px; margin: 0 0 10px 0;'>
                <strong>To achieve Team Victory:</strong> {reason_str}.
            </p>
            <p style='font-size: 0.88rem; opacity: 0.9; margin: 0;'>
                Review the science cards, discuss why buffer strips and stabilized slopes protect waterways, and try another collaborative round!
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Performance Breakdown Table
    st.markdown("### 📋 6-Round Comprehensive Scorecard")

    table_data = []
    for idx, c in enumerate(challenges):
        rr = state.round_results[idx]
        pred_p = 5 if rr.prediction_correct else 0
        act_p = 10 if rr.action_correct else 0
        exp_p = 5 if rr.explanation_verified else 0
        tot_p = pred_p + act_p + exp_p
        table_data.append({
            "Round": f"R{idx+1}",
            "Scenario": c.title,
            "Decision Maker": rr.player_name,
            "Prediction": f"{pred_p} pts ({'✓' if pred_p else '✗'})",
            "Action (1st)": f"{act_p} pts ({'✓' if act_p else '✗'})",
            "Explanation": f"{exp_p} pts ({'✓' if exp_p else '✗'})",
            "Restored?": "✅ Yes" if rr.restoration_confirmed else "❌ No",
            "Total": f"{tot_p} / 20"
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Key Science Takeaways
    with st.expander("🔬 Core Science Takeaways for Judges & Classrooms", expanded=True):
        st.markdown("""
        1. **Vegetated Buffer Strips:** Help slow overland runoff and filter out excess nutrients before entering the pond.
        2. **Invasive Plant Management:** Requires verification, proper protocols, and replanting of native sedges/grasses.
        3. **Pollinator Habitat:** Native flowering plants provide crucial nectar, pollen, and overwintering shelters.
        4. **Shoreline Litter:** Physical removal prevents ingestion, entanglement, and chemical breakdown into microplastics.
        5. **Shoreline Stabilization:** Native root systems hold soils together, mitigating wave erosion and offering amphibian shelter.
        6. **Sediment Management:** Stabilizing bare slopes prevents muddy runoff that reduces light penetration and smothers fish habitats.
        """)

    # Demonstration script for FLL judges
    with st.expander("🎙️ Physical Demonstration & Judge Script Guide", expanded=False):
        st.markdown("""
        **For the FLL Student Presenter:**
        1. Point out the tabletop model: *"Judges, our tabletop model began with 6 active environmental threats."*
        2. Explain the physical change: *"When our app evaluated the correct conservation action, we swapped the threat marker for a native solution piece."*
        3. State the science limitation honestly: *"Importantly, our physical model demonstrates a planned conservation strategy, not immediate biological recovery, which requires repeated long-term water testing."*
        """)

    st.markdown("<br/>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Another Game", key="final_play_again", type="primary", use_container_width=True):
            clear_saved_game()
            state.start_game(state.mode, state.player_names)
            state.navigate_to("S04_DASHBOARD")
            st.rerun()

    with col2:
        if st.button("⬅️ Return to Pond Dashboard", key="final_to_dashboard", use_container_width=True):
            state.navigate_to("S04_DASHBOARD")
            st.rerun()

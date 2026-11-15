"""S09: Round Results Screen."""

import streamlit as st
from bioguardian.engine import GameState, TOTAL_ROUNDS, MAX_TOTAL_POINTS, MAX_ROUND_POINTS
from bioguardian.challenges import get_challenge_by_round
from bioguardian.storage import save_game_state


def render_s09_round_result(state: GameState):
    challenge = get_challenge_by_round(state.current_round_number)
    rr = state.current_round_result

    st.markdown(f"<div class='step-indicator'>Round {state.current_round_number} of 6 Completed!</div>", unsafe_allow_html=True)
    st.markdown(f"<h2>📊 Round {state.current_round_number} Scorecard</h2>", unsafe_allow_html=True)

    # Score breakdown card
    pred_pts = 5 if rr.prediction_correct else 0
    act_pts = 10 if rr.action_correct else 0
    exp_pts = 5 if rr.explanation_verified else 0
    round_pts = pred_pts + act_pts + exp_pts

    st.markdown(f"""
    <div class="status-card" style='border-top: 4px solid #15803d;'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <h4 style='margin:0;'>{challenge.icon} {challenge.title}</h4>
            <span style='background:#15803d; color:white; padding:4px 12px; border-radius:12px; font-weight:700;'>
                {round_pts} / {MAX_ROUND_POINTS} pts
            </span>
        </div>
        <p style='color:#64748b; font-size:0.9rem; margin: 4px 0 12px 0;'>Decision Maker: <strong>{rr.player_name}</strong></p>
        <hr style='margin:8px 0;'/>
        <div style='display:grid; grid-template-columns: 1fr auto; row-gap: 8px; font-size: 0.95rem;'>
            <div>🔮 Prediction Challenge (First Attempt):</div>
            <div><strong>+{pred_pts} pts</strong> {'✅' if pred_pts else '❌'}</div>
            
            <div>🛡️ Conservation Action (First Attempt):</div>
            <div><strong>+{act_pts} pts</strong> {'✅' if act_pts else '❌'}</div>
            
            <div>🗣️ Scientific Explanation Verified:</div>
            <div><strong>+{exp_pts} pts</strong> {'✅' if exp_pts else '❌'}</div>
            
            <div style='font-weight:700; border-top:1px solid #e2e8f0; padding-top:6px;'>Total Earned This Round:</div>
            <div style='font-weight:700; border-top:1px solid #e2e8f0; padding-top:6px; color:#15803d;'>+{round_pts} pts</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Physical restoration badge
    if rr.restoration_confirmed:
        st.markdown(f"""
        <div style='background:#f0fdf4; border:1px solid #86efac; border-radius:8px; padding:10px 14px; margin-bottom:16px;'>
            ✅ <strong>Physical Model Restoration: Completed!</strong><br/>
            <span style='font-size:0.88rem; color:#166534;'>{challenge.solution_piece} successfully attached.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:10px 14px; margin-bottom:16px;'>
            ⏳ <strong>Physical Model Restoration: Not Completed.</strong>
        </div>
        """, unsafe_allow_html=True)

    # Cumulative standing
    st.markdown(f"""
    <div style='text-align:center; padding:10px; background:#f8fafc; border-radius:8px;'>
        <span style='color:#475569;'>Current Team Cumulative Score:</span><br/>
        <span style='font-size:1.6rem; font-weight:800; color:#0f766e;'>{state.total_score} / {MAX_TOTAL_POINTS} pts</span>
        <span style='color:#64748b; font-size:0.9rem;'> &bull; {state.restorations_completed}/6 Restorations</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    is_last_round = (state.current_round_index >= TOTAL_ROUNDS - 1)
    btn_label = "🏆 Finish Game & View Final Report" if is_last_round else f"➡️ Advance to Round {state.current_round_number + 1}"

    if st.button(btn_label, key="round_result_next_btn", type="primary", use_container_width=True):
        state.advance_to_next_round()
        save_game_state(state)
        st.rerun()

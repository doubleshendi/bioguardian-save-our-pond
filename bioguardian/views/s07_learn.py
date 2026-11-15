"""S07: Learn & Explain Screen (Step 3 of 4)."""

import streamlit as st
from bioguardian.engine import GameState
from bioguardian.challenges import get_challenge_by_round
from bioguardian.storage import save_game_state


def render_s07_learn(state: GameState):
    challenge = get_challenge_by_round(state.current_round_number)
    if not challenge:
        st.error("Challenge not found.")
        return

    rr = state.current_round_result

    st.markdown(f"<div class='step-indicator'>Round {state.current_round_number} of 6 — Step 3 of 4</div>", unsafe_allow_html=True)
    st.markdown(f"<h2>🔬 Science Behind the Solution</h2>", unsafe_allow_html=True)

    correct_choice = next(c for c in challenge.action.choices if c.id == challenge.action.correct_id)

    # Science Explanation Card
    st.markdown(f"""
    <div class="status-card" style='border-left: 4px solid #10b981; background: #ecfdf5;'>
        <h4 style='margin-top:0; color:#065f46;'>🌱 Recommended Action: {correct_choice.id}. {correct_choice.text}</h4>
        <p style='font-size:1.02rem; color:#047857; margin-bottom: 8px;'>
            <strong>Scientific Mechanism:</strong> {challenge.science_explanation}
        </p>
        <p style='font-size:0.88rem; color:#065f46; margin:0;'>
            <em>Note: Ecological responses vary in nature; conservation actions may reduce pressure or support habitats, but outcomes must be monitored rather than guaranteed.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Real-life verification box
    st.markdown(f"""
    <div class="status-card" style='border-left: 4px solid #3b82f6;'>
        <h5 style='margin-top:0; color:#1e40af;'>🔍 How to Verify in Real Life</h5>
        <p style='margin:0; font-size:0.95rem; color:#1e3a8a;'>{challenge.real_life_verification}</p>
    </div>
    """, unsafe_allow_html=True)

    # Explanation checklist (+5 pts)
    st.markdown("### 🗣️ Explain Why It Works (+5 pts)")
    verifier_label = "Peer or Facilitator Check:" if state.mode == "cooperative" else "Self-Check Reflection:"
    st.markdown(f"<p style='color:#334155; font-size:0.95rem;'><strong>{verifier_label}</strong> Have the Decision Maker ({state.active_player_name}) explain aloud in their own words how this conservation action protects the pond ecosystem.</p>", unsafe_allow_html=True)

    verified_checked = st.checkbox(
        "✅ Explanation Verified: The reasoning clearly connects the conservation action to habitat protection (+5 pts)",
        value=bool(rr.explanation_verified),
        key=f"explain_checkbox_round_{state.current_round_number}"
    )

    if verified_checked != bool(rr.explanation_verified):
        state.verify_explanation(verified_checked)
        save_game_state(state)
        st.rerun()

    # Retry Section if first attempt was incorrect
    if not rr.action_correct and not rr.best_action_selected:
        st.markdown("<hr style='margin: 16px 0;'/>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background: #fffbeb; border: 2px solid #f59e0b; border-radius: 10px; padding: 14px;'>
            <h4 style='margin:0 0 6px 0; color:#b45309;'>🔄 Retry Opportunity to Unlock Physical Model Restoration</h4>
            <p style='margin:0 0 10px 0; font-size:0.9rem; color:#92400e;'>
                Your first attempt was recorded (0 pts for action). To unlock the physical model restoration piece, choose the best conservation action now:
            </p>
        </div>
        """, unsafe_allow_html=True)

        choice_labels = [f"{c.id}. {c.text}" for c in challenge.action.choices]
        choice_map = {f"{c.id}. {c.text}": c.id for c in challenge.action.choices}

        retry_choice = st.radio(
            "Select the best conservation response:",
            options=choice_labels,
            key=f"retry_radio_round_{state.current_round_number}"
        )
        retry_id = choice_map[retry_choice]

        if st.button("Submit Retry Selection", key="submit_retry_btn", type="secondary", use_container_width=True):
            is_ok = state.retry_action(retry_id, challenge.action.correct_id)
            save_game_state(state)
            if is_ok:
                st.success("✅ Excellent! You identified the best action. Physical model restoration is now UNLOCKED!")
            else:
                st.error("That's still not the recommended action. Review the science explanation card above!")
            st.rerun()

    # Navigation to S08: Restore Model
    st.markdown("<br/>", unsafe_allow_html=True)
    if rr.best_action_selected:
        if st.button("Proceed to Physical Pond Restoration ➡️", key="learn_to_restore_btn", type="primary", use_container_width=True):
            state.navigate_to("S08_RESTORE")
            save_game_state(state)
            st.rerun()
    else:
        st.info("🔒 **Physical Restoration Locked:** Please select the correct conservation action in the retry section above to unlock the tabletop model change.")

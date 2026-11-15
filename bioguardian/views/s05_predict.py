"""S05: Threat & Prediction Screen (Step 1 of 4)."""

import streamlit as st
from bioguardian.engine import GameState
from bioguardian.challenges import get_challenge_by_round
from bioguardian.storage import save_game_state


def render_s05_predict(state: GameState):
    challenge = get_challenge_by_round(state.current_round_number)
    if not challenge:
        st.error("Challenge not found.")
        return

    rr = state.current_round_result

    st.markdown(f"<div class='step-indicator'>Round {state.current_round_number} of 6 — Step 1 of 4</div>", unsafe_allow_html=True)
    st.markdown(f"<h2>{challenge.icon} {challenge.title}</h2>", unsafe_allow_html=True)

    # Physical card match reminder
    st.markdown(f"""
    <div class="card-match-box">
        🃏 <strong>Tabletop Card Match:</strong> Please take out <strong>{challenge.card_code}: {challenge.title}</strong> and inspect the problem on the model.
    </div>
    """, unsafe_allow_html=True)

    # Threat scenario
    st.markdown("""
    <div class="status-card" style='border-left: 4px solid #ef4444;'>
        <h4 style='margin-top:0; color:#b91c1c;'>⚠️ Threat Scenario</h4>
        <p style='margin:0; font-size:1.05rem; color:#1f2937;'>""" + challenge.threat_story + """</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### ❓ Prediction Challenge (+5 pts)")
    st.markdown(f"**{challenge.prediction.prompt}**")

    # Options
    choice_labels = [f"{c.id}. {c.text}" for c in challenge.prediction.choices]
    choice_map = {f"{c.id}. {c.text}": c.id for c in challenge.prediction.choices}

    # If already submitted, pre-select their first answer
    default_idx = 0
    if rr.submitted_prediction and rr.prediction_first_answer:
        for idx, c in enumerate(challenge.prediction.choices):
            if c.id == rr.prediction_first_answer:
                default_idx = idx
                break

    selected_choice_label = st.radio(
        "Select your prediction:",
        options=choice_labels,
        index=default_idx,
        disabled=rr.submitted_prediction,
        key=f"predict_radio_round_{state.current_round_number}"
    )
    selected_id = choice_map[selected_choice_label]

    if not rr.submitted_prediction:
        if st.button("Submit Prediction (+5 pts)", key="predict_submit_btn", type="primary", use_container_width=True):
            state.submit_prediction(selected_id, challenge.prediction.correct_id)
            save_game_state(state)
            st.rerun()
    else:
        # Show outcome
        if rr.prediction_correct:
            st.success(f"🎉 **Correct Prediction! (+5 pts)** You predicted: {rr.prediction_first_answer}. Excellent ecological insight!")
        else:
            correct_choice = next(c for c in challenge.prediction.choices if c.id == challenge.prediction.correct_id)
            st.warning(f"🧐 **Good Try! (+0 pts)** You selected {rr.prediction_first_answer}. The primary ecological effect is: **{correct_choice.id}. {correct_choice.text}**.")

        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Next: Choose Conservation Action ➡️", key="predict_to_action_btn", type="primary", use_container_width=True):
            state.navigate_to("S06_ACTION")
            save_game_state(state)
            st.rerun()

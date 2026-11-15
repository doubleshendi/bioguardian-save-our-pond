"""S06: Choose Conservation Action Screen (Step 2 of 4)."""

import streamlit as st
from bioguardian.engine import GameState
from bioguardian.challenges import get_challenge_by_round
from bioguardian.storage import save_game_state


def render_s06_action(state: GameState):
    challenge = get_challenge_by_round(state.current_round_number)
    if not challenge:
        st.error("Challenge not found.")
        return

    rr = state.current_round_result

    st.markdown(f"<div class='step-indicator'>Round {state.current_round_number} of 6 — Step 2 of 4</div>", unsafe_allow_html=True)
    st.markdown(f"<h2>🛡️ Take Action: {challenge.title}</h2>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card-match-box">
        👤 <strong>Decision Maker:</strong> {state.active_player_name} leads the team in selecting the conservation response.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### ❓ Action Challenge (+10 pts)")
    st.markdown(f"**{challenge.action.prompt}**")

    choice_labels = [f"{c.id}. {c.text}" for c in challenge.action.choices]
    choice_map = {f"{c.id}. {c.text}": c.id for c in challenge.action.choices}

    default_idx = 0
    if rr.submitted_action and rr.action_first_answer:
        for idx, c in enumerate(challenge.action.choices):
            if c.id == rr.action_first_answer:
                default_idx = idx
                break

    selected_choice_label = st.radio(
        "Select your conservation response:",
        options=choice_labels,
        index=default_idx,
        disabled=rr.submitted_action,
        key=f"action_radio_round_{state.current_round_number}"
    )
    selected_id = choice_map[selected_choice_label]

    if not rr.submitted_action:
        if st.button("Submit Conservation Action (+10 pts)", key="action_submit_btn", type="primary", use_container_width=True):
            state.submit_action(selected_id, challenge.action.correct_id)
            save_game_state(state)
            st.rerun()
    else:
        if rr.action_correct:
            st.success(f"🎉 **Great Decision! (+10 pts)** Choice {rr.action_first_answer} is the recommended conservation response.")
        else:
            st.warning(f"🤔 **Not quite the best action (+0 pts on first try).** In Step 3, you will explore the science mechanism and can retry for free to discover the best action!")

        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Proceed to Science Explanation & Verification ➡️", key="action_to_learn_btn", type="primary", use_container_width=True):
            state.navigate_to("S07_LEARN")
            save_game_state(state)
            st.rerun()

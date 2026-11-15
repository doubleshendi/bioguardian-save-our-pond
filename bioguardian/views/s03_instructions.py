"""S03: Instructions & How to Play Screen."""

import streamlit as st
from bioguardian.engine import GameState


def render_s03_instructions(state: GameState):
    st.markdown("<h2>📖 How to Play BioGuardian</h2>", unsafe_allow_html=True)
    st.markdown("<div class='step-indicator'>Rules & Model Synchronization Guide</div>", unsafe_allow_html=True)

    with st.expander("🧩 Physical Model & Materials Checklist", expanded=True):
        st.markdown("""
        Prepare your tabletop model area:
        - **24" &times; 36" Tabletop Pond Model:** Includes lawn, shoreline, slope, and water sections.
        - **6 Physical Threat Markers:** Place all 6 problem markers on the model at setup (Fertilizer, Invasive Weed, Missing Flowers, Litter Debris, Bare Shore, Bare Slope).
        - **6 Solution Pieces:** Keep nearby ready to attach (Native Buffer Strip, Native Plant piece, Flower patch & Pollinators, Waste Bin & Sign, Planted Shore Panel, Stabilized Slope).
        - **6 Printed Challenge Cards:** Numbered #1 to #6 matching each round.
        """)

    st.markdown("""
    <div class="status-card">
        <h4 style='margin-top:0;'>🔄 6-Step Round Flow</h4>
        <ol style='padding-left: 20px; line-height: 1.6; color: #1e293b;'>
            <li><strong>Match Physical Card:</strong> Find the matching physical challenge card (#1 to #6).</li>
            <li><strong>Predict Consequence (+5 pts):</strong> Read the threat scenario and predict the ecological effect. (First attempt scored).</li>
            <li><strong>Choose Conservation Action (+10 pts):</strong> Pick the best conservation response. (First attempt scored).</li>
            <li><strong>Explain the Mechanism (+5 pts):</strong> Explain aloud why the action helps. Have a teammate or facilitator verify your explanation.</li>
            <li><strong>Modify the Pond Model:</strong> Remove the threat marker from the physical model and attach the restoration solution piece.</li>
            <li><strong>Confirm Model Changed:</strong> Tap <em>"I changed the model"</em> in the app to record your restoration badge.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div style='background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px;'>
            <h5 style='margin:0 0 6px 0; color:#166534;'>🏆 Winning Conditions</h5>
            <ul style='font-size:0.88rem; margin:0; padding-left:18px; color:#166534;'>
                <li>Score at least <strong>90 / 120 points</strong></li>
                <li>Complete at least <strong>4 / 6 physical restorations</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div style='background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px;'>
            <h5 style='margin:0 0 6px 0; color:#92400e;'>💡 Learning & Retry Rule</h5>
            <p style='font-size:0.85rem; margin:0; color:#92400e;'>
                If you select an incorrect action, first-attempt points are locked (0 pts), but you can <strong>retry for free</strong> to discover the best action and unlock physical model restoration!
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🌊 Ready! Go to Pond Dashboard", key="instructions_to_dashboard", type="primary", use_container_width=True):
            state.navigate_to("S04_DASHBOARD")
            st.rerun()
    with col2:
        if st.button("⬅️ Back", key="instructions_back", use_container_width=True):
            state.navigate_back()
            st.rerun()

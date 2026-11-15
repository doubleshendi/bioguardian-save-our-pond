"""S11: Help, Glossary & Field Safety Screen."""

import streamlit as st
from bioguardian.engine import GameState


def render_s11_help(state: GameState):
    st.markdown("<h2>❓ Help & Reference Guide</h2>", unsafe_allow_html=True)

    if st.button("⬅️ Return to Previous Screen", key="help_back_btn", type="primary"):
        state.navigate_back()
        st.rerun()

    st.markdown("<hr style='margin: 12px 0;'/>", unsafe_allow_html=True)

    st.markdown("### 📚 Environmental Glossary")
    st.markdown("""
    - **Buffer Strip:** A permanent band of native vegetation (grasses, shrubs, trees) positioned between human-managed land (like lawns or farms) and a body of water to filter runoff and slow erosion.
    - **Runoff:** Water from rain or snowmelt that flows over land surfaces, carrying dissolved fertilizers, oils, and sediment into waterways.
    - **Invasive Species:** Non-native organisms that spread rapidly and aggressively, often displacing native plants and degrading wildlife habitats.
    - **Suspended Sediment:** Fine soil particles floating in the water column that block sunlight for submerged plants and clog fish gills.
    - **Eutrophication:** Excessive nutrient enrichment (especially nitrogen and phosphorus) that leads to dense algae growth and low dissolved oxygen levels.
    """)

    st.markdown("### 🦺 Field Safety & Best Practices")
    st.markdown("""
    When conducting real-world citizen science or pond surveys:
    1. **Adult Supervision:** Always visit water bodies with an adult facilitator or teacher.
    2. **Personal Protective Equipment:** Wear closed-toe waterproof footwear and rubber gloves when handling water or litter samples.
    3. **Respect Wildlife:** Observe animals from a safe distance; never capture or disrupt nesting birds, frogs, or turtles.
    4. **Chemical Testing Kits:** Handle test strips and indicator reagents strictly following manufacturer safety protocols.
    """)

    st.markdown("### 🔬 Scientific Integrity & Caveats")
    st.markdown("""
    <div class="edu-disclaimer">
        <strong>Important Distinction:</strong> In BioGuardian, scores represent educational mastery of conservation concepts.
        In nature, ecological restoration is a gradual biological process requiring ongoing chemical and biological monitoring, not instant digital success.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("⬅️ Back to Game", key="help_bottom_back_btn", use_container_width=True):
        state.navigate_back()
        st.rerun()

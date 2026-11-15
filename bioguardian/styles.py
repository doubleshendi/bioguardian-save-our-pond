"""Custom CSS styles and UI header/footer components for BioGuardian."""

import streamlit as st
from bioguardian.engine import GameState, TOTAL_ROUNDS, MAX_TOTAL_POINTS


def inject_custom_css():
    """Inject mobile-first responsive styling and typography."""
    st.markdown("""
    <style>
    /* Mobile-first responsive container */
    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 680px;
        margin: auto;
    }
    
    /* Typography and header styling */
    h1, h2, h3 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #1b4332;
    }
    
    /* Educational disclaimer banner */
    .edu-disclaimer {
        background: #e8f5e9;
        border-left: 4px solid #2e7d32;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.82rem;
        color: #1b5e20;
        margin-bottom: 12px;
        font-weight: 500;
    }
    
    /* Status banner on dashboard */
    .status-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Active player badge */
    .player-turn-badge {
        display: inline-block;
        background: #0284c7;
        color: white;
        padding: 4px 10px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.88rem;
    }
    
    /* Score chip */
    .score-chip {
        display: inline-block;
        background: #15803d;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 700;
        font-size: 0.92rem;
    }
    
    /* Threat tile warning & restored states */
    .threat-tile {
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        transition: transform 0.15s ease;
    }
    
    .threat-tile-warning {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        color: #92400e;
    }
    
    .threat-tile-completed {
        background: #f0fdf4;
        border: 2px solid #22c55e;
        color: #166534;
    }

    .threat-tile-current {
        box-shadow: 0 0 0 3px #0284c7;
    }
    
    /* Large mobile buttons */
    div.stButton > button:first-child {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        min-height: 48px;
        font-size: 1rem;
    }
    
    /* Card match highlight */
    .card-match-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 14px;
        font-weight: 600;
        color: #1e40af;
    }
    
    /* Physical instruction callout */
    .physical-box {
        background: #fdf4ff;
        border: 2px dashed #c084fc;
        border-radius: 10px;
        padding: 14px;
        margin: 14px 0;
        color: #581c87;
    }
    
    /* Step indicator */
    .step-indicator {
        font-size: 0.85rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    /* Print styling */
    @media print {
        header, footer, .stButton, .no-print {
            display: none !important;
        }
        .main .block-container {
            max-width: 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def render_app_header(state: GameState, show_nav: bool = True):
    """Render top header with turn, score, progress and quick links."""
    inject_custom_css()
    
    # Static educational disclaimer required by PRD
    st.markdown(
        """<div class="edu-disclaimer">
        ℹ️ <strong>Educational Note:</strong> All points are game learning points, not real-world measured biodiversity.
        </div>""",
        unsafe_allow_html=True
    )

    if show_nav and state.status == "in_progress":
        cols = st.columns([3, 2, 1])
        with cols[0]:
            st.markdown(
                f"<div class='player-turn-badge'>👤 {state.active_player_name}'s Turn</div>",
                unsafe_allow_html=True
            )
        with cols[1]:
            st.markdown(
                f"<div class='score-chip'>⭐ {state.total_score}/{MAX_TOTAL_POINTS} pts</div>",
                unsafe_allow_html=True
            )
        with cols[2]:
            if st.button("❓ Help", key="header_help_btn", use_container_width=True):
                state.navigate_to("S11_HELP")
                st.rerun()
        st.markdown("<hr style='margin: 8px 0 16px 0;'/>", unsafe_allow_html=True)

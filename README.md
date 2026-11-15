# BioGuardian: Save Our Pond! 🦆🌿🌊

> **Tabletop Environmental Conservation Game & Mobile Companion**  
> Built according to the Product Requirements Document (PRD v1.0) for FIRST LEGO League (FLL) student challenge prototypes.

---

## 🎯 Educational Goal & Overview

Human activities can degrade freshwater pond habitats. **BioGuardian** bridges an on-screen mobile interface with a **24" &times; 36" physical tabletop model** and **6 printed challenge cards**.

Players work cooperatively (1–4 players) or solo to:
1. **Predict** environmental impacts of human activities.
2. **Choose** evidence-based conservation actions.
3. **Explain** the scientific mechanism behind the chosen action.
4. **Physically modify** the tabletop pond model by swapping threat markers for native restoration pieces.
5. **Sync** the physical change with the digital dashboard to earn their restoration badge.

> ℹ️ **Scientific Integrity Caveat:** All scores represent educational game points, not measured real-world biodiversity. Physical model changes represent *planned conservation interventions*, not instant biological recovery.

---

## 📁 Repository Structure

```
bioguardian/
├── app.py                      # Streamlit application entrypoint
├── requirements.txt            # Python dependencies (streamlit, pytest)
├── README.md                   # This documentation & judge demo script
├── data/
│   ├── challenges.json         # Canonical 6 challenge definitions
│   └── bioguardian_state.json  # Local JSON game save state (auto-generated)
├── bioguardian/
│   ├── __init__.py
│   ├── challenges.py           # Dataclasses & JSON loader
│   ├── engine.py               # State machine, turn rotation & scoring engine
│   ├── storage.py              # Persistence manager (save/resume/clear)
│   ├── styles.py               # Mobile-first CSS, badges, and headers
│   └── views/
│       ├── __init__.py         # View exports
│       ├── s01_welcome.py      # S01: Welcome, New Game, Resume
│       ├── s02_setup.py        # S02: 1-4 Players & Nicknames
│       ├── s03_instructions.py # S03: 6-step rules & checklist
│       ├── s04_dashboard.py    # S04: Pond habitat dashboard & 6 tiles
│       ├── s05_predict.py      # S05: Threat story & Prediction (+5 pts)
│       ├── s06_action.py       # S06: Action selection (+10 pts)
│       ├── s07_learn.py        # S07: Science mechanism, explain checklist, retry
│       ├── s08_restore.py      # S08: Tabletop physical model instructions
│       ├── s09_round_result.py # S09: Scorecard breakdown & next turn
│       ├── s10_final_report.py # S10: Victory assessment & judge summary
│       └── s11_help.py         # S11: Glossary, safety & scientific caveats
└── tests/
    ├── __init__.py
    ├── test_challenges.py           # Challenge data integrity & answers
    ├── test_engine.py               # Turn rotation, solo/coop, navigation
    ├── test_scoring.py              # 5/10/5 scoring, retries, victory thresholds
    ├── test_storage.py              # State serialization & reload consistency
    └── test_acceptance_criteria.py # Direct mapping to PRD Section 10 tests
```

---

## 🚀 Setup & Run Instructions

### 1. Prerequisites
- Python 3.10+ installed
- Virtual environment tool (`uv` or `python3 -m venv`)

### 2. Quick Start
```bash
# Clone / navigate to project directory
cd bioguardian

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 3. Running Unit & Acceptance Tests
The test suite validates all 11 acceptance criteria from PRD Section 10:
```bash
PYTHONPATH=. pytest tests -v
```

---

## 🏆 Game Rules & Scoring

| Component | Points Rule | Description |
|---|---|---|
| **Step 1: Prediction** | **+5 pts** | First attempt only; evaluates prediction of ecological effects. |
| **Step 2: Action** | **+10 pts** | First attempt only; evaluates conservation response. |
| **Step 3: Explanation** | **+5 pts** | Verified once per round by peer/facilitator (or self-check in solo). |
| **Step 4: Model Restoration** | **Badge** | Unlocked only after selecting best action (first attempt or retry). Increments restorations counter. |
| **Max Round Points** | **20 pts** | 6 rounds &times; 20 = **120 max total points**. |

### 🌟 Victory Condition
After 6 rounds:
- **Total Points &ge; 90 / 120** **AND**
- **Restorations Completed &ge; 4 / 6**
- *Result:* **Team Victory! Pond Habitat Stewards**
- If either condition is not met: Displays **Keep Learning: How to Improve**.

---

## 🎙️ FLL Judge Demonstration Script (< 3 Minutes)

1. **Before Judges Arrive (Setup):**
   - Place all 6 problem markers in the physical model (fertilizer, weed token, barren area, litter, bare shore, bare slope).
   - Launch app on tablet/laptop; open **Pond Dashboard** showing 6 active warnings.
2. **Step 1 — Threat & Prediction (30s):**
   - *"Judges, our pond is facing 6 active threats. Let's look at Round 1: Fertilizer Runoff."*
   - Read the threat scenario; submit prediction: `A. More algae growth` (+5 pts).
3. **Step 2 — Conservation Action (30s):**
   - Select action: `B. Reduce unnecessary fertilizer and protect a vegetated buffer` (+10 pts).
4. **Step 3 — Science Explanation & Verification (30s):**
   - Decision maker explains: *"The vegetated buffer slows stormwater and filters out excess nitrogen and phosphorus before it enters the water."*
   - Check the verification box (+5 pts).
5. **Step 4 — Physical Model Synchronization (45s):**
   - Remove the fertilizer marker from the physical model.
   - Attach the **Native Buffer Strip** between the lawn and the pond.
   - Tap **"I Changed the Model!"**
   - Point to dashboard: Threat icon flips to `✅ Planned / Demonstrated`.
6. **Closing Science Statement (15s):**
   - *"Importantly, our physical model demonstrates a planned conservation strategy, not guaranteed immediate recovery, which requires repeated seasonal water testing."*

---

## ✏️ How to Edit Challenges & Content

All challenge content is separated cleanly from application logic in `data/challenges.json`:
- To adjust questions, options, or correct answers: edit `data/challenges.json`.
- Changes are immediately picked up on application reload.
- Dataclass validation in `bioguardian/challenges.py` ensures consistency.

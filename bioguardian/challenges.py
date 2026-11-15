"""Challenge data definitions and loaders for BioGuardian."""

from dataclasses import dataclass
from typing import List, Dict, Optional
import json
from pathlib import Path


@dataclass
class Choice:
    id: str
    text: str


@dataclass
class Question:
    prompt: str
    choices: List[Choice]
    correct_id: str


@dataclass
class Challenge:
    id: int
    round_number: int
    card_code: str
    title: str
    icon: str
    threat_story: str
    threat_marker: str
    solution_piece: str
    physical_instruction: str
    prediction: Question
    action: Question
    science_explanation: str
    real_life_verification: str
    demonstration_note: str

    @classmethod
    def from_dict(cls, data: dict) -> "Challenge":
        pred = data["prediction"]
        pred_q = Question(
            prompt=pred["prompt"],
            choices=[Choice(c["id"], c["text"]) for c in pred["choices"]],
            correct_id=pred["correct_id"]
        )
        act = data["action"]
        act_q = Question(
            prompt=act["prompt"],
            choices=[Choice(c["id"], c["text"]) for c in act["choices"]],
            correct_id=act["correct_id"]
        )
        return cls(
            id=data["id"],
            round_number=data["round_number"],
            card_code=data["card_code"],
            title=data["title"],
            icon=data.get("icon", "🌿"),
            threat_story=data["threat_story"],
            threat_marker=data["threat_marker"],
            solution_piece=data["solution_piece"],
            physical_instruction=data["physical_instruction"],
            prediction=pred_q,
            action=act_q,
            science_explanation=data["science_explanation"],
            real_life_verification=data["real_life_verification"],
            demonstration_note=data.get("demonstration_note", "Planned/demonstrated conservation action.")
        )


def load_challenges(json_path: Optional[Path] = None) -> List[Challenge]:
    """Load all 6 canonical challenges."""
    if json_path is None:
        json_path = Path(__file__).resolve().parent.parent / "data" / "challenges.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Challenge.from_dict(item) for item in data]


def get_challenge_by_round(round_number: int, challenges: Optional[List[Challenge]] = None) -> Optional[Challenge]:
    if challenges is None:
        challenges = load_challenges()
    for c in challenges:
        if c.round_number == round_number:
            return c
    return None

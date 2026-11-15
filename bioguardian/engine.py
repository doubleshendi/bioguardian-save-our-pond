"""Game engine, state machine, and scoring logic for BioGuardian: Save Our Pond!"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid


PREDICTION_POINTS = 5
ACTION_POINTS = 10
EXPLANATION_POINTS = 5
MAX_ROUND_POINTS = 20
TOTAL_ROUNDS = 6
MAX_TOTAL_POINTS = 120
WIN_POINTS_THRESHOLD = 90
WIN_RESTORATIONS_THRESHOLD = 4


@dataclass
class RoundResult:
    challenge_id: int
    round_number: int
    player_index: int
    player_name: str
    prediction_first_answer: Optional[str] = None
    prediction_correct: int = 0
    action_first_answer: Optional[str] = None
    action_correct: int = 0
    best_action_selected: bool = False
    action_retried: bool = False
    explanation_verified: int = 0
    restoration_confirmed: bool = False
    physical_pieces_changed: str = ""
    round_points: int = 0
    submitted_prediction: bool = False
    submitted_action: bool = False
    completed_at: Optional[str] = None

    def calculate_points(self) -> int:
        """Calculate points based solely on first attempt and verified explanation."""
        self.round_points = (
            PREDICTION_POINTS * (1 if self.prediction_correct else 0) +
            ACTION_POINTS * (1 if self.action_correct else 0) +
            EXPLANATION_POINTS * (1 if self.explanation_verified else 0)
        )
        return self.round_points


@dataclass
class GameState:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    mode: str = "cooperative"  # "cooperative" or "solo"
    player_names: List[str] = field(default_factory=lambda: ["Player 1"])
    active_player_index: int = 0
    current_round_index: int = 0  # 0-indexed (0 to 5)
    current_screen: str = "S01_WELCOME"
    previous_screen: str = "S01_WELCOME"
    status: str = "setup"  # "setup", "in_progress", "complete"
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    finished_at: Optional[str] = None
    round_results: List[RoundResult] = field(default_factory=list)
    show_restart_confirm: bool = False

    def __post_init__(self):
        if not self.round_results:
            self.round_results = [
                RoundResult(
                    challenge_id=i,
                    round_number=i,
                    player_index=0,
                    player_name=self.player_names[0] if self.player_names else "Player 1"
                )
                for i in range(1, TOTAL_ROUNDS + 1)
            ]

    @property
    def current_round_number(self) -> int:
        return self.current_round_index + 1

    @property
    def current_round_result(self) -> RoundResult:
        return self.round_results[self.current_round_index]

    @property
    def active_player_name(self) -> str:
        if not self.player_names:
            return "Player 1"
        idx = self.active_player_index % len(self.player_names)
        return self.player_names[idx]

    @property
    def total_score(self) -> int:
        return sum(r.calculate_points() for r in self.round_results)

    @property
    def restorations_completed(self) -> int:
        return sum(1 for r in self.round_results if r.restoration_confirmed)

    @property
    def is_team_winner(self) -> bool:
        return (
            self.total_score >= WIN_POINTS_THRESHOLD and
            self.restorations_completed >= WIN_RESTORATIONS_THRESHOLD
        )

    def start_game(self, mode: str, player_names: List[str]):
        """Initialize and start a new game."""
        self.mode = mode
        clean_names = [p.strip() for p in player_names if p.strip()]
        if not clean_names:
            clean_names = ["Player 1"] if mode == "solo" else ["Player 1", "Player 2"]
        self.player_names = clean_names
        self.active_player_index = 0
        self.current_round_index = 0
        self.status = "in_progress"
        self.started_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.finished_at = None
        self.round_results = [
            RoundResult(
                challenge_id=i,
                round_number=i,
                player_index=(i - 1) % len(self.player_names),
                player_name=self.player_names[(i - 1) % len(self.player_names)]
            )
            for i in range(1, TOTAL_ROUNDS + 1)
        ]
        self.current_screen = "S04_DASHBOARD"

    def submit_prediction(self, answer_id: str, correct_id: str) -> bool:
        """Submit prediction answer. Only first submission sets score."""
        rr = self.current_round_result
        if rr.submitted_prediction:
            return bool(rr.prediction_correct)

        rr.prediction_first_answer = answer_id
        rr.prediction_correct = 1 if answer_id.strip().upper() == correct_id.strip().upper() else 0
        rr.submitted_prediction = True
        rr.calculate_points()
        self.updated_at = datetime.now().isoformat()
        return bool(rr.prediction_correct)

    def submit_action(self, answer_id: str, correct_id: str) -> bool:
        """Submit action choice. Only first submission awards points."""
        rr = self.current_round_result
        is_correct = (answer_id.strip().upper() == correct_id.strip().upper())
        if not rr.submitted_action:
            rr.action_first_answer = answer_id
            rr.action_correct = 1 if is_correct else 0
            rr.submitted_action = True
            if is_correct:
                rr.best_action_selected = True
            rr.calculate_points()
        self.updated_at = datetime.now().isoformat()
        return is_correct

    def retry_action(self, answer_id: str, correct_id: str) -> bool:
        """Retry action selection for learning. Does not award action points."""
        rr = self.current_round_result
        is_correct = (answer_id.strip().upper() == correct_id.strip().upper())
        rr.action_retried = True
        if is_correct:
            rr.best_action_selected = True
        self.updated_at = datetime.now().isoformat()
        return is_correct

    def verify_explanation(self, verified: bool):
        """Mark explanation verified by peer/facilitator or self-check."""
        rr = self.current_round_result
        rr.explanation_verified = 1 if verified else 0
        rr.calculate_points()
        self.updated_at = datetime.now().isoformat()

    def confirm_restoration(self, piece_info: str):
        """Confirm physical model modification."""
        rr = self.current_round_result
        if rr.best_action_selected:
            rr.restoration_confirmed = True
            rr.physical_pieces_changed = piece_info
            rr.completed_at = datetime.now().isoformat()
            self.updated_at = datetime.now().isoformat()

    def advance_to_next_round(self):
        """Advance round or finish game."""
        self.current_round_result.completed_at = datetime.now().isoformat()
        if self.current_round_index < TOTAL_ROUNDS - 1:
            self.current_round_index += 1
            if self.mode == "cooperative":
                self.active_player_index = self.current_round_index % len(self.player_names)
            else:
                self.active_player_index = 0
            # Update player info on round result
            self.current_round_result.player_index = self.active_player_index
            self.current_round_result.player_name = self.active_player_name
            self.current_screen = "S04_DASHBOARD"
        else:
            self.status = "complete"
            self.finished_at = datetime.now().isoformat()
            self.current_screen = "S10_FINAL_REPORT"
        self.updated_at = datetime.now().isoformat()

    def navigate_to(self, screen: str):
        if self.current_screen != "S11_HELP":
            self.previous_screen = self.current_screen
        self.current_screen = screen

    def navigate_back(self):
        if self.previous_screen:
            self.current_screen = self.previous_screen
        else:
            self.current_screen = "S04_DASHBOARD"

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameState":
        round_results_data = data.pop("round_results", [])
        state = cls(**data)
        state.round_results = [RoundResult(**r) for r in round_results_data]
        return state

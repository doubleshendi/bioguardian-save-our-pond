"""Local JSON storage for save, resume, and game state persistence."""

import json
from pathlib import Path
from typing import Optional
from bioguardian.engine import GameState

DEFAULT_STORAGE_PATH = Path(__file__).resolve().parent.parent / "data" / "bioguardian_state.json"


def save_game_state(state: GameState, path: Optional[Path] = None) -> bool:
    """Save the game state to local JSON file."""
    target_path = path or DEFAULT_STORAGE_PATH
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(state.to_dict(), f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving game state: {e}")
        return False


def load_game_state(path: Optional[Path] = None) -> Optional[GameState]:
    """Load game state from local JSON file if exists."""
    target_path = path or DEFAULT_STORAGE_PATH
    if not target_path.exists():
        return None
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return GameState.from_dict(data)
    except Exception as e:
        print(f"Error loading game state: {e}")
        return None


def has_saved_game(path: Optional[Path] = None) -> bool:
    """Check if there is an in-progress saved game that can be resumed."""
    state = load_game_state(path)
    if state and state.status == "in_progress":
        return True
    return False


def clear_saved_game(path: Optional[Path] = None) -> bool:
    """Clear or delete the saved game file."""
    target_path = path or DEFAULT_STORAGE_PATH
    if target_path.exists():
        try:
            target_path.unlink()
            return True
        except Exception:
            return False
    return True

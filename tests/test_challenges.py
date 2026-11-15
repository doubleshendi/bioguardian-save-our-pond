"""Tests for challenge data definitions and structure."""

import pytest
from bioguardian.challenges import load_challenges, get_challenge_by_round


def test_all_six_challenges_present():
    challenges = load_challenges()
    assert len(challenges) == 6
    assert [c.id for c in challenges] == [1, 2, 3, 4, 5, 6]
    assert [c.round_number for c in challenges] == [1, 2, 3, 4, 5, 6]


def test_canonical_answers_match_prd():
    challenges = load_challenges()
    
    # Round 1: Fertilizer runoff
    r1 = challenges[0]
    assert r1.title == "Fertilizer Runoff"
    assert r1.prediction.correct_id == "A"
    assert r1.action.correct_id == "B"
    assert "native buffer strip" in r1.physical_instruction.lower()

    # Round 2: Invasive plants
    r2 = challenges[1]
    assert r2.title == "Invasive Plants"
    assert r2.prediction.correct_id == "B"
    assert r2.action.correct_id == "C"

    # Round 3: Pollinators
    r3 = challenges[2]
    assert r3.title == "Pollinator Habitat Decline"
    assert r3.prediction.correct_id == "A"
    assert r3.action.correct_id == "A"

    # Round 4: Litter
    r4 = challenges[3]
    assert r4.title == "Pond Litter"
    assert r4.prediction.correct_id == "B"
    assert r4.action.correct_id == "B"

    # Round 5: Shoreline habitat loss
    r5 = challenges[4]
    assert r5.title == "Shoreline Habitat Loss"
    assert r5.prediction.correct_id == "A"
    assert r5.action.correct_id == "C"

    # Round 6: Sediment runoff
    r6 = challenges[5]
    assert r6.title == "Sediment Runoff"
    assert r6.prediction.correct_id == "B"
    assert r6.action.correct_id == "A"


def test_choices_count_and_ids():
    challenges = load_challenges()
    for c in challenges:
        assert len(c.prediction.choices) == 3
        assert [ch.id for ch in c.prediction.choices] == ["A", "B", "C"]
        assert len(c.action.choices) == 3
        assert [ch.id for ch in c.action.choices] == ["A", "B", "C"]
        assert c.prediction.correct_id in ["A", "B", "C"]
        assert c.action.correct_id in ["A", "B", "C"]
        assert c.science_explanation != ""
        assert c.real_life_verification != ""

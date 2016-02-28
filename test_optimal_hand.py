import pytest
import optimal_hand


def test_state():
    """test state constructor interface"""
    s = optimal_hand.State((1,1,1,1,1), 3)
    assert s.hand == (1,1,1,1,1)
    assert s.rolls == 3


def test_roll():
    optimal_hand.random.seed(0)
    assert optimal_hand.roll(
        (1, 2, 3, 5, 5),
        keep_mask=(0, 0, 0, 1, 1)) == (5, 5, 6, 5, 3)
    assert optimal_hand.roll(
        (1, 2, 3, 4, 5),
        keep_mask=(1, 1, 1, 1, 1)) == (1, 2, 3, 4, 5)
    assert optimal_hand.roll((1, 2, 3, 4, 5)) == (2, 4, 3, 5, 2)

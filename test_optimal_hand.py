import pytest
import sys

assert sys.version_info >= (3, 5), "py3.4 and below not supported"
import optimal_hand


def test_state():
    """test state constructor interface"""
    s = optimal_hand.State((1, 1, 1, 1, 1), 3)
    assert s.hand == (1, 1, 1, 1, 1)
    assert s.rolls == 3


@pytest.mark.xfail(sys.version_info[:2] != (3, 5), reason="different randon generator")
def test_roll():
    optimal_hand.random.seed(0)
    assert optimal_hand.roll(
        (1, 2, 3, 5, 5),
        keep_mask=(0, 0, 0, 1, 1)) == (5, 5, 4, 4, 1)
    assert optimal_hand.roll(
        (1, 2, 3, 4, 5),
        keep_mask=(1, 1, 1, 1, 1)) == (1, 2, 3, 4, 5)
    assert optimal_hand.roll((1, 2, 3, 4, 5)) == (3, 5, 4, 4, 3)


def test_score_invalid_category():
    with pytest.raises(ValueError) as e:
        optimal_hand.score((1, 2, 3, 4, 5), 'Not A Category')


def test_score_pair():
    assert optimal_hand.score((2, 2, 1, 4, 5), 'One Pair') == 2
    assert optimal_hand.score((2, 6, 1, 4, 5), 'One Pair') == 0
    assert optimal_hand.score((2, 6, 1, 6, 5), 'One Pair') == 3
    assert optimal_hand.score((4, 6, 1, 4, 5), 'One Pair') == 2


def test_score_two_pair():
    assert optimal_hand.score((2, 2, 3, 4, 4), "Two Pair") == 4
    assert optimal_hand.score((2, 2, 3, 6, 6), "Two Pair") == 5
    assert optimal_hand.score((2, 2, 3, 2, 2), "Two Pair") == 4
    assert optimal_hand.score((2, 2, 3, 4, 6), "Two Pair") == 0
    assert optimal_hand.score((6, 6, 6, 6, 6), "Two Pair") == 0


def test_score_three_of_a_kind():
    assert optimal_hand.score((2, 2, 3, 4, 4), "Three of a Kind") == 0
    assert optimal_hand.score((2, 1, 4, 4, 4), "Three of a Kind") == 6
    assert optimal_hand.score((2, 6, 6, 6, 6), "Three of a Kind") == 8
    assert optimal_hand.score((1, 2, 3, 4, 5), "Three of a Kind") == 0


def test_score_straight():
    assert optimal_hand.score((1, 2, 3, 4, 5), "Straight") == 25
    assert optimal_hand.score((1, 2, 3, 4, 4), "Straight") == 0
    assert optimal_hand.score((2, 3, 4, 5, 6), "Straight") == 25


def test_score_full_house():
    assert optimal_hand.score((1, 2, 3, 4, 5), "Full House") == 0
    assert optimal_hand.score((3, 3, 3, 5, 5), "Full House") == 25
    assert optimal_hand.score((3, 3, 6, 6, 6), "Full House") == 30
    assert optimal_hand.score((3, 3, 6, 6, 5), "Full House") == 0
    assert optimal_hand.score((3, 3, 3, 3, 6), "Full House") == 0
    assert optimal_hand.score((3, 3, 3, 3, 3), "Full House") == 25


def test_score_four_of_a_kind():
    assert optimal_hand.score((2, 2, 2, 2, 6), "Four of a Kind") == 50
    assert optimal_hand.score((2, 6, 6, 6, 6), "Four of a Kind") == 60
    assert optimal_hand.score((6, 6, 6, 6, 6), "Four of a Kind") == 60
    assert optimal_hand.score((2, 2, 2, 2, 2), "Four of a Kind") == 50
    assert optimal_hand.score((3, 3, 3, 6, 6), "Four of a Kind") == 0


def test_score_five_of_a_kind():
    assert optimal_hand.score((2, 2, 2, 2, 6), "Five of a Kind") == 0
    assert optimal_hand.score((2, 2, 2, 2, 2), "Five of a Kind") == 200
    assert optimal_hand.score((6, 6, 6, 6, 6), "Five of a Kind") == 240


def test_possible_hands():
    pos_hands = optimal_hand.possible_hands
    assert list(pos_hands((2, 2, 2, 2, 2), (1, 1, 1, 1, 1))) == [(2, 2, 2, 2, 2)]

    pos = {
        (1, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 3),
        (2, 2, 2, 2, 4),
        (2, 2, 2, 2, 5),
        (2, 2, 2, 2, 6),
    }
    assert set(pos_hands((2, 2, 2, 2, 2), (1, 1, 1, 1, 0))) == pos
    assert len(list(pos_hands((2, 2, 2, 2, 2), (0, 0, 0, 0, 0)))) == 252


def test_possible_hands_sort():
    pos_hands = optimal_hand.possible_hands
    assert set(pos_hands((4, 2, 5, 1, 3), (1, 1, 1, 1, 1))) == {(1, 2, 3, 4, 5)}

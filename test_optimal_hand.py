import pytest
import sys

assert sys.version_info >= (3, 5), "py3.4 and below not supported"
import optimal_hand


def test_state():
    """test state constructor interface"""
    s = optimal_hand.State((1, 1, 1, 1, 1), 3, 6)
    assert s.hand == (1, 1, 1, 1, 1)
    assert s.rolls == 3
    assert s.score == 6


@pytest.mark.xfail(sys.version_info[:2] != (3, 5), reason="different randon generator")
def test_roll():
    optimal_hand.random.seed(0)
    assert optimal_hand.roll(
        (1, 2, 3, 5, 5),
        keep_mask=(0, 0, 0, 1, 1)) == (1, 4, 4, 5, 5)
    assert optimal_hand.roll(
        (1, 2, 3, 4, 5),
        keep_mask=(1, 1, 1, 1, 1)) == (1, 2, 3, 4, 5)
    assert optimal_hand.roll((1, 2, 3, 4, 5)) == (3, 3, 4, 4, 5)


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


def test_get_actions():
    state = optimal_hand.State((1, 1, 1, 1, 1), 2, 0)
    assert optimal_hand.get_actions(
        state) == optimal_hand.DICE_MASKS | optimal_hand.SCORE_CATEGORIES
    state = optimal_hand.State((1, 1, 1, 1, 1), 0, 0)
    assert optimal_hand.get_actions(state) == optimal_hand.SCORE_CATEGORIES


def test_do():
    State = optimal_hand.State
    state = State((1, 1, 1, 1, 1), 0, 0)
    assert optimal_hand.do(state, "Five of a Kind") == State((1, 1, 1, 1, 1), 0, 200)
    assert optimal_hand.do(state, "One Pair") == State((1, 1, 1, 1, 1), 0, 2)
    assert optimal_hand.do(state, "Straight") == State((1, 1, 1, 1, 1), 0, 0)
    state1 = state
    state = State((1, 1, 1, 1, 1), 1, 0)
    next_hand = (1, 1, 1, 3, 3)
    assert optimal_hand.do(state,
                           (1, 1, 1, 0, 0),
                           next_hand=next_hand) == State(next_hand, 0, 0)

    with pytest.raises(ValueError):
        optimal_hand.do(state1, (0, 0, 0, 0, 0))


def test_num_possible_hands():
    nph = optimal_hand.num_possible_hands
    assert nph(1) == 6
    assert nph(5) == 252
    assert nph(2) == 21


def test_utility():
    u = optimal_hand.utility
    state1 = optimal_hand.State((1, 1, 1, 1, 2), 0, 0)
    assert u(state1) == 50
    state2 = optimal_hand.State((1, 1, 1, 1, 2), 1, 0)
    assert u(state2) > u(state1)


def test_best_action():
    best = optimal_hand.best_action
    state1 = optimal_hand.State((1, 1, 1, 1, 2), 0, 0)
    state2 = optimal_hand.State((1, 1, 1, 1, 2), 1, 0)
    assert best(state1) == "Four of a Kind"
    assert best(state2) == (1, 1, 1, 1, 0)

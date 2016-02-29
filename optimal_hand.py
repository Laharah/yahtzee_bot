import random
import math
import itertools
from functools import wraps
from collections import namedtuple, Counter

def memo(func):
    """A quick and dirty caching function"""
    memo.cache = {}
    @wraps(func)
    def wrapper(*args):
        try:
            return memo.cache[args]
        except KeyError:
            memo.cache[args] = result = func(*args)
            return result
        except TypeError:
            return func(*args)
    return wrapper


random.seed(0)

State = namedtuple("State", 'hand, rolls, score')
#  every dice combination for re-roll is represented as a mask in 0-31 in binary
DICE_MASKS = {tuple(int(i) for i in '{:>05}'.format(bin(n)[2:])) for n in range(31)}
SCORE_CATEGORIES = {
    'One Pair',
    'Two Pair',
    'Three of a Kind',
    'Straight',
    'Full House',
    'Four of a Kind',
    'Five of a Kind',
}


def roll(hand, keep_mask=None):
    if not hand:
        hand = tuple()
    keep_mask = (0, 0, 0, 0, 0) if not keep_mask else keep_mask
    hand = list(itertools.compress(hand, keep_mask))
    for d in range(5 - len(hand)):
        hand.append(random.randrange(1, 7))
    return tuple(sorted(hand))


def score(hand, category):
    if category not in SCORE_CATEGORIES:
        raise ValueError("Invalid Category: {}".format(category))

    if category == 'One Pair':
        c = Counter(hand)
        if c[6] == 2:
            return 3
        return 2 if c.most_common()[0][1] > 1 else 0

    if category == 'Two Pair':
        c = Counter(hand)
        try:
            p1, p2, *_ = c.most_common()
        except ValueError:
            return 0
        if p1[1] == 4 or p1[1] == p2[1] == 2:
            return 5 if p1[0] == 6 or p2[0] == 6 else 4
        else:
            return 0

    if category == 'Three of a Kind':
        c = Counter(hand)
        value, n = c.most_common()[0]
        if n < 3:
            return 0
        else:
            return 8 if value == 6 else 6

    if category == 'Straight':
        start = min(hand)
        if all(a == b for a, b in zip(sorted(hand), range(start, start + 6))):
            return 25
        else:
            return 0

    if category == 'Full House':
        c = Counter(hand)
        house, *family = c.most_common()
        if house[1] == 5 or (house[1] == 3 and len(family) == 1):
            return 30 if house[0] == 6 else 25
        else:
            return 0

    if category == 'Four of a Kind':
        c = Counter(hand)
        most = c.most_common()[0]
        if most[1] >= 4:
            return 60 if most[0] == 6 else 50
        else:
            return 0

    if category == 'Five of a Kind':
        if len(set(hand)) > 1:
            return 0
        else:
            return 240 if hand[0] == 6 else 200


def possible_hands(hand, mask):
    hand = tuple(itertools.compress(hand, mask))
    possible_rolls = itertools.combinations_with_replacement(range(1, 7), 5 - len(hand))
    for r in possible_rolls:
        yield tuple(sorted(hand + r))

def num_possible_hands(dice):
    return math.factorial(6+dice-1)/(math.factorial(dice)*120)


def get_actions(state):
    if state.rolls:
        return DICE_MASKS | SCORE_CATEGORIES
    else:
        return SCORE_CATEGORIES

def do(state, action, next_hand=None):
    if action in SCORE_CATEGORIES:
        return State(state.hand, state.rolls, score(state.hand, action))

    rolls = state.rolls - 1
    if rolls < 0:
        raise ValueError("out of rolls, cannot re-roll")
    if next_hand:
        hand = next_hand
    else:
        hand = roll(state.hand, keep_mask=action)
    return State(hand, rolls, state.score)

@memo
def utility(state):
    """The value of being in a certain state"""
    if state.score:
        return state.score

    return max(quality(state, action) for action in get_actions(state))

def quality(state, action):
    """The value of taking a certain action in a given state"""
    if action in SCORE_CATEGORIES:
        return score(state.hand, action)

    # if the value relies on chance, average the utilities of the possible states together
    num_dice = 5 - sum(action)
    total_possible = num_possible_hands(num_dice)
    return sum(utility(do(state, action, next_hand=h))
               for h in possible_hands(state.hand, action)) / total_possible


def best_action(state):
    """returns the best action for a given state"""
    return max((a for a in get_actions(state)), key=lambda a: quality(state, a))


if __name__ == '__main__':
    import os
    import pickle
    if os.path.exists("util_cache.pickle"):
        with open("util_cache.pickle", 'rb') as p:
            memo.cache = pickle.load(p)
    random.seed()
    state = State(roll(None), 5, 0)
    action = None
    while not isinstance(action, str):
        print(state)
        action = best_action(state)
        print(action)
        state = do(state, action)
    print('Score: {}'.format(state.score))

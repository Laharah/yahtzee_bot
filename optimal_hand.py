import random
import itertools
from collections import namedtuple, Counter

random.seed(0)

State = namedtuple("State", 'hand, rolls')
#  every dice combination for re-roll is represented as a mask in 0-31 in binary
DICE_MASKS = [[int(i) for i in '{:>05}'.format(bin(n)[2:])] for n in range(31)]
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

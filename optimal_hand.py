import random
import itertools
from collections import namedtuple

random.seed(0)

State = namedtuple("State", 'hand, rolls')
#  every dice combination for re-roll is represented as a mask in 0-31 in binary
DICE_MASKS = [[int(i) for i in '{:>05}'.format(bin(n)[2:])] for n in range(31)]

def roll(hand, keep_mask=None):
    keep_mask = (0,0,0,0,0) if not keep_mask else keep_mask
    hand = [d for d, k in zip(hand, keep_mask) if k]
    for d in range(5 - len(hand)):
        hand.append(random.randrange(1,7))
    return tuple(hand)

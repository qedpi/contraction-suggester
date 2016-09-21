from itertools import tee
from collections import Counter

from layouts import COLEMAK, DVORAK, QWERTY, base
from utilities import dot_product, adj_triples, normalize_alpha as normalize
from model import kb, kp, ks, ws, wb, wp, p_weights, Pf, Pr, Ph

layouts = [COLEMAK, DVORAK, QWERTY]  # default value
layout = layouts[1]  # Dvorak


# column of key -> right or left handed
def get_hand(col):
    return 'R' if col > 4 else 'L'


# column of key -> finger id: left pinkie, ring, middle, index, right index, middle, ring, pinkie
def get_finger(col):
    if col in [4, 5, 9, 10, 11]:  # normal offset or right pinkie
        return col - 1
    elif col > 5:                 # right hand offsets more because of middle columns
        return col - 2
    else:                         # left hand requires no offset
        return col

# Map each char to a n-tuple of characteristics
keymap = {}

for row, e in enumerate(layout):  # each char given row, col, travel dist, which hand
    for col, c in enumerate(e):
        keymap[c] = {'row': row, 'col': col, 'base': base[row][col], 'hand': get_hand(col), 'finger': get_finger(col)}


# -> Counter of triplet frequencies (also single and double letter words)
def tokenize_map(s):
    words = normalize(s).split()
    triplet_count = Counter()
    for word in words:
        triplet_count += Counter([word] if len(word) <= 3 else adj_triples(word))
    return triplet_count

# eg: print(tokenize_map('lolol me'))


def penalty(c):  # positional penalty for each character in a layout
    key = keymap[c]
    penalties = map([1, Ph[key['hand']], Pf[key['finger']], Pr[key['row']]])
    return dot_product(p_weights, penalties)


def path(layout):
    ''' Modified from original Carpalx Perl program. Calculate triad source path
    :param layout:
    :return:
    '''

    def ph(h):
        if h[0] == h[2]:
            return 2 if h[1] == h[2] else 1
        else:
            return 0

    def pf(f, c):
        f1 = f[0]; f2 = f[1]; f3 = f[2]
        c1 = c[0]; c2 = c[1]; c3 = c[2]

        if f1 > f2:
            if f2 > f3:
                return 0
            elif f2 == f3:
                return 1 if c2 == c3 else 6
            elif f3 == f1:
                return 4
            elif f1 > f3 > f2:
                return 2
            else:
                return 3
        elif f1 < f2:
            if f2 < f3:
                return 0
            elif f2 == f3:
                return 1 if c2 == c3 else 6
            elif f3 == f1:
                return 4
            elif f1 < f3 < f2:
                return 2
            else:
                return 3
        else:  # f1 == f2
            if f2 < f3 or f3 < f1:
                return 1 if c1 == c2 else 6
            elif f2 == f3:
                return 7 if c1 != c2 and c2 != c3 and c1 != c3 else 5

    def pr(r):
        r1 = r[0]; r2 = r[1]; r3 = r[2]

        def drmax(r1, r2, r3):
            def cmp(a, b):
                return (a > b) - (a < b)

            def abs_orig(d):
                return abs(d), d

            difs = [r1-r2, r1-r3, r2-r3]

            return sorted(map(abs_orig, difs))[0][1]

        if r1 < r2:
            if r3 == r2:
                return 1
            elif r2 < r3:
                return 4
            elif abs(drmax(r1,r2,r3)) == 1:
                return 3
            else:
                return 7 if drmax(r1,r2,r3) < 0 else 5

        elif r1 > r2:
            if r3 == r2:
                return 2
            elif r2 > r3:
                return 6
            elif abs(drmax(r1, r2, r3)) == 1:
                return 3
            else:
                return 7 if drmax(r1, r2, r3) < 0 else 5
        else:
            if r2 > r3:
                return 2
            else:
                return r2 < r3


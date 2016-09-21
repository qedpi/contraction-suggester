from itertools import tee
from collections import Counter

base = [[2, 2, 2, 2, 2.5, 3, 2, 2, 2, 2, 2.5, 4, 6],
        [0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 3.5, 2, 2, 2, 2, 2]]

DVORAK = [["'", ",", ".", "p", "y", "f", "g", "c", "r", "l", "/", "="],
          ["a", "o", "e", "u", "i", "d", "h", "t", "n", "s", "-"],
          [":", "q", "j", "k", "x", "b", "m", "w", "v", "z"]]

# helper functions


def get_hand(col):
    return 'R' if col > 4 else 'L'


# Map each char to a n-tuple of characteristics

keymap = {}

for row, e in enumerate(DVORAK):
    for col, c in enumerate(e):
        keymap[c] = {'row': row, 'col':col, 'base': base[row][col], 'hand': get_hand(col)}


def adj_triples(s):
    yield from map(lambda i: s[i:i+3], range(len(s) - 3 + 1))

#print(*adj_triples('fish'))


def normalize(s):
    return ''.join([c for c in s.lower() if c.isalpha() or c == ' '])


def tokenize_map(s):
    words = normalize(s).split()
    triplet_count = Counter()
    for word in words:
        triplet_count += Counter([word] if len(word) <= 3 else adj_triples(word))
    return triplet_count

#print(tokenize_map('lolol me'))



# Default model params
kb = 0.3555
kp = 0.6423
ks = 0.4268
ws = [1, 0.3, 0.3]
wb = [1, 0.367, 0.235]
wp = [1, 0.367, 0.235]

def path(layout):

    ''' Modified from original Carpalx Perl program. Calculate triad source path
    :param layout:
    :return:
    '''

    def ph(h):
        h1 = h[0]; h2 = h[1]; h3 = h[2]
        if h1 == h3:
            return 2 if h2 == h3 else 1
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
            elif abs(drmax(r1,r2,r3)) == 1:
                return 3
            else:
                return 7 if drmax(r1,r2,r3) < 0 else 5
        else:
            if r2 > r3:
                return 2
            else:
                return r2 < r3


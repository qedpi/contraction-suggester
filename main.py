'''
' Model based off of carpalx specifications
'''

from itertools import tee
from collections import Counter
from copy import deepcopy

from layouts import COLEMAK, DVORAK, QWERTY, QEDPI, base_distance, my_keyboard as base
from utilities import dot_product, adj_triples, compound, normalize_alpha as normalize
from model import e_weights, ws, wb, wp, p_weights, Pf, Pr, Ph

layouts = [COLEMAK, DVORAK, QWERTY, QEDPI]  # default value
layout = layouts[3]  # QEDPI


# column of key -> right or left handed
def get_hand(col):
    pivot = 4
    return 'R' if col > pivot else 'L'


# column of key -> finger id: left pinkie, ring, middle, index, right index, middle, ring, pinkie
def get_finger(col):
    if col > 8:
        return 7        # right pinkie
    if col in [4, 5]:   # normal offset or right pinkie
        return col - 1
    elif col > 5:       # right hand offsets more because of middle columns
        return col - 2
    else:               # left hand requires no offset
        return col

# Map each char to a n-tuple of characteristics
keymap = {}

for row, e in enumerate(layout):  # each char given row, col, travel dist, which hand
    for col, c in enumerate(e):
        keymap[c] = {'row': row, 'col': col, 'base': base[row][col],
                     'hand': get_hand(row), 'finger': get_finger(col)}


# -> Counter of triplet frequencies (also single and double letter words)
def tokenize_map(s):
    words = normalize(s).split()
    triplet_count = Counter()
    for word in words:
        triplet_count += Counter([word] if len(word) <= 3 else adj_triples(word))
    return triplet_count

# eg: print(tokenize_map('lolol me'))

'''
def penalty(c):  # positional penalty for each character in a layout
    key = keymap[c]
    penalties = [1, Ph[key['hand']], Pf[key['finger']], Pr[key['row'] + 1]]
    return dot_product(p_weights, penalties)

# map each key to its penalty
penalties = {}
for key in keymap.keys():
    penalties[key] = penalty(key) + keymap[key]['base']
'''

'''
layout_pen = deepcopy(layout)
for r in range(len(layout)):
    for c in range(len(layout[r])):
        layout_pen[r][c] = penalties[layout[r][c]]

print(*layout_pen, sep='\n')'''


def path(triad):

    def ph(h):           # Path cost for hands
        a, b, c = h
        if a == b == c:  # all in the same hand
            return 2
        elif a == c:     # ABA alternate
            return 1
        else:            # dif hands, no alternate: ABB
            return 0

    def pf(f, d):        # Path cost for fingers
        fa, fb, fc = f
        a, b, c = d
        fset = len(set(f))
        dset = len(set(d))
        monotone = fa <= fb <= fc or fa >= fb >= fc
        strict_monotone = fa < fb < fc or fa > fb > fc

        if strict_monotone:                 # unique, monotonic
            return 0
        elif fa < fc < fb or fb < fc < fa:      # rolling: third between first and second
            return 2
        elif fset == len(f):                    # neither
            return 3
        elif fset == 1:                     # same finger
            if dset == len(d):                  # unique keys
                return 7
            else:
                return 5                        # repeated keys
        else:                               # some different
            if monotone:                        # monotone
                if dset < len(d):                   # key repeat
                    return 1
                else:
                    return 6
            else:                                   # otherwise
                return 4

    def pr(r):                              # path cost for rows
        a, b, c = r
        rset = len(set(r))
        monotone = a <= b <= c or a >= b >= c

        if rset == 1:                       # same row: AAA
            return 0
        elif rset == 2:                     # two rows used
            if monotone:                        # monotone: AAB
                return 1 if a > c else 2            # downward, or upward
            else:                               # ABA
                return 3
        else:                               # all three used
            if monotone:                        # monotone
                return 4 if a > c else 6            # ABC or CBA
            else:
                return 5 if a > c else 7            # BAC or BCA

    keys = [keymap[c] for c in triad]

    return [ph([k['hand'] for k in keys]), pr([k['row'] for k in keys]), pf([k['finger'] for k in keys], triad)]


def ease_triad(triad):
    #bs = [keymap[triad[i]]['base'] * wb[i] / 10 for i in range(len(triad))]
    # ps = [penalties[c] for c in triad]
    ss = path(triad)
    #print(triad + ' ---------------------------')
    #print('stroke path: ' + str(ss))
    # commented out, compound(ps, wp), dot_product(bs, wb)
    components = dot_product(ss, ws)
    #print('penalty: %.2f' % components)
    return 0


def ease_word(w):
    base_total = 0
    total = 0

    freqs = Counter(w)
    for c in freqs:
        base_total += keymap[c]['base'] * freqs[c]

    for triad in adj_triples(w):
        total += ease_triad(triad)
        #print(triad)

    total += base_total / len(w)

    return round(total, 2)

'''
with open('big.txt') as text:
    comb = ''.join([t for t in text])
    print(ease_word(normalize(comb)))
'''

import csv
with open('frequency_data_cleaned.csv', 'r') as file:
    #reader = csv.DictReader(file)
    reader = csv.reader(file)
    words = []
    for r in reader:
        words += [(r[0].strip(), int(r[1]))]
    #print(words)
    total_count = sum([w[1] for w in words])
    print(total_count)
    words = [(w[0], round(100 * w[1]/total_count, 4)) for w in words]

    def buf(w, n):
        w = str(w)
        return w + ' ' * (n - len(w))

    savings = []
    for word in words:
        w = word[0].lower()
        e = ease_word(w)
        saving = word[1] * (e/10 + 10) * (len(w) - 1)
        #print(buf(w, 20), buf(e, 8), buf(round(e * len(w), 2), 8), saving)
        savings += [(round(saving, 2), w)]

    savings.sort(reverse=True)
    for i, s in enumerate(savings):
        print(i+1, s)
    #print(*savings[:], sep='\n')

    contracts = ["t n h b f ta w fo u in "
                 "o ty fr ti ta te sa wu o bu "  # to repeated
                 "it ab p wa hs n't ot tr tnk sh "
                 "kn d wi he bc cu mk wy on yr "
                 "tm ur oth j thru wh ge smt sm ca "
                 "wn em tes tk fst nt cm er we l "
                 "gov by li at tn shu tg mo bt sk "
                 "thn stu lo unt one amer tos or al cte "
                 "ath wom ut dt re chi qu pb fam him "
                 "bec af g info fi wir comp c as v "    # 100
                 "mo el tr na prog gv ag mn ol hr "  # mo - more repeated
                 "st gu poc tl ba imp nati com ust ou "
                 "ho bis en e bv lf prez m mil ne "  # if as e
                 "two sta its sy dw wo wae three dur wor "  # way as wae
                 "gp le ert num da cl inati aw prov devt "
                 "wie ov gra bef edu relp hap ey bei ser "
                 "fe cont ew exp up hoe ue la inci nyt "
                 ""]

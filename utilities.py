from operator import mul


def dot_product(xs, ys):
    return sum(map(mul, xs, ys))


# eg: print(*adj_triples('fish'))
def adj_triples(s):
    yield from map(lambda i: s[i:i+3], range(len(s) - 3 + 1))


# consider only alpha characters and spaces
def normalize_alpha(s):
    return ''.join([c for c in s.lower() if c.isalpha() or c == ' '])
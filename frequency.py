from collections import Counter
#import matplotlib.pyplot as plt

files = ['python_collections.txt', 'contraction-suggester.txt']

with open(files[1], 'r') as text:
    lines = []
    for line in text:
        lines.append(line)
    lines = ''.join(lines).lower()
    n = len(lines)
    freq = Counter(lines)
    del freq[' ']
    freq = [x for x in freq.items()]
    freq = [(x[1], x[0]) for x in freq]

    freq.sort(reverse=True)
    #print(freq)

    for f, x in freq:
        print(x, '#' * (f // (n // 1600)))


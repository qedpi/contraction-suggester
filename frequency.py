from collections import Counter
#import matplotlib.pyplot as plt

files = ['python_collections.txt', 'contraction-suggester.txt', 'big.txt']

with open(files[0], 'r') as text:
    lines = []
    for line in text:
        lines.append(line)
    lines = ''.join(lines)
    linez = lines
    lines = lines.lower()
    n = len(lines)
    freq = Counter(lines)
    del freq[' ']
    freq = [x for x in freq.items()]
    freq = [(x[1], x[0]) for x in freq]

    lines = lines.replace(' ', '')
    nupper = len([x for x in linez if x.isupper()])
    nlower = len([x for x in linez if x.islower()])
    bif = Counter(lines[i:i+2] for i in range(len(lines) - 2))
    bif = sorted([(bif[x], x) for x in bif], reverse=True)

    freq.sort(reverse=True)
    #print(freq)

    for f, x in freq:
        print(x, '#' * (f // (n // 1600)))


    def good(x):
        a, b = x
        def well(a):
            return not a.isalpha()
        return well(a) and well(b)

    for f, x in bif:
        if good(x):


            print(x, '#' * (f // (n // 12000)))

    print(nupper, nlower, len(lines))



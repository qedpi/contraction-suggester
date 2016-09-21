# Default model params
kb, kp, ks = 0.3555, 0.6423, 0.4268
ws = [1, 0.3, 0.3]
wb = [1, 0.367, 0.235]
wp = [1, 0.367, 0.235]

# base, hand, finger, row penalties, and their relative weights
p_weights = [1, 1, 1, 1]  # w0, wh, wf, wr
Pf = [1, 0.5, 0, 0, 0, 0, 0.5,  1]  # pinkies bad, ring-finger decent, otherwise perfect
Pr = [1.5, 0.5, 0, 1]  # number row worst, bottom row bad, top row decent, home-row perfect
Ph = {'L': 0, 'R': 0}  # assuming ambidextrous is good, don't penalize left hand usage

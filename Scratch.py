import random

k = [10, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 24, 27, 32, 38, 47, 62, 82]
n = random.randint(0, sum(k))
a = ['b', 'g', 'j', 'f', 'h', 'd', 'p', 'r', 't', 'm', 'c', 'x', 'q', 'n', 'k', 'l', unichr(8217), 's']
try:
    h = a[[i < n for i in [sum(k[:i]) for i in range(len(k))]].index(False)]
except ValueError:
    h = a[-1]
print(h)

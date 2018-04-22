"""
Functions for practicing decision tree algorithms.
"""

import math

def percent(S, D, positive=True):
    """
    Returns what percent of S has desired property D.
    S is a set of dicts, D is a key in those dicts.
    """
    return len([X for X in S if X[D] == positive])/len(S)

def H(S, D):
    """
    Returns the entropy for the data subset S, a set of dicts.
    D is the desired attribute in those dicts.
    """
    p0 = percent(S, D)
    p1 = 1-p0
    if p0 == 0 or p1 == 0: return 0
    return -p0*math.log2(p0) -p1*math.log2(p1)

def Gain(S, D, A):
    """
    Returns the Gain for splitting on attribute A in subset S.
    S is a dict. D is the desired attribute. A is a key in that dict.
    """
    result = H(S, D)
    for V in set(X[A] for X in S):
        result -= percent(S, A, V) * H([X for X in S if X[A] == V], D)

    return result

if __name__ == '__main__':
    S = [
            {'Tall': True, 'Fat': 1, 'Happy': True,},
            {'Tall': True, 'Fat': 1, 'Happy': False},
            {'Tall': True, 'Fat': 2, 'Happy': True},
            {'Tall': False, 'Fat': 3, 'Happy': False} ]
    print(percent(S, 'Happy'))
    print(percent(S, 'Fat', 2))
    print(H(S, 'Happy'))
    print(Gain(S, 'Happy', 'Fat'))

    cutoff = 6.9
    h = lambda x: x >= cutoff
    S = [
            {'Gender': 'M', 'Height': h(5.2), 'King': False},
            {'Gender': 'M', 'Height': h(6.2), 'King': False},
            {'Gender': 'M', 'Height': h(6.8), 'King': False},
            {'Gender': 'M', 'Height': h(6.9), 'King': True},
            {'Gender': 'M', 'Height': h(6.1), 'King': True},
            {'Gender': 'F', 'Height': h(5.3), 'King': True},
            {'Gender': 'F', 'Height': h(6.2), 'King': False},
            ]
    print('Entropy of King:', H(S, 'King'))
    print('Gain for Gender:', Gain(S, 'King', 'Gender'))
    print('Gain for Height:', Gain(S, 'King', 'Height'))

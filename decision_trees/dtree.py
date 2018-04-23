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

def ID3(S, D):
    """
    Constructs a decision tree.
    S is a set of data points, D is the desired attribute in the dicts of S.
    """
    # End if we have a pure data set
    purity = percent(S, D)
    if purity == 1:
        return D
    if purity == 0:
        return "Not "+D

    split_attr = None
    split_gain = -1
    binary_cutoff = None

    attrs = [attr for attr in S[0] if attr != D and not attr.startswith('_id3')]
    for attr in attrs:

        if type(S[0][attr]) == int or type(S[0][attr]) == float:
            # Check all binary splits
            for value in set(X[attr] for X in S):

                # Expensively add a new attribute to split the data
                fake_attr = '_id3{}>={}'.format(attr, value)
                for X in S:
                    if not hasattr(X, fake_attr):
                        X[fake_attr] = X[attr] >= value
                gain = Gain(S, D, fake_attr)

                if gain > split_gain:
                    split_attr = fake_attr
                    split_gain = gain
                    binary_cutoff = value
        else:
            # Assess gain simply
            gain = Gain(S, D, attr)
            if gain > split_gain:
                split_attr = attr
                split_gain = gain
                binary_cutoff = None

    # Split the data and recurse
    leftS = [X for X in S if X[split_attr]]
    rightS = [X for X in S if not X[split_attr]]

    left = ID3(leftS, D)
    right = ID3(rightS, D)

    return [split_attr, split_gain, left, right]

if __name__ == '__main__':
    S = [
            {'Tall': True,  'Fat': 1,   'Happy': True,},
            {'Tall': True,  'Fat': 0.5, 'Happy': False},
            {'Tall': True,  'Fat': 2,   'Happy': True},
            {'Tall': False, 'Fat': 3,   'Happy': False},
            ]

    print(ID3(S, 'Happy'))

    S = [
            {'Male': True,  'Height': 5.2, 'King': False},
            {'Male': True,  'Height': 6.2, 'King': False},
            {'Male': True,  'Height': 6.8, 'King': False},
            {'Male': True,  'Height': 6.9, 'King': True},
            {'Male': True,  'Height': 6.1, 'King': True},
            {'Male': False, 'Height': 5.3, 'King': True},
            {'Male': False, 'Height': 6.2, 'King': False},
            ]

    print(ID3(S, 'King'))

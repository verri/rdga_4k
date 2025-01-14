def catbird(m, n, k, lmbd=.5, eps=.5, random_state=None):

    # libraries
    import numpy as np
    import math
    from numpy.random import RandomState
    
    # checking
    assert type(m) == int and m > 1
    
    assert type(n) == int and n > 1
    
    assert type(k) == int and k > 1
    
    assert type(lmbd) == float and (lmbd >= 0.0 and lmbd <= 1.0)
    
    assert type(eps) == float and (eps >= 0.0 and eps <= 1.0)
    
    # tools
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def sig_f(x):
        return [sigmoid(i) for i in x]

    def binarize(x, lmbd):
        xbin = []
        for i in range(len(x)):
            if x[i] < lmbd:
                xbin.append(1)
            else:
                xbin.append(0)
        return xbin

    # initialization
    s = int(n//2)+1
    rem = n - s
    
    n_samples_per_center = [int(m // k)] * k
    for i in range(m % k):
        n_samples_per_center[i] += 1

    X = []
    y = []
    q = -1

    for i in range(len(n_samples_per_center)):
        if random_state == None:
            W = RandomState().normal(0, 1, (s, s))
            idx = list(RandomState().choice(list(range(n)), size=rem, replace=False))
            idx.sort()
            
        elif type(random_state) == int:
            W = RandomState(random_state*(i+1)).normal(0, 1, (s, s))
            idx = list(RandomState(random_state*(i+1)).choice(list(range(n)), size=rem, replace=False))
            idx.sort()
            
        else:
            assert type(random_state) == RandomState
            
        q += 1
        for j in range(n_samples_per_center[i]):
            if random_state == None:
                A = [RandomState().normal(0, 1, s)]
            else:
                A = [RandomState(random_state*(j+1)).normal(0, 1, s)]
                
            A_W = [[sum(a*b for a,b in zip(A_row,W_col)) for W_col in zip(*W)] for A_row in A]
            A_W_sig = sig_f(A_W[0])
                    
            for l in idx:
                A_W_sig.insert(l, eps)
            
            A_W_sig_bin = binarize(A_W_sig, lmbd)
            
            y.append(q)
            X.append(A_W_sig_bin)
                
    X = np.array(X, dtype=np.int64)
    y = np.array(y, dtype=np.int64)
    
    return X, y
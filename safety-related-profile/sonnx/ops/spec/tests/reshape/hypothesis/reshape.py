import numpy as np

def size (dims):
    result = 1
    for x in dims:
        result = result * x
    return result

def offset(ks, ds):
    if ks and ds:
        k, ks_rest = ks[0], ks[1:]
        ds_rest = ds[1:]
        return k * size(ds_rest) + offset(ks_rest, ds_rest)
    else:
        return 0
    
def index(p, ds):
    if ds:
        _, ds_rest = ds[0], ds[1:]  
        return [p // size(ds_rest)] + index(p % size(ds_rest), ds_rest)
    else:
        return []


def reshape(X,Y):
    for idx in np.ndindex(Y.shape):
        idx_list = list(idx)
        y_coords_flat = offset(idx_list, list(Y.shape))
        x_coords = index(y_coords_flat, list(X.shape))
        Y[idx] = X[tuple(x_coords)]
    return Y
    
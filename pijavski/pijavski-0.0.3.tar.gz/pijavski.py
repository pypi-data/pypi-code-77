from _pijavski import ffi, lib
import numpy as np

@ffi.def_extern()
def fun(x, f):
    f[0] = (-1)*np.cos(x[0])+0.00001*(x[0]-100*3.1415)*(x[0]-100*3.1415)


def get_minimum(lip=2, xl=-50000, xu=90000, precision=0.000000000001, maxiter=300000):
    x0 = ffi.new("double *")
    f = ffi.new("double *")
    M = ffi.new("double *", lip)
    x1 = ffi.new("double *", xl)
    x2 = ffi.new("double *", xu)
    prec = ffi.new("double *", precision)
    maxit = ffi.new("int *", maxiter)
    
    res = lib.Pijavski(x0, f, lib.fun, M, x1, x2, prec, maxit)
    print(res, x0[0], f[0], prec[0], maxit[0])


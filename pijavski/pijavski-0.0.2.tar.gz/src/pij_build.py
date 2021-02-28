import cffi

ffibuilder = cffi.FFI()

ffibuilder.cdef("""

    void fun(double* x, double* f);
    typedef void ( *USER_FUNCTION)(double *, double *);
    
    int Pijavski(double* x0, double *val, USER_FUNCTION F, double* Lip, double* Xl, double* Xu, double* precision, int* maxiter);
    
    extern "Python" void fun(double* x, double* f);
    """, override=True)

ffibuilder.set_source("_pijavski", r"""
    #include "/home/santiagov/deakin/pijavski/tests/packaging/src/heap.h"
    #include "/home/santiagov/deakin/pijavski/tests/packaging/src/pijavski.h"
""",
    sources=['./src/pijavski.cpp'])


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

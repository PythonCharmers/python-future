class longsubclass(long):
    pass

def test_numpy_cast_as_long():
    import numpy as np
    a = np.arange(10**6, dtype=np.float64).reshape(10**4, 100)
    b = a.astype(longsubclass)
    print(b.dtype)
    assert b.dtype == np.int64

test_numpy_cast_as_long()

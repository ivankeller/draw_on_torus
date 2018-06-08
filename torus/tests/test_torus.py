from torus.torus import *

def test_torus_coordinates():
    assert Point.torus_coodinates(1, 1, 2, 2) == (1, 1)
    assert Point.torus_coodinates(2.2, 3.1, 1, 1) == (0.20000000000000018, 0.10000000000000009)
    

    

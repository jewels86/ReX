import numpy as np
from shapely.geometry import Point, Polygon

epsilon = 1e-15 # you can make this smaller if your shape is tiny

# Below are some example shapes

# should have an area of around 1.72 (unit pentagon)
pentagon = [
    (0, -0.851),
    (0.809, -0.263),
    (0.5, 0.688),
    (-0.5, 0.688),
    (-0.809, -0.263),
]

# should have an area of 14- its a 2x4 + 2x3
l_shape = [
    (0, 0),
    (2, 0),
    (2, 3),
    (4, 3),
    (4, 5),
    (0, 5)
]

# should have an area of 1
s = np.sqrt(2 / (3 * np.sqrt(3)))
hexagon = [
    (s, 0),
    (s/2, s*np.sqrt(3)/2),
    (-s/2, s*np.sqrt(3)/2),
    (-s, 0),
    (-s/2, -s*np.sqrt(3)/2),
    (s/2, -s*np.sqrt(3)/2)
]

# this was for the original assigment :) 
# shoelace confirmed the area to be around 5859
cafeteria = [
    (0,                 0            ),
    (-5/6,              59  + (3/4)),
    (-9,                61          ),
    (-5     - (2/5),    88      + 0.5),
    (-2     - (3/6),    87      + (5/6)),
    (1      + (1/6),    142     + (2/3)),
    (53     + 0.5,      118     + (2/3)),
    (47,                82      + (5/12)),
    (39     + (7/12),   81      + (11/12)),
    (42     + (2/12),   53      + (5/12)),
    (44     + (5/12),   53      + (1/12)),
    (36     + 0.5,      8       + (1/12)),
    (28     + (5/12),   14      + (8/12)),
    (14,                0)
    
] 

# self-intersecting star (pentagram style - edges cross)
self_intersecting_star = [
    (0, 3),      # top
    (2.5, -1),   # bottom right
    (-2, 1),     # left
    (2, 1),      # right
    (-2.5, -1),  # bottom left
    (0, 3)       # back to top (closes it)
]

np.seterr(all='raise')

shape = [np.array(p) for p in hexagon] # put whatever shape you want in here 
max_iterations = len(shape) * 5
index = lambda i, p: i % len(p)
get = lambda i, arr: np.array(arr[index(i, arr)])
magnitude = lambda v: np.sqrt(v[0]**2 + v[1]**2)
_not_nan = lambda x: x == x
not_nan = lambda x: _not_nan(x[0]) and _not_nan(x[1])
cross = lambda v1, v2: v1[0]*v2[1] - v1[1]*v2[0]

def in_polygon(point: np.ndarray, polygon: list) -> bool: 
    poly = Polygon(polygon)
    p = Point(point)
    return poly.contains(p) or poly.touches(p)

def _area(ab: float, ac: float, bc: float) -> float: 
    s = 0.5 * (ab + ac + bc)
    return np.sqrt(s * (s - ab) * (s - ac) * (s - bc))
def area(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    ab = magnitude(b - a)
    ac = magnitude(c - a)
    bc = magnitude(c - b)
    return _area(ab, ac, bc)


def attempt(ai: int, polygon: list):
    a = get(ai, polygon)
    b = get(ai + 1, polygon) # dropped if X is used
    d = get(ai + 2, polygon) # dropped if X is used
    f = get(ai + 3, polygon)
    c = get(ai - 1, polygon) # dropped if Y is used
    e = get(ai - 2, polygon) # dropped if Y is used
    g = get(ai - 3, polygon)

    u = b[0] - a[0]
    p = d[0] - a[0]
    r = f[0] - b[0]
    v = b[1] - a[1]
    q = d[1] - a[1]
    s = f[1] - b[1]
    X_x = a[0] + (p * ((u*s) - (r*v))) / ((p*s) - (q*r))
    X_y = a[1] + (q * ((u*s) - (r*v))) / ((p*s) - (q*r))
    X = np.array((X_x, X_y)) # intersection of ad bf

    u = c[0] - a[0]
    p = e[0] - a[0]
    r = g[0] - c[0]
    v = c[1] - a[1]
    q = e[1] - a[1]
    s = g[1] - c[1]
    Y_x = a[0] + (p * ((u*s) - (r*v))) / ((p*s) - (q*r))
    Y_y = a[1] + (q * ((u*s) - (r*v))) / ((p*s) - (q*r))
    Y = np.array((Y_x, Y_y)) # intersection of ae cg

    A = 0

    useX = not_nan(X) and in_polygon(X, polygon)
    if useX:
        A += area(b, X, d)
        A += area(d, X, f)
        A += area(b, X, a)

    useY = not_nan(Y) and in_polygon(Y, polygon)
    if useY:
        A += area(a, Y, c)
        A += area(c, Y, e)
        A += area(e, Y, g)

    dropped = [
        b if useX else None,
        d if useX else None,
        c if useY else None,
        e if useY else None
    ]
    dropped = [pt for pt in dropped if pt is not None]
    
    return (X if useX else None, Y if useY else None, A, dropped)

def rex(_shape, verbose=True):
    total = 0
    target = 0
    for i in range(max_iterations):
        if len(_shape) < 3:
            if (verbose): print("Final shape has less than 3 points.")
            break
        elif len(_shape) == 3:
            if (verbose): print ("Final shape is a triangle, adding its area.")
            total += area(_shape[0], _shape[1], _shape[2])
            break
        elif len(_shape) == 4 or len(_shape) == 5: 
            if (verbose): print (f"Final shape has {len(_shape)} points, adding its area.")
            shoelace_area = 0.0
            n = len(_shape)
            for j in range(n):
                k = (j + 1) % n
                shoelace_area += _shape[j][0] * _shape[k][1]
                shoelace_area -= _shape[k][0] * _shape[j][1]
            total += abs(shoelace_area) / 2.0
            break
            
        try: X, Y, A, dropped = attempt(target, _shape)
        except Exception as e:
            target = index(target + 1, _shape)
            if (verbose): print(f"Iteration {i + 1}: {e}, moving to next target ({target - 1} -> {target}).")
            continue
        
        X_exists = X is not None
        Y_exists = Y is not None
        n_dropped = len(dropped) - (1 if X_exists else 0) - (1 if Y_exists else 0)
        if (verbose): print(f"Iteration {i + 1}: target={target}, len={len(_shape)} - {n_dropped}, X={X_exists}, Y={Y_exists}, A={A:.2f}, total={total:.2f} -> {total + A:.2f}")

        if A < epsilon:
            target = index(target + 1, _shape)
            if (verbose): print(f"Iteration {i + 1}: Area below epsilon, moving to next target ({target - 1} -> {target}).")
            continue
        
        new_shape = []
        for j in range(len(_shape)):
            pt = _shape[j]
            if any(np.array_equal(pt, drop) for drop in dropped):
                continue
            new_shape.append(pt)
        
        target_in_new = None
        for j in range(len(new_shape)):
            if np.array_equal(new_shape[j], _shape[target]):
                target_in_new = j
                break
        
        if Y is not None and target_in_new is not None:
            new_shape.insert(target_in_new, Y)
            target_in_new += 1  
        
        if X is not None and target_in_new is not None:
            new_shape.insert(target_in_new + 1, X)

        _shape = new_shape
        total += A

    return total


print(f"Final area: {rex(shape)}")



import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon

epsilon = 1e-15

pentagon = [
    (0, -0.851),
    (0.809, -0.263),
    (0.5, 0.688),
    (-0.5, 0.688),
    (-0.809, -0.263),
]
l_shape = [
    (0, 0),
    (2, 0),
    (2, 3),
    (4, 3),
    (4, 5),
    (0, 5)
]

s = np.sqrt(2 / (3 * np.sqrt(3)))
hexagon = [
    (s, 0),
    (s/2, s*np.sqrt(3)/2),
    (-s/2, s*np.sqrt(3)/2),
    (-s, 0),
    (-s/2, -s*np.sqrt(3)/2),
    (s/2, -s*np.sqrt(3)/2)
]
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

np.seterr(all='raise')

# self-intersecting star (pentagram style - edges cross)
self_intersecting_star = [
    (0, 3),      # top
    (2.5, -1),   # bottom right
    (-2, 1),     # left
    (2, 1),      # right
    (-2.5, -1),  # bottom left
    (0, 3)       # back to top (closes it)
]

shape = [np.array(p) for p in cafeteria]
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
    X = np.array((X_x, X_y))

    u = c[0] - a[0]
    p = e[0] - a[0]
    r = g[0] - c[0]
    v = c[1] - a[1]
    q = e[1] - a[1]
    s = g[1] - c[1]
    Y_x = a[0] + (p * ((u*s) - (r*v))) / ((p*s) - (q*r))
    Y_y = a[1] + (q * ((u*s) - (r*v))) / ((p*s) - (q*r))
    Y = np.array((Y_x, Y_y))

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

def rex(visualize=False):
    total = 0
    target = 0
    _shape = shape
    
    if visualize:
        fig, ax = plt.subplots(figsize=(12, 10))
        colors = plt.cm.viridis(np.linspace(0, 1, max_iterations))
        iteration_shapes = []
        
    for i in range(max_iterations):
        if visualize and len(_shape) >= 3:
            iteration_shapes.append((_shape.copy(), target, None, None))
        
        if len(_shape) < 3:
            print ("Final shape has less than 3 points.")
            break
        elif len(_shape) == 3:
            print ("Final shape is a triangle, adding its area.")
            total += area(_shape[0], _shape[1], _shape[2])
            break
        elif len(_shape) == 4 or len(_shape) == 5: 
            print (f"Final shape has {len(_shape)} points, adding its area.")
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
            print(f"Iteration {i + 1}: {e}, moving to next target ({target - 1} -> {target}).")
            continue

        if visualize and (X is not None or Y is not None):
            iteration_shapes[-1] = (_shape.copy(), target, X.copy() if X is not None else None, Y.copy() if Y is not None else None)
        
        X_exists = X is not None
        Y_exists = Y is not None
        n_dropped = len(dropped) - (1 if X_exists else 0) - (1 if Y_exists else 0)
        print(f"Iteration {i + 1}: target={target}, len={len(_shape)} - {n_dropped}, X={X_exists}, Y={Y_exists}, A={A:.2f}, total={total:.2f} -> {total + A:.2f}")

        if A < epsilon:
            target = index(target + 1, _shape)
            print(f"Iteration {i + 1}: Area below epsilon, moving to next target ({target - 1} -> {target}).")
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
    
    if visualize:
        if len(_shape) >= 3:
            iteration_shapes.append((_shape.copy(), None, None, None))
        
        for idx, (shape_data, tgt, X, Y) in enumerate(iteration_shapes):
            alpha = 0.3 + (0.5 * idx / len(iteration_shapes))  
            polygon_points = np.array(shape_data + [shape_data[0]])
            
            linewidth = 1.0 + (1.5 * idx / len(iteration_shapes))
            ax.plot(polygon_points[:, 0], polygon_points[:, 1], 
                   color=colors[idx], linewidth=linewidth, alpha=0.9, 
                   label=f'Iter {idx+1} ({len(shape_data)} pts)', zorder=idx+1)
            ax.fill(polygon_points[:, 0], polygon_points[:, 1], 
                   alpha=alpha*0.2, color=colors[idx])
            
            if tgt is not None and tgt < len(shape_data):
                a = shape_data[tgt]
                b = shape_data[(tgt + 1) % len(shape_data)]
                c = shape_data[(tgt - 1) % len(shape_data)]
                d = shape_data[(tgt + 2) % len(shape_data)]
                e = shape_data[(tgt - 2) % len(shape_data)]
                f = shape_data[(tgt + 3) % len(shape_data)]
                g = shape_data[(tgt - 3) % len(shape_data)]
                
                if X is not None:
                    ax.plot([a[0], d[0]], [a[1], d[1]], '--', color='blue', alpha=0.5, linewidth=1, zorder=1)
                    ax.plot([b[0], f[0]], [b[1], f[1]], '--', color='blue', alpha=0.5, linewidth=1, zorder=1)
                
                if Y is not None:
                    ax.plot([a[0], e[0]], [a[1], e[1]], '--', color='red', alpha=0.5, linewidth=1, zorder=1)
                    ax.plot([c[0], g[0]], [c[1], g[1]], '--', color='red', alpha=0.5, linewidth=1, zorder=1)
                
                ax.text(a[0], a[1], 'a', fontsize=10, fontweight='bold', 
                       color='purple', ha='center', va='center', zorder=1000,
                       bbox=dict(boxstyle='circle,pad=0.3', facecolor='white', edgecolor='purple', linewidth=1.5))
            
            if X is not None:
                ax.text(X[0], X[1], 'X', fontsize=10, fontweight='bold', 
                       color='blue', ha='center', va='center', zorder=1000,
                       bbox=dict(boxstyle='circle,pad=0.3', facecolor='white', edgecolor='blue', linewidth=1.5))
            if Y is not None:
                ax.text(Y[0], Y[1], 'Y', fontsize=10, fontweight='bold', 
                       color='red', ha='center', va='center', zorder=1000,
                       bbox=dict(boxstyle='circle,pad=0.3', facecolor='white', edgecolor='red', linewidth=1.5))
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.25, linestyle='--', linewidth=0.5)
        ax.legend(loc='best', fontsize=8, framealpha=0.9)
        ax.set_title(f'Recursive Exploration: Total area = {total:.4f}', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.set_facecolor('#fafafa')
        plt.tight_layout()
        plt.show()

    return total

print(rex(visualize=True))
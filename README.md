# ReX
An algorithm for finding the area of polygons using **Re**cursive e**X**ploration.

## What is ReX?
ReX is an algorithm that can find the area of most polygons recursively. 
As long as you know the points and their order, ReX can give you the area!

Each iteration, ReX selects a point $a$ and gets:
- $b$: the point ahead of it
- $c$: the point behind it
- $d$: the point 2 indices ahead of it
- $e$: the point 2 indices behind it
- $f$: the point 2 indices ahead of $b$ (3 ahead of $a$)
- $g$: the point 2 indices behind $c$ (3 behind $a$)

Next, we find the intersection of line segments $ae$ and $bf$ to get a point $X$, which we use to get the areas of the triangles $\triangle bXd$, $\triangle dXf$, and $\triangle bXa$.
We do the same for $ad$ and $cg$, making a point $Y$ to find the areas of $\triangle aYc$, $\triangle cYe$, $\triangle eYg$. 
We then construct a new polygon by dropping points $b$, $d$, $c$, $e$, and adding $X$ and $Y$. 
The next iteration will use $a$ again, but this time on the new polygon we formed this iteration.

In some cases, $X$ or $Y$ will fall outside the polygon or just not exist in general; if this happens, ReX will discard the areas found and keep the respective points ($b$ and $d$ for $X$, $c$ and $e$ for $Y$) for the next iteration.

If ReX finds that no progress is being made from $a$, it will move to the next point in an attempt to change things up.

## What was it for?
My pre-calc teacher told us to find the area of our cafeteria, and someone said something about the Shoelace theorem, which got me thinking about unrolling polygons. 
I came up with this a few days later because I really didn't want to divide the whole thing up into triangles.

### Why not just use Shoelace?
At the time, I didn't realize it worked on all polygons, no matter how weird; I just thought it was for more normal shapes. 
So I derived an entirely new algorithm for finding the area of polygons twice before finding out it actually does work on everything.
It was fun to make, but you should absolutely use shoelace. Unless you feel like you want a cool visualization. Then use this :)

## Usage
Replace the $shape$ variable at the top with whatever your shape is:
```py
my_weird_shape = [
  (100, 2787),
  (82379874, 92384729348),
  (3274234, 8734287.238),
  (0, 0),
  (0, 1),
  (10, 20)
]

shape = [np.array(p) for p in my_weird_shape] # make sure you end up with a list of numpy tuples, not python ones
```

## Examples
Testing this on a hexagon formed with:
```py
s = np.sqrt(2 / (3 * np.sqrt(3)))
hexagon = [
    (s, 0),
    (s/2, s*np.sqrt(3)/2),
    (-s/2, s*np.sqrt(3)/2),
    (-s, 0),
    (-s/2, -s*np.sqrt(3)/2),
    (s/2, -s*np.sqrt(3)/2)
]
```
We should get an area of 1, which ReX correctly found:
<img width="1126" height="989" alt="image" src="https://github.com/user-attachments/assets/3afbf5dd-abb9-47a0-8337-ef8e74604ba7" />
```
Iteration 1: target=0, len=6 - 2, X=True, Y=True, A=0.56, total=0.00 -> 0.56
Final shape has 4 points, adding its area.
1.0
```

Or, with the cafeteria:
<img width="625" height="975" alt="image" src="https://github.com/user-attachments/assets/cceb6332-bdb7-4897-8e76-47a10b343c7b" />
```
Iteration 1: target=0, len=14 - 0, X=False, Y=False, A=0.00, total=0.00 -> 0.00
Iteration 1: Area below epsilon, moving to next target (0 -> 1).
Iteration 2: target=1, len=14 - 2, X=True, Y=True, A=601.29, total=0.00 -> 601.29
Iteration 3: target=1, len=12 - 0, X=False, Y=False, A=0.00, total=601.29 -> 601.29
Iteration 3: Area below epsilon, moving to next target (1 -> 2).
Iteration 4: target=2, len=12 - 1, X=False, Y=True, A=498.08, total=601.29 -> 1099.36
Iteration 5: target=2, len=11 - 2, X=True, Y=True, A=2105.19, total=1099.36 -> 3204.55
Iteration 6: target=2, len=9 - 1, X=False, Y=True, A=363.55, total=3204.55 -> 3568.10
Iteration 7: target=2, len=8 - 1, X=False, Y=True, A=1454.37, total=3568.10 -> 5022.47
Iteration 8: target=2, len=7 - 0, X=False, Y=False, A=0.00, total=5022.47 -> 5022.47
Iteration 8: Area below epsilon, moving to next target (2 -> 3).
Iteration 9: target=3, len=7 - 1, X=True, Y=False, A=217.32, total=5022.47 -> 5239.80
Iteration 10: target=3, len=6 - 1, X=True, Y=False, A=411.09, total=5239.80 -> 5650.88
Final shape has 5 points, adding its area.
5859.536805555559
```
## Limitations
If your polygon is self-intersecting, you'll get a result but I'm not sure exactly what it represents. Take it with a grain of salt.

## Contributing
If you find a case that ReX can't solve, let me know- I'll add it to the list of limitations. And if you end up using ReX for some reason, reach out to me! I'd love to hear about it.

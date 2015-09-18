# A\* Search
## Author: Adrian Chen

The code can be run using:
```
$ python aStar.py World1.txt manhattan
```
or
```
$ python aStar.py World1.txt diagonal
```

The diagonal heuristic calculates possible distance including diagonal distances, whereas the manhattan distance does not.
The diagonal heuristic is calculated the same way the diagonal is calculated, with a score of 14 for a diagonal move, and a score of 10 for a vertical or horizontal move. This can be calculated by the following:

```
10*abs(delta_x) + 10*abs(delta_y) + (14 - 20) * min(delta_x, delta_y)
```

Using a diagonal heuristic certainly has an advantage over a manhattan heuristic. The final path discovered is more optimal, however the number of squares expolored is also higher, meaning it is slower.
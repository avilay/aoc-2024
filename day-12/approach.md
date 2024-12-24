Basic Algo -

Take all the plots with perimeter > 0
Group them into -
  * same row consecutive columns
  * same column consective rows

Take all the plots with perimeter > 1
Group them into -
  * same row consecutive columns
  * same column consective rows

...And so on.

The number of groups is the region perimeter

```
    [0] [1] [2] [3] [4] [5]
[0]  A   A   A   A   A   A
[1]  A   *   A   B   B   A
[2]  A   A   A   B   B   A
[3]  A   B   B   A   A   A
[4]  A   B   B   A   *   A
[5]  A   A   A   A   A   A
```

```
Plots > 1
Same row consecutive columns
[0 x 3]: <Plot(A T 2)>
[0 x 4]: <Plot(A T 2)>

[5 x 1]: <Plot(A T 2)>
[5 x 2]: <Plot(A T 2)>

Same column consecutive rows
[3 x 0]: <Plot(A T 2)>
[4 x 0]: <Plot(A T 2)>
[5 x 0]: <Plot(A T 2)>

[1 x 5]: <Plot(A T 2)>
[2 x 5]: <Plot(A T 2)>


Plots > 0
Same row and consecutive columns
[0 x 0]: <Plot(A T 2)>
[0 x 1]: <Plot(A T 1)>
[0 x 2]: <Plot(A T 1)>
[0 x 3]: <Plot(A T 2)>
[0 x 4]: <Plot(A T 2)>
[0 x 5]: <Plot(A T 2)>

[0 x 5]: <Plot(A T 2)>
[5 x 1]: <Plot(A T 2)>
[5 x 2]: <Plot(A T 2)>
[5 x 3]: <Plot(A T 1)>
[5 x 4]: <Plot(A T 1)>
[5 x 5]: <Plot(A T 2)>

[2 x 1]: <Plot(A T 1)>
[2 x 2]: <Plot(A T 2)>

[3 x 3]: <Plot(A T 2)>
[3 x 4]: <Plot(A T 1)>


Same column consecutive rows
[0 x 0]: <Plot(A T 2)>
[1 x 0]: <Plot(A T 1)>
[2 x 0]: <Plot(A T 1)>
[3 x 0]: <Plot(A T 2)>
[4 x 0]: <Plot(A T 2)>
[5 x 0]: <Plot(A T 2)>

[1 x 5]: <Plot(A T 2)>
[2 x 5]: <Plot(A T 2)>
[3 x 5]: <Plot(A T 1)>
[4 x 5]: <Plot(A T 1)>
[5 x 5]: <Plot(A T 2)>

[1 x 2]: <Plot(A T 1)>
[2 x 2]: <Plot(A T 2)>

[4 x 3]: <Plot(A T 1)>
[3 x 3]: <Plot(A T 2)>
```

Ok let me try this with another example  input -
```
    [0] [1] [2] [3] [4]
[0]  E   E   E   E   E
[1]  E   X   X   X   X
[2]  E   E   E   E   E
[3]  E   X   X   X   X
[4]  E   E   E   E   E
```


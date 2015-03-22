b-spline
========
### B-spline interpolation

B-spline interpolation of control points of any dimensionality using [de Boor's algorithm](http://en.wikipedia.org/wiki/De_Boor%27s_algorithm).

Install
-------

```bash
$ npm install b-spline
```

Usage
-----

Basic usage

```javascript
var bspline = require('b-spline');

var points = [
  [-1.0,  0.0],
  [-0.5,  0.5],
  [ 0.5, -0.5],
  [ 1.0,  0.0]
];

var order = 3;

for(var t=0; t<1; t+=0.01) {
  var point = bspline(t, order, points);
}
```

<img src="http://i.imgur.com/ew8CMVj.png" />

Non-uniform rational.

```javascript
var bspline = require('b-spline');

// see 

var points = [
  [ 0.0, -0.5],
  [-0.5, -0.5],

  [-0.5,  0.0],
  [-0.5,  0.5],

  [ 0.0,  0.5],
  [ 0.5,  0.5],

  [ 0.5,  0.0],
  [ 0.5, -0.5],
  [ 0.0, -0.5]  // P0
]

var knots = [
  0, 0, 0, 1/4, 1/4, 1/2, 1/2, 3/4, 3/4, 1, 1, 1
];

var w = Math.pow(2, 0.5) / 2;

var weights = [
  1, w, 1, w, 1, w, 1, w, 1
]

var order = 3;

for(var t=0; t<1; t+=0.01) {
  var point = bspline(t, order, points, knots, weights);
}
```

<img src="http://i.imgur.com/flvmdds.png" />

See [here](http://www.cs.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/NURBS/RB-circles.html) for parameters reference.

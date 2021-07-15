b-spline
========
### B-spline interpolation

B-spline interpolation of control points of any dimensionality using [de Boor's algorithm](http://en.wikipedia.org/wiki/De_Boor%27s_algorithm).

The interpolator can take an optional weight vector, making the resulting curve a Non-Uniform Rational B-Spline (NURBS) curve if you wish so.

The knot vector is optional too, and when not provided an unclamped uniform knot vector will be generated internally.


Install
-------

```bash
$ npm install b-spline
```

Examples
--------

#### Unclamped knot vector

```javascript
var bspline = require('b-spline');

var points = [
  [-1.0,  0.0],
  [-0.5,  0.5],
  [ 0.5, -0.5],
  [ 1.0,  0.0]
];

var degree = 2;

// As we don't provide a knot vector, one will be generated 
// internally and have the following form :
//
// var knots = [0, 1, 2, 3, 4, 5, 6];
//
// Knot vectors must have `number of points + degree + 1` knots.
// Here we have 4 points and the degree is 2, so the knot vector 
// length will be 7.
//
// This knot vector is called "uniform" as the knots are all spaced uniformly,
// ie. the knot spans are all equal (here 1).

for(var t=0; t<1; t+=0.01) {
  var point = bspline(t, degree, points);
}
```

<img src="http://i.imgur.com/MldaigE.png" />


#### Clamped knot vector

```javascript
var bspline = require('b-spline');

var points = [
  [-1.0,  0.0],
  [-0.5,  0.5],
  [ 0.5, -0.5],
  [ 1.0,  0.0]
];

var degree = 2;

// B-splines with clamped knot vectors pass through 
// the two end control points.
//
// A clamped knot vector must have `degree + 1` equal knots 
// at both its beginning and end.

var knots = [
  0, 0, 0, 1, 2, 2, 2
];

for(var t=0; t<1; t+=0.01) {
  var point = bspline(t, degree, points, knots);
}
```

<img src="http://i.imgur.com/KqWdaNK.png" />


#### Closed curves

```javascript
var bspline = require('b-spline');

// Closed curves are built by repeating the `degree + 1` first 
// control points at the end of the curve

var points = [
  [-1.0,  0.0],
  [-0.5,  0.5],
  [ 0.5, -0.5],
  [ 1.0,  0.0],

  // repeat the first `degree + 1` points
  [-1.0,  0.0],
  [-0.5,  0.5],
  [ 0.5, -0.5]
];

var degree = 2;
// The number of control points without the last repeated
// points
var originalNumPoints = points.length - (degree + 1);

// and using an unclamped knot vector

var knots = [
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9
];

/*
Disclaimer: If you are using a unclamped knot vector
with closed curves, you may want to remap the t value
to properly loop the curve.

To do that, remap t value from [0.0, 1.0] to
[0.0, 1.0 - 1.0 / (n + 1)] where 'n' is the number of
the original control points used (discard the last repeated points).

In this case, the number of points is 4 (discarded the last 3 points)
*/
var maxT = 1.0 - 1.0 / (originalNumPoints + 1);

for(var t=0; t<1; t+=0.01) {
  var point = bspline(t * maxT, degree, points, knots);
}
```

<img src="http://i.imgur.com/npF2ke9.png" />


#### Non-uniform rational

```javascript
var bspline = require('b-spline');

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

// Here the curve is called non-uniform as the knots 
// are not equally spaced

var knots = [
  0, 0, 0, 1/4, 1/4, 1/2, 1/2, 3/4, 3/4, 1, 1, 1
];

var w = Math.pow(2, 0.5) / 2;

// and rational as its control points have varying weights

var weights = [
  1, w, 1, w, 1, w, 1, w, 1
]

var degree = 2;

for(var t=0; t<1; t+=0.01) {
  var point = bspline(t, degree, points, knots, weights);
}
```

<img src="http://i.imgur.com/flvmdds.png" />


Usage
-----

### `bspline(t, degree, points[, knots, weights])`

* `t` position along the curve in the [0, 1] range
* `degree` degree of the curve. Must be less than or equal to the number of control points minus 1. 1 is linear, 2 is quadratic, 3 is cubic, and so on.
* `points` control points that will be interpolated. Can be vectors of any dimensionality (`[x, y]`, `[x, y, z]`, ...)
* `knots` optional knot vector. Allow to modulate the control points interpolation spans on `t`. Must be a non-decreasing sequence of `number of points + degree + 1` length values.
* `weights` optional control points weights. Must be the same length as the control point array.
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

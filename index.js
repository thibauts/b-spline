

function interpolate(t, order, points, knots) {

  var n = points.length;    // points count
  var d = points[0].length; // point dimensionality

  if(order < 2) throw new Error('order must be at least 2 (linear)');
  if(order > n) throw new Error('order must be less than point count');

  if(!knots) {
    // build knot vector
    var knots = new Array(n + order);
    for(var i=0; i<n+order; i++) {
      knots[i] = i;
    }
  } else {
    if(knots.length !== n+order) throw new Error('bad knot vector length');
  }

  var domain = [
    order-1,
    knots.length-1 - (order-1)
  ];

  // remap t to the domain where the spline is defined
  var low  = knots[domain[0]];
  var high = knots[domain[1]];
  t = t * (high - low) + low;

  if(t < low || t > high) throw new Error('out of bounds');

  for(var s=domain[0]; s<domain[1]; s++) {
    if(t >= knots[s] && t <= knots[s+1]) {
      break;
    }
  }

  // create a copy of the source points array
  // to store intermediate results
  var v = points.map(function(point) {
    return point.slice();
  });

  // l (level) goes from 1 to the curve order
  for(var l=1; l<=order; l++) {
    // build level l of the pyramid
    for(var i=s; i>s-order+l; i--) {
      var a = (t - knots[i]) / (knots[i+order-l] - knots[i]);

      // interpolate each component of the input vectors
      for(var j=0; j<d; j++) {
        v[i][j] = (1 - a) * v[i-1][j] + a * v[i][j];
      }
    }
  }

  return v[s];
}


module.exports = interpolate;
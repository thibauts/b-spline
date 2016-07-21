

function interpolate(t, order, points, knots, weights, result) {

  var i,j,s,l;              // function-scoped iteration variables
  var n = points.length;    // points count
  var d = points[0].length; // point dimensionality

  if(order < 2) throw new Error('order must be at least 2 (linear)');
  if(order > n) throw new Error('order must be less than point count');

  if(!weights) {
    // build weight vector of length [n]
    weights = [];
    for(i=0; i<n; i++) {
      weights[i] = 1;
    }
  }

  if(!knots) {
    // build knot vector of length [n + order]
    var knots = [];
    for(i=0; i<n+order; i++) {
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

  // find s (the spline segment) for the [t] value provided
  for(s=domain[0]; s<domain[1]; s++) {
    if(t >= knots[s] && t <= knots[s+1]) {
      break;
    }
  }

  // convert points to homogeneous coordinates
  var v = [];
  for(i=0; i<n; i++) {
    v[i] = [];
    for(j=0; j<d; j++) {
      v[i][j] = points[i][j] * weights[i];
    }
  }

  // l (level) goes from 1 to the curve order
  var alpha;
  for(l=1; l<=order; l++) {
    // build level l of the pyramid
    for(i=s; i>s-order+l; i--) {
      alpha = (t - knots[i]) / (knots[i+order-l] - knots[i]);

      // interpolate each component
      for(j=0; j<d+1; j++) {
        v[i][j] = (1 - alpha) * v[i-1][j] + alpha * v[i][j];
      }
    }
  }

  // convert back to cartesian and return
  var result = result || [];
  for(i=0; i<d; i++) {
    result[i] = v[s][i] / weights[s];
  }

  return result;
}


module.exports = interpolate;

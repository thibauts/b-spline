

function interpolate(t, order, points, knots, weights, result) {

  var n = points.length;    // points count
  var d = points[0].length; // point dimensionality

  if(order < 2) throw new Error('order must be at least 2 (linear)');
  if(order > n) throw new Error('order must be less than point count');

  if(!weights) {
    // build weight vector
    weights = new Array(n);
    for(var i=0; i<n; i++) {
      weights[i] = 1;
    }
  }

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

  // convert points to homogeneous coordinates
  var v = new Array(n);
  for(var i=0; i<n; i++) {
    v[i] = new Array(d + 1);
    for(var j=0; j<d; j++) {
      v[i][j] = points[i][j] * weights[i];
    }
    v[i][d] = weights[i];
  }

  // l (level) goes from 1 to the curve order
  for(var l=1; l<=order; l++) {
    // build level l of the pyramid
    for(var i=s; i>s-order+l; i--) {
      var a = (t - knots[i]) / (knots[i+order-l] - knots[i]);

      // interpolate each component
      for(var j=0; j<d+1; j++) {
        v[i][j] = (1 - a) * v[i-1][j] + a * v[i][j];
      }

      //console.log(JSON.stringify(v[i]))
    }
  }

  // convert back to cartesian and return
  var result = result || new Array(d);
  for(var i=0; i<d; i++) {
    result[i] = v[s][i] / v[s][d];
  }

  return result;
}


module.exports = interpolate;
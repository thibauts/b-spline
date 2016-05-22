function interpolate(t, degree, points, knots, weights, extra_dim_values) {
  var num_points = points.length;    // points count
  var dimensionality = points[0].length; // point dimensionality

  if(degree < 2) throw new Error('degree must be at least 2 (linear)');
  if(degree > num_points) throw new Error('degree must be less than point count');

  if(!weights) {
    // build weight vector
    weights = new Array(num_points);
    for(var i=0; i<num_points; i++) {
      weights[i] = 1;
    }
  }

  if(!knots) {
    // build knot vector
    var knots = new Array(num_points + degree);
    for(var i=0; i<num_points+degree; i++) {
      knots[i] = i;
    }
  } else if(knots.length !== num_points+degree){
    throw new Error('bad knot vector length');
  }

  var domain = [
    degree-1,
    knots.length-1 - (degree-1)
  ];

  // remap t to the domain where the spline is defined
  var low  = knots[domain[0]];
  var high = knots[domain[1]];
  t = t * (high - low) + low;

  if(t < low || t > high) throw new Error('out of bounds');

  var s;
  for(s=domain[0]; s<domain[1]; s++) {
    if(t >= knots[s] && t <= knots[s+1]) {
      break;
    }
  }

  // convert points to homogeneous coordinates
  var v = new Array(num_points);
  for(var i=0; i<num_points; i++) {
    v[i] = new Array(dimensionality + 1);
    for(var j=0; j<dimensionality; j++) {
      v[i][j] = points[i][j] * weights[i];
    }
    v[i][dimensionality] = weights[i];
  }

  // l (level) goes from 1 to the curve degree
  for(var l=1; l<degree+1; l++) {
    // build level l of the pyramid
    for(var i=s; i>s-degree+l; i--) {
      var a = (t - knots[i]) / (knots[i+degree-l] - knots[i]);

      // interpolate each component
      for(var j=0; j<dimensionality+1; j++) {
        v[i][j] = (1 - a) * v[i-1][j] + a * v[i][j];
      }
    }
  }

  // convert back to cartesian and return
  var result = extra_dim_values || new Array(dimensionality);
  for(var i=0; i<dimensionality; i++) {
    result[i] = v[s][i] / v[s][dimensionality];
  }

  return result;
}


module.exports = interpolate;

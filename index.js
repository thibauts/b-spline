

function interpolate(t, degree, points, knots, weights, result) {

  // for testing
  var test_return = {}

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
  } else {
    if(knots.length !== num_points+degree) throw new Error('bad knot vector length');
  }

  var domain = [
    degree-1,
    knots.length-1 - (degree-1)
  ];
  console.log('domain', domain)
  test_return.domain = domain

  // remap t to the domain where the spline is defined
  var low  = knots[domain[0]];
  var high = knots[domain[1]];
  t = t * (high - low) + low;
  console.log('low', low)
  test_return.low = low
  console.log('high', high)
  test_return.high = high
  console.log('t', t)
  test_return.t = t

  if(t < low || t > high) throw new Error('out of bounds');

  for(var s=domain[0]; s<domain[1]; s++) {
    if(t >= knots[s] && t <= knots[s+1]) {
      break;
    }
  }

  console.log('s', s)
  test_return.s = s

  test_return.v_c = []
  // convert points to homogeneous coordinates
  var v = new Array(num_points);
  for(var i=0; i<num_points; i++) {
    v[i] = new Array(dimensionality + 1);
    for(var j=0; j<dimensionality; j++) {
      v[i][j] = points[i][j] * weights[i];
      var v_tmp = {}
      v_tmp['v[i][j]'.replace('i', i).replace('j', j)] = v[i][j]
      test_return.v_c.push(v_tmp)
    }
    v[i][dimensionality] = weights[i];
    var v_tmp = {}
    v_tmp['v[i][dimensionality]_d'.replace('dimensionality', dimensionality).replace('i', i)] = v[i][dimensionality]
    test_return.v_c.push(v_tmp)
  }

  console.log('v', v)
  test_return.v = v

  // l (level) goes from 1 to the curve degree
  for(var l=1; l<=degree; l++) {
    // build level l of the pyramid
    for(var i=s; i>s-degree+l; i--) {
      var a = (t - knots[i]) / (knots[i+degree-l] - knots[i]);

      // interpolate each component
      for(var j=0; j<dimensionality+1; j++) {
        v[i][j] = (1 - a) * v[i-1][j] + a * v[i][j];
      }
    }
  }

  console.log('v', v)
  test_return.v2 = v

  // convert back to cartesian and return
  var result = result || new Array(dimensionality);
  for(var i=0; i<dimensionality; i++) {
    result[i] = v[s][i] / v[s][dimensionality];
  }

  test_return.result = result
  return test_return
  return result;
}


module.exports = interpolate;
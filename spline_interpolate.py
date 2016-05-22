# Transposed by William Rusnack https://github.com/BebeSparkelSparkel
# from the javascript libray https://github.com/thibauts/b-spline/ by Thibaut Séguy

def interpolate(t, degree, points, knots=None, weights=None, result=None):
	num_points = len(points)
	dimensionality = len(points[0])

	if degree < 2:
		raise ValueError('degree must be at least 2 (linear)')
	if degree > num_points:
		raise ValueError('degree must be less than point count')

	if weights is None:
		weights = (1,) * num_points
	if knots is None:
		knots = tuple(i for i in range(num_points+degree))
	elif len(knots) != num_points + degree:
		raise ValueError('bad knot vector length')

	domain = degree - 1, len(knots) - degree

	# remap t to the domain where the spline is defined
	low, high = [knots[d] for d in domain]
	t = t * (high - low) + low

	if not low <= t < high:
		raise ValueError('out of bounds')

	s = domain[0]
	for i in range(domain[0], domain[1]):
		if knots[s] <= t <= knots[s+1]:
			break
		s += 1

	v_c = []
	# convert points to homogeneous coordinates
	v = [None] * num_points
	for i in range(num_points):
		v[i] = [None] * (dimensionality + 1)
		for j in range(dimensionality):
			v[i][j] = points[i][j] * weights[i]
			v_c.append({'v[i][j]'.replace('i', str(i)).replace('j', str(j)): v[i][j]})
		v[i][dimensionality] = weights[i]
		v_c.append({'v[i][dimensionality]_d'.replace('dimensionality', str(dimensionality)).replace('i', str(i)): v[i][dimensionality]})

	v2_c = []
	# l (level) goes from 1 to the curve degree
	for l in range(1, degree+1):
		# build level l of the pyramid
		for i in range(s, s-degree+l, -1):
			a = (t - knots[i]) / (knots[i+degree-l] - knots[i])

			# interpolate each component
			for j in range(dimensionality+1):
				v[i][j] = (1 - a) * v[i-1][j] + a * v[i][j]
				v2_c.append({'v[i][j]'.replace('i', str(i)).replace('j', str(j)): v[i][j]})

	# convert back to cartesian and return
	if result is None:
		result = [None] * dimensionality
	for i in range(dimensionality):
		result[i] = v[s][i] / v[s][dimensionality]

	return result

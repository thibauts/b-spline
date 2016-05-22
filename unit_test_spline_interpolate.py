from pprint import pprint

from spline_interpolate import interpolate as py_interpolate
import execjs
js_interpolate = execjs.compile(open('index.js').read()).call

test_data = (
		{
			'degree': 4,
			'points': [ [3.547949666913399, 4.015292376017764, 0.0 ],  [2.326818379115456, 4.735446725231935, 0.0 ],  [-1.364091662421916, 9.383406024977491, 0.0 ],  [5.407467426288706, 5.190828314342068, 0.0 ],  [9.283378812528207, 9.836223562475746, 0.0 ],  [7.623911799584189, 2.411642775044972, 0.0 ],  [4.501326022260053, 3.513515346887946, 0.0 ],  [3.547949666913399, 4.015292376017764, 0.0 ] ],
			'knots': [0.0, 0.0, 0.0, 0.0, 4.253005428938497, 9.534503315359672, 11.99652095351233, 16.56330621460171, 19.79538912768852, 19.79538912768852, 19.79538912768852, 19.79538912768852 ],
			'weights': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 ]
		}
		# more tests can be added here
	,)


num_pt_checks = 100
for td in test_data:
	for i in range(num_pt_checks):
		t = i / num_pt_checks
		print('javascript')
		js_pt = js_interpolate('interpolate', t, td['degree'], td['points'], td['knots'])
		# pprint(js_pt)
		print('domain', js_pt['domain'])
		print('low', js_pt['low'])
		print('high', js_pt['high'])
		print('t', js_pt['t'])
		print('s', js_pt['s'])
		print('v_c')
		pprint(js_pt['v_c'])
		print('v')
		pprint(js_pt['v'])
		print('v2')
		pprint(js_pt['v'])

		print()
		print('python')
		py_pt = py_interpolate(t, td['degree'], td['points'], td['knots'])

		if js_pt['result'] != py_pt:
			print('js', js_pt['result'], '!=', 'py', py_pt)
			raise ValueError('not equivilent values')

		print()
		print()

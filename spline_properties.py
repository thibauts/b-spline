import dxfgrabber
from math import atan2
import sys

script, file_name = sys.argv

stuff = dxfgrabber.readfile(file_name)

spline = [ent for ent in stuff.entities][0]


print('degree')
print(spline.degree)
print()

print('starttangent')
print(list(spline.starttangent[0:2]))
print('angle', atan2(spline.starttangent[1], spline.starttangent[0]), 'rad')
print()

print('endtangent')
print(list(spline.endtangent[0:2]))
print('angle', atan2(spline.endtangent[1], spline.endtangent[0]), 'rad')
print()

print('controlpoints')
print([list(pt[0:2]) for pt in spline.controlpoints])
print('number of controlpoints', len(spline.controlpoints))
print()

print('fitpoints')
print([list(pt[0:2]) for pt in spline.fitpoints])
print('number of fitpoints', len(spline.fitpoints))
print()

print('knots')
print(list(spline.knots))
print('number of knots', len(spline.knots))
print()

print('weights')
print(list(spline.weights))
print('number of weights', len(spline.weights))
print()

print('normalvector')
print(spline.normalvector)
print()

print('is_closed')
print(spline.is_closed)
print()

print('is_periodic')
print(spline.is_periodic)
print()

print('is_rational')
print(spline.is_rational)
print()

print('is_planar')
print(spline.is_planar)
print()

print('is_linear')
print(spline.is_linear)
print()


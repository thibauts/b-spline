from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['interpolate'])
@Js
def PyJsHoisted_interpolate_(t, degree, points, knots, weights, result, this, arguments, var=var):
    var = Scope({'degree':degree, 'result':result, 'weights':weights, 'this':this, 't':t, 'points':points, 'arguments':arguments, 'knots':knots}, var)
    var.registers(['l', 'degree', 'num_points', 's', 'weights', 'domain', 't', 'i', 'result', 'v', 'a', 'low', 'dimensionality', 'high', 'points', 'j', 'knots'])
    var.put('num_points', var.get('points').get('length'))
    var.put('dimensionality', var.get('points').get('0').get('length'))
    if (var.get('degree')<Js(2.0)):
        PyJsTempException = JsToPyException(var.get('Error').create(Js('degree must be at least 2 (linear)')))
        raise PyJsTempException
    if (var.get('degree')>var.get('num_points')):
        PyJsTempException = JsToPyException(var.get('Error').create(Js('degree must be less than point count')))
        raise PyJsTempException
    if var.get('weights').neg():
        var.put('weights', var.get('Array').create(var.get('num_points')))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('num_points')):
            try:
                var.get('weights').put(var.get('i'), Js(1.0))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    if var.get('knots').neg():
        var.put('knots', var.get('Array').create((var.get('num_points')+var.get('degree'))))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<(var.get('num_points')+var.get('degree'))):
            try:
                var.get('knots').put(var.get('i'), var.get('i'))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    else:
        if PyJsStrictNeq(var.get('knots').get('length'),(var.get('num_points')+var.get('degree'))):
            PyJsTempException = JsToPyException(var.get('Error').create(Js('bad knot vector length')))
            raise PyJsTempException
    var.put('domain', Js([(var.get('degree')-Js(1.0)), ((var.get('knots').get('length')-Js(1.0))-(var.get('degree')-Js(1.0)))]))
    var.put('low', var.get('knots').get(var.get('domain').get('0')))
    var.put('high', var.get('knots').get(var.get('domain').get('1')))
    var.put('t', ((var.get('t')*(var.get('high')-var.get('low')))+var.get('low')))
    if ((var.get('t')<var.get('low')) or (var.get('t')>var.get('high'))):
        PyJsTempException = JsToPyException(var.get('Error').create(Js('out of bounds')))
        raise PyJsTempException
    #for JS loop
    var.put('s', var.get('domain').get('0'))
    while (var.get('s')<var.get('domain').get('1')):
        try:
            if ((var.get('t')>=var.get('knots').get(var.get('s'))) and (var.get('t')<=var.get('knots').get((var.get('s')+Js(1.0))))):
                break
        finally:
                (var.put('s',Js(var.get('s').to_number())+Js(1))-Js(1))
    var.put('v', var.get('Array').create(var.get('num_points')))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('num_points')):
        try:
            var.get('v').put(var.get('i'), var.get('Array').create((var.get('dimensionality')+Js(1.0))))
            #for JS loop
            var.put('j', Js(0.0))
            while (var.get('j')<var.get('dimensionality')):
                try:
                    var.get('v').get(var.get('i')).put(var.get('j'), (var.get('points').get(var.get('i')).get(var.get('j'))*var.get('weights').get(var.get('i'))))
                finally:
                        (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
            var.get('v').get(var.get('i')).put(var.get('dimensionality'), var.get('weights').get(var.get('i')))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('l', Js(1.0))
    while (var.get('l')<=var.get('degree')):
        try:
            #for JS loop
            var.put('i', var.get('s'))
            while (var.get('i')>((var.get('s')-var.get('degree'))+var.get('l'))):
                try:
                    var.put('a', ((var.get('t')-var.get('knots').get(var.get('i')))/(var.get('knots').get(((var.get('i')+var.get('degree'))-var.get('l')))-var.get('knots').get(var.get('i')))))
                    #for JS loop
                    var.put('j', Js(0.0))
                    while (var.get('j')<(var.get('dimensionality')+Js(1.0))):
                        try:
                            var.get('v').get(var.get('i')).put(var.get('j'), (((Js(1.0)-var.get('a'))*var.get('v').get((var.get('i')-Js(1.0))).get(var.get('j')))+(var.get('a')*var.get('v').get(var.get('i')).get(var.get('j')))))
                        finally:
                                (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
                finally:
                        (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
        finally:
                (var.put('l',Js(var.get('l').to_number())+Js(1))-Js(1))
    var.put('result', (var.get('result') or var.get('Array').create(var.get('dimensionality'))))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('dimensionality')):
        try:
            var.get('result').put(var.get('i'), (var.get('v').get(var.get('s')).get(var.get('i'))/var.get('v').get(var.get('s')).get(var.get('dimensionality'))))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return var.get('result')
PyJsHoisted_interpolate_.func_name = 'interpolate'
var.put('interpolate', PyJsHoisted_interpolate_)
pass
var.get('module').put('exports', var.get('interpolate'))
pass

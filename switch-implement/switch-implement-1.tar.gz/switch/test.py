

from .Switch import switch, bswitch


__all__ = ["test_switch", "test_bswitch", "test_if", "teoric"]

def _decore_name(name):
    n = name.center(40, "=").replace(name, " %s " % name)
    print("<%s>" % n)


def test_switch(day):
    _decore_name("switch")
    with switch(day) as case:
        if case(1):
            print("es lunes")
            case.sbreak
        if case(2, sbreak=True):
            print("es martes")
        if case.check(lambda value: value == 3):
            print("es miercoles")
            case.sbreak
        if case.match(r"4"):
            print("es jueves")
            case.sbreak
        if case(5):
            print("es viernes")
        if case(6):
            print("es sabado")
            case.sbreak
        if case(7, 7.0): # you can use more of one cases
            print("es domingo")
        if case.default:
            print("ese dia no existe")
    with switch(10, comparator=lambda v, cases: \
            any(c > v for c in cases)) as case:
        if case(2):
            print(1)
        if case(12):
            print(2)
    

def test_bswitch(day):
    _decore_name("bswitch")
    
    with bswitch(day) as case:
        if case(1):
            print("es lunes")
        if case(2):
            print("es martes")
        if case(3):
            print("es miercoles")
        if case(4):
            print("es jueves")
        if case(5):
            print("es viernes")
        if case(6):
            print("es sabado")
        if case(7):
            print("es domingo")
        if case.default:
            print("ese dia no existe")
        # if you use a case after a default
        # this raise a error!
        # example:
        #if case(8):
        #    print("el dia 8 no existe")



def test_if(day):
    _decore_name("if elif else")
    
    if day == 1:
        print("es lunes")
    elif day == 2:
        print("es martes")
    elif day == 3:
        print("es miercoles")
    elif day == 4:
        print("es jueves")
    elif day == 5:
        print("es viernes")
    elif day == 6:
        print("es sabado")
    elif day == 7:
        print("es domingo")
    else:
        print("ese dia no existe")
    
    
teoric = """
switch 2:
    case 1:
        print("es lunes")
        break
    case 2:
        print("es martes")
        break
    case 3:
        print("es miercoles")
        break
    case 4:
        print("es jueves")
        break
    case 5:
        print("es viernes")
        break
    case 6:
        print("sabado")
        break
    case 7, 7.0:
        print("domingo")
        break
    default:
        print("ese dia no existe")
"""










































































































































































































































































































































































































































































































































































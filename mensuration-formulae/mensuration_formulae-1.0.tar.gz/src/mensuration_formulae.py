import math

PI = math.pi


def square_area(side):
    area = side * side
    return area


def square_perimeter(side):
    perimeter = 4 * side
    return perimeter


def rectangle_area(length, breadth):
    area = length * breadth
    return area


def rectangle_perimeter(length, breadth):
    perimeter = 2*(length + breadth)
    return perimeter


def circle_area(radius):
    area = PI * (radius ** 2)
    return area


def circle_perimeter(radius):
    perimeter = 2 * PI * radius
    return perimeter


def scalene_triangle_area(side1, side2, side3):
    s = (side1 + side2 + side3) / 2
    area = math.sqrt((s * (s - side1) * (s - side2) * (s - side3)))
    return area


def scalene_triangle_perimeter(side1, side2, side3):
    perimeter = side1 + side2 + side3
    return perimeter


def isosceles_triangle_area(breadth, height):
    area = 0.5 * breadth * height
    return area


def isosceles_triangle_perimeter(side, breadth):
    perimeter = 2*(side + breadth)
    return perimeter


def equivalent_triangle_area(a):
    area = math.sqrt(3/4)*(a*a)
    return area


def equivalent_triangle_perimeter(a):
    perimeter = 3*a
    return perimeter


def right_angle_triangle_area(b, h):
    area = 	0.5 * b * h
    return area


def right_angle_triangle_perimeter(b, hypotenuse, h):
    perimeter = b+hypotenuse+h
    return perimeter


def rhombus_area(diag1, diag2):
    area = 0.5 * diag1 * diag2
    return area


def rhombus_perimeter(s):
    perimeter = 4 * s
    return perimeter


def parallelogram_area(b, h):
    area = b * h
    return area


def parallelogram_perimeter(l, b):
    perimeter = 2*(l+b)
    return perimeter


def trapezium_area(a, c, h):
    area = 0.5 * (h*(a+c))
    return area


def trapezium_perimeter(a, b, c, d):
    perimeter = a+b+c+d
    return perimeter


def cube_volume(a):
    vol = a**3
    return vol


def cube_csa(a):
    csa = 4 * (a*a)
    return csa


def cube_tsa(a):
    tsa = 6 * (a*a)
    return tsa





def sphere_volume(r):
    vol = 4/3 * r ** 3
    return vol


def sphere_sa(r):
    sa = 4 * PI * r ** 2
    return sa


def cylinder_volume(r, h):
    vol = PI * r ** 2 * h
    return vol


def cylinder_tsa(r, h):
    sa = 2 * PI * r * (r + h)
    return sa


def cylinder_csa(r, h):
    sa = 2 * PI * r * h
    return sa


def cuboid_volume(l, b, h):
    vol = l * b * h
    return vol


def cuboid_csa(l, b, h):
    csa = 2 * h * (l + b)
    return csa


def cuboid_tsa(l, b, h):
    sa = 2 * ((l * b) + (b * h) + (l * h))
    return sa




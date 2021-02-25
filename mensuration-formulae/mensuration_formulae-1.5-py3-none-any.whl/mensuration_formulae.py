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
    perimeter = 2 * (length + breadth)
    return perimeter


def circle_area(radius):
    area = 3.14 * (radius ** 2)
    return area


def circle_perimeter(radius):
    perimeter = 2 * 3.14 * radius
    return perimeter


def scalene_triangle_area(side1, side2, side3):
    s = (side1 + side2 + side3) / 2
    area = (s * (s - side1) * (s - side2) * (s - side3)) ** 0.5
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


def equivalent_triangle_area(side):
    area = ((0.5 ** 3)/4)*(side * side)
    return area


def equivalent_triangle_perimeter(side):
    perimeter = 3 * side
    return perimeter


def right_angle_triangle_area(breadth, height):
    area = 0.5 * breadth * height
    return area


def right_angle_triangle_perimeter(breadth, hypotenuse, height):
    perimeter = breadth + hypotenuse + height
    return perimeter


def rhombus_area(diag1, diag2):
    area = 0.5 * diag1 * diag2
    return area


def rhombus_perimeter(side):
    perimeter = 4 * side
    return perimeter


def parallelogram_area(breadth, height):
    area = breadth * height
    return area


def parallelogram_perimeter(length, breadth):
    perimeter = 2*(length + breadth)
    return perimeter


def trapezium_area(side1, side2, height):
    area = 0.5 * (height * (side1 + side2))
    return area


def trapezium_perimeter(side1, side2, side3, side4):
    perimeter = side1 + side2 + side3 + side4
    return perimeter


def cube_volume(side):
    vol = side ** 3
    return vol


def cube_csa(side):
    csa = 4 * (side * side)
    return csa


def cube_tsa(side):
    tsa = 6 * (side * side)
    return tsa


def sphere_volume(radius):
    vol = 4 / 3 * radius ** 3
    return vol


def sphere_csa(radius):
    csa = 4 * 3.14 * radius ** 2
    return csa


def cylinder_volume(radius, height):
    vol = 3.14 * radius ** 2 * height
    return vol


def cylinder_tsa(radius, height):
    tsa = 2 * 3.14 * radius * (radius + height)
    return tsa


def cylinder_csa(radius, height):
    csa = 2 * 3.14 * radius * height
    return csa


def cuboid_volume(length, breadth, height):
    vol = length * breadth * height
    return vol


def cuboid_csa(length, breadth, height):
    csa = 2 * height * (length + breadth)
    return csa


def cuboid_tsa(length, breadth, height):
    tsa = 2 * ((length * breadth) + (breadth * height) + (length * height))
    return tsa


def cone_volume(radius, height):
    vol = 0.33 * 3.14 * (radius ** 2) * height
    return vol


def cone_tsa(radius, length):
    tsa = 3.14 * radius * ( radius + length )
    return tsa


def cone_csa(radius, length):
    csa = 3.14 * radius * length
    return csa


def hemisphere_volume(radius):
    vol = 0.66 * 3.14 * (radius ** 2)
    return vol


def hemisphere_csa(radius):
    csa = 2 * 3.14 * (radius ** 2)
    return csa


def hemisphere_tsa(radius):
    tsa = 3 * 3.14 * (radius ** 2)
    return tsa




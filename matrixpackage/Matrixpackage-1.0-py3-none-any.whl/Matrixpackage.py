##Matrix Addition

def matrix_add(matrix1, matrix2):
    result = []
    for i in range(len(matrix1)):
        for j in range(len(matrix2)):
            result.append(matrix1[i][j] + matrix2[i][j])
    return result


print(matrix_add(eval(input()), eval(input())))


##Matrix Subtraction

def matrix_sub(mat1, mat2):
    res = []
    for i in range(len(mat1)):
        for j in range(len(mat2)):
            res.append(mat1[i][j] - mat2[i][j])
    return res


print(matrix_sub(eval(input()), eval(input())))


##Matrix Multiplication

def matrix_mul(m1, m2):
    r = [[0, 0], [0, 0]]
    for i in range(len(m1)):
        for j in range(len(m1)):
            for k in range(len(m1)):
                r[i][j] = r[i][j] + m1[j][k] * m2[k][i]
    return r


print(matrix_mul(eval(input()), eval(input())))

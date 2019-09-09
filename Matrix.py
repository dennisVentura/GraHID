from __future__ import print_function
import ast


class Matrix:
    def __init__(self, data):
        if isinstance(data, Matrix):
            self.m = data.m
        if isinstance(data, str):
            self.m = string_to_matrix(data)
        if isinstance(data, list):
            if check_matrix(data):
                self.m = data
            else:
                raise ValueError("Rows not the same size.")
        if isinstance(data, float):
            raise ValueError("Could not convert float to matrix")

    def __str__(self):
        tr = matrix_to_string(self.m)
        trn_tr = transpose(tr)
        n_str = [max([len(i) for i in j]) for j in trn_tr]
        tr = [[i.center(n_str[j]) for (j, i) in enumerate(k)] for k in tr]
        return 'Matrix (' + str(len(self.m)) + ',' + str(len(self.m[0])) + '): \n' + '\n'.join(['\t'.join(i) for i in tr])

    def __add__(self, other):
        if isinstance(other, Matrix):
            if equals_size(self.m, other.m):
                return Matrix([list(map(lambda x,y: x+y, i, j)) for i,j in zip(self.m,other.m)])
            else:
                raise ValueError("Invalid dimension")
        elif isinstance(other, (int, float)):
            return Matrix([[j+other for j in i] for i in self.m])
        else:
            raise TypeError("Invalid Value Type")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if equals_size(self.m, other.m):
            return Matrix([list(map(lambda x,y: x-y, i, j)) for i,j in zip(self.m, other.m)])
        else:
            raise ValueError("Could not convert float/int to matrix")

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return mul_m(self.m, other)
        elif isinstance(other, Matrix):
            return mul_m(self.m, other.m)

    def __rmul__(self, other):
        return mul_m(self.m, other)

    def __floordiv__(self, other):
        if len(other.m[0]) < 2:
            return matrix_solve(self.m, other.m)
        else:
            return matrix_solve_matrix(self.m, other.m)

    def __setitem__(self, key, value):
        if isinstance(value, (int, float)):
            if isinstance(key, tuple):
                self[key[0]][key[1]] = value
            else:
                raise TypeError("Invalid Key Type")
        else:
            raise TypeError("Invalid Value Type")

    def __getitem__(self, item):
        if isinstance(item, tuple):
            return self.m[item[0]][item[1]]
        elif isinstance(item, (int, slice)):
            return self.m[item]
        else:
            raise TypeError('Invalid Item Type')

    def __len__(self):
        return len(self.m)

    def __neg__(self):
        return Matrix([[-i for i in j] for j in self.m])

    def __abs__(self):
        return Matrix([[abs(i) for i in j] for j in self.m])

    def __round__(self, decimals=0):
        return Matrix([[round(i, decimals) for i in j] for j in self.m])

    def __pow__(self, other):
        return pow_m(self.m, other)

    def copy(self):
        return Matrix(self.m.copy())

    def del_col(self, n):
        m1 = self.m.copy()
        for i in m1:
            i.pop(n)
        return Matrix(m1)

    def get_col(self, l):
        m1 = self.m.copy()
        for i in range(len(self.m)):
            for j in range(len(l)):
                m1[i][j] = self.m[i][l[j]]
        return Matrix(m1)

    @property
    def tolist(self):
        return self.m

    T = property(lambda self: transpose(self), lambda self, v: None, lambda self: None)
    N = property(lambda self: norm(self), lambda self, v: None, lambda self: None)
    I = property(lambda self: invert_matrix(self), lambda self, v: None, lambda self: None)
    D = property(lambda self: det(self), lambda self, v: None, lambda self: None)


def zeros(w, h):
    return Matrix([[0 for _ in range(w)] for __ in range(h)])


def string_to_matrix(data):
    """ Code extracted from package Numpy """
    for char in '[]':
        data = data.replace(char, '')

    rows = data.split(';')
    new_data = []
    count = 0
    n_cols = 0
    for row in rows:
        trow = row.split(',')
        new_row = []
        for col in trow:
            temp = col.split()
            new_row.extend(map(ast.literal_eval, temp))
        if count == 0:
            n_cols = len(new_row)
        elif len(new_row) != n_cols:
            raise ValueError("Rows not the same size.")
        count += 1
        new_data.append(new_row)
    return new_data


def matrix_to_string(matrix):
    return [[str(i) for i in j] for j in matrix]


def check_matrix(matrix):
    data = []
    row = matrix[0]
    for i in matrix:
        n_cols = len(i)
        data.append(n_cols == len(row))
    return all(data)


def equals_size(m1, m_2):
    if check_matrix(m1) and check_matrix(m_2):
        if len(m1) == len(m_2):
            if len(m1[0]) == len(m_2[0]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def mul_m(m_1, other):
    if isinstance(other, list):
        if len(m_1[0]) == len(other):
            m1 = zeros(len(other[0]), len(m_1))
            for i in range(len(m_1)):
                for j in range(len(other[0])):
                    for k in range(len(other)):
                        m1[i][j] = m1[i][j] + m_1[i][k] * other[k][j]
            return Matrix(m1)
        else:
            raise IndexError('Invalid Dimension')
    elif isinstance(other, float) or isinstance(other, int):
        return Matrix([[i * other for i in j] for j in m_1])
    else:
        raise ValueError('Invalid value')


def det(matrix):
    a = matrix.copy()
    n = len(matrix)
    for k in range(n - 1):
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] -= a[i][k] * a[k][j] / a[k][k]
    deter = 1.0
    for i in range(n):
        deter *= a[i][i]
    return deter


def transpose(matrix):
    return Matrix([[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))])


def diagonal(data, size=2):
    if isinstance(data, float) or isinstance(data, int):
        new_data = zeros(size, size)
        for i in range(size):
            for j in range(size):
                if i == j:
                    new_data[i][j] = data
        return new_data
    elif isinstance(data, list):
        new_data = zeros(len(data), len(data))
        for i in range(len(data)):
            for j in range(len(data)):
                if i == j:
                    new_data[i][j] = data[i]
        return new_data


def invert_matrix(m):
    rows = len(m)
    cols = len(m[0])
    if rows == cols:
        a = m.copy()
        b = zeros(cols, rows)
        c = zeros(cols, rows)
        for i in range(rows):
            b[i][i] = 1.0
        for k in range(rows - 1):
            for i in range(k + 1, rows):
                for s in range(rows):
                    b[i][s] -= a[i][k] * b[k][s] / a[k][k]
                for j in range(k + 1, rows):
                    a[i][j] -= a[i][k] * a[k][j] / a[k][k]
        for s in range(rows):
            c[rows - 1][s] = b[rows - 1][s] / a[rows - 1][rows - 1]
            for i in range(rows - 2, -1, -1):
                c[i][s] = b[i][s] / a[i][i]
                for k in range(rows - 1, i, -1):
                    c[i][s] -= a[i][k] * c[k][s] / a[i][i]
        return c
    else:
        return


def matrix_solve(m, column):
    """
    :param m: Matrix, system equation.
    :param column: Column Matrix, system equation.
    :return: Column matrix, result of system equation.
    For L. Code by: Michael Halls-Moore"""
    size = len(m)
    l_1 = zeros(size, size)
    for i in range(size):
        for k in range(i + 1):
            tmp_sum = sum(l_1[i][j] * l_1[k][j] for j in range(k))
            if i == k:
                l_1[i][k] = (m[i][i] - tmp_sum) ** 0.5
            else:
                l_1[i][k] = (1.0 / l_1[k][k] * (m[i][k] - tmp_sum))
    z = zeros(1, size)
    for i in range(size):
        sum1 = 0
        for k in range(i):
            sum1 = sum1 + l_1[i][k] * z[k][0]
        z[i][0] = (column[i][0] - sum1) / l_1[i][i]
    x = zeros(1, size)
    for i in range(size - 1, -1, -1):
        sum1 = 0
        for k in range(i + 1, size):
            sum1 = sum1 + l_1[k][i] * x[k][0]
        x[i][0] = (z[i][0] - sum1) / l_1[i][i]
    return x


def matrix_solve_matrix(m, m2):
    m_f = [[i * 0 for i in j] for j in m2]
    m3 = Matrix([[i for i in j] for j in m2]).T
    l_c = []
    for i in range(len(m3)):
        l_c.append(Matrix([m3[i]]).T)
    l_r = []
    for i in l_c:
        column = matrix_solve(m, i)
        l_r.append(column)
    for i in range(len(m_f)):
        for j in range(len(m_f[0])):
            m_f[i][j] = l_r[j][i][0]
    return Matrix(m_f)


def norm(matrix):
    return (sum([sum([i ** 2 for i in j]) for j in matrix])) ** .5


def pow_ma(m, n):
    c = diagonal(1.0, len(m))
    mat = Matrix(m)
    for i in range(n):
        c = c * mat
    return c


def pow_m(m, other):
    if isinstance(other, int):
        if other < -1:
            return Matrix(m).I ** abs(other)
        elif other == -1:
            return Matrix(m).I
        elif other == 0:
            return diagonal(1.0, len(m))
        elif other == 1:
            return Matrix(m)
        else:
            return pow_ma(m, other)


a = Matrix("1,3;3,5")
print(3+a)
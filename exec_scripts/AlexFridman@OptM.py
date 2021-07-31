#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
# In[2]:
def zerofy(x, tol=1e-6):
    return np.where(np.abs(x) < tol, 0, x)
def quadratic_simplex(A, D, c, x_base, J_base, J_star, tol=1e-6):
    m, n = A.shape
    j_0 = None
    skip_til_3_step = False
    while True:
        # сохранение j_0 для возможности восстановления
        j_0_old = j_0
        if not skip_til_3_step:
            # Шаг 1
            c_x = c + D.dot(x_base)
            A_b_inv = np.linalg.inv(A[:, J_base])
            # вычисление вектора потенциалов
            u_x = -c_x[J_base].dot(A_b_inv)
            # вычисление вектора оценок
            d_x = u_x.dot(A) + c_x
            # Шаг 2. Критерий оптимальности
            # Возврат, если все небазисные оценки >= 0
            if np.all(zerofy(d_x[J_star == False]) >= 0):
                return x_base
        # Шаг 3. Построение направлений L и изменение плана
        # нахождение минимального индекса, соответствующего отрицательной небазисной оценке
        j_0 = np.argwhere(zerofy(np.where(J_star == False, d_x, np.infty)) < 0).min()
        m = len(np.argwhere(J_base))
        D_star = D[J_star, :][:, J_star]
        D_J_j0 = D[J_star, j_0]
        A_star = A[:, J_star]
        H = np.concatenate([np.concatenate([D_star, A_star]), np.concatenate([A_star.T, np.zeros([m, m])])], 1)
        bb = np.hstack((D_J_j0, A[:, j_0]))
        J_star_non_0_count = len(np.argwhere(J_star))
        l_y = -np.linalg.inv(H).dot(bb)
        l_star, y = l_y[:J_star_non_0_count], l_y[J_star_non_0_count:]
        l = np.zeros(n)
        l[j_0] = 1
        l[J_star] = l_star
        # Шаг 4. Подсчет theta
        delta = l.dot(D).dot(l)
        theta = np.zeros(n)
        if abs(delta) < tol:
            theta[j_0] = np.infty
        elif delta > tol:
            theta[j_0] = abs(d_x[j_0]) / delta
        theta[J_star] = np.where(l[J_star] >= 0, np.infty, -x_base[J_star] / l[J_star])
        theta_0 = min(theta[J_star].min(), theta[j_0])
        j_star = np.argwhere(theta == theta_0).min()
        if theta_0 == np.infty:
            raise Exception('Target function is not limited')
        # Шаг 5. Построение нового плана
        x_base = x_base + theta_0 * l
        # Шаг 6. Обновление J_b, J_star
        j_plus = None
        def case_C(eq=True):
            nonlocal j_plus
            J_star_except_J_base = J_star & (J_base == False)
            J_base_col_n = len(np.argwhere(J_base))
            A_base_inv = np.linalg.inv(A[:, J_base])
            for j_s in np.argwhere(J_base).ravel():
                for j_plus_local in np.argwhere(J_star_except_J_base).ravel():
                    e = np.zeros(J_base_col_n)
                    e[j_s] = 1
                    if e.dot(A_base_inv).dot(A[:, j_plus_local]) != 0 and eq:
                        j_plus = j_plus_local
                        return True
            return False
        def case_D():
            return case_C(eq=False) or np.all(J_star == J_base)
        skip_til_3_step = False
        if j_0 == j_star:
            J_star[j_0] = True
        elif (J_star & (J_base == False))[j_star]:
            J_star[j_star] = False
            d_x[j_0] += theta_0 * delta
            j_0 = j_0_old
            skip_til_3_step = True
        elif case_C():
            J_base[j_star] = False
            J_base[j_plus] = True
            J_star[j_star] = False
            d_x[j_0] += theta_0 * delta
            j_0 = j_0_old
            skip_til_3_step = True
        elif case_D():
            J_base[j_star] = False
            J_base[j_0] = True
            J_star[j_star] = False
            J_star[j_0] = True
# In[3]:
A = np.array([
    [1, 2, 0, 1, 0, 4, -1, -3],
    [1, 3, 0, 0, 1, -1, -1, 2],
    [1, 4, 1, 0, 0, 2, -2, 0]
])
m, n = A.shape
b = np.array([4, 5, 6])
B = np.array([
    [1, 1, -1, 0, 3, 4, -2, 1],
    [2, 6, 0, 0, 1, -5, 0, -1],
    [-1, 2, 0, 0, -1, 1, 1, 1]
])
d = np.array([7, 3, 3])
D = B.T.dot(B)
c = -d.dot(B)
x_0 = np.array([0, 0, 6, 4, 5, 0, 0, 0])
J_base = np.array([False, False, True, True, True, False, False, False])
J_star = np.array([False, False, True, True, True, False, False, False])
quadratic_simplex(A, D, c, x_0, J_base, J_star).round(2)
# In[4]:
A = np.array([
    [11, 0, 0, 1, 0, -4, -1, 1],
    [1, 1, 0, 0, 1, -1, -1, 1],
    [1, 1, 1, 0, 1, 2, -2, 1]
])
m, n = A.shape
b = np.array([8, 5, 2])
B = np.array([
    [1, -1, 0, 3, -1, 5, -2, 1],
    [2, 5, 0, 0, -1, 4, 0, 0],
    [-1, 3, 0, 5, 4, -1, -2, 1],
])
d = np.array([6, 10, 9])
D = B.T.dot(B)
c = -d.dot(B)
x_0 = np.array([0.7921, 1.2576, 1.3811, 1.1526, 0.1258, 0.5634, 0.0713, 0.4592])
J_base = np.array([True, True, True, False, False, False, False, False])
J_star = np.array([True, True, True, False, False, False, False, False])
quadratic_simplex(A, D, c, x_0, J_base, J_star).round(2)
# In[5]:
A = np.array([
    [2, -3, 1, 1, 3, 0, 1, 2],
    [-1, 3, 1, 0, 1, 4, 5, -6],
    [1, 1, -1, 0, 1, -2, 4, 8]
])
m, n = A.shape
b = np.array([8, 4, 14])
B = np.array([
    [1, 0, 0, 3, -1, 5, 0, 1],
    [2, 5, 0, 0, 0, 4, 0, 0],
    [-1, 9, 0, 5, 2, -1, -1, 5],
])
D = B.T.dot(B)
c = np.array([-13, -217, 0, -117, -27, -71, 18, -99])
x_0 = np.array([0, 2, 0, 0, 4, 0, 0, 1])
J_base = np.array([False, True, False, False, True, False, False, True])
J_star = np.array([False, True, False, False, True, False, False, True])
quadratic_simplex(A, D, c, x_0, J_base, J_star).round(2)
# In[6]:
A = np.array([
    [0, 2, 1, 4, 3, 0, -5, -10],
    [-1, 3, 1, 0, 1, 3, -5, -6],
    [1, 1, 1, 0, 1, -2, -5, 8]
])
b = np.array([6, 4, 14])
D = np.array([
    [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
    [ 0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.],
    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
    [ 0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.],
    [ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.],
    [ 0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.],
    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.]
])
x_0 = np.array([0, 2, 0, 0, 4, 0, 0, 1])
c = np.array([1, 3, -1, 3, 5, 2, -2, 0])
J_base = np.array([False, True, False, False, True, False, False, True])
J_star = np.array([False, True, False, False, True, False, False, True])
try:
    quadratic_simplex(A, D, c, x_0, J_base, J_star).round(2)
except Exception as e:
    print(e)
# In[7]:
A = np.array([
    [0, 2, 1, 4, 3, 0, -5, -10],
    [-1, 1, 1, 0, 1, 1, -1, -1],
    [1, 1, 1, 0, 1, -2, -5, 8]
])
b = np.array([20, 1, 7])
D = np.array([
    [25., 10., 0., 3., -1., 13., 0., 1.],
    [10., 45., 0., 0., 0., 20., 0., 0.],
    [0., 0., 20., 0., 0., 0., 0., 0.],
    [3., 0., 0., 29., -3., 15., 0., 3.],
    [-1., 0., 0., -3., 21., -5., 0., -1],
    [13., 20., 0., 15., -5., 61., 0., 5],
    [0., 0., 0., 0., 0., 0., 20., 0.],
    [1., 0., 0., 3., -1., 5., 0., 21.]
])
x_0 = np.array([3, 0, 0, 2, 4, 0, 0, 0])
c = np.array([1, -3, 4, 3, 5, 6, -2, 0])
J_base = np.array([True, False, False, True, True, False, False, False])
J_star = np.array([True, False, False, True, True, False, False, False])
quadratic_simplex(A, D, c, x_0, J_base, J_star).round(2)
# In[8]:
A = np.array([
    [0, 0, 1, 5, 2, 0, -5, -4],
    [1, 1, -1, 0, 1, -1, -1, -1],
    [1, 1, 1, 0, 1, 2, 5, 8]
])
m, n = A.shape
b = np.array([15, -1, 9])
D = np.array([
    [0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0.]
])
x_0 = np.array([4, 0, 5, 2, 0, 0, 0, 0])
c = np.array([1, -3, 4, 3, 5, 6, -2, 0])
J_base = np.array([True, False, True, True, False, False, False, False])
J_star = np.array([True, False, True, True, False, False, False, False])
quadratic_simplex(A, D, c, x_0, J_base, J_star).round(2)
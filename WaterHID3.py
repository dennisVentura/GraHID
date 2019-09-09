# *-* coding: utf-8 *-*

from math import pow, log
from Matrix import Matrix, diagonal

pi = 3.14159265359
A1 = 0.314159265359e04   # * 1000*PI
A2 = 0.157079632679e04   # * 500*PI
A3 = 0.502654824574e02   # * 16*PI
A4 = 6.283185307         # * 2*PI
A5 = 1.27323954474       # 4/PI
A8 = 4.61841319859       # 5.74*(PI/4)^.9
A9 = -8.685889638e-01    # -2/ln(10)
AA = -1.5634601348       # -2*.9*2/ln(10)
AB = 3.28895476345e-03   # 5.74/(4000^.9)
AC = -5.14214965799e-03  # AA*AB
G = 9.81                 # GRAVITY
G2 = 19.62               # 2*9.81
G2_1 = 5.0968399592e-02  # 1/(G2)
G3 = 0.0826268           # CTE 3


def d_w(flow, ks, d, vis):
    q = abs(flow)
    s = vis*d
    w = q/s
    if w >= A1:
        y1 = A8 / pow(w, 0.9)
        y2 = ks / (3.7 * d) + y1
        y3 = A9 * log(y2)
        f = 1 / y3**2
    elif w > A2:
        y2 = ks / (3.7 * d) + AB
        y3 = A9 * log(y2)
        fa = 1.0 / y3**2
        fb = (2.0 + AC / (y2 * y3)) * fa
        r = w / A2
        x1 = 7.0 * fa - fb
        x2 = 0.128 - 17.0 * fa + 2.5 * fb
        x3 = -0.128 + 13.0 * fa - (fb + fb)
        x4 = r * (0.032 - 3.0 * fa + 0.5 * fb)
        f = x1 + r * (x2 + r * (x3 + x4))
    elif w > A4:
        f = A3 * s / q
    else:
        f = 8.0
    return f


def a_11(flow: float, alpha: float, beta: float, lamb: float, co_m: float):
    return alpha * flow ** (co_m - 1) + beta + lamb / flow


def f_alpha(flow: float, diam: float, long: float, ks: float, c: float, n_m: float,
            vis: float, t: float, v_t: bool, eq: str):
    if eq == 'd-w':
        vis = vis if v_t else (1.14-0.031*(t-15)+0.00068*(t-15)**2)*.000001
        f = d_w(flow, ks, diam, vis)
        return G3 * f * long/diam**5
    elif eq == 'c-m':
        return 10.294 * n_m ** 2 * long / diam ** 5.33
    elif eq == 'h-w':
        return 10.674 * long / (c**1.85 * diam ** 4.78)


def f_beta(flow: float, kl: float, diam: float):
    return G3 * flow * kl / diam ** 4


def f_lambda(flow: float, a: float, b: float, c: float):
    return a * flow * flow + b * flow + c


def constant(l_pipes: list, l_nodes: list, l_reservoir: list, eq: str):
    pass


def l_a_11(flow: float, alpha: float, beta: float, lamb:float, co_m:float):
    return alpha * flow ** (co_m -1) + beta + lamb / flow


def iterate_w(data: list, bomb: list, a_21: Matrix, a_12: Matrix, a_10: Matrix, n_d: Matrix, q_o: Matrix, h_o: Matrix, q_d: Matrix,
              ide: Matrix, error=1e-4, i_max=20):
    flow = data[0]
    diam = data[1]
    long = data[2]
    ks = data[3]
    kl = data[4]
    c = data[5]
    n_m = data[6]
    vis = data[7]
    t = data[8]
    v_t = data[9]
    eq = data[10]
    co_m = data[11]
    a_b = bomb[0]
    b_b = bomb[1]
    c_b = bomb[2]
    for i in range(i_max):
        l_alpha = list(map(f_alpha, flow, diam, long, ks, c, n_m, vis, t, v_t, eq))
        beta = list(map(f_beta, flow, kl, diam))
        lamb = list(map(f_lambda, flow, a_b, b_b, c_b))
        a_11 = diagonal(list(map(l_a_11, flow, l_alpha, beta, lamb, co_m)))
        h_nxt = -(a_21 * (n_d * a_11.I * a_12)).I * (a_21 * (n_d.I * (q_o + a_11.I * a_10 * h_o)) + q_d - a_21 * q_o)
        q_nxt = ide * q_o - n_d.I * q_o - (n_d * a_11).I * (a_12 * h_nxt + a_10 * h_o)
        pres = (abs(q_o)-abs(q_nxt)).N
        if pres < error:
            break
        q_o = abs(q_nxt)
    else:
        return False, dict
    return True, {'q': q_nxt, 'h': h_nxt, 'a_11': a_11}
flow = []
diam = [1]
long = [2]
ks = [3]
kl = [4]
c = [5]
n_m = [6]
vis = [7]
t = [8]
v_t = [9]
eq = [10]
co_m = [11]
a_b = [0]
b_b = [1]
c_b = [2]
data = [flow, diam, long, ks, kl, c, n_m, vis, t, v_t, eq, co_m]
bomb = [a_b, b_b, c_b]
a_21 = 

a = iterate_w(data, bomb, a_21, a_12, a_10, n_d, q_o, h_o, q_d, ide)
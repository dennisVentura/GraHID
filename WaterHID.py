from __future__ import print_function
from math import log
from Matrix import *
from random import randint, sample, random


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


class Reservoir(object):
    level = 0.0
    cond = True
    name = ''
    t_level = ''
    item = None
    x = 0
    y = 0


class Node(object):
    demand = 0.0
    level = 0.0
    height = 0.0
    cond = True
    name = ''
    t_pressure = ''
    t_level = ''
    t_height = ''
    item = None
    x = 0
    y = 0

    def pressure(self):
        return self.height - self.level


class Pipe(object):
    n_i = None
    n_f = None
    diam = 0.0
    long = 0.0
    ks = 0.0
    C = 0.0
    n_m = 0.0
    kl = 0.0
    flow = 0.0
    vis = 0.0
    t = 0.0
    v_t = True  # True->Vis, False->Temperature
    bomb_a = 0.0
    bomb_b = 0.0
    bomb_c = 0.0
    f = 0.0
    cond = 'Open'
    name = ''
    t_flow = ''
    t_speed = ''
    t_long = ''
    t_hf = ''
    item = None

    @property
    def area(self):
        return pi*self.diam*self.diam/4

    @property
    def speed(self):
        return self.flow/self.area

    @property
    def reynolds(self):
        return A5*self.flow/(self.diam*self.vis)

    def alpha(self, eq: str):
        if eq == 'd-w':
            self.vis = self.vis if self.v_t else (1.14-0.031*(self.t-15)+0.00068*(self.t-15)**2)*.000001
            self.f = d_w(self.flow, self.ks, self.diam, self.vis)
            return G3 * self.f*self.long/self.diam**5
        elif eq == 'c-m':
            return 10.294 * self.n_m ** 2 * self.long / self.diam ** 5.33
        elif eq == 'h-w':
            return 10.674 * self.long / (self.C ** 1.85 * self.diam ** 4.78)

    @property
    def beta(self):
        return G3 * self.flow * self.kl / self.diam ** 4

    @property
    def lamb(self):
        return self.bomb_a*self.flow*self.flow + self.bomb_b*self.flow + self.bomb_c


def calc_cte(l_pipes, l_nodes, l_reservoir, eq='D-W'):
    n_p = len(l_pipes)
    n_n = len(l_nodes)
    n_r = len(l_reservoir)
    n_t = n_n + n_r
    a_t = zeros(n_t, n_p)
    l_t = l_reservoir + l_nodes
    co_m = 2
    equation = eq.lower()
    if equation == 'd-w':
        co_m = 2
    elif equation == 'c-m':
        co_m = 2
    elif equation == 'h-w':
        co_m = 1.85
    for i in range(n_p):
        a_t[i][l_t.index(l_pipes[i].n_i)] = -1
        a_t[i][l_t.index(l_pipes[i].n_f)] = 1
    n_c_d = [i + n_r for i in range(n_n) if l_nodes[i].cond]
    a_12 = a_t.get_col(n_c_d)
    n_c_c = [i for i in range(n_r) if l_reservoir[i].cond]
    a_10 = a_t.get_col(n_c_c)
    a_21 = a_12.T
    n_d = diagonal(co_m, n_p)
    ide = diagonal(1, n_p)
    h_o = Matrix([[i.level] for i in l_reservoir])
    q_d = Matrix([[i.demand] for i in l_nodes])
    q_o = Matrix([[i.flow] for i in l_pipes])
    return equation, co_m, a_21, n_d, a_12, a_10, h_o, q_d, q_o, {'n_p': n_p, 'n_n': n_n, 'n_r': n_r, 'n_t': n_t, 'a_t': a_t, 'a_12': a_12,
                                                                  'a_21': a_21, 'a_10': a_10, 'n_d': n_d, 'ide': ide}


def iterate_w(l_pipes, equation, co_m, a_21, a_12, a_10, n_d, q_o, h_o, q_d, ide, error, i_max, status):
    cont = 0
    while cont < i_max:
        if not status is None:
            status.showMessage("Iteración: " + str(cont))

        l_a11 = []
        for i in l_pipes:
            l_a11.append(i.alpha(equation) * i.flow ** (co_m - 1) + i.beta + i.lamb / i.flow)
        a_11 = diagonal(l_a11)
        h_nxt = -(a_21 * (n_d * a_11.I*a_12)).I*(a_21 * (n_d.I * (q_o + a_11.I*a_10 * h_o)) + q_d - a_21 * q_o)
        q_nxt = ide * q_o - n_d.I * q_o - (n_d * a_11).I * (a_12 * h_nxt + a_10 * h_o)
        if isinstance(h_nxt[0][0], complex) or isinstance(q_nxt[0][0], complex):
            if h_nxt[0][0].imag < 1e-3 or h_nxt[0][0].imag < 1e-3:
                h_nxt = Matrix([[i.real for i in j] for j in h_nxt])
                q_nxt = Matrix([[i.real for i in j] for j in q_nxt])
            else:
                return False, dict
        pres = (abs(q_o) - abs(q_nxt)).N
        if pres < error:
            break
        q_o = abs(q_nxt)
        for i, j in enumerate(l_pipes):
            j.flow = q_o[i][0]
        cont += 1
    else:
        return False, dict
    if not status is None:
        status.showMessage("Presición: "+ str(pres))
    return True, {'q': q_nxt, 'h': h_nxt, 'a_11': a_11}


def water_net(l_pipes, l_nodes, l_reservoir, status=None, eq='D-W', error=1e-3, i_max=1):
    """
    EXAMPLE:
    node1 = Node()
    node1.demand, node1.level = .06, 0.0
    node2 = Node()
    node2.demand, node2.level = .04, 0.0
    node3 = Node()
    node3.demand, node3.level = .03, 0.0
    node4 = Node()
    node4.demand, node4.level = .03, 0.0
    node5 = Node()
    node5.demand, node5.level = .04, 0.0
    l_n = [node1, node2, node3, node4, node5]
    res1 = Reservoir()
    res1.level = 100
    l_r = [res1]
    pipe1 = Pipe()
    pipe1.n_i, pipe1.n_f, pipe1.flow, pipe1.diam, pipe1.long, pipe1.vis, pipe1.ks =
        res1, node1,.1, .254, 500, 1.14E-6, 6E-5
    pipe2 = Pipe()
    pipe2.n_i, pipe2.n_f, pipe2.flow, pipe2.diam, pipe2.long, pipe2.vis, pipe2.ks, pipe2.kl =
        node1, node2, .1, .1524, 400, 1.14E-6, 6E-5, 10
    pipe3 = Pipe()
    pipe3.n_i, pipe3.n_f, pipe3.flow, pipe3.diam, pipe3.long, pipe3.vis, pipe3.ks =
        node3, node2, .1, .1016, 200, 1.14E-6, 6E-5
    pipe4 = Pipe()
    pipe4.n_i, pipe4.n_f, pipe4.flow, pipe4.diam, pipe4.long, pipe4.vis, pipe4.ks =
        node4, node3, .1, .1524, 400, 1.14E-6, 6E-5
    pipe5 = Pipe()
    pipe5.n_i, pipe5.n_f, pipe5.flow, pipe5.diam, pipe5.long, pipe5.vis, pipe5.ks =
        node1, node4, .1, .1016, 200, 1.14E-6, 6E-5
    pipe6 = Pipe()
    pipe6.n_i, pipe6.n_f, pipe6.flow, pipe6.diam, pipe6.long, pipe6.vis, pipe6.ks =
        node5, node4, .1, .2032, 600, 1.14E-6, 6E-5
    pipe7 = Pipe()
    pipe7.n_i, pipe7.n_f, pipe7.flow, pipe7.diam, pipe7.long, pipe7.vis, pipe7.ks =
        res1, node5, .1, .254, 300, 1.14E-6, 6E-5
    l_p = [pipe1, pipe2, pipe3, pipe4, pipe5, pipe6, pipe7]
    water_net(l_p, l_n, l_r, i_max=45)"""
    equation, co_m, a_21, n_d, a_12, a_10, h_o, q_d, q_o, di = calc_cte(l_pipes, l_nodes, l_reservoir, eq)
    ide = di['ide']
    cond, res = iterate_w(l_pipes, equation, co_m, a_21, a_12, a_10, n_d, q_o, h_o, q_d, ide, error, i_max, status)
    
    if cond:
        q_nxt = res['q']
        h_nxt = res['h']
        for i, j in enumerate(l_pipes):
            j.flow = q_nxt[i][0]
        for i, j in enumerate(l_nodes):
            j.height = h_nxt[i][0]
        return True, dict(res, **di)
    else:
        return False, dict


def copy_of(l_i):
    l_i2 = []
    for i in l_i:
        new_item = i
        l_i2.append(new_item)
    return l_i2


def individual(diam: dict, l_pipes):
    return [list(diam.keys())[randint(0, len(diam)-1)] for i in range(l_pipes)]


def population(num, diam, l_pipes):
    return [individual(diam, l_pipes) for i in range(num)]


def weight(l_d, l_pipes, l_nodes, l_reservoir, h_v, diam):
    k = 2e5
    l_pipes2 = copy_of(l_pipes)
    for i, j in enumerate(l_pipes2):
        j.diam = l_d[i]
    cond, _ = water_net(l_pipes2, l_nodes, l_reservoir, status=None)
    if cond:
        f_p = 0
        cost = 0
        for i in l_nodes:
            f_p += abs((i.pressure()-h_v['h_max'])/h_v['h_max']) + abs((i.pressure() - h_v['h_min'])/h_v['h_min'])
        for i in l_pipes2:
            f_p += abs((i.speed-h_v['v_max'])/h_v['v_max']) + abs((i.speed-h_v['v_min'])/h_v['v_min'])
            cost += i.long * diam[i.diam]
        if k-f_p*cost > 0:
            return k-f_p*cost
        else:
            return 0
    else:
        return 0


def sel_and_rep(new_pop, l_pipes, l_nodes, l_res, cond, diam):
    l_w = []
    for j in new_pop:
        l_w.append(weight(j, l_pipes, l_nodes, l_res, cond, diam))
    d_l = [(l_w[i], new_pop[i]) for i in range(len(new_pop))]
    punt = [i[1] for i in sorted(d_l, reverse=True)]
    pop = [[i for i in j] for j in punt]
    selected = punt[int(len(d_l) / 2):]
    for i in range(int(len(d_l)/2)):
        point = randint(1, len(l_pipes) - 1)  # Se elige un punto para hacer el intercambio
        padre = sample(selected, 2)  # Se eligen dos padres
        pop[1][:point] = padre[0][:point]  # Se mezcla el material genetico de los padres en cada nuevo individuo
        pop[1][point:] = padre[1][point:]
    return pop


def mutation(n_pop, l_pipes, l_nodes, l_res, h_v, d_di, n_p):
    pop = copy_of(n_pop)
    for i in range(len(n_pop)):
        if random() <= 1:  # Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar
            point = randint(0, len(l_pipes) - 1)  # Se elgie un punto al azar
            diam = n_pop[i]
            n_l_pipes = copy_of(l_pipes)
            for j, k in enumerate(diam):
                n_l_pipes[j].diam = k
            cond, _ = water_net(n_l_pipes, l_nodes, l_res)
            l_diams = list(d_di.keys())
            if cond:
                ind = l_diams.index(n_l_pipes[point].diam)
                if n_l_pipes[point].speed < h_v['v_min']:
                    if ind < (len(l_diams) - 1):
                        pop[i][point] = l_diams[ind+1]
                elif n_l_pipes[point].speed > h_v['v_max']:
                    if ind > 0:
                        pop[i][point] = l_diams[ind-1]
            else:
                pop = population(n_p, d_di, len(l_pipes))
    return pop


def designer_e_g(l_pipes, l_nodes, l_res, diam, cond, ge=40, n_p=10, bar=None):
    pop = population(n_p, diam, len(l_pipes))
    n_pop = [[i for i in j] for j in pop]
    if bar is not None:
        bar.setMinimum(0)
        bar.setMaximum(ge)
    for i in range(ge):
        if bar is not None:
            bar.setValue(i)
        n_pop = sel_and_rep(n_pop, l_pipes, l_nodes, l_res, cond, diam)
        n_pop = mutation(n_pop, l_pipes, l_nodes, l_res, cond, diam, n_p)
    return n_pop

"""

node1 = Node()
node1.demand, node1.level = .05, 0.0
node2 = Node()
node2.demand, node2.level = .03, 0.0
node3 = Node()
node3.demand, node3.level = .04, 0.0
node4 = Node()
node4.demand, node4.level = .02, 0.0
node5 = Node()
node5.demand, node5.level = .04, 0.0
l_n = [node1, node2, node3, node4, node5]
res1 = Reservoir()
res1.level = 80
l_r = [res1]
pipe1 = Pipe()
pipe1.n_i, pipe1.n_f, pipe1.flow, pipe1.diam, pipe1.long, pipe1.vis, pipe1.ks = res1, node1,.1, .254, 300, 1.14E-6, 6E-5
pipe2 = Pipe()
pipe2.n_i, pipe2.n_f, pipe2.flow, pipe2.diam, pipe2.long, pipe2.vis, pipe2.ks= res1, node2, .1, .2032, 400, 1.14E-6, 6E-5
pipe3 = Pipe()
pipe3.n_i, pipe3.n_f, pipe3.flow, pipe3.diam, pipe3.long, pipe3.vis, pipe3.ks = node1, node3, .1, .2032, 400, 1.14E-6, 6E-5
pipe4 = Pipe()
pipe4.n_i, pipe4.n_f, pipe4.flow, pipe4.diam, pipe4.long, pipe4.vis, pipe4.ks = node3, node5, .1, .1324, 500, 1.14E-6, 6E-5
pipe5 = Pipe()
pipe5.n_i, pipe5.n_f, pipe5.flow, pipe5.diam, pipe5.long, pipe5.vis, pipe5.ks, pipe5.kl = node2, node4, .1, .1524, 500, 1.14E-6, 6E-5, 4
pipe6 = Pipe()
pipe6.n_i, pipe6.n_f, pipe6.flow, pipe6.diam, pipe6.long, pipe6.vis, pipe6.ks = node4, node5, .1, .1524, 300, 1.14E-6, 6E-5
pipe7 = Pipe()
pipe7.n_i, pipe7.n_f, pipe7.flow, pipe7.diam, pipe7.long, pipe7.vis, pipe7.ks = node3, node2, .1, .1524, 300, 1.14E-6, 6E-5
l_p = [pipe1, pipe2, pipe3, pipe4, pipe5, pipe6, pipe7]
a = water_net(l_p, l_n, l_r, i_max=45, status=None)
print(a[0])

l_d_c = {.5: 2.5, .254: 1.3, .2032: 0.9, .1524: 0.7, .1016: 0.4}  # major to minor
cnd = {'v_min': .6, 'v_max': 3, 'h_min': 10, 'h_max': 50}
a = designer_e_g(l_p, l_n, l_r, l_d_c, cnd)
l = a[0]
for i, j in enumerate(l_p):
    j.diam = l[i]
cond, a = water_net(l_p, l_n, l_r, status=None)
for i in l_p:
    print(i.speed)
"""

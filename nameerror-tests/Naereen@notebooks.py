import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import numpy.random as rd
def I(n):
    def f(t):
        return 1 / ((1+t)**n * np.sqrt(1-t))
    i, err = integrate.quad(f, 0, 1)
    return i
def J(n):
    def f(t):
        return 1 / ((1+t)**n * np.sqrt(1-t))
    i, err = integrate.quad(f, 0, 0.5)
    return i
valeurs_n = np.arange(1, 50)
valeurs_In = np.array([I(n) for n in valeurs_n])
plt.figure()
plt.plot(valeurs_n, valeurs_In, 'ro')
plt.title("Valeurs de $I_n$")
plt.show()
plt.figure()
plt.plot(np.log(valeurs_n), np.log(valeurs_In), 'go')
plt.title(r"Valeurs de $\ln(I_n)$ en fonction de $\ln(n)$")
plt.show()
valeurs_Jn = np.array([J(n) for n in valeurs_n])
alpha = 1
plt.figure()
plt.plot(valeurs_n, valeurs_n**alpha * valeurs_In, 'r+', label=r'$n^{\alpha} I_n$')
plt.plot(valeurs_n, valeurs_n**alpha * valeurs_Jn, 'b+', label=r'$n^{\alpha} J_n$')
plt.legend()
plt.title(r"Valeurs de $n^{\alpha} I_n$ et $n^{\alpha} J_n$")
plt.show()
plt.figure()
plt.plot(valeurs_n, valeurs_n**alpha * (valeurs_In - valeurs_Jn), 'g+', label=r'$n^{\alpha} (I_n - J_n)$')
plt.legend()
plt.title(r"Valeurs de $n^{\alpha} (I_n - J_n)$")
plt.show()
X = np.linspace(0, 100, 10000)
plt.plot(X, np.log(1 + X), 'r-', label=r'$\log(1+x)$')
plt.plot(X, X / (1 + X), 'b-', label=r'$\frac{x}{1+x}$')
plt.legend()
plt.title("Comparaison entre deux fonctions")
plt.show()
def f(x):
    return x * (1 - x) * (1 + np.cos(5 * np.pi * x))
Xs = np.linspace(0, 1, 2000)
Ys = f(Xs)
M = max_de_f = max(Ys)
print("Sur [0, 1], avec 2000 points, M =", M)
plt.figure()
plt.plot(Xs, Ys)
plt.title("Fonction $f(x)$ sur $[0,1]$")
plt.show()
def In(x, n):
    def fn(x):
        return f(x) ** n
    return integrate.quad(fn, 0, 1)[0]
def Sn(x):
    return np.sum([In(Xs, n) * x**n for n in range(0, n+1)], axis=0)
for n in range(10):
    print("In(x,", n, ") =", In(Xs, n))
a = 1/M + 0.1
X2s = np.linspace(-a, a, 2000)
plt.figure()
for n in [10, 20, 30, 40, 50]:
    plt.plot(X2s, Sn(X2s), label="n =" + str(n))
plt.legend()
plt.show()
def un(n):
    return In(Xs, n + 1) / In(Xs, n)
for n in range(10):
    print("un =", un(n), "pour n =", n)
def affiche_termes_un(N):
    valeurs_un = [0] * N
    for n in range(N):
        valeurs_un[n] = un(n)
    plt.figure()
    plt.plot(valeurs_un, 'o-')
    plt.title("Suite $u_n$")
    plt.grid()
    plt.show()
affiche_termes_un(30)
affiche_termes_un(100)
case_max = 12
univers = list(range(case_max))
def prochaine_case(case):
    return (case + rd.randint(1, 6+1)) % case_max
def Yn(duree, depart=0):
    case = depart
    for coup in range(duree):
        case = prochaine_case(case)
    return case
[Yn(1) for _ in range(10)]
[Yn(100) for _ in range(10)]
np.bincount(_, minlength=case_max)
def histogramme(duree, repetitions=5000):
    cases = [Yn(duree) for _ in range(repetitions)]
    frequences = np.bincount(cases, minlength=case_max)
    # aussi a la main si besoin
    frequences = [0] * case_max
    for case in cases:
        frequences[case] += 1
    return frequences / np.sum(frequences)
histogramme(50)
def voir_histogramme(valeurs_n):
    for n in valeurs_n:
        plt.figure()
        plt.bar(np.arange(case_max), histogramme(n))
        plt.title("Histogramme de cases visitées en " + str(n) + " coups")
        plt.show()
voir_histogramme([1, 2, 3, 50, 100, 200])
P = np.zeros((case_max, case_max))
for k in range(case_max):
    for i in range(k - 6, k):
        P[k, i] = 1
P
import numpy.linalg as LA
spectre, vecteur_propres = LA.eig(P)
np.round(spectre)
np.round(vecteur_propres[0])
def f(x):
    return 1 / (2 - np.exp(x))
from math import factorial
def a_0an(nMax):
    valeurs_a = np.zeros(nMax+1)
    valeurs_a[0] = 1.0
    for n in range(1, nMax+1):
        valeurs_a[n] = sum(valeurs_a[n-k] / factorial(k) for k in range(1, n+1))
    return valeurs_a
nMax = 10
valeurs_n = np.arange(0, nMax + 1)
valeurs_a = a_0an(nMax)
for n in valeurs_n:
    print("Pour n =", n, "on a a(n) =", valeurs_a[n])
plt.figure()
plt.plot(valeurs_n, valeurs_a, 'ro', label=r'$a(n)$')
plt.plot(valeurs_n, 1 / np.log(2)**valeurs_n, 'g+', label=r'$1/\log(2)^n$')
plt.plot(valeurs_n, 1 / (2 * np.log(2)**valeurs_n), 'bd', label=r'$1/(2\log(2)^n)$')
plt.title("$a(n)$ et deux autres suites")
plt.legend()
plt.show()
def Sn(x, n):
    valeurs_a = a_0an(n)
    return sum(valeurs_a[k] * x**k for k in range(0, n + 1))
x = 0.5
for n in range(0, 6 + 1):
    print("Pour n =", n, "S_n(x) =", Sn(x, n))
valeurs_x = np.linspace(0, 0.5, 1000)
valeurs_f = f(valeurs_x)
plt.figure()
for n in range(0, 6 + 1):
    valeurs_Sn = []
    for x in valeurs_x:
        valeurs_Sn.append(Sn(x, n))
    plt.plot(valeurs_x, valeurs_Sn, ':', label='$S_' + str(n) + '(x)$')
plt.plot(valeurs_x, valeurs_f, '-', label='$f(x)$')
plt.title("$f(x)$ et $S_n(x)$ pour $n = 0$ à $n = 6$")
plt.legend()
plt.show()
def u(n):
    return np.arctan(n+1) - np.arctan(n)
valeurs_n = np.arange(50)
valeurs_u = u(valeurs_n)
plt.figure()
plt.plot(valeurs_n, valeurs_u, "o-")
plt.title("Premières valeurs de $u_n$")
pi/2
sum(valeurs_u)
somme_serie = pi/2
somme_partielle = sum(valeurs_u)
erreur_relative = abs(somme_partielle - somme_serie) / somme_serie
erreur_relative
valeurs_n = np.arange(10, 1000)
valeurs_u = u(valeurs_n)
valeurs_equivalents = 1 / (valeurs_n * (valeurs_n + 1))
plt.figure()
plt.plot(valeurs_n, valeurs_u / valeurs_equivalents, "-")
plt.title(r"Valeurs de $u_n / \frac{1}{n(n+1)}$")
from math import ceil, sqrt, pi
def Se(e, delta=1e-5, borne_sur_n_0=10000):
    borne_sur_n_1 = int(ceil(1 + sqrt(delta)/2.0))
    borne_sur_n = max(borne_sur_n_0, borne_sur_n_1)
    somme_partielle = 0
    for n in range(0, borne_sur_n + 1):
        somme_partielle += e(n) * u(n)
    return somme_partielle
def e010101(n):
    return 1 if n % 2 == 0 else 0
delta = 1e-5
Se010101 = Se(e010101, delta)
print("Pour delta =", delta, "on a Se010101(delta) ~=", round(Se010101, 5))
def inverse_Se(x, n):
    assert 0 < x < pi/2.0, "Erreur : x doit être entre 0 et pi/2 strictement."
    print("Je vous laisse chercher.")
    raise NotImplementedError
from random import random
def pile(proba):
    """ True si pile, False si face (false, face, facile à retenir)."""
    return random() < proba
def En(n, p):
    lance = pile(p)
    for i in range(n - 1):
        nouveau_lance = pile(p)
        if lance and nouveau_lance:
            return False
        nouveau_lance = lance
    return True
import numpy as np
lances = [ En(2, 0.5) for _ in range(100) ]
np.bincount(lances)
def pn(n, p, nbSimulations=100000):
    return np.mean([ En(n, p) for _ in range(nbSimulations) ])
pn(2, 0.5)
pn(4, 0.5)
pn(4, 0.1)
pn(4, 0.9)
pn(6, 0.2)
pn(20, 0.2)
pn(100, 0.2)
from math import floor, log, pi
delta = 1e-5
def f(x):
    if x == 0: return 0
    borne_sur_n = int(floor(log((6/pi**2 * delta), abs(x)) - 1))
    somme_partielle = 0
    for n in range(1, borne_sur_n + 1):
        somme_partielle += x**n / n**2
    return somme_partielle
for x in [-0.75, -0.5, 0.25, 0, 0.25, 0.5, 0.75]:
    print("Pour x =", x, "\tf(x) =", round(f(x), 5))
from scipy import integrate
def g(x):
    def h(t):
        return log(1 - t) / t
    integrale, erreur = integrate.quad(h, 0, x)
    return integrale
import numpy as np
import matplotlib.pyplot as plt
domaine = np.linspace(-0.99, 0.99, 1000)
valeurs_f = [f(x) for x in domaine]
valeurs_g = [g(x) for x in domaine]
plt.figure()
plt.plot(domaine, valeurs_f, label="$f(x)$")
plt.plot(domaine, valeurs_g, label="$g(x)$")
plt.legend()
plt.grid()
plt.title("Représentation de $f(x)$ et $g(x)$")
plt.show()
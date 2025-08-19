# -*- coding: utf-8 -*-# fixed_point_iteracion.py
import math

def g(x):
    return 5.0/(x**2) + 2.0

def gprime_abs(x):
    return abs(-10.0/(x**3))

def fixed_point(g, x0, tol=1e-3, max_iter=1000):
    x_prev = x0
    for n in range(1, max_iter+1):
        x_next = g(x_prev)
        if abs(x_next - x_prev) < tol:
            return x_next, n, True
        x_prev = x_next
    return x_prev, max_iter, False

if __name__ == "__main__":
    # Interval elegido
    a, b = 2.3, 3.0

    # Comprobaciones del teorema del punto fijo
    ga = g(a)
    gb = g(b)
    k_max = max(gprime_abs(a), gprime_abs(b))  # en realidad máximo en a porque g' decrece en x>0

    print(f"Intervalo elegido: [{a}, {b}]")
    print(f"g(a) = {ga:.6f}, g(b) = {gb:.6f}")
    print(f"Máximo |g'(x)| en extremos aproximado: k <= {k_max:.6f}")

    if not (a <= gb <= ga <= b):
        print("ADVERTENCIA: g([a,b]) no está garantizado dentro de [a,b]. Revisa el intervalo.")
    elif k_max >= 1:
        print("ADVERTENCIA: k >= 1, no se garantiza convergencia por contracción.")
    else:
        print("Condiciones verificadas: g([a,b]) ⊆ [a,b] y k < 1. Convergencia garantizada.")
        # Elegimos x0 en el intervalo (por ejemplo b)
        x0 = b
        tol = 1e-3
        root, iterations, converged = fixed_point(g, x0, tol=tol, max_iter=1000)
        if converged:
            print(f"Convergió en {iterations} iteraciones.")
            print(f"Aproximación del punto fijo: x ≈ {root:.12f}")
            # También imprimo g(root) y diferencia con root
            print(f"g(x) = {g(root):.12f}, diferencia |g(x)-x| = {abs(g(root)-root):.3e}")
        else:
            print(f"No convergió en {iterations} iteraciones. Último valor: {root}")


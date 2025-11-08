import numpy as np
from scipy.linalg import eig
import sympy as sp

sp.init_printing()
t = sp.Symbol('t', real=True)

sistemas_nh = {
    1: {'A': np.array([[0, -1], [-9, 0]]), 'f': np.array([1, 9])},
    2: {'A': np.array([[1, 2], [2, 1]]), 'f': np.array([-5, -7])},
    3: {'A': np.array([[4, -1], [2, 1]]), 'f': np.array([0, -6])},
    4: {'A': np.array([[-2, 1], [1, -2]]), 'f': np.array([3, 2])},
    5: {'A': np.array([[-1, 2], [-1, 1]]), 'f': np.array([-8, 3])},
    6: {'A': np.array([[-1, 0], [0, -2]]), 'f': np.array([3, 5])},
    7: {'A': np.array([[-1, 0], [0, -2]]), 'f_sym': sp.Matrix([sp.cos(t), 0])},
    8: {'A': np.array([[-1, 0], [0, -2]]), 'f_sym': sp.Matrix([sp.exp(t), 0])},
    9: {'A': np.array([[1, 0], [0, -2]]), 'f_sym': sp.Matrix([sp.exp(t), 0])},
    10: {'A': np.array([[1, 2], [0, -1]]), 'f_sym': sp.Matrix([t, -t])},
}

def resolver_sistema(num):
    sistema = sistemas_nh[num]
    A = sp.Matrix(sistema['A'])
    
    # Autovalores y autovectores
    eigendata = A.eigenvects()
    eigenvalues = [ev[0] for ev in eigendata]
    eigenvectors = []
    for ev in eigendata:
        for vec in ev[2]:
            eigenvectors.append(vec)
    
    print(f"\n{'='*90}")
    print(f"SISTEMA {num}")
    print(f"{'='*90}")
    
    # SOLUCIÓN HOMOGÉNEA EN FORMA VECTORIAL
    c1, c2 = sp.symbols('c1 c2')
    
    if len(eigenvalues) >= 2:
        lam1, lam2 = eigenvalues[0], eigenvalues[1]
        v1, v2 = eigenvectors[0], eigenvectors[1]
        
        if lam1.has(sp.I):
            alpha = sp.re(lam1)
            beta = sp.im(lam1)
            v_real = sp.re(v1)
            v_imag = sp.im(v1)
            
            exp_t = sp.exp(alpha * t)
            X_h = exp_t * (c1 * (v_real * sp.cos(beta*t) - v_imag * sp.sin(beta*t)) + 
                          c2 * (v_real * sp.sin(beta*t) + v_imag * sp.cos(beta*t)))
            
            print("\nSOLUCIÓN HOMOGÉNEA:")
            print(f"X_h(t) = e^({alpha}t) [ c1·{v_real}·cos({beta}t) - c1·{v_imag}·sin({beta}t)")
            print(f"                      + c2·{v_real}·sin({beta}t) + c2·{v_imag}·cos({beta}t) ]")
        else:
            X_h = c1 * sp.exp(lam1 * t) * v1 + c2 * sp.exp(lam2 * t) * v2
            
            print("\nSOLUCIÓN HOMOGÉNEA:")
            print(f"X_h(t) = c1·e^({lam1}t)·{v1} + c2·e^({lam2}t)·{v2}")
    
    # SOLUCIÓN PARTICULAR EN FORMA VECTORIAL
    print("\nSOLUCIÓN PARTICULAR:")
    
    if 'f' in sistema:  # Forzamiento constante
        f = sp.Matrix(sistema['f'])
        try:
            X_p = -A.inv() * f
            print(f"X_p = {X_p}")
        except:
            print("X_p = No existe (A singular)")
    
    elif 'f_sym' in sistema:  # Forzamiento variable
        f_sym = sistema['f_sym']
        
        if f_sym.has(sp.cos):
            # Para cos(t)
            a1, a2, b1, b2 = sp.symbols('a1 a2 b1 b2', real=True)
            a_vec = sp.Matrix([a1, a2])
            b_vec = sp.Matrix([b1, b2])
            X_p = a_vec * sp.cos(t) + b_vec * sp.sin(t)
            dX_p = sp.diff(X_p, t)
            
            eq = dX_p - A * X_p - f_sym
            sol = sp.solve([eq[0], eq[1]], [a1, a2, b1, b2])
            
            if sol:
                a_vec_val = sp.Matrix([sol[a1], sol[a2]])
                b_vec_val = sp.Matrix([sol[b1], sol[b2]])
                print(f"X_p(t) = {a_vec_val}·cos(t) + {b_vec_val}·sin(t)")
        
        elif f_sym.has(sp.exp):
            # Para e^t
            exp_coef = 1
            hay_resonancia = any((lam - exp_coef).simplify() == 0 for lam in eigenvalues)
            
            a1, a2 = sp.symbols('a1 a2', real=True)
            a_vec = sp.Matrix([a1, a2])
            
            if hay_resonancia:
                X_p = t * sp.exp(t) * a_vec
                print(f"(Resonancia: λ = {exp_coef})")
            else:
                X_p = sp.exp(t) * a_vec
            
            dX_p = sp.diff(X_p, t)
            eq = dX_p - A * X_p - f_sym
            
            try:
                sol = sp.solve([eq[0], eq[1]], [a1, a2])
                if sol:
                    a_vec_val = sp.Matrix([sol[a1], sol[a2]])
                    if hay_resonancia:
                        print(f"X_p(t) = t·e^t·{a_vec_val}")
                    else:
                        print(f"X_p(t) = e^t·{a_vec_val}")
            except:
                print("X_p(t) = (requiere cálculo manual)")
        
        elif f_sym.has(t) and not f_sym.has(sp.exp):
            # Para polinomios en t
            a1, a2, b1, b2 = sp.symbols('a1 a2 b1 b2', real=True)
            a_vec = sp.Matrix([a1, a2])
            b_vec = sp.Matrix([b1, b2])
            X_p = a_vec * t + b_vec
            dX_p = sp.diff(X_p, t)
            
            eq = dX_p - A * X_p - f_sym
            
            try:
                sol = sp.solve([eq[0], eq[1]], [a1, a2, b1, b2])
                if sol:
                    a_vec_val = sp.Matrix([sol[a1], sol[a2]])
                    b_vec_val = sp.Matrix([sol[b1], sol[b2]])
                    print(f"X_p(t) = {a_vec_val}·t + {b_vec_val}")
            except:
                print("X_p(t) = (requiere cálculo manual)")
    
    print("\nSOLUCIÓN GENERAL:")
    print("X(t) = X_h(t) + X_p(t)")

if __name__ == "__main__":
    print("\n" + "🎯 "*35)
    print("SOLUCIONES DE SISTEMAS NO HOMOGÉNEOS EN FORMA VECTORIAL")
    print("🎯 "*35)
    
    for i in range(1, 11):
        try:
            resolver_sistema(i)
        except Exception as e:
            print(f"\nSistema {i}: Error - {e}")
    
    print("\n" + "="*90)
    print("FINALIZADO")
    print("="*90)
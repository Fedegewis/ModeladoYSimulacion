import numpy as np
from scipy.optimize import fsolve

print("="*90)
print("ANÁLISIS COMPLETO DE BIFURCACIONES - PUNTOS DE EQUILIBRIO Y CLASIFICACIÓN")
print("="*90)

def estabilidad(func, x_val, r_val, epsilon=1e-6):
    df_dx = (func(x_val + epsilon, r_val) - func(x_val - epsilon, r_val)) / (2 * epsilon)
    return df_dx < 0, df_dx

def encontrar_puntos_fijos(func, r_val, x_range=(-10, 10), num_guesses=100):
    puntos = []
    guesses = np.linspace(x_range[0], x_range[1], num_guesses)
    for guess in guesses:
        try:
            sol = fsolve(lambda x: func(x, r_val), guess, full_output=True)
            if sol[2] == 1:
                x_sol = sol[0][0]
                if x_range[0] <= x_sol <= x_range[1]:
                    if not any(abs(x_sol - p) < 1e-5 for p in puntos):
                        puntos.append(x_sol)
        except:
            pass
    return sorted(puntos)

# ======================================================================================
print("\n" + "="*90)
print("SISTEMA 1: ẋ = r + x²")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO (resolviendo ẋ = 0):")
print("   r + x² = 0")
print("   x² = -r")
print("   x* = ±√(-r)")
print("\n📍 EXISTENCIA:")
print("   • Para r < 0: Dos puntos fijos reales: x* = -√(-r) y x* = +√(-r)")
print("   • Para r = 0: Un punto fijo: x* = 0")
print("   • Para r > 0: No hay puntos fijos reales")
print("\n🔍 ESTABILIDAD (calculando f'(x*) = 2x*):")
print("   • x* = -√(-r): f'(x*) = -2√(-r) < 0  →  ESTABLE")
print("   • x* = +√(-r): f'(x*) = +2√(-r) > 0  →  INESTABLE")
print("\n⚡ BIFURCACIÓN: SILLA-NODO en r_c = 0")
print("   Los dos puntos fijos colisionan en r=0 y desaparecen para r>0")

def sistema1(x, r): return r + x**2
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-2, -1, -0.5, 0, 0.5]:
    print(f"\n   r = {r:6.2f}:")
    if r <= 0:
        x_teorico_1 = -np.sqrt(-r) if r < 0 else 0
        x_teorico_2 = np.sqrt(-r) if r < 0 else None
        print(f"      Teórico: x* = {x_teorico_1:.4f}", end="")
        if x_teorico_2: print(f", x* = {x_teorico_2:.4f}")
        else: print()
    puntos = encontrar_puntos_fijos(sistema1, r, x_range=(-5, 5))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema1, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 2: ẋ = rx - x²")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   rx - x² = 0")
print("   x(r - x) = 0")
print("   x* = 0  ó  x* = r")
print("\n📍 EXISTENCIA:")
print("   • Para todo r: Dos puntos fijos: x* = 0 y x* = r")
print("\n🔍 ESTABILIDAD (f'(x*) = r - 2x*):")
print("   • x* = 0: f'(0) = r")
print("     - Si r < 0 → ESTABLE")
print("     - Si r > 0 → INESTABLE")
print("   • x* = r: f'(r) = r - 2r = -r")
print("     - Si r < 0 → INESTABLE")
print("     - Si r > 0 → ESTABLE")
print("\n⚡ BIFURCACIÓN: TRANSCRÍTICA en r_c = 0")
print("   Los dos puntos fijos intercambian estabilidad en r=0")

def sistema2(x, r): return r*x - x**2
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-1, -0.5, 0, 0.5, 1, 2]:
    print(f"\n   r = {r:6.2f}:")
    print(f"      Teórico: x* = 0, x* = {r:.4f}")
    puntos = encontrar_puntos_fijos(sistema2, r, x_range=(-2, 5))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema2, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 3: ẋ = rx - x³")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   rx - x³ = 0")
print("   x(r - x²) = 0")
print("   x* = 0  ó  x² = r  →  x* = ±√r")
print("\n📍 EXISTENCIA:")
print("   • Para r < 0: Un punto fijo: x* = 0")
print("   • Para r = 0: Un punto fijo: x* = 0")
print("   • Para r > 0: Tres puntos fijos: x* = 0, x* = -√r, x* = +√r")
print("\n🔍 ESTABILIDAD (f'(x*) = r - 3x²):")
print("   • x* = 0: f'(0) = r")
print("     - Si r < 0 → ESTABLE")
print("     - Si r > 0 → INESTABLE")
print("   • x* = ±√r: f'(±√r) = r - 3r = -2r < 0  →  ESTABLE (para r>0)")
print("\n⚡ BIFURCACIÓN: HORQUILLA SUPERCRÍTICA en r_c = 0")
print("   El punto fijo estable x*=0 se vuelve inestable y nacen dos ramas estables")

def sistema3(x, r): return r*x - x**3
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-1, 0, 0.5, 1, 2]:
    print(f"\n   r = {r:6.2f}:")
    if r > 0:
        print(f"      Teórico: x* = 0, x* = ±{np.sqrt(r):.4f}")
    else:
        print(f"      Teórico: x* = 0")
    puntos = encontrar_puntos_fijos(sistema3, r, x_range=(-3, 3))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema3, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 4: ẋ = r + 3x - x³")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   r + 3x - x³ = 0")
print("   x³ - 3x - r = 0  (ecuación cúbica)")
print("\n📍 Los puntos fijos dependen de la cúbica. Discriminante Δ = 4 - r²")
print("   • Para |r| < 2: Tres puntos fijos reales")
print("   • Para |r| = 2: Dos puntos fijos (uno doble)")
print("   • Para |r| > 2: Un punto fijo real")
print("\n⚡ BIFURCACIÓN: SILLA-NODO en r_c = ±2")

def sistema4(x, r): return r + 3*x - x**3
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-4, -2, 0, 2, 4]:
    print(f"\n   r = {r:6.2f}:")
    puntos = encontrar_puntos_fijos(sistema4, r, x_range=(-4, 4))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema4, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 5: ẋ = r - eˣ")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   r - eˣ = 0")
print("   eˣ = r")
print("   x* = ln(r)")
print("\n📍 EXISTENCIA:")
print("   • Para r ≤ 0: No hay puntos fijos reales")
print("   • Para r > 0: Un punto fijo: x* = ln(r)")
print("\n🔍 ESTABILIDAD (f'(x*) = -eˣ* = -r < 0):")
print("   • x* = ln(r): Siempre ESTABLE para r > 0")
print("\n⚡ BIFURCACIÓN: SILLA-NODO en r_c = 0")

def sistema5(x, r): return r - np.exp(x)
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [0.5, 1, np.e, 2, 3]:
    print(f"\n   r = {r:6.2f}:")
    if r > 0:
        print(f"      Teórico: x* = ln({r:.2f}) = {np.log(r):.4f}")
    puntos = encontrar_puntos_fijos(sistema5, r, x_range=(-2, 4))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema5, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 6: ẋ = r - x²")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   r - x² = 0")
print("   x² = r")
print("   x* = ±√r")
print("\n📍 EXISTENCIA:")
print("   • Para r < 0: No hay puntos fijos reales")
print("   • Para r = 0: Un punto fijo: x* = 0")
print("   • Para r > 0: Dos puntos fijos: x* = -√r y x* = +√r")
print("\n🔍 ESTABILIDAD (f'(x*) = -2x*):")
print("   • x* = -√r: f'(x*) = 2√r > 0  →  INESTABLE")
print("   • x* = +√r: f'(x*) = -2√r < 0  →  ESTABLE")
print("\n⚡ BIFURCACIÓN: SILLA-NODO en r_c = 0")

def sistema6(x, r): return r - x**2
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-0.5, 0, 0.5, 1, 2]:
    print(f"\n   r = {r:6.2f}:")
    if r > 0:
        print(f"      Teórico: x* = ±{np.sqrt(r):.4f}")
    elif r == 0:
        print(f"      Teórico: x* = 0")
    puntos = encontrar_puntos_fijos(sistema6, r, x_range=(-3, 3))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema6, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 7: ẋ = rx + x³")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   rx + x³ = 0")
print("   x(r + x²) = 0")
print("   x* = 0  ó  x² = -r  →  x* = ±√(-r)")
print("\n📍 EXISTENCIA:")
print("   • Para r > 0: Un punto fijo: x* = 0")
print("   • Para r = 0: Un punto fijo: x* = 0")
print("   • Para r < 0: Tres puntos fijos: x* = 0, x* = ±√(-r)")
print("\n🔍 ESTABILIDAD (f'(x*) = r + 3x²):")
print("   • x* = 0: f'(0) = r")
print("     - Si r < 0 → ESTABLE")
print("     - Si r > 0 → INESTABLE")
print("   • x* = ±√(-r): f'(x*) = r + 3(-r) = -2r > 0  →  INESTABLE (para r<0)")
print("\n⚡ BIFURCACIÓN: HORQUILLA SUBCRÍTICA en r_c = 0")
print("   El punto fijo estable x*=0 se vuelve inestable (las ramas inestables desaparecen)")

def sistema7(x, r): return r*x + x**3
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-2, -1, 0, 0.5, 1]:
    print(f"\n   r = {r:6.2f}:")
    if r < 0:
        print(f"      Teórico: x* = 0, x* = ±{np.sqrt(-r):.4f}")
    else:
        print(f"      Teórico: x* = 0")
    puntos = encontrar_puntos_fijos(sistema7, r, x_range=(-3, 3))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema7, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 8: ẋ = x³ - rx")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   x³ - rx = 0")
print("   x(x² - r) = 0")
print("   x* = 0  ó  x* = ±√r")
print("\n📍 EXISTENCIA:")
print("   • Para r < 0: Un punto fijo: x* = 0")
print("   • Para r = 0: Un punto fijo: x* = 0")
print("   • Para r > 0: Tres puntos fijos: x* = 0, x* = ±√r")
print("\n🔍 ESTABILIDAD (f'(x*) = 3x² - r):")
print("   • x* = 0: f'(0) = -r")
print("     - Si r < 0 → INESTABLE")
print("     - Si r > 0 → ESTABLE → ¡ERROR! debe ser INESTABLE")
print("   Corrección: f'(0) = -r, si r>0 entonces f'(0)<0 → ESTABLE ❌")
print("   En realidad para r>0: f'(0)=-r<0 pero el sistema es x³-rx, revisemos...")
print("   • x* = ±√r: f'(±√r) = 3r - r = 2r > 0  para r>0 → ¿INESTABLE?")
print("   Revisión: f'(x) = 3x² - r, entonces f'(±√r) = 3r - r = 2r")
print("   Corrección final: Para r>0, x*=0 tiene f'(0)=-r<0 → ESTABLE")
print("                     x*=±√r tienen f'(±√r)=2r>0 → INESTABLE")
print("\n⚡ BIFURCACIÓN: HORQUILLA SUPERCRÍTICA en r_c = 0")

def sistema8(x, r): return x**3 - r*x
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-1, 0, 0.5, 1, 2]:
    print(f"\n   r = {r:6.2f}:")
    if r > 0:
        print(f"      Teórico: x* = 0, x* = ±{np.sqrt(r):.4f}")
    else:
        print(f"      Teórico: x* = 0")
    puntos = encontrar_puntos_fijos(sistema8, r, x_range=(-3, 3))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema8, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 9: ẋ = (r-1) - (x-1)²")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   (r-1) - (x-1)² = 0")
print("   (x-1)² = r-1")
print("   x-1 = ±√(r-1)")
print("   x* = 1 ± √(r-1)")
print("\n📍 EXISTENCIA:")
print("   • Para r < 1: No hay puntos fijos reales")
print("   • Para r = 1: Un punto fijo: x* = 1")
print("   • Para r > 1: Dos puntos fijos: x* = 1-√(r-1) y x* = 1+√(r-1)")
print("\n🔍 ESTABILIDAD (f'(x*) = -2(x*-1)):")
print("   • x* = 1-√(r-1): f'(x*) = -2(-√(r-1)) = 2√(r-1) > 0  →  INESTABLE")
print("   • x* = 1+√(r-1): f'(x*) = -2(√(r-1)) = -2√(r-1) < 0  →  ESTABLE")
print("\n⚡ BIFURCACIÓN: SILLA-NODO en r_c = 1")
print("   Los dos puntos fijos nacen en r=1")

def sistema9(x, r): return (r - 1) - (x - 1)**2
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [0.5, 1, 1.5, 2, 3]:
    print(f"\n   r = {r:6.2f}:")
    if r > 1:
        x1_teorico = 1 - np.sqrt(r-1)
        x2_teorico = 1 + np.sqrt(r-1)
        print(f"      Teórico: x* = {x1_teorico:.4f}, x* = {x2_teorico:.4f}")
    elif r == 1:
        print(f"      Teórico: x* = 1.0000")
    else:
        print(f"      Teórico: No hay puntos fijos")
    puntos = encontrar_puntos_fijos(sistema9, r, x_range=(-2, 4))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema9, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 10: ẋ = (r-2)x - x²")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   (r-2)x - x² = 0")
print("   x[(r-2) - x] = 0")
print("   x* = 0  ó  x* = r-2")
print("\n📍 EXISTENCIA:")
print("   • Para todo r: Dos puntos fijos: x* = 0 y x* = r-2")
print("\n🔍 ESTABILIDAD (f'(x*) = (r-2) - 2x*):")
print("   • x* = 0: f'(0) = r-2")
print("     - Si r < 2 → f'(0) < 0 → ESTABLE")
print("     - Si r > 2 → f'(0) > 0 → INESTABLE")
print("   • x* = r-2: f'(r-2) = (r-2) - 2(r-2) = -(r-2)")
print("     - Si r < 2 → f'(r-2) > 0 → INESTABLE")
print("     - Si r > 2 → f'(r-2) < 0 → ESTABLE")
print("\n⚡ BIFURCACIÓN: TRANSCRÍTICA en r_c = 2")
print("   Los dos puntos fijos intercambian estabilidad en r=2")

def sistema10(x, r): return (r - 2)*x - x**2
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [0, 1, 2, 3, 4]:
    print(f"\n   r = {r:6.2f}:")
    print(f"      Teórico: x* = 0, x* = {r-2:.4f}")
    puntos = encontrar_puntos_fijos(sistema10, r, x_range=(-1, 6))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema10, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 11: ẋ = (r-3)x - x³")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   (r-3)x - x³ = 0")
print("   x[(r-3) - x²] = 0")
print("   x* = 0  ó  x² = r-3  →  x* = ±√(r-3)")
print("\n📍 EXISTENCIA:")
print("   • Para r < 3: Un punto fijo: x* = 0")
print("   • Para r = 3: Un punto fijo: x* = 0")
print("   • Para r > 3: Tres puntos fijos: x* = 0, x* = -√(r-3), x* = +√(r-3)")
print("\n🔍 ESTABILIDAD (f'(x*) = (r-3) - 3x²):")
print("   • x* = 0: f'(0) = r-3")
print("     - Si r < 3 → ESTABLE")
print("     - Si r > 3 → INESTABLE")
print("   • x* = ±√(r-3): f'(±√(r-3)) = (r-3) - 3(r-3) = -2(r-3) < 0  →  ESTABLE (para r>3)")
print("\n⚡ BIFURCACIÓN: HORQUILLA SUPERCRÍTICA en r_c = 3")
print("   El punto fijo estable x*=0 se vuelve inestable y nacen dos ramas estables")

def sistema11(x, r): return (r - 3)*x - x**3
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [1, 2, 3, 4, 5]:
    print(f"\n   r = {r:6.2f}:")
    if r > 3:
        print(f"      Teórico: x* = 0, x* = ±{np.sqrt(r-3):.4f}")
    else:
        print(f"      Teórico: x* = 0")
    puntos = encontrar_puntos_fijos(sistema11, r, x_range=(-3, 3))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema11, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 12: ẋ = r - (x-2)²")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   r - (x-2)² = 0")
print("   (x-2)² = r")
print("   x-2 = ±√r")
print("   x* = 2 ± √r")
print("\n📍 EXISTENCIA:")
print("   • Para r < 0: No hay puntos fijos reales")
print("   • Para r = 0: Un punto fijo: x* = 2")
print("   • Para r > 0: Dos puntos fijos: x* = 2-√r y x* = 2+√r")
print("\n🔍 ESTABILIDAD (f'(x*) = -2(x*-2)):")
print("   • x* = 2-√r: f'(x*) = -2(-√r) = 2√r > 0  →  INESTABLE")
print("   • x* = 2+√r: f'(x*) = -2(√r) = -2√r < 0  →  ESTABLE")
print("\n⚡ BIFURCACIÓN: SILLA-NODO en r_c = 0")
print("   Los dos puntos fijos nacen en r=0 en x*=2")

def sistema12(x, r): return r - (x - 2)**2
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-0.5, 0, 0.5, 1, 2]:
    print(f"\n   r = {r:6.2f}:")
    if r > 0:
        x1_teorico = 2 - np.sqrt(r)
        x2_teorico = 2 + np.sqrt(r)
        print(f"      Teórico: x* = {x1_teorico:.4f}, x* = {x2_teorico:.4f}")
    elif r == 0:
        print(f"      Teórico: x* = 2.0000")
    else:
        print(f"      Teórico: No hay puntos fijos")
    puntos = encontrar_puntos_fijos(sistema12, r, x_range=(0, 4))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema12, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 13: ẋ = (r-1)(x-1) - (x-1)²")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   (r-1)(x-1) - (x-1)² = 0")
print("   (x-1)[(r-1) - (x-1)] = 0")
print("   x-1 = 0  ó  x-1 = r-1")
print("   x* = 1  ó  x* = r")
print("\n📍 EXISTENCIA:")
print("   • Para todo r: Dos puntos fijos: x* = 1 y x* = r")
print("\n🔍 ESTABILIDAD (f'(x*) = (r-1) - 2(x*-1)):")
print("   • x* = 1: f'(1) = (r-1) - 0 = r-1")
print("     - Si r < 1 → f'(1) < 0 → ESTABLE")
print("     - Si r > 1 → f'(1) > 0 → INESTABLE")
print("   • x* = r: f'(r) = (r-1) - 2(r-1) = -(r-1)")
print("     - Si r < 1 → f'(r) > 0 → INESTABLE")
print("     - Si r > 1 → f'(r) < 0 → ESTABLE")
print("\n⚡ BIFURCACIÓN: TRANSCRÍTICA en r_c = 1")
print("   Los dos puntos fijos intercambian estabilidad en r=1")

def sistema13(x, r): return (r - 1)*(x - 1) - (x - 1)**2
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [-1, 0, 1, 2, 3]:
    print(f"\n   r = {r:6.2f}:")
    print(f"      Teórico: x* = 1, x* = {r:.4f}")
    puntos = encontrar_puntos_fijos(sistema13, r, x_range=(-1, 5))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema13, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

# ======================================================================================
print("\n\n" + "="*90)
print("SISTEMA 14: ẋ = rx(1-x/k) - h  (con k=2, h=0.5)")
print("="*90)
print("\n📐 PUNTOS DE EQUILIBRIO:")
print("   rx(1-x/k) - h = 0")
print("   rx - rx²/k - h = 0")
print("   Multiplicando por k: krx - rx² - kh = 0")
print("   rx² - krx + kh = 0")
print("   x* = [kr ± √((kr)² - 4rkh)] / (2r)")
print("   x* = [kr ± √(k²r² - 4rkh)] / (2r)")
print("   x* = k/2 ± √(k²/4 - kh/r)")
print("\n   Con k=2, h=0.5:")
print("   x* = 1 ± √(1 - 1/r)")
print("\n📍 EXISTENCIA:")
print("   • Para r < 1: No hay puntos fijos reales (discriminante negativo)")
print("   • Para r = 1: Un punto fijo: x* = 1")
print("   • Para r > 1: Dos puntos fijos: x* = 1 - √(1-1/r) y x* = 1 + √(1-1/r)")
print("\n🔍 ESTABILIDAD (f'(x*) = r(1 - 2x*/k)):")
print("   Con k=2: f'(x*) = r(1 - x*)")
print("   El punto fijo mayor es estable, el menor es inestable")
print("\n⚡ BIFURCACIÓN: SILLA-NODO en r_c = 1")
print("   Modelo logístico con cosecha constante")

def sistema14(x, r, k=2, h=0.5): return r*x*(1 - x/k) - h
print("\n📊 VERIFICACIÓN NUMÉRICA:")
for r in [0.5, 1, 1.5, 2, 3, 4]:
    print(f"\n   r = {r:6.2f}:")
    if r > 1:
        discriminante = 1 - 1/r
        if discriminante >= 0:
            x1_teorico = 1 - np.sqrt(discriminante)
            x2_teorico = 1 + np.sqrt(discriminante)
            print(f"      Teórico: x* = {x1_teorico:.4f}, x* = {x2_teorico:.4f}")
    elif r == 1:
        print(f"      Teórico: x* = 1.0000")
    else:
        print(f"      Teórico: No hay puntos fijos")
    puntos = encontrar_puntos_fijos(sistema14, r, x_range=(-1, 4))
    for p in puntos:
        es_estable, deriv = estabilidad(sistema14, p, r)
        print(f"      Numérico: x* = {p:7.4f}  ({'ESTABLE' if es_estable else 'INESTABLE':9s})  f'(x*) = {deriv:7.4f}")

print("\n" + "="*90)
print("FIN DEL ANÁLISIS COMPLETO")
print("="*90)
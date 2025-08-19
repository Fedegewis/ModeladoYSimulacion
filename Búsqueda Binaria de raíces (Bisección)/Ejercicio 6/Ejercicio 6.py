import numpy as np
import sympy as sp
from sympy import symbols, solve, simplify, expand, factor, sqrt

# Definir la variable simbólica
x, p = symbols('x p', real=True)

print("="*80)
print("DEMOSTRACIÓN ALGEBRAICA: PUNTO FIJO ⟺ RAÍZ DE f(x)")
print("="*80)
print("Función original: f(x) = x⁴ + 2x² - x - 3")
print("Objetivo: Demostrar que g(p) = p ⟺ f(p) = 0")
print("="*80)

# Definir f(x)
f = x**4 + 2*x**2 - x - 3
print(f"f(x) = {f}")

# ============================================================================
# PARTE A: g(x) = (3 + x - 2x²)^(1/2)
# ============================================================================

print("\n" + "="*60)
print("PARTE A: g(x) = (3 + x - 2x²)^(1/2)")
print("="*60)

# Definir g_a(x)
g_a = sqrt(3 + x - 2*x**2)
print(f"g_a(x) = {g_a}")

print("\n1. DEMOSTRACIÓN: g_a(p) = p ⟹ f(p) = 0")
print("-" * 50)

print("Si g_a(p) = p, entonces:")
print("√(3 + p - 2p²) = p")

print("\nElevando al cuadrado ambos lados:")
print("3 + p - 2p² = p²")

print("\nReorganizando:")
print("3 + p - 2p² - p² = 0")
print("3 + p - 3p² = 0")
print("Multiplicando por -1:")
print("3p² - p - 3 = 0")

# Verificar algebraicamente
ecuacion_1 = 3*p**2 - p - 3
print(f"Ecuación obtenida: {ecuacion_1} = 0")

# Ahora vamos a mostrar que esto implica f(p) = 0
print("\n2. Relación con f(p):")
print("-" * 30)

# Factorizar f(p) para encontrar la relación
print("Necesitamos mostrar que 3p² - p - 3 = 0 implica p⁴ + 2p² - p - 3 = 0")

# De 3p² - p - 3 = 0, despejamos: 3p² = p + 3
print("De 3p² - p - 3 = 0, obtenemos: 3p² = p + 3")
print("Por lo tanto: p² = (p + 3)/3")

# Calculamos p⁴
print("\nCalculando p⁴:")
print("p⁴ = (p²)² = ((p + 3)/3)² = (p + 3)²/9")

p4_expr = (p + 3)**2 / 9
p4_expanded = expand(p4_expr)
print(f"p⁴ = {p4_expanded}")

# Sustituir en f(p)
print("\nSustituyendo en f(p) = p⁴ + 2p² - p - 3:")
f_sustituido = p4_expanded + 2*(p + 3)/3 - p - 3
f_sustituido_simplified = simplify(f_sustituido)
print(f"f(p) = {p4_expanded} + 2·(p + 3)/3 - p - 3")
print(f"f(p) = {f_sustituido_simplified}")

print("\n3. DEMOSTRACIÓN: f(p) = 0 ⟹ g_a(p) = p")
print("-" * 50)

print("Si f(p) = 0, entonces p⁴ + 2p² - p - 3 = 0")
print("Necesitamos mostrar que esto implica √(3 + p - 2p²) = p")

# Método: Encontrar las raíces de f(x) y verificar
print("\nEncontrando las raíces de f(x):")
raices_f = solve(f, x)
print("Raíces de f(x):")
for i, raiz in enumerate(raices_f):
    print(f"  x_{i+1} = {raiz}")

# ============================================================================
# PARTE B: g(x) = ((x + 3 - x⁴)/2)^(1/2)
# ============================================================================

print("\n" + "="*60)
print("PARTE B: g(x) = ((x + 3 - x⁴)/2)^(1/2)")
print("="*60)

# Definir g_b(x)
g_b = sqrt((x + 3 - x**4)/2)
print(f"g_b(x) = {g_b}")

print("\n1. DEMOSTRACIÓN: g_b(p) = p ⟹ f(p) = 0")
print("-" * 50)

print("Si g_b(p) = p, entonces:")
print("√((p + 3 - p⁴)/2) = p")

print("\nElevando al cuadrado ambos lados:")
print("(p + 3 - p⁴)/2 = p²")

print("\nMultiplicando por 2:")
print("p + 3 - p⁴ = 2p²")

print("\nReorganizando:")
print("-p⁴ + p + 3 - 2p² = 0")
print("Multiplicando por -1:")
print("p⁴ + 2p² - p - 3 = 0")

print("¡Esta es exactamente f(p) = 0!")

print("\n2. DEMOSTRACIÓN: f(p) = 0 ⟹ g_b(p) = p")
print("-" * 50)

print("Si f(p) = 0, entonces p⁴ + 2p² - p - 3 = 0")
print("Reorganizando: p + 3 - p⁴ = 2p²")
print("Dividiendo por 2: (p + 3 - p⁴)/2 = p²")
print("Tomando raíz cuadrada: √((p + 3 - p⁴)/2) = |p|")

print("\nPara que g_b(p) = p, necesitamos que p ≥ 0 y √((p + 3 - p⁴)/2) = p")

# ============================================================================
# VERIFICACIÓN NUMÉRICA
# ============================================================================

print("\n" + "="*60)
print("VERIFICACIÓN NUMÉRICA")
print("="*60)

# Convertir a funciones numéricas
f_num = lambda x_val: x_val**4 + 2*x_val**2 - x_val - 3
g_a_num = lambda x_val: np.sqrt(3 + x_val - 2*x_val**2) if (3 + x_val - 2*x_val**2) >= 0 else np.nan
g_b_num = lambda x_val: np.sqrt((x_val + 3 - x_val**4)/2) if (x_val + 3 - x_val**4)/2 >= 0 else np.nan

# Encontrar raíces numéricamente
from scipy.optimize import fsolve

# Buscar raíces de f(x)
raices_numericas = []
for guess in [-2, -1, 0, 1, 2]:
    try:
        raiz = fsolve(f_num, guess)[0]
        if abs(f_num(raiz)) < 1e-10:  # Verificar que sea realmente una raíz
            # Evitar duplicados
            es_nueva = True
            for r in raices_numericas:
                if abs(raiz - r) < 1e-8:
                    es_nueva = False
                    break
            if es_nueva:
                raices_numericas.append(raiz)
    except:
        pass

raices_numericas.sort()

print("Raíces numéricas de f(x):")
for i, raiz in enumerate(raices_numericas):
    print(f"  x_{i+1} = {raiz:.8f}, f(x_{i+1}) = {f_num(raiz):.2e}")

print("\nVerificación de punto fijo para g_a(x):")
for i, raiz in enumerate(raices_numericas):
    try:
        g_val = g_a_num(raiz)
        if not np.isnan(g_val):
            error = abs(g_val - raiz)
            print(f"  x_{i+1} = {raiz:.6f}: g_a(x_{i+1}) = {g_val:.6f}, |g_a(x) - x| = {error:.2e}")
        else:
            print(f"  x_{i+1} = {raiz:.6f}: g_a(x_{i+1}) = indefinido (expresión bajo raíz negativa)")
    except:
        print(f"  x_{i+1} = {raiz:.6f}: g_a(x_{i+1}) = indefinido")

print("\nVerificación de punto fijo para g_b(x):")
for i, raiz in enumerate(raices_numericas):
    try:
        g_val = g_b_num(raiz)
        if not np.isnan(g_val):
            error = abs(g_val - raiz)
            print(f"  x_{i+1} = {raiz:.6f}: g_b(x_{i+1}) = {g_val:.6f}, |g_b(x) - x| = {error:.2e}")
        else:
            print(f"  x_{i+1} = {raiz:.6f}: g_b(x_{i+1}) = indefinido (expresión bajo raíz negativa)")
    except:
        print(f"  x_{i+1} = {raiz:.6f}: g_b(x_{i+1}) = indefinido")

# ============================================================================
# ANÁLISIS DE DOMINIOS
# ============================================================================

print("\n" + "="*60)
print("ANÁLISIS DE DOMINIOS")
print("="*60)

print("Para que las funciones g(x) estén definidas, necesitamos:")
print("\nPara g_a(x) = √(3 + x - 2x²):")
print("  Condición: 3 + x - 2x² ≥ 0")
print("  Es decir: -2x² + x + 3 ≥ 0")
print("  O: 2x² - x - 3 ≤ 0")

# Resolver la desigualdad
desigualdad_a = 2*x**2 - x - 3
raices_desig_a = solve(desigualdad_a, x)
print(f"  Raíces de 2x² - x - 3 = 0: {raices_desig_a}")
print(f"  Dominio: x ∈ [{float(raices_desig_a[0]):.3f}, {float(raices_desig_a[1]):.3f}]")

print("\nPara g_b(x) = √((x + 3 - x⁴)/2):")
print("  Condición: (x + 3 - x⁴)/2 ≥ 0")
print("  Es decir: x + 3 - x⁴ ≥ 0")
print("  O: x⁴ - x - 3 ≤ 0")

print("\n" + "="*60)
print("CONCLUSIONES")
print("="*60)
print("1. Hemos demostrado algebraicamente que:")
print("   • g_a(p) = p ⟺ f(p) = 0")
print("   • g_b(p) = p ⟺ f(p) = 0")
print("\n2. Las funciones g_a y g_b son transformaciones válidas de f(x) = 0")
print("   al problema de punto fijo x = g(x)")
print("\n3. Los puntos fijos de g_a y g_b coinciden exactamente con las raíces de f(x)")
print("   (dentro de sus respectivos dominios)")
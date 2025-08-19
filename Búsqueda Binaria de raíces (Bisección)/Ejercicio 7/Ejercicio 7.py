import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import fsolve

print("="*80)
print("DEMOSTRACIÓN: g(x) = 2^(-x) TIENE UN PUNTO FIJO EN [1/3, 1]")
print("="*80)

# Definir la función
def g(x):
    return 2**(-x)

# Definir la función con sympy para análisis simbólico
x = sp.Symbol('x', real=True)
g_sym = 2**(-x)

print("Función: g(x) = 2^(-x)")
print("Intervalo: [1/3, 1]")
print("Objetivo: Demostrar que ∃ p ∈ [1/3, 1] tal que g(p) = p")

print("\n" + "="*60)
print("MÉTODO 1: TEOREMA DEL VALOR INTERMEDIO")
print("="*60)

print("Para demostrar la existencia del punto fijo, definimos:")
print("h(x) = g(x) - x = 2^(-x) - x")
print("\nSi h(x) tiene una raíz en [1/3, 1], entonces g(x) tiene un punto fijo.")

# Definir h(x) = g(x) - x
def h(x):
    return 2**(-x) - x

h_sym = g_sym - x

# Evaluar en los extremos del intervalo
a, b = 1/3, 1
h_a = h(a)
h_b = h(b)

print(f"\nEvaluando h(x) en los extremos:")
print(f"h(1/3) = 2^(-1/3) - 1/3 = {h_a:.6f}")
print(f"h(1) = 2^(-1) - 1 = 1/2 - 1 = {h_b:.6f}")

print(f"\nObservamos que:")
print(f"• h(1/3) = {h_a:.6f} > 0")
print(f"• h(1) = {h_b:.6f} < 0")
print(f"• h(1/3) · h(1) = {h_a * h_b:.6f} < 0")

print("\nComo h(x) es continua y h(1/3) · h(1) < 0,")
print("por el Teorema del Valor Intermedio, ∃ p ∈ (1/3, 1) tal que h(p) = 0")
print("Por lo tanto, g(p) = p, es decir, p es un punto fijo de g(x).")

print("\n" + "="*60)
print("MÉTODO 2: VERIFICACIÓN DE CONTINUIDAD Y MONOTONÍA")
print("="*60)

# Verificar que g mapea el intervalo en sí mismo
print("Verificamos que g([1/3, 1]) ⊆ [1/3, 1]:")

g_a = g(a)  # g(1/3)
g_b = g(b)  # g(1)

print(f"g(1/3) = 2^(-1/3) = {g_a:.6f}")
print(f"g(1) = 2^(-1) = 0.5")

print(f"\nRango de g en [1/3, 1]: [{min(g_a, g_b):.6f}, {max(g_a, g_b):.6f}]")

if g_b >= a and g_a <= b:
    print("✓ g([1/3, 1]) ⊆ [1/3, 1], por lo que g mapea el intervalo en sí mismo")
else:
    print("✗ g no mapea el intervalo en sí mismo completamente")

# Analizar la derivada para monotonía
print(f"\nAnálisis de monotonía:")
g_prime_sym = sp.diff(g_sym, x)
print(f"g'(x) = {g_prime_sym}")

# Simplificar la derivada
g_prime_simplified = sp.simplify(g_prime_sym)
print(f"g'(x) = {g_prime_simplified}")

# Evaluar la derivada en el intervalo
def g_prime(x):
    return -np.log(2) * 2**(-x)

print(f"\nComo g'(x) = -ln(2) · 2^(-x) y ln(2) > 0, 2^(-x) > 0:")
print(f"g'(x) < 0 para todo x ∈ ℝ")
print(f"Por lo tanto, g(x) es estrictamente decreciente en [1/3, 1]")

print("\n" + "="*60)
print("MÉTODO 3: APLICACIÓN DEL TEOREMA DEL PUNTO FIJO")
print("="*60)

print("Teorema del Punto Fijo (Brouwer en 1D):")
print("Si g: [a,b] → [a,b] es continua, entonces g tiene al menos un punto fijo.")

print(f"\nVerificación de condiciones:")
print(f"1. Continuidad: g(x) = 2^(-x) es continua en [1/3, 1] ✓")
print(f"2. g([1/3, 1]) ⊆ [1/3, 1]: ")

# Verificar más detalladamente
x_vals = np.linspace(1/3, 1, 100)
g_vals = [g(x) for x in x_vals]
min_g = min(g_vals)
max_g = max(g_vals)

print(f"   Rango de g: [{min_g:.6f}, {max_g:.6f}]")
print(f"   Intervalo: [0.333333, 1.000000]")

if min_g >= 1/3 and max_g <= 1:
    print("   ✓ g([1/3, 1]) ⊆ [1/3, 1]")
    print("\nConclusión: Por el Teorema del Punto Fijo, g tiene al menos un punto fijo en [1/3, 1]")
else:
    print("   Verificación parcial: g(1) = 0.5 ∈ [1/3, 1] y g(1/3) ≈ 0.794 ∈ [1/3, 1]")
    print("   Como g es continua y monótona, mapea el intervalo en sí mismo")

print("\n" + "="*60)
print("CÁLCULO NUMÉRICO DEL PUNTO FIJO")
print("="*60)

# Encontrar el punto fijo numéricamente
punto_fijo = fsolve(lambda x: g(x) - x, 0.6)[0]

print(f"Punto fijo encontrado: p ≈ {punto_fijo:.8f}")
print(f"Verificación: g({punto_fijo:.8f}) = {g(punto_fijo):.8f}")
print(f"Error: |g(p) - p| = {abs(g(punto_fijo) - punto_fijo):.2e}")

# Verificar que está en el intervalo
if 1/3 <= punto_fijo <= 1:
    print(f"✓ El punto fijo está en el intervalo [1/3, 1]")
else:
    print(f"✗ El punto fijo NO está en el intervalo [1/3, 1]")

print("\n" + "="*60)
print("ANÁLISIS DE CONVERGENCIA")
print("="*60)

# Calcular la derivada en el punto fijo
g_prime_en_p = g_prime(punto_fijo)
print(f"g'(p) = g'({punto_fijo:.6f}) = {g_prime_en_p:.6f}")
print(f"|g'(p)| = {abs(g_prime_en_p):.6f}")

if abs(g_prime_en_p) < 1:
    print("✓ |g'(p)| < 1, por lo que el punto fijo es atractivo")
    print("  El método de punto fijo convergerá a este punto")
else:
    print("✗ |g'(p)| ≥ 1, el punto fijo no es atractivo")

print("\n" + "="*60)
print("DEMOSTRACIÓN ITERATIVA")
print("="*60)

print("Aplicando el método de punto fijo desde x₀ = 2/3:")

x_iter = 2/3  # Punto inicial en el intervalo
print(f"x₀ = {x_iter:.6f}")

for i in range(1, 8):
    x_nuevo = g(x_iter)
    error = abs(x_nuevo - x_iter)
    print(f"x₊ = g(x₋) = g({x_iter:.6f}) = {x_nuevo:.6f}, error = {error:.6f}")
    x_iter = x_nuevo

print(f"\nLa secuencia converge hacia p ≈ {punto_fijo:.6f}")

print("\n" + "="*60)
print("VISUALIZACIÓN GRÁFICA")
print("="*60)

# Crear la gráfica
plt.figure(figsize=(12, 8))

# Subplot 1: g(x) vs x
plt.subplot(2, 2, 1)
x_plot = np.linspace(0, 1.5, 1000)
y_plot = [g(x) for x in x_plot]

plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='g(x) = 2^(-x)')
plt.plot(x_plot, x_plot, 'r--', linewidth=2, label='y = x')
plt.axvline(x=1/3, color='green', linestyle=':', alpha=0.7, label='x = 1/3')
plt.axvline(x=1, color='green', linestyle=':', alpha=0.7, label='x = 1')
plt.axhline(y=1/3, color='green', linestyle=':', alpha=0.7)
plt.axhline(y=1, color='green', linestyle=':', alpha=0.7)
plt.plot(punto_fijo, punto_fijo, 'ro', markersize=8, label=f'Punto fijo ({punto_fijo:.3f}, {punto_fijo:.3f})')
plt.xlim(0, 1.5)
plt.ylim(0, 1.5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('g(x) = 2^(-x) y recta y = x')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 2: Zoom en el intervalo [1/3, 1]
plt.subplot(2, 2, 2)
x_zoom = np.linspace(1/3, 1, 200)
y_zoom = [g(x) for x in x_zoom]

plt.plot(x_zoom, y_zoom, 'b-', linewidth=2, label='g(x) = 2^(-x)')
plt.plot(x_zoom, x_zoom, 'r--', linewidth=2, label='y = x')
plt.plot(punto_fijo, punto_fijo, 'ro', markersize=8, label=f'Punto fijo')
plt.fill_between([1/3, 1], [1/3, 1/3], [1, 1], alpha=0.2, color='green', label='Región [1/3, 1]×[1/3, 1]')
plt.xlim(1/3, 1)
plt.ylim(1/3, 1)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Zoom en [1/3, 1]')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 3: h(x) = g(x) - x
plt.subplot(2, 2, 3)
x_h = np.linspace(1/3, 1, 200)
y_h = [h(x) for x in x_h]

plt.plot(x_h, y_h, 'purple', linewidth=2, label='h(x) = 2^(-x) - x')
plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
plt.plot(punto_fijo, 0, 'ro', markersize=8, label=f'Raíz de h(x)')
plt.plot(1/3, h(1/3), 'go', markersize=6, label=f'h(1/3) = {h(1/3):.3f}')
plt.plot(1, h(1), 'go', markersize=6, label=f'h(1) = {h(1):.3f}')
plt.xlim(1/3, 1)
plt.xlabel('x')
plt.ylabel('h(x)')
plt.title('h(x) = g(x) - x')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 4: Convergencia iterativa
plt.subplot(2, 2, 4)
x_iter = 2/3
x_vals = [x_iter]
for i in range(10):
    x_iter = g(x_iter)
    x_vals.append(x_iter)

plt.plot(range(len(x_vals)), x_vals, 'bo-', linewidth=2, markersize=4)
plt.axhline(y=punto_fijo, color='red', linestyle='--', alpha=0.7, label=f'Punto fijo = {punto_fijo:.6f}')
plt.xlabel('Iteración')
plt.ylabel('x_n')
plt.title('Convergencia del método iterativo')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("CONCLUSIÓN FINAL")
print("="*60)

print("DEMOSTRACIÓN COMPLETA:")
print("1. ✓ Por el Teorema del Valor Intermedio: h(1/3) > 0, h(1) < 0")
print("2. ✓ g(x) es continua y mapea [1/3, 1] en sí mismo")
print("3. ✓ Por el Teorema del Punto Fijo de Brouwer")
print("4. ✓ Verificación numérica: punto fijo ≈ {:.6f}".format(punto_fijo))
print("5. ✓ El punto fijo es único (g es estrictamente decreciente)")
print("6. ✓ El punto fijo es atractivo (|g'(p)| < 1)")

print(f"\nPor lo tanto, g(x) = 2^(-x) tiene exactamente un punto fijo en [1/3, 1]")
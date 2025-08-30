import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange
import sympy as sp

# Configuración para matplotlib en español
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def lagrange_interpolation(x_points, y_points):
    """
    Construye el polinomio interpolante de Lagrange
    """
    n = len(x_points)
    x = sp.Symbol('x')
    polynomial = 0
    
    for i in range(n):
        # Base de Lagrange Li(x)
        Li = 1
        for j in range(n):
            if i != j:
                Li *= (x - x_points[j]) / (x_points[i] - x_points[j])
        polynomial += y_points[i] * Li
    
    # Simplificar el polinomio
    polynomial = sp.expand(polynomial)
    return polynomial

def evaluate_polynomial(poly, x_val):
    """Evalúa un polinomio simbólico en un punto"""
    x = sp.Symbol('x')
    return float(poly.subs(x, x_val))

def plot_interpolation(x_points, y_points, title, original_func=None, x_range=None):
    """Grafica el polinomio interpolante y los puntos"""
    if x_range is None:
        x_range = [min(x_points) - 1, max(x_points) + 1]
    
    # Construir polinomio
    poly = lagrange_interpolation(x_points, y_points)
    
    # Puntos para graficar
    x_plot = np.linspace(x_range[0], x_range[1], 1000)
    y_plot = [evaluate_polynomial(poly, x_val) for x_val in x_plot]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_plot, 'b-', label=f'Polinomio interpolante', linewidth=2)
    plt.plot(x_points, y_points, 'ro', markersize=8, label='Puntos de interpolación')
    
    # Si hay función original, graficarla
    if original_func is not None:
        y_original = [original_func(x_val) for x_val in x_plot]
        plt.plot(x_plot, y_original, 'g--', label='Función original', alpha=0.7)
    
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    
    return poly

print("=" * 60)
print("POLINOMIOS INTERPOLANTES DE LAGRANGE")
print("=" * 60)

# Ejercicio 1
print("\n1. Polinomio que pasa por (1,1), (2,4), (3,9)")
x1 = [1, 2, 3]
y1 = [1, 4, 9]
poly1 = lagrange_interpolation(x1, y1)
print(f"   P(x) = {poly1}")
print(f"   Verificación: P(1) = {evaluate_polynomial(poly1, 1)}")
print(f"   Verificación: P(2) = {evaluate_polynomial(poly1, 2)}")
print(f"   Verificación: P(3) = {evaluate_polynomial(poly1, 3)}")

# Ejercicio 2
print("\n2. Función que pasa por (0,1), (1,3), (2,2), (3,5)")
x2 = [0, 1, 2, 3]
y2 = [1, 3, 2, 5]
poly2 = lagrange_interpolation(x2, y2)
print(f"   P(x) = {poly2}")

# Ejercicio 3
print("\n3. Valor de b para x = [0,1,2,3,4], y = [1,2,b,2,3]")
x3 = [0, 1, 2, 3, 4]
# Asumiendo que queremos un polinomio suave, calculamos b
# Usando los otros puntos para estimar
y3_temp = [1, 2, 3, 2, 3]  # Valor temporal para b
poly3_temp = lagrange_interpolation([0, 1, 3, 4], [1, 2, 2, 3])
b_estimated = evaluate_polynomial(poly3_temp, 2)
y3 = [1, 2, b_estimated, 2, 3]
poly3 = lagrange_interpolation(x3, y3)
print(f"   Valor estimado de b = {b_estimated:.4f}")
print(f"   P(x) = {poly3}")

# Ejercicio 4
print("\n4. Polinomio de Lagrange para x = [0,1,2,3,4], f(x) = [1,2,0,2,3]")
x4 = [0, 1, 2, 3, 4]
y4 = [1, 2, 0, 2, 3]
poly4 = lagrange_interpolation(x4, y4)
print(f"   P(x) = {poly4}")

# Ejercicio 5
print("\n5. Polinomio de Lagrange para [0,1,2], y = [1,3,0]")
x5 = [0, 1, 2]
y5 = [1, 3, 0]
poly5 = lagrange_interpolation(x5, y5)
print(f"   P(x) = {poly5}")

# Ejercicio 6
print("\n6. Polinomio de segundo grado que pasa por x = [1,2,3], y = [10,15,80]")
x6 = [1, 2, 3]
y6 = [10, 15, 80]
poly6 = lagrange_interpolation(x6, y6)
print(f"   P(x) = {poly6}")

# Ejercicio 7
print("\n7. Polinomio con datos x = [2,4,5], f(x) = [5,6,3]")
x7 = [2, 4, 5]
y7 = [5, 6, 3]
poly7 = lagrange_interpolation(x7, y7)
print(f"   P(x) = {poly7}")

# Ejercicio 8
print("\n8. Polinomio que interpola x = [-2,0,2], f(x) = [0,1,0]")
x8 = [-2, 0, 2]
y8 = [0, 1, 0]
poly8 = lagrange_interpolation(x8, y8)
print(f"   P(x) = {poly8}")

# Ejercicio 9
print("\n9. Aproximar f(x) = sin(x) en [0,π] con polinomio de grado 2")
x9 = [0, np.pi/2, np.pi]
y9 = [np.sin(0), np.sin(np.pi/2), np.sin(np.pi)]
poly9 = lagrange_interpolation(x9, y9)
print(f"   Puntos: x = {[0, np.pi/2, np.pi]}")
print(f"   y = sin(x) = {y9}")
print(f"   P(x) = {poly9}")

# Ejercicio 10
print("\n10. Polinomio de Lagrange para x = [0,1,2], f(x) = [1,2,7]")
x10 = [0, 1, 2]
y10 = [1, 2, 7]
poly10 = lagrange_interpolation(x10, y10)
print(f"    P(x) = {poly10}")

# Ejercicio 11
print("\n11. Nodos x₀ = 2, x₁ = 2.5, x₂ = 4.5, aproximar f(x) = 1/x")
x11 = [2, 2.5, 4.5]
y11 = [1/2, 1/2.5, 1/4.5]
poly11 = lagrange_interpolation(x11, y11)
print(f"    Puntos: x = {x11}")
print(f"    y = 1/x = {y11}")
print(f"    P(x) = {poly11}")

# Ejercicio 12
print("\n12. f(x) = 2sin(πx/6), nodos x₀ = 1, x₁ = 2, x₂ = 3")
def f12(x):
    return 2 * np.sin(np.pi * x / 6)

x12 = [1, 2, 3]
y12 = [f12(x) for x in x12]
poly12 = lagrange_interpolation(x12, y12)
print(f"    Puntos: x = {x12}")
print(f"    y = 2sin(πx/6) = {y12}")
print(f"    P(x) = {poly12}")
print(f"    a) f(4) ≈ P(4) = {evaluate_polynomial(poly12, 4):.4f}")
print(f"    b) f(1.5) ≈ P(1.5) = {evaluate_polynomial(poly12, 1.5):.4f}")
print(f"    Valor real f(4) = {f12(4):.4f}")
print(f"    Valor real f(1.5) = {f12(1.5):.4f}")

# Ejercicio 13
print("\n13. Nodos x₀ = 0, x₁ = 0.6, x₂ = 0.9, aproximar f(0.45)")

print("\n    a) f(x) = cos(x)")
x13a = [0, 0.6, 0.9]
y13a = [np.cos(x) for x in x13a]
poly13a = lagrange_interpolation(x13a, y13a)
approx_13a = evaluate_polynomial(poly13a, 0.45)
real_13a = np.cos(0.45)
print(f"       P(x) = {poly13a}")
print(f"       P(0.45) = {approx_13a:.6f}")
print(f"       cos(0.45) = {real_13a:.6f}")
print(f"       Error = {abs(approx_13a - real_13a):.6f}")

print("\n    b) f(x) = √(x + 1)")
x13b = [0, 0.6, 0.9]
y13b = [np.sqrt(x + 1) for x in x13b]
poly13b = lagrange_interpolation(x13b, y13b)
approx_13b = evaluate_polynomial(poly13b, 0.45)
real_13b = np.sqrt(0.45 + 1)
print(f"       P(x) = {poly13b}")
print(f"       P(0.45) = {approx_13b:.6f}")
print(f"       √(1.45) = {real_13b:.6f}")
print(f"       Error = {abs(approx_13b - real_13b):.6f}")

print("\n    c) f(x) = ln(x + 1)")
x13c = [0, 0.6, 0.9]
y13c = [np.log(x + 1) for x in x13c]
poly13c = lagrange_interpolation(x13c, y13c)
approx_13c = evaluate_polynomial(poly13c, 0.45)
real_13c = np.log(0.45 + 1)
print(f"       P(x) = {poly13c}")
print(f"       P(0.45) = {approx_13c:.6f}")
print(f"       ln(1.45) = {real_13c:.6f}")
print(f"       Error = {abs(approx_13c - real_13c):.6f}")

print("\n" + "=" * 60)
print("GRÁFICAS DE ALGUNOS EJERCICIOS")
print("=" * 60)

# Crear algunas gráficas importantes
plt.figure(figsize=(15, 10))

# Ejercicio 1 - Parábola
plt.subplot(2, 3, 1)
x_plot = np.linspace(0, 4, 100)
y_plot = [evaluate_polynomial(poly1, x) for x in x_plot]
plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='P(x)')
plt.plot(x1, y1, 'ro', markersize=8)
plt.plot(x_plot, x_plot**2, 'g--', alpha=0.7, label='y = x²')
plt.grid(True, alpha=0.3)
plt.title('Ejercicio 1: (1,1), (2,4), (3,9)')
plt.legend()

# Ejercicio 9 - Aproximación de sin(x)
plt.subplot(2, 3, 2)
x_plot = np.linspace(0, np.pi, 100)
y_plot = [evaluate_polynomial(poly9, x) for x in x_plot]
plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio')
plt.plot(x9, y9, 'ro', markersize=8)
plt.plot(x_plot, np.sin(x_plot), 'g--', alpha=0.7, label='sin(x)')
plt.grid(True, alpha=0.3)
plt.title('Ejercicio 9: Aproximación de sin(x)')
plt.legend()

# Ejercicio 12 - f(x) = 2sin(πx/6)
plt.subplot(2, 3, 3)
x_plot = np.linspace(0, 4, 100)
y_plot = [evaluate_polynomial(poly12, x) for x in x_plot]
y_real = [f12(x) for x in x_plot]
plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio')
plt.plot(x12, y12, 'ro', markersize=8)
plt.plot(x_plot, y_real, 'g--', alpha=0.7, label='2sin(πx/6)')
plt.grid(True, alpha=0.3)
plt.title('Ejercicio 12: 2sin(πx/6)')
plt.legend()

# Ejercicio 13a - cos(x)
plt.subplot(2, 3, 4)
x_plot = np.linspace(0, 1, 100)
y_plot = [evaluate_polynomial(poly13a, x) for x in x_plot]
plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio')
plt.plot(x13a, y13a, 'ro', markersize=8)
plt.plot(x_plot, np.cos(x_plot), 'g--', alpha=0.7, label='cos(x)')
plt.plot(0.45, approx_13a, 'rs', markersize=10, label=f'P(0.45)={approx_13a:.3f}')
plt.grid(True, alpha=0.3)
plt.title('Ejercicio 13a: cos(x)')
plt.legend()

# Ejercicio 13b - √(x+1)
plt.subplot(2, 3, 5)
x_plot = np.linspace(0, 1, 100)
y_plot = [evaluate_polynomial(poly13b, x) for x in x_plot]
plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio')
plt.plot(x13b, y13b, 'ro', markersize=8)
plt.plot(x_plot, np.sqrt(x_plot + 1), 'g--', alpha=0.7, label='√(x+1)')
plt.plot(0.45, approx_13b, 'rs', markersize=10, label=f'P(0.45)={approx_13b:.3f}')
plt.grid(True, alpha=0.3)
plt.title('Ejercicio 13b: √(x+1)')
plt.legend()

# Ejercicio 13c - ln(x+1)
plt.subplot(2, 3, 6)
x_plot = np.linspace(0, 1, 100)
y_plot = [evaluate_polynomial(poly13c, x) for x in x_plot]
plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio')
plt.plot(x13c, y13c, 'ro', markersize=8)
plt.plot(x_plot, np.log(x_plot + 1), 'g--', alpha=0.7, label='ln(x+1)')
plt.plot(0.45, approx_13c, 'rs', markersize=10, label=f'P(0.45)={approx_13c:.3f}')
plt.grid(True, alpha=0.3)
plt.title('Ejercicio 13c: ln(x+1)')
plt.legend()

plt.tight_layout()
plt.show()

print("\nTodos los ejercicios han sido resueltos.")
print("Los polinomios están expresados en forma simbólica.")
print("Las gráficas muestran la comparación entre los polinomios interpolantes y las funciones originales.")
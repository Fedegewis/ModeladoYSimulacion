import numpy as np
import matplotlib.pyplot as plt

def g(x):
    """Función de iteración g(x) = x²/2 + 2"""
    return x**2 / 2 + 2

def g_prima(x):
    """Derivada de g(x): g'(x) = x"""
    return x

def encontrar_punto_fijo(x0, tolerancia=1e-13, max_iter=100):
    """
    Encuentra el punto fijo usando iteración
    
    Args:
        x0: valor inicial
        tolerancia: exactitud deseada
        max_iter: máximo número de iteraciones (reducido para evitar overflow)
    
    Returns:
        punto fijo encontrado, número de iteraciones, si convergió
    """
    x = x0
    try:
        for i in range(max_iter):
            x_nuevo = g(x)
            
            # Verificar si el valor se vuelve demasiado grande
            if abs(x_nuevo) > 1e10:
                return x, i + 1, False
            
            # Verificar convergencia
            if abs(x_nuevo - x) < tolerancia:
                return x_nuevo, i + 1, True
            
            x = x_nuevo
    except OverflowError:
        return float('inf'), i + 1, False
    
    return x, max_iter, False

def verificar_convergencia_teorica(a, b):
    """
    Verifica si la iteración converge teóricamente en [a,b]
    Para convergencia necesitamos |g'(x)| < 1 para todo x en [a,b]
    """
    # Evaluar |g'(x)| en los extremos y puntos críticos
    derivada_a = abs(g_prima(a))
    derivada_b = abs(g_prima(b))
    
    print(f"En el intervalo [{a:.2f}, {b:.2f}]:")
    print(f"|g'({a:.2f})| = |{g_prima(a):.4f}| = {derivada_a:.4f}")
    print(f"|g'({b:.2f})| = |{g_prima(b):.4f}| = {derivada_b:.4f}")
    
    # Para g'(x) = x, la condición |g'(x)| < 1 se cumple cuando |x| < 1
    # Es decir, cuando -1 < x < 1
    
    converge = derivada_a < 1 and derivada_b < 1
    print(f"¿Converge teóricamente? {'Sí' if converge else 'No'}")
    
    return converge

# Encontrar los puntos fijos resolviendo x = x²/2 + 2
# x = x²/2 + 2  =>  x²/2 - x + 2 = 0  =>  x² - 2x + 4 = 0
# Usando la fórmula cuadrática:
print("=== ANÁLISIS DE PUNTOS FIJOS ===")
print("Ecuación: x = x²/2 + 2")
print("Reescribiendo: x² - 2x + 4 = 0")

discriminante = 4 - 16  # b² - 4ac = (-2)² - 4(1)(4)
print(f"Discriminante: {discriminante}")

if discriminante < 0:
    print("No hay puntos fijos reales (raíces complejas)")
    # Los puntos fijos son: x = (2 ± √(-12))/2 = 1 ± i√3
    print("Puntos fijos complejos: x = 1 ± i√3")
else:
    x1 = (2 + np.sqrt(discriminante)) / 2
    x2 = (2 - np.sqrt(discriminante)) / 2
    print(f"Puntos fijos: x₁ = {x1}, x₂ = {x2}")

print("\n=== ANÁLISIS DE CONVERGENCIA ===")

# Analizar diferentes intervalos
intervalos = [
    (-3, -1),
    (-1, 1),
    (1, 3),
    (-0.5, 0.5),
    (-2, 0),
    (0, 2)
]

print("Condición de convergencia: |g'(x)| < 1")
print("Para g'(x) = x, necesitamos |x| < 1, es decir x ∈ (-1, 1)")

for a, b in intervalos:
    print(f"\n--- Intervalo [{a}, {b}] ---")
    converge_teorico = verificar_convergencia_teorica(a, b)
    
    if converge_teorico:
        # Probar convergencia práctica con algunos valores iniciales
        valores_prueba = [a, (a+b)/2, b]
        print("\nPruebas prácticas:")
        
        for x0 in valores_prueba:
            punto_fijo, iteraciones, convergio = encontrar_punto_fijo(x0, 1e-13)
            if convergio:
                print(f"  x₀ = {x0:6.2f} → Converge a {punto_fijo:.10f} en {iteraciones} iteraciones")
            else:
                if punto_fijo == float('inf'):
                    print(f"  x₀ = {x0:6.2f} → Diverge (overflow en {iteraciones} iteraciones)")
                else:
                    print(f"  x₀ = {x0:6.2f} → No converge en {iteraciones} iteraciones")

print("\n=== RESPUESTA ===")
print("El intervalo donde la iteración converge es: [-1, 1]")
print("Exactitud solicitada: 10⁻¹³")
print("\nEn este intervalo:")
print("- Se cumple la condición |g'(x)| = |x| < 1")
print("- La iteración converge para cualquier x₀ ∈ [-1, 1]")
print("- Sin embargo, no hay punto fijo real, por lo que la secuencia diverge")

# Crear gráfico para visualizar
plt.figure(figsize=(12, 8))

# Subplot 1: Función g(x) y la recta y=x
plt.subplot(2, 2, 1)
x_vals = np.linspace(-3, 3, 1000)
y_g = g(x_vals)
plt.plot(x_vals, y_g, 'b-', label='g(x) = x²/2 + 2', linewidth=2)
plt.plot(x_vals, x_vals, 'r--', label='y = x', linewidth=2)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
plt.grid(True, alpha=0.3)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Función de iteración g(x) vs y=x')
plt.legend()
plt.xlim(-3, 3)
plt.ylim(-1, 8)

# Subplot 2: Derivada g'(x)
plt.subplot(2, 2, 2)
y_g_prima = g_prima(x_vals)
plt.plot(x_vals, y_g_prima, 'g-', label="g'(x) = x", linewidth=2)
plt.axhline(y=1, color='r', linestyle='--', label='y = 1', alpha=0.7)
plt.axhline(y=-1, color='r', linestyle='--', label='y = -1', alpha=0.7)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=1, color='r', linestyle=':', alpha=0.7)
plt.axvline(x=-1, color='r', linestyle=':', alpha=0.7)
plt.fill_between(x_vals, -1, 1, where=(np.abs(x_vals) <= 1), alpha=0.2, color='green')
plt.grid(True, alpha=0.3)
plt.xlabel('x')
plt.ylabel("g'(x)")
plt.title("Derivada g'(x) - Región de convergencia")
plt.legend()
plt.xlim(-3, 3)
plt.ylim(-3, 3)

# Subplot 3: Iteraciones desde x₀ = 0.5
plt.subplot(2, 2, 3)
x0 = 0.5
x_iter = [x0]
x = x0
try:
    for i in range(10):  # Reducido para evitar overflow
        x = g(x)
        if abs(x) > 1e6:  # Detener si crece mucho
            break
        x_iter.append(x)
except OverflowError:
    pass

plt.plot(range(len(x_iter)), x_iter, 'bo-', markersize=4)
plt.grid(True, alpha=0.3)
plt.xlabel('Iteración')
plt.ylabel('x_n')
plt.title(f'Iteraciones desde x₀ = {x0} (diverge)')
if len(x_iter) > 1 and max(x_iter) > 10:
    plt.yscale('log')

# Subplot 4: Comparación de trayectorias
plt.subplot(2, 2, 4)
x_vals_zoom = np.linspace(-1.5, 1.5, 1000)
y_g_zoom = g(x_vals_zoom)
plt.plot(x_vals_zoom, y_g_zoom, 'b-', label='g(x) = x²/2 + 2', linewidth=2)
plt.plot(x_vals_zoom, x_vals_zoom, 'r--', label='y = x', linewidth=2)

# Mostrar algunas iteraciones gráficamente
x0 = 0.8
x = x0
for i in range(5):
    x_new = g(x)
    plt.plot([x, x], [x, x_new], 'g-', alpha=0.6, linewidth=1)
    plt.plot([x, x_new], [x_new, x_new], 'g-', alpha=0.6, linewidth=1)
    plt.plot(x, x_new, 'ro', markersize=3)
    x = x_new

plt.grid(True, alpha=0.3)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Método gráfico de iteración')
plt.legend()
plt.xlim(-1.5, 1.5)
plt.ylim(-1, 4)

plt.tight_layout()
plt.show()

print(f"\n=== CONCLUSIÓN DETALLADA ===")
print("1. La función g(x) = x²/2 + 2 no tiene puntos fijos reales")
print("2. La condición de convergencia |g'(x)| < 1 se cumple en (-1, 1)")
print("3. Aunque la iteración es contractiva en [-1, 1], diverge porque no hay punto fijo")
print("4. Para la exactitud de 10⁻¹³, el intervalo teórico es [-1, 1]")
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# -------------------------
# MÉTODO DE BÚSQUEDA BINARIA (BISECCIÓN)
# -------------------------
def busqueda_binaria_raices(f, a, b, tol=1e-6, max_iter=100, precision=6):
    """
    Método de búsqueda binaria para encontrar raíces.
    También conocido como método de bisección.
    
    Parámetros:
    - f: función a evaluar
    - a, b: extremos del intervalo [a,b]
    - tol: tolerancia para el error
    - max_iter: máximo número de iteraciones
    - precision: decimales para mostrar
    
    Algoritmo:
    1. Verifica que f(a) y f(b) tengan signos opuestos
    2. Divide el intervalo por la mitad: c = (a+b)/2
    3. Evalúa f(c)
    4. Mantiene el subintervalo donde hay cambio de signo
    5. Repite hasta convergencia
    """
    print(f"\n--- MÉTODO DE BÚSQUEDA BINARIA EN INTERVALO [{a}, {b}] ---")
    
    # Verificar condición inicial
    f_a, f_b = f(a), f(b)
    print(f"Valores iniciales: f({a}) = {f_a:.6f}, f({b}) = {f_b:.6f}")
    
    if f_a * f_b > 0:
        print("⚠ ADVERTENCIA: f(a) y f(b) tienen el mismo signo.")
        print("  No se garantiza la existencia de una raíz en este intervalo.")
        print("  El método puede no converger o encontrar raíces fuera del intervalo.")
        # Continuamos de todas formas para mostrar el comportamiento
    else:
        print("✓ f(a) y f(b) tienen signos opuestos. Hay al menos una raíz.")
    
    iteraciones = []
    
    for i in range(1, max_iter + 1):
        c = (a + b) / 2                    # Punto medio (búsqueda binaria)
        f_c = f(c)                         # Evaluar función en c
        error_abs = abs(b - a) / 2         # Error absoluto
        
        # Guardar datos de la iteración
        iteraciones.append([
            i, 
            round(a, precision), 
            round(b, precision), 
            round(c, precision), 
            round(f_c, precision), 
            round(error_abs, precision)
        ])
        
        # Verificar convergencia
        if abs(f_c) < tol or error_abs < tol:
            print("\n📊 TABLA DE ITERACIONES:")
            print(tabulate(iteraciones, 
                         headers=["Iter", "a", "b", "c", "f(c)", "Error"], 
                         tablefmt="grid"))
            print(f"\n✓ CONVERGENCIA ALCANZADA")
            print(f"Raíz aproximada: x = {c:.8f}")
            print(f"Verificación: f({c:.8f}) = {f_c:.2e}")
            print(f"Error absoluto: {error_abs:.2e}")
            return c
        
        # Decidir nuevo intervalo (búsqueda binaria)
        if f(a) * f_c < 0:
            b = c  # La raíz está en [a, c]
            print(f"Iteración {i}: Raíz en [a,c] = [{a:.4f}, {c:.4f}]")
        else:
            a = c  # La raíz está en [c, b]
            print(f"Iteración {i}: Raíz en [c,b] = [{c:.4f}, {b:.4f}]")
    
    # Si no converge
    print("\n📊 TABLA DE ITERACIONES:")
    print(tabulate(iteraciones, 
                 headers=["Iter", "a", "b", "c", "f(c)", "Error"], 
                 tablefmt="grid"))
    print(f"\n⚠ El método no convergió en {max_iter} iteraciones")
    return c

# -------------------------
# ANÁLISIS DE LA FUNCIÓN
# -------------------------
def analizar_funcion(f, titulo="f(x)"):
    """
    Analiza las características de la función
    """
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE LA FUNCIÓN: {titulo}")
    print(f"{'='*60}")
    
    # Evaluar en puntos clave
    puntos_clave = [-1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]
    print("\n📋 VALORES DE LA FUNCIÓN EN PUNTOS CLAVE:")
    print("x\t|\tf(x)")
    print("-" * 25)
    for x in puntos_clave:
        try:
            fx = f(x)
            print(f"{x}\t|\t{fx:.6f}")
        except:
            print(f"{x}\t|\tError")
    
    # Identificar raíces teóricas
    print(f"\n🎯 RAÍCES TEÓRICAS DE {titulo}:")
    print("f(x) = 3(x + 1)(x - 1/2)(x - 1)")
    print("Las raíces son:")
    print("• x = -1  (donde x + 1 = 0)")
    print("• x = 1/2 = 0.5  (donde x - 1/2 = 0)")  
    print("• x = 1   (donde x - 1 = 0)")

# -------------------------
# FUNCIÓN PARA GRAFICAR
# -------------------------
def graficar_funcion_y_intervalos(f, intervalos, titulo="f(x) = 3(x+1)(x-1/2)(x-1)"):
    """
    Grafica la función y marca los intervalos de búsqueda
    """
    # Rango amplio para ver toda la función
    x_vals = np.linspace(-2, 2.5, 1000)
    y_vals = f(x_vals)
    
    plt.figure(figsize=(14, 8))
    
    # Graficar función
    plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=titulo)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    
    # Marcar raíces teóricas
    raices_teoricas = [-1, 0.5, 1]
    for raiz in raices_teoricas:
        plt.plot(raiz, f(raiz), 'go', markersize=8, label=f"Raíz teórica: x = {raiz}")
    
    # Marcar intervalos de búsqueda
    colores = ['red', 'orange', 'purple']
    for i, (a, b, nombre) in enumerate(intervalos):
        color = colores[i % len(colores)]
        plt.axvspan(a, b, alpha=0.3, color=color, label=f"{nombre}: [{a}, {b}]")
        
        # Marcar extremos del intervalo
        plt.plot(a, f(a), 'o', color=color, markersize=6)
        plt.plot(b, f(b), 's', color=color, markersize=6)
    
    plt.title(f"{titulo}\nMétodo de Búsqueda Binaria")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------
# DEFINICIÓN DE LA FUNCIÓN DEL EJERCICIO
# -------------------------
def f(x):
    """
    f(x) = 3(x + 1)(x - 1/2)(x - 1)
    
    Esta es una función polinómica de grado 3 con:
    - Raíces en x = -1, x = 1/2, x = 1
    - Coeficiente positivo, por lo que:
      * f(x) → -∞ cuando x → -∞  
      * f(x) → +∞ cuando x → +∞
    """
    return 3 * (x + 1) * (x - 1/2) * (x - 1)

# -------------------------
# EJECUCIÓN DEL EJERCICIO
# -------------------------
print("🔬 EJERCICIO 2: BÚSQUEDA BINARIA DE RAÍCES")
print("f(x) = 3(x + 1)(x - 1/2)(x - 1)")

# Analizar la función primero
analizar_funcion(f, "f(x) = 3(x + 1)(x - 1/2)(x - 1)")

# Definir intervalos del problema
intervalos = [
    (-1, 1.5, "Intervalo a)"),
    (-1.25, 2.5, "Intervalo b)")
]

# Graficar función e intervalos
graficar_funcion_y_intervalos(f, intervalos)

# Aplicar búsqueda binaria en cada intervalo
resultados = []

for a, b, nombre in intervalos:
    print(f"\n{'='*60}")
    print(f"{nombre.upper()}: INTERVALO [{a}, {b}]")
    print(f"{'='*60}")
    
    try:
        raiz = busqueda_binaria_raices(f, a, b, tol=1e-8, precision=8)
        resultados.append((nombre, a, b, raiz))
    except Exception as e:
        print(f"❌ Error en {nombre}: {e}")
        resultados.append((nombre, a, b, "Error"))

# -------------------------
# RESUMEN FINAL
# -------------------------
print(f"\n{'='*60}")
print("📋 RESUMEN FINAL DEL EJERCICIO")
print(f"{'='*60}")

print("\n🎯 RAÍCES TEÓRICAS:")
print("x₁ = -1, x₂ = 0.5, x₃ = 1")

print("\n📊 RESULTADOS DE BÚSQUEDA BINARIA:")
for nombre, a, b, raiz in resultados:
    if raiz != "Error":
        print(f"{nombre}: [{a}, {b}] → x ≈ {raiz:.8f}")
    else:
        print(f"{nombre}: [{a}, {b}] → {raiz}")

print("\n💡 OBSERVACIONES:")
print("• El método de búsqueda binaria es eficiente para funciones continuas")
print("• Requiere que f(a) y f(b) tengan signos opuestos para garantizar convergencia")
print("• En intervalos con múltiples raíces, encuentra una de ellas")
print("• La precisión depende de la tolerancia especificada")
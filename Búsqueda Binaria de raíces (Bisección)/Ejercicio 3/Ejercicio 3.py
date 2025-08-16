import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# -------------------------
# MÉTODO DE BISECCIÓN CON TOLERANCIA ESPECÍFICA
# -------------------------
def biseccion_tolerancia(f, a, b, tol=1e-3, max_iter=100, precision=6):
    """
    Método de bisección con tolerancia específica.
    
    Parámetros:
    - f: función a evaluar
    - a, b: extremos del intervalo [a,b]
    - tol: tolerancia específica (10^-3 para este ejercicio)
    - max_iter: máximo número de iteraciones
    - precision: decimales para mostrar
    
    Criterio de parada:
    - |f(c)| < tolerancia  O  |b-a|/2 < tolerancia
    """
    print(f"\n--- MÉTODO DE BISECCIÓN EN INTERVALO [{a}, {b}] ---")
    print(f"Tolerancia requerida: {tol}")
    
    # Verificar condición inicial del Teorema de Bolzano
    f_a, f_b = f(a), f(b)
    print(f"Verificación inicial: f({a}) = {f_a:.6f}, f({b}) = {f_b:.6f}")
    
    if f_a * f_b > 0:
        print("⚠ ADVERTENCIA: f(a) y f(b) tienen el mismo signo.")
        print("  No se garantiza la existencia de una raíz en este intervalo.")
        return None
    else:
        print("✓ f(a) y f(b) tienen signos opuestos. Hay al menos una raíz.")
    
    iteraciones = []
    
    for i in range(1, max_iter + 1):
        c = (a + b) / 2                    # Punto medio
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
        
        # Verificar convergencia con tolerancia específica
        if abs(f_c) < tol or error_abs < tol:
            print("\n📊 TABLA DE ITERACIONES:")
            print(tabulate(iteraciones, 
                         headers=["Iter", "a", "b", "c", "f(c)", "Error"], 
                         tablefmt="grid"))
            print(f"\n✅ CONVERGENCIA ALCANZADA EN ITERACIÓN {i}")
            print(f"Raíz aproximada: x = {c:.6f}")
            print(f"Valor de la función: f({c:.6f}) = {f_c:.6f}")
            print(f"Error absoluto: {error_abs:.6f}")
            print(f"Tolerancia cumplida: {abs(f_c):.6f} < {tol} o {error_abs:.6f} < {tol}")
            return c, i, error_abs
        
        # Decidir nuevo intervalo
        if f_a * f_c < 0:
            b = c  # La raíz está en [a, c]
        else:
            a = c  # La raíz está en [c, b]
            f_a = f_c  # Actualizar f_a
    
    # Si no converge
    print("\n📊 TABLA DE ITERACIONES:")
    print(tabulate(iteraciones, 
                 headers=["Iter", "a", "b", "c", "f(c)", "Error"], 
                 tablefmt="grid"))
    print(f"\n⚠ El método no convergió en {max_iter} iteraciones")
    return c, max_iter, error_abs

# -------------------------
# ANÁLISIS DE CADA FUNCIÓN
# -------------------------
def analizar_funcion_detallado(f, nombre, intervalos, expresion):
    """
    Analiza una función específica en sus intervalos dados
    """
    print(f"\n{'='*70}")
    print(f"ANÁLISIS: {nombre}")
    print(f"Expresión: {expresion}")
    print(f"{'='*70}")
    
    resultados = []
    
    for j, (a, b) in enumerate(intervalos):
        print(f"\n🔍 INTERVALO {j+1}: [{a}, {b}]")
        print("-" * 40)
        
        # Evaluar en los extremos
        try:
            f_a = f(a)
            f_b = f(b)
            print(f"f({a}) = {f_a:.6f}")
            print(f"f({b}) = {f_b:.6f}")
            print(f"Producto f(a)×f(b) = {f_a * f_b:.6f}")
            
            if f_a * f_b < 0:
                print("✅ Hay cambio de signo → Existe al menos una raíz")
                
                # Aplicar bisección
                resultado = biseccion_tolerancia(f, a, b, tol=1e-3)
                if resultado:
                    raiz, iteraciones, error = resultado
                    resultados.append((f"[{a}, {b}]", raiz, iteraciones, error))
                else:
                    resultados.append((f"[{a}, {b}]", "No converge", "-", "-"))
            else:
                print("❌ No hay cambio de signo → No se garantiza raíz")
                resultados.append((f"[{a}, {b}]", "Sin cambio de signo", "-", "-"))
                
        except Exception as e:
            print(f"❌ Error evaluando función: {e}")
            resultados.append((f"[{a}, {b}]", "Error", "-", "-"))
    
    return resultados

# -------------------------
# FUNCIÓN PARA GRAFICAR TODAS LAS FUNCIONES
# -------------------------
def graficar_funcion(f, intervalos, titulo, rango_grafico):
    """
    Grafica una función con sus intervalos de búsqueda
    """
    x_vals = np.linspace(rango_grafico[0], rango_grafico[1], 1000)
    
    try:
        y_vals = []
        for x in x_vals:
            try:
                y_vals.append(f(x))
            except:
                y_vals.append(np.nan)
        y_vals = np.array(y_vals)
    except:
        return
    
    plt.figure(figsize=(12, 6))
    plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=titulo)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    
    # Marcar intervalos
    colores = ['red', 'green', 'orange', 'purple', 'brown']
    for i, (a, b) in enumerate(intervalos):
        color = colores[i % len(colores)]
        plt.axvspan(a, b, alpha=0.3, color=color, label=f"Intervalo [{a}, {b}]")
        
        try:
            plt.plot(a, f(a), 'o', color=color, markersize=6)
            plt.plot(b, f(b), 's', color=color, markersize=6)
        except:
            pass
    
    plt.title(f"{titulo}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------
# DEFINICIÓN DE LAS FUNCIONES DEL EJERCICIO
# -------------------------

# a) √x - cos(x) = 0, para 0 ≤ x ≤ 1
def f_a(x):
    return np.sqrt(x) - np.cos(x)

# b) x - 2^(-x) = 0, para 0 ≤ x ≤ 1  
def f_b(x):
    return x - 2**(-x)

# c) e^x - x² + 3x - 2 = 0, para 0 ≤ x ≤ 1
def f_c(x):
    return np.exp(x) - x**2 + 3*x - 2

# d) 2x cos(x) - (x + 1)² = 0, para -3 ≤ x ≤ -2, para -1 ≤ x ≤ 0
def f_d(x):
    return 2*x*np.cos(x) - (x + 1)**2

# e) x cos(x) - 2x² + 3x - 1 = 0, para 0.2 ≤ x ≤ 0.3, para 1.2 ≤ x ≤ 1.3
def f_e(x):
    return x*np.cos(x) - 2*x**2 + 3*x - 1

# -------------------------
# DEFINICIÓN DE INTERVALOS PARA CADA FUNCIÓN
# -------------------------
ejercicios = [
    (f_a, "a) √x - cos(x) = 0", "√x - cos(x)", [(0, 1)], (0, 1)),
    (f_b, "b) x - 2^(-x) = 0", "x - 2^(-x)", [(0, 1)], (0, 1)),
    (f_c, "c) e^x - x² + 3x - 2 = 0", "e^x - x² + 3x - 2", [(0, 1)], (0, 1)),
    (f_d, "d) 2x cos(x) - (x + 1)² = 0", "2x cos(x) - (x + 1)²", [(-3, -2), (-1, 0)], (-3.5, 0.5)),
    (f_e, "e) x cos(x) - 2x² + 3x - 1 = 0", "x cos(x) - 2x² + 3x - 1", [(0.2, 0.3), (1.2, 1.3)], (0, 1.5))
]

# -------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------
print("🔬 EJERCICIO 3: MÉTODO DE BISECCIÓN CON TOLERANCIA 10⁻³")
print("="*70)

todos_los_resultados = []

for f, nombre, expresion, intervalos, rango_graf in ejercicios:
    # Analizar función
    resultados = analizar_funcion_detallado(f, nombre, intervalos, expresion)
    todos_los_resultados.extend([(nombre, r[0], r[1], r[2], r[3]) for r in resultados])
    
    # Graficar función
    graficar_funcion(f, intervalos, nombre, rango_graf)

# -------------------------
# RESUMEN FINAL DE TODOS LOS EJERCICIOS
# -------------------------
print(f"\n{'='*80}")
print("📋 RESUMEN FINAL - TODAS LAS RAÍCES ENCONTRADAS")
print(f"{'='*80}")

print("\n📊 TABLA RESUMEN:")
headers = ["Ejercicio", "Intervalo", "Raíz", "Iteraciones", "Error Final"]
tabla_resumen = []

for ejercicio, intervalo, raiz, iters, error in todos_los_resultados:
    if isinstance(raiz, float):
        tabla_resumen.append([ejercicio, intervalo, f"{raiz:.6f}", iters, f"{error:.6f}"])
    else:
        tabla_resumen.append([ejercicio, intervalo, raiz, iters, error])

print(tabulate(tabla_resumen, headers=headers, tablefmt="grid"))

print(f"\n💡 OBSERVACIONES:")
print(f"• Tolerancia utilizada: 10⁻³ = 0.001")
print(f"• Criterio de parada: |f(c)| < 0.001 o |b-a|/2 < 0.001")
print(f"• El método converge cuando se alcanza la precisión requerida")
print(f"• Algunas funciones pueden tener múltiples raíces en intervalos diferentes")

print(f"\n🎯 ANÁLISIS POR EJERCICIO:")
print(f"a) √x - cos(x): Encuentra intersección entre √x y cos(x)")
print(f"b) x - 2^(-x): Encuentra donde x = 2^(-x)")  
print(f"c) e^x - x² + 3x - 2: Función exponencial vs polinómica")
print(f"d) 2x cos(x) - (x + 1)²: Función trigonométrica en intervalos negativos")
print(f"e) x cos(x) - 2x² + 3x - 1: Múltiples intervalos pequeños")

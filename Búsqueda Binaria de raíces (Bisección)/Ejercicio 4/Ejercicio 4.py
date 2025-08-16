import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# -------------------------
# MÉTODO DE BISECCIÓN PARA POLINOMIOS
# -------------------------
def biseccion_polinomio(f, a, b, tol=1e-2, max_iter=100, precision=6):
    """
    Método de bisección específico para el ejercicio del polinomio.
    
    Parámetros:
    - f: función polinómica a evaluar
    - a, b: extremos del intervalo [a,b]
    - tol: tolerancia específica (10^-2 para este ejercicio)
    - max_iter: máximo número de iteraciones
    - precision: decimales para mostrar
    
    Tolerancia: 10^-2 = 0.01
    """
    print(f"\n--- BISECCIÓN EN INTERVALO [{a}, {b}] ---")
    print(f"Tolerancia requerida: {tol} = 10⁻²")
    
    # Verificar condición inicial del Teorema de Bolzano
    f_a, f_b = f(a), f(b)
    print(f"Evaluación inicial:")
    print(f"  f({a}) = {f_a:.6f}")
    print(f"  f({b}) = {f_b:.6f}")
    print(f"  f(a) × f(b) = {f_a * f_b:.6f}")
    
    if f_a * f_b > 0:
        print("❌ NO HAY CAMBIO DE SIGNO")
        print("   No se garantiza la existencia de una raíz en este intervalo.")
        return None
    elif f_a * f_b == 0:
        if f_a == 0:
            print(f"✅ RAÍZ EXACTA ENCONTRADA: x = {a}")
            return a, 0, 0
        else:
            print(f"✅ RAÍZ EXACTA ENCONTRADA: x = {b}")
            return b, 0, 0
    else:
        print("✅ HAY CAMBIO DE SIGNO → Existe al menos una raíz")
    
    iteraciones = []
    a_original = a  # Guardar para referencia
    
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
        
        # Verificar convergencia con tolerancia 10^-2
        if abs(f_c) < tol or error_abs < tol:
            print("\n📊 TABLA DE ITERACIONES:")
            print(tabulate(iteraciones, 
                         headers=["Iter", "a", "b", "c", "f(c)", "Error"], 
                         tablefmt="grid"))
            print(f"\n✅ CONVERGENCIA EN ITERACIÓN {i}")
            print(f"Raíz aproximada: x = {c:.4f}")
            print(f"Valor función: f({c:.4f}) = {f_c:.6f}")
            print(f"Error absoluto: {error_abs:.6f}")
            print(f"Cumple tolerancia: |f(c)| = {abs(f_c):.4f} < {tol}")
            return c, i, error_abs
        
        # Decidir nuevo intervalo
        if f(a_original) * f_c < 0:
            b = c  # La raíz está en [a, c]
            print(f"Iter {i}: f(a)×f(c) < 0 → raíz en [a,c] = [{a:.4f}, {c:.4f}]")
        else:
            a = c  # La raíz está en [c, b]
            print(f"Iter {i}: f(a)×f(c) > 0 → raíz en [c,b] = [{c:.4f}, {b:.4f}]")
    
    # Si no converge
    print("\n📊 TABLA DE ITERACIONES:")
    print(tabulate(iteraciones, 
                 headers=["Iter", "a", "b", "c", "f(c)", "Error"], 
                 tablefmt="grid"))
    print(f"\n⚠ No convergió en {max_iter} iteraciones")
    return c, max_iter, error_abs

# -------------------------
# ANÁLISIS COMPLETO DEL POLINOMIO
# -------------------------
def analizar_polinomio_completo(f, expresion):
    """
    Realiza un análisis completo del polinomio antes de aplicar bisección
    """
    print(f"\n{'='*80}")
    print(f"ANÁLISIS COMPLETO DEL POLINOMIO")
    print(f"f(x) = {expresion}")
    print(f"{'='*80}")
    
    # Evaluar en puntos clave para entender el comportamiento
    puntos_test = [-3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4]
    
    print("\n📋 EVALUACIÓN EN PUNTOS CLAVE:")
    print("x\t|\tf(x)\t\t|\tSigno")
    print("-" * 45)
    
    valores = []
    for x in puntos_test:
        fx = f(x)
        signo = "+" if fx > 0 else "-" if fx < 0 else "0"
        print(f"{x}\t|\t{fx:.6f}\t|\t{signo}")
        valores.append((x, fx))
    
    # Identificar cambios de signo
    print(f"\n🔍 BÚSQUEDA DE CAMBIOS DE SIGNO:")
    cambios_signo = []
    for i in range(len(valores) - 1):
        x1, f1 = valores[i]
        x2, f2 = valores[i + 1]
        if f1 * f2 < 0:
            cambios_signo.append((x1, x2))
            print(f"✅ Cambio de signo entre x = {x1} y x = {x2}")
            print(f"   f({x1}) = {f1:.6f}, f({x2}) = {f2:.6f}")
    
    if not cambios_signo:
        print("❌ No se encontraron cambios de signo en el rango evaluado")
    
    print(f"\n📊 RESUMEN DEL ANÁLISIS:")
    print(f"• Polinomio de grado 4 → máximo 4 raíces reales")
    print(f"• Cambios de signo encontrados: {len(cambios_signo)}")
    print(f"• Posibles raíces por Teorema de Bolzano: {len(cambios_signo)}")
    
    return cambios_signo

# -------------------------
# FUNCIÓN PARA GRAFICAR EL POLINOMIO
# -------------------------
def graficar_polinomio_completo(f, intervalos_ejercicio, raices_encontradas):
    """
    Grafica el polinomio mostrando todos los intervalos y raíces
    """
    # Rango amplio para ver todo el comportamiento
    x_vals = np.linspace(-3, 4, 2000)
    y_vals = f(x_vals)
    
    plt.figure(figsize=(15, 10))
    
    # Gráfico principal
    plt.subplot(2, 1, 1)
    plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x) = x⁴ - 2x³ - 4x² + 4x + 4')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    
    # Marcar intervalos del ejercicio
    colores = ['red', 'green', 'orange', 'purple']
    nombres = ['a) [-2,-1]', 'b) [0,2]', 'c) [2,3]', 'd) [-1,0]']
    
    for i, ((a, b), nombre) in enumerate(zip(intervalos_ejercicio, nombres)):
        color = colores[i]
        plt.axvspan(a, b, alpha=0.3, color=color, label=f"{nombre}")
        plt.plot(a, f(a), 'o', color=color, markersize=8)
        plt.plot(b, f(b), 's', color=color, markersize=8)
    
    # Marcar raíces encontradas
    for i, (intervalo, raiz, iteraciones) in enumerate(raices_encontradas):
        if raiz != "Sin raíz":
            plt.plot(raiz, f(raiz), '*', color='gold', markersize=12, 
                    markeredgecolor='black', markeredgewidth=1)
    
    plt.title('Polinomio f(x) = x⁴ - 2x³ - 4x² + 4x + 4', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Gráfico zoom en región de raíces
    plt.subplot(2, 1, 2)
    x_zoom = np.linspace(-2.5, 3.5, 1000)
    y_zoom = f(x_zoom)
    plt.plot(x_zoom, y_zoom, 'b-', linewidth=2)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    
    # Marcar intervalos en zoom
    for i, ((a, b), nombre) in enumerate(zip(intervalos_ejercicio, nombres)):
        color = colores[i]
        plt.axvspan(a, b, alpha=0.3, color=color)
    
    # Marcar raíces en zoom
    for i, (intervalo, raiz, iteraciones) in enumerate(raices_encontradas):
        if raiz != "Sin raíz":
            plt.plot(raiz, f(raiz), '*', color='gold', markersize=10, 
                    markeredgecolor='black', markeredgewidth=1)
            plt.annotate(f'x≈{raiz:.3f}', (raiz, f(raiz)), 
                        xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    plt.title('Vista ampliada de las raíces', fontsize=12)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------
# DEFINICIÓN DEL POLINOMIO
# -------------------------
def polinomio(x):
    """
    f(x) = x⁴ - 2x³ - 4x² + 4x + 4
    
    Polinomio de grado 4:
    - Puede tener hasta 4 raíces reales
    - Comportamiento: f(x) → +∞ cuando x → ±∞ (coeficiente principal positivo)
    """
    return x**4 - 2*x**3 - 4*x**2 + 4*x + 4

# -------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------
print("🔬 EJERCICIO 4: BISECCIÓN EN POLINOMIO CON TOLERANCIA 10⁻²")
print("f(x) = x⁴ - 2x³ - 4x² + 4x + 4")

# Análisis previo del polinomio
cambios_signo = analizar_polinomio_completo(polinomio, "x⁴ - 2x³ - 4x² + 4x + 4")

# Intervalos del ejercicio
intervalos_ejercicio = [(-2, -1), (0, 2), (2, 3), (-1, 0)]
nombres_intervalos = ["a) [-2,-1]", "b) [0,2]", "c) [2,3]", "d) [-1,0]"]

print(f"\n{'='*80}")
print("APLICACIÓN DE BISECCIÓN EN LOS INTERVALOS DEL EJERCICIO")
print(f"{'='*80}")

resultados = []

for i, ((a, b), nombre) in enumerate(zip(intervalos_ejercicio, nombres_intervalos)):
    print(f"\n{'='*50}")
    print(f"{nombre.upper()}: INTERVALO [{a}, {b}]")
    print(f"{'='*50}")
    
    resultado = biseccion_polinomio(polinomio, a, b, tol=1e-2)
    
    if resultado:
        raiz, iteraciones, error = resultado
        resultados.append((f"[{a}, {b}]", raiz, iteraciones))
        print(f"\n🎯 RESULTADO: Raíz encontrada en x = {raiz:.4f}")
    else:
        resultados.append((f"[{a}, {b}]", "Sin raíz", "-"))
        print(f"\n❌ RESULTADO: No hay raíz en este intervalo")

# Graficar todo
graficar_polinomio_completo(polinomio, intervalos_ejercicio, resultados)

# -------------------------
# RESUMEN FINAL COMPLETO
# -------------------------
print(f"\n{'='*80}")
print("📋 RESUMEN FINAL DEL EJERCICIO 4")
print(f"{'='*80}")

print(f"\n🎯 POLINOMIO ANALIZADO:")
print(f"f(x) = x⁴ - 2x³ - 4x² + 4x + 4")

print(f"\n📊 RESULTADOS POR INTERVALO:")
tabla_final = []
for (intervalo, raiz, iteraciones) in resultados:
    if raiz != "Sin raíz":
        tabla_final.append([intervalo, f"{raiz:.4f}", iteraciones, "✅"])
    else:
        tabla_final.append([intervalo, "No encontrada", "-", "❌"])

print(tabulate(tabla_final, 
              headers=["Intervalo", "Raíz", "Iteraciones", "Estado"], 
              tablefmt="grid"))

print(f"\n💡 ANÁLISIS DE RESULTADOS:")
raices_validas = [r for r in resultados if r[1] != "Sin raíz"]
print(f"• Total de raíces encontradas: {len(raices_validas)}")
print(f"• Tolerancia utilizada: 10⁻² = 0.01")
print(f"• Método: Bisección (división binaria del intervalo)")

if raices_validas:
    print(f"\n🔢 RAÍCES APROXIMADAS:")
    for i, (intervalo, raiz, iter_count) in enumerate(raices_validas):
        print(f"  Raíz {i+1}: x ≈ {raiz:.4f} (encontrada en {intervalo})")
        print(f"           Verificación: f({raiz:.4f}) = {polinomio(raiz):.6f}")

print(f"\n📈 OBSERVACIONES:")
print(f"• El polinomio de grado 4 puede tener hasta 4 raíces reales")
print(f"• Cada intervalo puede contener 0 o 1 raíz (por continuidad)")
print(f"• La tolerancia 10⁻² da aproximaciones con 2 decimales de precisión")
print(f"• El método garantiza convergencia cuando hay cambio de signo")


import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# -------------------------
# MÉTODO DE BISECCIÓN
# -------------------------
def biseccion(f, a, b, tol=1e-6, max_iter=100, precision=6):
    """
    Método de bisección para encontrar raíces de una función.
    
    Parámetros:
    - f: función a evaluar
    - a, b: extremos del intervalo [a,b]
    - tol: tolerancia para el error
    - max_iter: máximo número de iteraciones
    - precision: decimales para mostrar en la tabla
    
    Proceso:
    1. Verifica que f(a) y f(b) tengan signos opuestos
    2. Calcula punto medio c = (a+b)/2
    3. Evalúa f(c)
    4. Si f(a)*f(c) < 0, la raíz está en [a,c], sino en [c,b]
    5. Repite hasta alcanzar la tolerancia
    """
    if f(a) * f(b) > 0:
        raise ValueError("El intervalo no encierra una raíz (f(a) y f(b) tienen el mismo signo)")
    
    iteraciones = []
    for i in range(1, max_iter+1):
        c = (a + b) / 2                    # Punto medio
        error_abs = abs(b - a) / 2         # Error absoluto
        
        # Guardar datos de la iteración
        iteraciones.append([i, round(a, precision), round(b, precision), 
                            round(c, precision), round(f(c), precision), 
                            round(error_abs, precision)])
        
        # Verificar convergencia
        if abs(f(c)) < tol or error_abs < tol:
            print(tabulate(iteraciones, headers=["Iteración", "a", "b", "c", "f(c)", "Error"], tablefmt="grid"))
            return c
        
        # Decidir nuevo intervalo
        if f(a) * f(c) < 0:
            b = c  # La raíz está en [a,c]
        else:
            a = c  # La raíz está en [c,b]
    
    raise ValueError("El método no convergió en las iteraciones dadas.")

# -------------------------
# FUNCIÓN PARA BUSCAR INTERVALOS CON RAÍCES
# -------------------------
def buscar_intervalos_con_raices(f, inicio=-10, fin=10, paso=1):
    """
    Busca intervalos donde f(a)*f(b) < 0 (Teorema de Bolzano)
    
    Proceso:
    1. Evalúa la función en puntos consecutivos
    2. Si f(i) y f(i+1) tienen signos opuestos, hay una raíz en [i, i+1]
    3. Retorna lista de intervalos que contienen raíces
    """
    intervalos = []
    for i in range(inicio, fin):
        a, b = i, i + paso
        try:
            if f(a) * f(b) < 0:  # Cambio de signo = hay raíz
                intervalos.append((a, b))
        except:
            continue  # Manejo de errores (ej: log de números negativos)
    return intervalos

# -------------------------
# FUNCIÓN PARA GRAFICAR CON MÚLTIPLES RAÍCES
# -------------------------
def graficar_multiples_raices(f, raices_info, titulo="Método de Bisección", rango_x=(-3, 3)):
    """
    Grafica la función y marca todas las raíces encontradas.
    
    Proceso:
    1. Crea array de valores x en el rango especificado
    2. Evalúa f(x) para cada x
    3. Grafica la función
    4. Marca cada raíz con un punto de color diferente
    5. Sombrea los intervalos iniciales donde se buscó cada raíz
    """
    x_vals = np.linspace(rango_x[0], rango_x[1], 1000)
    try:
        y_vals = f(x_vals)
    except:
        # Manejo de funciones problemáticas (ej: ln(x) con x<0)
        y_vals = []
        for x in x_vals:
            try:
                y_vals.append(f(x))
            except:
                y_vals.append(np.nan)
        y_vals = np.array(y_vals)
    
    plt.figure(figsize=(12, 8))
    plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='$f(x)$')
    plt.axhline(0, color='black', linewidth=0.8)  # Eje x
    plt.axvline(0, color='black', linewidth=0.8)  # Eje y
    
    # Marcar todas las raíces con colores diferentes
    colores = ['red', 'green', 'orange', 'purple', 'brown']
    for i, (intervalo, raiz) in enumerate(raices_info):
        color = colores[i % len(colores)]
        plt.plot(raiz, f(raiz), 'o', color=color, markersize=8, 
                label=f"Raíz {i+1}: x ≈ {raiz:.6f}")
        
        # Sombrear intervalo inicial
        plt.axvspan(intervalo[0], intervalo[1], alpha=0.2, color=color)
    
    plt.title(f"{titulo} - Raíces encontradas")
    plt.xlabel("$x$")
    plt.ylabel("$f(x)$")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# -------------------------
# FUNCIÓN PRINCIPAL PARA RESOLVER EJERCICIO COMPLETO
# -------------------------
def resolver_ejercicio_completo(f, nombre, rango_busqueda=(-5, 5), rango_grafico=(-3, 3)):
    """
    Resuelve un ejercicio completo:
    1. Busca intervalos con raíces
    2. Aplica bisección a cada intervalo
    3. Grafica resultados
    4. Muestra resumen
    """
    print(f"\n{'='*50}")
    print(f"{nombre}")
    print(f"{'='*50}")
    
    # PASO 1: Buscar intervalos con cambio de signo
    intervalos = buscar_intervalos_con_raices(f, rango_busqueda[0], rango_busqueda[1])
    
    if not intervalos:
        print("⚠ No se encontraron intervalos con cambio de signo.")
        return
    
    print(f"Se encontraron {len(intervalos)} intervalo(s) con cambio de signo:")
    for i, (a, b) in enumerate(intervalos):
        print(f"  Intervalo {i+1}: [{a}, {b}] -> f({a})={f(a):.3f}, f({b})={f(b):.3f}")
    
    # PASO 2: Calcular raíces usando bisección
    raices_info = []
    for i, (a, b) in enumerate(intervalos):
        print(f"\n--- Calculando raíz en intervalo [{a}, {b}] ---")
        try:
            raiz = biseccion(f, a, b, tol=1e-8)
            raices_info.append(((a, b), raiz))
            print(f"✓ Raíz {i+1} encontrada: x = {raiz:.8f}")
            print(f"  Verificación: f({raiz:.8f}) = {f(raiz):.2e}")
        except Exception as e:
            print(f"✗ Error calculando raíz: {e}")
    
    # PASO 3: Graficar todas las raíces
    if raices_info:
        graficar_multiples_raices(f, raices_info, titulo=nombre, rango_x=rango_grafico)
        
        # PASO 4: Resumen final
        print(f"\n--- RESUMEN {nombre} ---")
        for i, (intervalo, raiz) in enumerate(raices_info):
            print(f"Raíz {i+1}: x = {raiz:.8f}")

# -------------------------
# EJERCICIOS DEL PROBLEMA
# -------------------------
ej_a = lambda x: np.exp(x) - 2 - x      # a) f(x) = e^x - 2 - x
ej_b = lambda x: np.cos(x) + x          # b) f(x) = cos(x) + x  
ej_c = lambda x: np.log(x) - 5 - x      # c) f(x) = ln(x) - 5 - x
ej_d = lambda x: x**2 - 10*x + 23       # d) f(x) = x² - 10x + 23

# -------------------------
# EJECUCIÓN DE LOS EJERCICIOS
# -------------------------
ejercicios = [
    (ej_a, "a) f(x) = e^x - 2 - x", (-3, 3), (-3, 3)),
    (ej_b, "b) f(x) = cos(x) + x", (-3, 1), (-3, 1)),
    (ej_c, "c) f(x) = ln(x) - 5 - x", (1, 8), (1, 8)),
    (ej_d, "d) f(x) = x² - 10x + 23", (2, 8), (2, 8)),
]

# Ejecutar todos los ejercicios
for f, nombre, rango_busq, rango_graf in ejercicios:
    resolver_ejercicio_completo(f, nombre, rango_busq, rango_graf)

print(f"\n{'='*50}")
print("ANÁLISIS COMPLETADO")
print(f"{'='*50}")
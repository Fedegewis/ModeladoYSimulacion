# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 10:54:33 2025

@author: fedeg
"""

import numpy as np
import matplotlib.pyplot as plt

def metodo_punto_fijo(g, x0, tol=1e-6, max_iter=100, verbose=True):
    """
    Implementa el método del punto fijo para encontrar raíces.
    
    Parámetros:
    g: función de iteración g(x) tal que f(x) = 0 equivale a x = g(x)
    x0: valor inicial
    tol: tolerancia para convergencia
    max_iter: número máximo de iteraciones
    verbose: mostrar iteraciones
    
    Retorna: (raíz aproximada, número de iteraciones, convergió)
    """
    x = x0
    iteraciones = []
    
    if verbose:
        print(f"Iteración 0: x = {x:.6f}")
    
    for i in range(1, max_iter + 1):
        x_nuevo = g(x)
        iteraciones.append((i, x, x_nuevo, abs(x_nuevo - x)))
        
        if verbose:
            print(f"Iteración {i}: x = {x_nuevo:.6f}, error = {abs(x_nuevo - x):.6f}")
        
        if abs(x_nuevo - x) < tol:
            return x_nuevo, i, True, iteraciones
        
        x = x_nuevo
    
    return x, max_iter, False, iteraciones

def graficar_convergencia(iteraciones, titulo):
    """Grafica la convergencia del método"""
    if not iteraciones:
        return
    
    iter_nums = [it[0] for it in iteraciones]
    errores = [it[3] for it in iteraciones]
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(iter_nums, errores, 'bo-', linewidth=2, markersize=6)
    plt.xlabel('Iteración')
    plt.ylabel('Error absoluto (escala log)')
    plt.title(f'Convergencia - {titulo}')
    plt.grid(True, alpha=0.3)
    plt.show()

# Problema 1: f(x) = 2e^(x²) - 5x, x ∈ [0,1], x₀ = 0
# Transformamos a punto fijo: x = g(x) = (2e^(x²))/5
print("="*60)
print("PROBLEMA 1: f(x) = 2e^(x²) - 5x")
print("Transformación: x = (2e^(x²))/5")
print("="*60)

def g1(x):
    return (2 * np.exp(x**2)) / 5

resultado1, iter1, conv1, hist1 = metodo_punto_fijo(g1, 0, verbose=True)
print(f"\nResultado: x = {resultado1:.6f}")
print(f"Converge: {conv1}, Iteraciones: {iter1}")
print(f"Verificación f({resultado1:.6f}) = {2*np.exp(resultado1**2) - 5*resultado1:.6f}")

# Problema 2: f(x) = cos(x), x* ∈ [1,2], x₀ = 1
# Ya está en forma de punto fijo: x = cos(x)
print("\n" + "="*60)
print("PROBLEMA 2: f(x) = cos(x)")
print("Ya en forma de punto fijo: x = cos(x)")
print("="*60)

def g2(x):
    return np.cos(x)

resultado2, iter2, conv2, hist2 = metodo_punto_fijo(g2, 1, verbose=True)
print(f"\nResultado: x = {resultado2:.6f}")
print(f"Converge: {conv2}, Iteraciones: {iter2}")
print(f"Verificación f({resultado2:.6f}) = {np.cos(resultado2):.6f}")

# Problema 3: f(x) = e^(-x) - x, x* ∈ [0,1], x₀ = 0
# Transformamos: x = e^(-x)
print("\n" + "="*60)
print("PROBLEMA 3: f(x) = e^(-x) - x")
print("Transformación: x = e^(-x)")
print("="*60)

def g3(x):
    return np.exp(-x)

resultado3, iter3, conv3, hist3 = metodo_punto_fijo(g3, 0, verbose=True)
print(f"\nResultado: x = {resultado3:.6f}")
print(f"Converge: {conv3}, Iteraciones: {iter3}")
print(f"Verificación f({resultado3:.6f}) = {np.exp(-resultado3) - resultado3:.6f}")

# Problema 4: f(x) = x³ - x - 1, x* ∈ [1,2], x₀ = 1
# Transformamos: x = ∛(x + 1)
print("\n" + "="*60)
print("PROBLEMA 4: f(x) = x³ - x - 1")
print("Transformación: x = ∛(x + 1)")
print("="*60)

def g4(x):
    return (x + 1)**(1/3)

resultado4, iter4, conv4, hist4 = metodo_punto_fijo(g4, 1, verbose=True)
print(f"\nResultado: x = {resultado4:.6f}")
print(f"Converge: {conv4}, Iteraciones: {iter4}")
print(f"Verificación f({resultado4:.6f}) = {resultado4**3 - resultado4 - 1:.6f}")

# Problema 5: f(x) = π + 0.5sin(x/2) - x, x* ∈ [0,2π], x₀ = 0
# Transformamos: x = π + 0.5sin(x/2)
print("\n" + "="*60)
print("PROBLEMA 5: f(x) = π + 0.5sin(x/2) - x")
print("Transformación: x = π + 0.5sin(x/2)")
print("="*60)

def g5(x):
    return np.pi + 0.5 * np.sin(x/2)

resultado5, iter5, conv5, hist5 = metodo_punto_fijo(g5, 0, verbose=True)
print(f"\nResultado: x = {resultado5:.6f}")
print(f"Converge: {conv5}, Iteraciones: {iter5}")
print(f"Verificación f({resultado5:.6f}) = {np.pi + 0.5*np.sin(resultado5/2) - resultado5:.6f}")

# Resumen de resultados
print("\n" + "="*80)
print("RESUMEN DE RESULTADOS")
print("="*80)
resultados = [
    ("Problema 1", resultado1, iter1, conv1),
    ("Problema 2", resultado2, iter2, conv2),
    ("Problema 3", resultado3, iter3, conv3),
    ("Problema 4", resultado4, iter4, conv4),
    ("Problema 5", resultado5, iter5, conv5)
]

for nombre, x, iters, converge in resultados:
    estado = "Converge" if converge else "No converge"
    print(f"{nombre}: x = {x:.6f}, Iteraciones: {iters}, Estado: {estado}")

# Análisis de convergencia
print("\n" + "="*80)
print("ANÁLISIS DE CONVERGENCIA")
print("="*80)

funciones_g = [g1, g2, g3, g4, g5]
nombres = ["g1(x) = (2e^(x²))/5", "g2(x) = cos(x)", "g3(x) = e^(-x)", 
           "g4(x) = ∛(x+1)", "g5(x) = π + 0.5sin(x/2)"]
puntos_fijos = [resultado1, resultado2, resultado3, resultado4, resultado5]

for i, (g, nombre, pf) in enumerate(zip(funciones_g, nombres, puntos_fijos)):
    # Calcular derivada numérica en el punto fijo
    h = 1e-8
    derivada = (g(pf + h) - g(pf - h)) / (2 * h)
    print(f"\n{nombre}:")
    print(f"  Punto fijo: x = {pf:.6f}")
    print(f"  g'({pf:.6f}) ≈ {derivada:.6f}")
    
    if abs(derivada) < 1:
        print(f"  |g'(x)| = {abs(derivada):.6f} < 1 → Convergencia garantizada")
    else:
        print(f"  |g'(x)| = {abs(derivada):.6f} ≥ 1 → Convergencia no garantizada")
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 10:45:55 2025

@author: fedeg
"""

import numpy as np
import matplotlib.pyplot as plt

# Configurar matplotlib para mostrar gráficos
plt.style.use('default')

print("EJERCICIOS DE DIFERENCIAS FINITAS")
print("=" * 50)

# EJERCICIO 1: f(x) = sin(x) en x = [0, 0.1, 0.2, 0.3, 0.4, 0.5] con h = 0.1
print("\n1. DERIVADA DE f(x) = sin(x)")
print("-" * 30)

def f1(x):
    return np.sin(x)

def f1_prime(x):
    return np.cos(x)  # Derivada exacta

# Diferencia finita central
def diferencia_central(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

x_vals = np.array([0.1, 0.2, 0.3, 0.4])  # Puntos donde podemos calcular (no los extremos)
h = 0.1

# Headers sin backslash
header_x = "x"
header_exacta = "f'(x) exacta"
header_aprox = "f'(x) aprox"
header_error = "Error"

print(f"{header_x:<5} {header_exacta:<15} {header_aprox:<15} {header_error:<15}")
print("-" * 60)

for x in x_vals:
    exacta = f1_prime(x)
    aprox = diferencia_central(f1, x, h)
    error = abs(exacta - aprox)
    print(f"{x:<5.1f} {exacta:<15.6f} {aprox:<15.6f} {error:<15.8f}")

# EJERCICIO 2: f(x) = e^x en x = [0, 0.1, 0.2, 0.3, 0.4, 0.5] con h = 0.1
print("\n\n2. DERIVADA DE f(x) = e^x")
print("-" * 30)

def f2(x):
    return np.exp(x)

def f2_prime(x):
    return np.exp(x)  # Derivada exacta

print(f"{header_x:<5} {header_exacta:<15} {header_aprox:<15} {header_error:<15}")
print("-" * 60)

for x in x_vals:
    exacta = f2_prime(x)
    aprox = diferencia_central(f2, x, h)
    error = abs(exacta - aprox)
    print(f"{x:<5.1f} {exacta:<15.6f} {aprox:<15.6f} {error:<15.8f}")

# EJERCICIO 3: f(x) = x³ - x en x = 1 con h = 0.1
print("\n\n3. DERIVADA DE f(x) = x³ - x EN x = 1")
print("-" * 40)

def f3(x):
    return x**3 - x

def f3_prime(x):
    return 3*x**2 - 1

def f3_double_prime(x):
    return 6*x

x = 1
h = 0.1

# Primera derivada
exacta_1 = f3_prime(x)
aprox_1 = diferencia_central(f3, x, h)

# Segunda derivada usando diferencias centrales
def segunda_derivada_central(f, x, h):
    return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)

exacta_2 = f3_double_prime(x)
aprox_2 = segunda_derivada_central(f3, x, h)

print(f"a) Primera derivada exacta: {exacta_1:.6f}")
print(f"   Primera derivada aproximada: {aprox_1:.6f}")
print(f"   Error primera derivada: {abs(exacta_1 - aprox_1):.8f}")
print()
print(f"b) Error absoluto primera derivada: {abs(exacta_1 - aprox_1):.8f}")
print()
print(f"c) Segunda derivada exacta: {exacta_2:.6f}")
print(f"   Segunda derivada aproximada: {aprox_2:.6f}")
print(f"   Error segunda derivada: {abs(exacta_2 - aprox_2):.8f}")

# EJERCICIO 4: f(x) = e^x * sin(x)
print("\n\n4. DERIVADAS DE f(x) = e^x * sin(x)")
print("-" * 35)

def f4(x):
    return np.exp(x) * np.sin(x)

def f4_prime(x):
    return np.exp(x) * (np.sin(x) + np.cos(x))

def f4_double_prime(x):
    return 2 * np.exp(x) * np.cos(x)

x = 1
h = 0.01

# a) Primera derivada con h = 0.01
exacta_1 = f4_prime(x)
aprox_1 = diferencia_central(f4, x, h)
error_abs = abs(exacta_1 - aprox_1)

print(f"a) h = 0.01:")
print(f"   f'(1) exacta: {exacta_1:.8f}")
print(f"   f'(1) aproximada: {aprox_1:.8f}")
print(f"   Error absoluto: {error_abs:.10f}")

# b) Error absoluto ya calculado arriba
print(f"b) Error absoluto: {error_abs:.10f}")

# c) Segunda derivada
exacta_2 = f4_double_prime(x)
aprox_2 = segunda_derivada_central(f4, x, h)
error_2 = abs(exacta_2 - aprox_2)

print(f"c) f''(1) exacta: {exacta_2:.8f}")
print(f"   f''(1) aproximada: {aprox_2:.8f}")
print(f"   Error: {error_2:.10f}")

# EJERCICIO 5: Comparar aproximaciones hacia adelante, atrás y centrales para f(x) = e^(-2x) - x
print("\n\n5. COMPARACIÓN DE APROXIMACIONES PARA f(x) = e^(-2x) - x")
print("-" * 55)

def f5(x):
    return np.exp(-2*x) - x

def f5_prime(x):
    return -2 * np.exp(-2*x) - 1

def f5_double_prime(x):
    return 4 * np.exp(-2*x)

def diferencia_adelante(f, x, h):
    return (f(x + h) - f(x)) / h

def diferencia_atras(f, x, h):
    return (f(x) - f(x - h)) / h

x = 2
h = 0.1

exacta_1 = f5_prime(x)
exacta_2 = f5_double_prime(x)

adelante = diferencia_adelante(f5, x, h)
atras = diferencia_atras(f5, x, h)
central = diferencia_central(f5, x, h)

print(f"Derivada exacta: {exacta_1:.8f}")
print(f"Diferencia hacia adelante: {adelante:.8f}, Error: {abs(exacta_1 - adelante):.8f}")
print(f"Diferencia hacia atrás: {atras:.8f}, Error: {abs(exacta_1 - atras):.8f}")
print(f"Diferencia central: {central:.8f}, Error: {abs(exacta_1 - central):.8f}")

print(f"\nSegunda derivada exacta: {exacta_2:.8f}")
aprox_2_central = segunda_derivada_central(f5, x, h)
print(f"Segunda derivada (centrales): {aprox_2_central:.8f}, Error: {abs(exacta_2 - aprox_2_central):.8f}")

# FUNCIONES PARA CALCULAR ACELERACIÓN CON DIFERENTES MÉTODOS
def aceleracion_progresiva(x, t, i, h):
    """Fórmula progresiva de 2do orden: a = (x[i+2] - 2*x[i+1] + x[i]) / h²"""
    return (x[i+2] - 2*x[i+1] + x[i]) / (h**2)

def aceleracion_central(x, t, i, h):
    """Fórmula central de 2do orden: a = (x[i+1] - 2*x[i] + x[i-1]) / h²"""
    return (x[i+1] - 2*x[i] + x[i-1]) / (h**2)

def aceleracion_regresiva(x, t, i, h):
    """Fórmula regresiva de 2do orden: a = (x[i] - 2*x[i-1] + x[i-2]) / h²"""
    return (x[i] - 2*x[i-1] + x[i-2]) / (h**2)

# Para espaciado irregular
def aceleracion_central_irregular(x, t, i):
    """Aceleración central para espaciado irregular"""
    h1 = t[i] - t[i-1]      # paso hacia atrás
    h2 = t[i+1] - t[i]      # paso hacia adelante
    
    # Fórmula para espaciado irregular (segunda derivada)
    return (2/(h1*(h1+h2))) * x[i-1] - (2/(h1*h2)) * x[i] + (2/(h2*(h1+h2))) * x[i+1]

# EJERCICIO 6: Análisis de movimiento con tabla de valores
print("\n\n6. ANÁLISIS DE MOVIMIENTO - TABLA 1")
print("-" * 40)

# Datos de la primera tabla
t1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
x1 = np.array([0, 1.5, 4, 7.5, 12, 17.5, 24, 31.5, 40], dtype=float)

# Calcular velocidad usando diferencias centrales
v1 = np.zeros_like(t1, dtype=float)
a1 = np.zeros_like(t1, dtype=float)

h = t1[1] - t1[0]  # paso constante = 1

# Velocidades (diferencias centrales para puntos interiores)
for i in range(1, len(t1)-1):
    v1[i] = (x1[i+1] - x1[i-1]) / (2 * h)

# Velocidades en los extremos (diferencias hacia adelante/atrás)
v1[0] = (x1[1] - x1[0]) / h
v1[-1] = (x1[-1] - x1[-2]) / h

# ACELERACIONES USANDO FÓRMULAS DE SEGUNDA DERIVADA DIRECTAMENTE
# Primer punto (progresiva)
a1[0] = aceleracion_progresiva(x1, t1, 0, h)

# Segundo punto (progresiva)
a1[1] = aceleracion_progresiva(x1, t1, 1, h)

# Puntos interiores (centrales)
for i in range(2, len(t1)-2):
    a1[i] = aceleracion_central(x1, t1, i, h)

# Penúltimo punto (regresiva)
a1[-2] = aceleracion_regresiva(x1, t1, len(x1)-2, h)

# Último punto (regresiva)
a1[-1] = aceleracion_regresiva(x1, t1, len(x1)-1, h)

# Headers para tabla de movimiento
t_header = "t(seg)"
x_header = "x(m)"
v_header = "v(m/s)"
a_header = "a(m/s²)"
metodo_header = "Método"

print(f"{t_header:<8} {x_header:<8} {v_header:<10} {a_header:<10} {metodo_header:<12}")
print("-" * 55)

metodos = ["Progresiva", "Progresiva", "Central", "Central", "Central", "Central", "Central", "Regresiva", "Regresiva"]

for i in range(len(t1)):
    print(f"{t1[i]:<8.0f} {x1[i]:<8.1f} {v1[i]:<10.2f} {a1[i]:<10.2f} {metodos[i]:<12}")

# EJERCICIO 7: Análisis de movimiento - Tabla 2
print("\n\n7. ANÁLISIS DE MOVIMIENTO - TABLA 2")
print("-" * 40)

# Datos de la segunda tabla
t2 = np.array([0, 2, 4.2, 6, 8, 10, 12, 14, 16], dtype=float)
x2 = np.array([0, 0.7, 1.8, 3.4, 5.1, 6.3, 7.3, 8.0, 8.4], dtype=float)

# Calcular velocidad y aceleración
v2 = np.zeros_like(t2, dtype=float)
a2 = np.zeros_like(t2, dtype=float)

# Velocidades usando diferencias centrales adaptadas para espaciado irregular
for i in range(1, len(t2)-1):
    h1 = t2[i] - t2[i-1]
    h2 = t2[i+1] - t2[i]
    v2[i] = (x2[i+1] - x2[i-1]) / (h1 + h2)

# Velocidades en los extremos
v2[0] = (x2[1] - x2[0]) / (t2[1] - t2[0])
v2[-1] = (x2[-1] - x2[-2]) / (t2[-1] - t2[-2])

# ACELERACIONES para espaciado irregular usando fórmulas de segunda derivada
# Primer punto: usar fórmula progresiva adaptada
h1 = t2[1] - t2[0]
h2 = t2[2] - t2[1]
a2[0] = (2/(h1*(h1+h2))) * x2[0] - (2/(h1*h2)) * x2[1] + (2/(h2*(h1+h2))) * x2[2]

# Puntos interiores: diferencias centrales para espaciado irregular
for i in range(1, len(t2)-1):
    a2[i] = aceleracion_central_irregular(x2, t2, i)

# Último punto: fórmula regresiva adaptada
h1 = t2[-2] - t2[-3]
h2 = t2[-1] - t2[-2]
a2[-1] = (2/(h1*(h1+h2))) * x2[-3] - (2/(h2*h1)) * x2[-2] + (2/(h2*(h1+h2))) * x2[-1]

metodos2 = ["Progresiva"] + ["Central"]*(len(t2)-2) + ["Regresiva"]

print(f"{t_header:<8} {x_header:<8} {v_header:<10} {a_header:<10} {metodo_header:<12}")
print("-" * 55)

for i in range(len(t2)):
    print(f"{t2[i]:<8.1f} {x2[i]:<8.1f} {v2[i]:<10.3f} {a2[i]:<10.3f} {metodos2[i]:<12}")

# Análisis del comportamiento
print("\n\nANÁLISIS DEL COMPORTAMIENTO:")
print("-" * 30)

print("\nTabla 1:")
print(f"- Velocidad promedio: {np.mean(v1[v1>0]):.2f} m/s")
print(f"- Aceleración promedio: {np.mean(a1[np.abs(a1)<10]):.2f} m/s²")
if np.std(a1[np.abs(a1)<10]) < 0.1:
    print("- Movimiento: Uniformemente acelerado (aceleración aproximadamente constante)")
else:
    print("- Movimiento: Aceleración variable")

print("\nTabla 2:")
print(f"- Velocidad promedio: {np.mean(v2[v2>0]):.3f} m/s")
print(f"- Aceleración promedio: {np.mean(a2[np.abs(a2)<10]):.3f} m/s²")
if np.mean(v2[4:]) < np.mean(v2[:4]):
    print("- Movimiento: Desacelerando (velocidad disminuye con el tiempo)")
else:
    print("- Movimiento: Acelerando")

print("\n\nFÓRMULAS UTILIZADAS:")
print("-" * 20)
print("Progresiva (2do orden): a = (x[i+2] - 2*x[i+1] + x[i]) / h²")
print("Central (2do orden):    a = (x[i+1] - 2*x[i] + x[i-1]) / h²")
print("Regresiva (2do orden):  a = (x[i] - 2*x[i-1] + x[i-2]) / h²")
print("Espaciado irregular:    Fórmulas adaptadas usando h1 y h2")

# Crear gráficos
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Gráfico 1: Posición vs Tiempo - Tabla 1
ax1.plot(t1, x1, 'bo-', label='Posición')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Posición (m)')
ax1.set_title('Tabla 1: Posición vs Tiempo')
ax1.grid(True)
ax1.legend()

# Gráfico 2: Velocidad vs Tiempo - Tabla 1
ax2.plot(t1, v1, 'ro-', label='Velocidad')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Velocidad (m/s)')
ax2.set_title('Tabla 1: Velocidad vs Tiempo')
ax2.grid(True)
ax2.legend()

# Gráfico 3: Posición vs Tiempo - Tabla 2
ax3.plot(t2, x2, 'go-', label='Posición')
ax3.set_xlabel('Tiempo (s)')
ax3.set_ylabel('Posición (m)')
ax3.set_title('Tabla 2: Posición vs Tiempo')
ax3.grid(True)
ax3.legend()

# Gráfico 4: Aceleración - Ambas tablas
ax4.plot(t1, a1, 'bo-', label='Tabla 1', alpha=0.7)
ax4.plot(t2, a2, 'ro-', label='Tabla 2', alpha=0.7)
ax4.set_xlabel('Tiempo (s)')
ax4.set_ylabel('Aceleración (m/s²)')
ax4.set_title('Comparación de Aceleraciones')
ax4.grid(True)
ax4.legend()

plt.tight_layout()
plt.show()

print(f"\n\nRESUMEN DE MÉTODOS APLICADOS:")
print("=" * 35)
print("- Primer punto: Fórmula PROGRESIVA de 2do orden")
print("- Puntos interiores: Fórmula CENTRAL de 2do orden")  
print("- Último punto: Fórmula REGRESIVA de 2do orden")
print("- Espaciado irregular: Fórmulas adaptadas para h1 ≠ h2")
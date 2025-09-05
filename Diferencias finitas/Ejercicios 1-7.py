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

# EJERCICIO 6: Análisis de movimiento con tabla de valores
print("\n\n6. ANÁLISIS DE MOVIMIENTO - TABLA 1")
print("-" * 40)

# Datos de la primera tabla
t1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
x1 = np.array([0, 1.5, 4, 7.5, 12, 17.5, 24, 31.5, 40])

# Calcular velocidad usando diferencias centrales
v1 = np.zeros_like(t1, dtype=float)
a1 = np.zeros_like(t1, dtype=float)

# Velocidades (diferencias centrales para puntos interiores)
for i in range(1, len(t1)-1):
    dt = t1[i+1] - t1[i-1]
    dx = x1[i+1] - x1[i-1]
    v1[i] = dx / dt

# Velocidades en los extremos (diferencias hacia adelante/atrás)
v1[0] = (x1[1] - x1[0]) / (t1[1] - t1[0])
v1[-1] = (x1[-1] - x1[-2]) / (t1[-1] - t1[-2])

# Aceleraciones
for i in range(1, len(t1)-1):
    dt = t1[i+1] - t1[i-1]
    dv = v1[i+1] - v1[i-1]
    a1[i] = dv / dt

# Aceleraciones en los extremos
a1[0] = (v1[1] - v1[0]) / (t1[1] - t1[0])
a1[-1] = (v1[-1] - v1[-2]) / (t1[-1] - t1[-2])

# Headers para tabla de movimiento
t_header = "t(seg)"
x_header = "x(m)"
v_header = "v(m/s)"
a_header = "a(m/s²)"

print(f"{t_header:<8} {x_header:<8} {v_header:<10} {a_header:<10}")
print("-" * 40)
for i in range(len(t1)):
    print(f"{t1[i]:<8} {x1[i]:<8} {v1[i]:<10.2f} {a1[i]:<10.2f}")

# EJERCICIO 7: Análisis de movimiento - Tabla 2
print("\n\n7. ANÁLISIS DE MOVIMIENTO - TABLA 2")
print("-" * 40)

# Datos de la segunda tabla
t2 = np.array([0, 2, 4.2, 6, 8, 10, 12, 14, 16])
x2 = np.array([0, 0.7, 1.8, 3.4, 5.1, 6.3, 7.3, 8.0, 8.4])

# Calcular velocidad y aceleración
v2 = np.zeros_like(t2, dtype=float)
a2 = np.zeros_like(t2, dtype=float)

# Velocidades usando diferencias centrales adaptadas para espaciado irregular
for i in range(1, len(t2)-1):
    # Para espaciado irregular, usamos la fórmula de diferencias centrales
    h1 = t2[i] - t2[i-1]
    h2 = t2[i+1] - t2[i]
    v2[i] = (x2[i+1] - x2[i-1]) / (h1 + h2)

# Velocidades en los extremos
v2[0] = (x2[1] - x2[0]) / (t2[1] - t2[0])
v2[-1] = (x2[-1] - x2[-2]) / (t2[-1] - t2[-2])

# Aceleraciones
for i in range(1, len(t2)-1):
    h1 = t2[i] - t2[i-1]
    h2 = t2[i+1] - t2[i]
    a2[i] = (v2[i+1] - v2[i-1]) / (h1 + h2)

a2[0] = (v2[1] - v2[0]) / (t2[1] - t2[0])
a2[-1] = (v2[-1] - v2[-2]) / (t2[-1] - t2[-2])

print(f"{t_header:<8} {x_header:<8} {v_header:<10} {a_header:<10}")
print("-" * 40)
for i in range(len(t2)):
    print(f"{t2[i]:<8} {x2[i]:<8} {v2[i]:<10.3f} {a2[i]:<10.3f}")

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

# Crear gráficos
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Gráfico 1: Posición vs Tiempo - Tabla 1
ax1.plot(t1, x1, 'bo-', label='Posición')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Posición (m)')
ax1.set_title('Tabla 1: Posición vs Tiempo')
ax1.grid
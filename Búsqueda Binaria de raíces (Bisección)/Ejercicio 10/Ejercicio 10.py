import numpy as np
import matplotlib.pyplot as plt

def g(x):
    """Función de iteración g(x) = √(x/3)"""
    if x < 0:
        return np.nan  # No definida para x < 0
    return np.sqrt(x / 3)

def g_prima(x):
    """Derivada de g(x): g'(x) = 1/(6√(x/3)) = 1/(2√(3x))"""
    if x <= 0:
        return np.inf
    return 1 / (2 * np.sqrt(3 * x))

def encontrar_punto_fijo_analitico():
    """
    Encuentra el punto fijo analíticamente
    x = √(x/3)
    x² = x/3
    3x² = x
    3x² - x = 0
    x(3x - 1) = 0
    Por tanto: x = 0 o x = 1/3
    """
    return [0, 1/3]

def encontrar_punto_fijo_numerico(x0, tolerancia=1e-12, max_iter=1000):
    """
    Encuentra el punto fijo usando iteración numérica
    """
    if x0 < 0:
        return np.nan, 0, False, []
        
    x = x0
    iteraciones = []
    
    try:
        for i in range(max_iter):
            iteraciones.append(x)
            x_nuevo = g(x)
            
            if np.isnan(x_nuevo):
                return np.nan, i + 1, False, iteraciones
            
            # Verificar convergencia
            if abs(x_nuevo - x) < tolerancia:
                return x_nuevo, i + 1, True, iteraciones
            
            x = x_nuevo
            
    except:
        return np.nan, i + 1, False, iteraciones
    
    return x, max_iter, False, iteraciones

def analizar_convergencia_teorica():
    """
    Analiza dónde converge teóricamente la iteración
    """
    print("=== ANÁLISIS TEÓRICO ===")
    print("Función: g(x) = √(x/3)")
    print("Dominio: x ≥ 0 (por la raíz cuadrada)")
    
    # Encontrar puntos fijos
    puntos_fijos = encontrar_punto_fijo_analitico()
    print(f"\nPuntos fijos:")
    for pf in puntos_fijos:
        print(f"  x* = {pf} → g({pf}) = {g(pf):.6f}")
    
    print(f"\nDerivada: g'(x) = 1/(2√(3x))")
    
    # Evaluar derivada en los puntos fijos
    print(f"\nEvaluación de la derivada en puntos fijos:")
    for pf in puntos_fijos:
        if pf > 0:
            derivada = g_prima(pf)
            print(f"  g'({pf}) = {derivada:.6f}")
            print(f"  |g'({pf})| = {abs(derivada):.6f} {'< 1' if abs(derivada) < 1 else '≥ 1'}")
        else:
            print(f"  g'({pf}) → ∞ (derivada no existe)")
    
    return puntos_fijos

def determinar_intervalo_convergencia():
    """
    Determina el intervalo donde |g'(x)| < 1
    """
    print(f"\n=== DETERMINACIÓN DEL INTERVALO ===")
    print("Para convergencia necesitamos |g'(x)| < 1")
    print("g'(x) = 1/(2√(3x)) < 1")
    print("1/(2√(3x)) < 1")
    print("1 < 2√(3x)")
    print("1/2 < √(3x)")
    print("1/4 < 3x")
    print("x > 1/12")
    
    limite_inferior = 1/12
    print(f"\nPor tanto: x > {limite_inferior:.6f} = {1/12}")
    
    # Como también necesitamos x ≥ 0 por el dominio
    print(f"Combinando con el dominio x ≥ 0:")
    print(f"El intervalo de convergencia teórica es: ({limite_inferior:.6f}, ∞)")
    
    return limite_inferior

def probar_convergencia_practica():
    """
    Prueba la convergencia con diferentes valores iniciales
    """
    limite_inferior = 1/12
    
    print(f"\n=== PRUEBAS PRÁCTICAS ===")
    
    # Valores de prueba
    valores_prueba = [
        0.01,      # Menor que 1/12
        limite_inferior - 0.001,  # Justo por debajo del límite
        limite_inferior,           # En el límite
        limite_inferior + 0.001,  # Justo por encima del límite
        0.1,       # Por encima del límite
        0.2,       # Más por encima
        0.5,       # Bastante por encima
        1.0,       # Muy por encima
        2.0        # Mucho más por encima
    ]
    
    print(f"Límite teórico: x > {limite_inferior:.6f}")
    print("\nResultados:")
    
    resultados = []
    
    for x0 in valores_prueba:
        punto_fijo, iteraciones, convergio, trayectoria = encontrar_punto_fijo_numerico(x0)
        
        if convergio:
            print(f"  x₀ = {x0:8.6f} → Converge a {punto_fijo:.8f} en {iteraciones:3d} iteraciones")
            resultados.append((x0, punto_fijo, iteraciones, True))
        else:
            print(f"  x₀ = {x0:8.6f} → No converge en {iteraciones} iteraciones")
            resultados.append((x0, punto_fijo, iteraciones, False))
    
    return resultados

# Ejecutar análisis completo
puntos_fijos = analizar_convergencia_teorica()
limite_inferior = determinar_intervalo_convergencia()
resultados = probar_convergencia_practica()

# Crear visualización
fig = plt.figure(figsize=(15, 10))

# Subplot 1: Función g(x) vs y=x
plt.subplot(2, 3, 1)
x_vals = np.linspace(0, 1, 1000)
y_g = [g(x) for x in x_vals]
plt.plot(x_vals, y_g, 'b-', label='g(x) = √(x/3)', linewidth=2)
plt.plot(x_vals, x_vals, 'r--', label='y = x', linewidth=2)

# Marcar puntos fijos
for pf in puntos_fijos:
    if 0 <= pf <= 1:
        plt.plot(pf, pf, 'ro', markersize=8, label=f'Punto fijo: x={pf:.3f}')

plt.grid(True, alpha=0.3)
plt.xlabel('x')
plt.ylabel('y')
plt.title('g(x) = √(x/3) vs y = x')
plt.legend()
plt.xlim(0, 1)
plt.ylim(0, 1)

# Subplot 2: Derivada g'(x)
plt.subplot(2, 3, 2)
x_vals_deriv = np.linspace(0.01, 1, 1000)  # Evitar x=0
y_g_prima = [g_prima(x) for x in x_vals_deriv]
plt.plot(x_vals_deriv, y_g_prima, 'g-', label="g'(x) = 1/(2√(3x))", linewidth=2)
plt.axhline(y=1, color='r', linestyle='--', label='y = 1', alpha=0.7)
plt.axvline(x=limite_inferior, color='orange', linestyle=':', label=f'x = 1/12 ≈ {limite_inferior:.3f}', alpha=0.7)

# Sombrear región de convergencia
x_conv = x_vals_deriv[x_vals_deriv > limite_inferior]
y_conv = [g_prima(x) for x in x_conv]
plt.fill_between(x_conv, 0, 1, alpha=0.2, color='green', label='Región de convergencia')

plt.grid(True, alpha=0.3)
plt.xlabel('x')
plt.ylabel("g'(x)")
plt.title("Derivada g'(x) y región de convergencia")
plt.legend()
plt.xlim(0, 0.5)
plt.ylim(0, 5)

# Subplot 3: Convergencia desde diferentes x₀
plt.subplot(2, 3, 3)
colores = ['red', 'blue', 'green', 'orange', 'purple']
x0_ejemplos = [0.05, 0.1, 0.2, 0.5, 1.0]

for i, x0 in enumerate(x0_ejemplos):
    x = x0
    x_iter = [x]
    
    for j in range(50):
        x = g(x)
        x_iter.append(x)
        if abs(x_iter[-1] - x_iter[-2]) < 1e-10:
            break
    
    plt.plot(range(len(x_iter)), x_iter, 'o-', 
             color=colores[i % len(colores)], 
             markersize=3, 
             label=f'x₀ = {x0}',
             alpha=0.7)

plt.grid(True, alpha=0.3)
plt.xlabel('Iteración')
plt.ylabel('x_n')
plt.title('Convergencia desde diferentes x₀')
plt.legend()

# Subplot 4: Método gráfico (telaraña)
plt.subplot(2, 3, 4)
x_vals = np.linspace(0, 0.6, 1000)
y_g = [g(x) for x in x_vals]
plt.plot(x_vals, y_g, 'b-', label='g(x) = √(x/3)', linewidth=2)
plt.plot(x_vals, x_vals, 'r--', label='y = x', linewidth=2)

# Mostrar iteraciones gráficamente para x₀ = 0.4
x0 = 0.4
x = x0
plt.plot(x0, 0, 'go', markersize=6, label=f'x₀ = {x0}')

for i in range(8):
    x_new = g(x)
    # Línea vertical: (x, x) → (x, g(x))
    plt.plot([x, x], [x, x_new], 'g-', alpha=0.6, linewidth=1)
    # Línea horizontal: (x, g(x)) → (g(x), g(x))
    plt.plot([x, x_new], [x_new, x_new], 'g-', alpha=0.6, linewidth=1)
    plt.plot(x, x_new, 'ro', markersize=2)
    x = x_new
    if abs(x - 1/3) < 0.001:  # Si está cerca del punto fijo
        break

plt.grid(True, alpha=0.3)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Método gráfico (telaraña)')
plt.legend()
plt.xlim(0, 0.6)
plt.ylim(0, 0.5)

# Subplot 5: Velocidad de convergencia
plt.subplot(2, 3, 5)
x0 = 0.5
x = x0
errores = []
x_exacto = 1/3

for i in range(30):
    error = abs(x - x_exacto)
    errores.append(error)
    x = g(x)
    if error < 1e-12:
        break

plt.semilogy(range(len(errores)), errores, 'bo-', markersize=4)
plt.grid(True, alpha=0.3)
plt.xlabel('Iteración')
plt.ylabel('Error |x_n - x*|')
plt.title(f'Velocidad de convergencia (x₀ = {x0})')

# Subplot 6: Comparación de derivadas en puntos fijos
plt.subplot(2, 3, 6)
x_pf = [1/3]  # Solo el punto fijo no trivial
derivadas = [g_prima(pf) for pf in x_pf]
colores_barras = ['green' if abs(d) < 1 else 'red' for d in derivadas]

plt.bar([f'x* = {pf:.3f}' for pf in x_pf], derivadas, color=colores_barras, alpha=0.7)
plt.axhline(y=1, color='red', linestyle='--', alpha=0.7)
plt.axhline(y=-1, color='red', linestyle='--', alpha=0.7)
plt.grid(True, alpha=0.3)
plt.ylabel("|g'(x*)|")
plt.title("Derivada en puntos fijos")
plt.ylim(0, 2)

plt.tight_layout()
plt.show()

print(f"\n=== RESPUESTA FINAL ===")
print(f"La función g(x) = √(x/3) tiene punto fijo en:")
print(f"• x* = 0 (trivial, pero g'(0) → ∞, no converge)")
print(f"• x* = 1/3 ≈ {1/3:.6f}")
print(f"")
print(f"Para convergencia necesitamos |g'(x)| < 1:")
print(f"• Esto ocurre cuando x > 1/12 ≈ {1/12:.6f}")
print(f"")
print(f"INTERVALO DE CONVERGENCIA: ({1/12:.6f}, ∞)")
print(f"")
print(f"En este intervalo:")
print(f"• La iteración converge al punto fijo x* = 1/3")
print(f"• La convergencia es más rápida cuanto mayor es x₀")
print(f"• Para x₀ ≤ 1/12, la convergencia es muy lenta o no hay convergencia")
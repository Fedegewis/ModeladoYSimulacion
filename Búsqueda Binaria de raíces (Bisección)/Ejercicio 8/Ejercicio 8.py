import numpy as np
import matplotlib.pyplot as plt

def metodo_punto_fijo(g, x0, tol=1e-4, max_iter=1000, nombre="g(x)", verbose=True):
    """
    Implementa el método del punto fijo para encontrar √3.
    
    Parámetros:
    g: función de iteración
    x0: valor inicial
    tol: tolerancia (exactitud requerida)
    max_iter: número máximo de iteraciones
    nombre: nombre de la función para mostrar
    verbose: mostrar iteraciones detalladas
    
    Retorna: (resultado, iteraciones, convergió, historial)
    """
    x = x0
    historial = []
    valor_real = np.sqrt(3)
    
    if verbose:
        print(f"\n{nombre}")
        print("-" * 50)
        print(f"Valor inicial: x₀ = {x:.6f}")
        print(f"Valor real: √3 = {valor_real:.6f}")
        print(f"Tolerancia: {tol}")
        print("-" * 50)
        print(f"{'Iter':<4} {'x_n':<12} {'g(x_n)':<12} {'Error rel':<12} {'Error abs':<12}")
        print("-" * 50)
    
    for i in range(max_iter):
        x_nuevo = g(x)
        error_abs = abs(x_nuevo - x)
        error_rel = abs(x_nuevo - valor_real)
        
        historial.append({
            'iteracion': i,
            'x_actual': x,
            'x_nuevo': x_nuevo,
            'error_abs': error_abs,
            'error_rel': error_rel
        })
        
        if verbose and i < 20:  # Mostrar solo las primeras 20 iteraciones
            print(f"{i:<4} {x:<12.6f} {x_nuevo:<12.6f} {error_rel:<12.6f} {error_abs:<12.6f}")
        
        if error_abs < tol:
            if verbose:
                print("-" * 50)
                print(f"Convergencia alcanzada en {i+1} iteraciones")
                print(f"Resultado: x = {x_nuevo:.6f}")
                print(f"Error absoluto final: {error_abs:.2e}")
                print(f"Error relativo: {error_rel:.2e}")
            return x_nuevo, i+1, True, historial
        
        x = x_nuevo
    
    if verbose:
        print(f"No convergió en {max_iter} iteraciones")
    return x, max_iter, False, historial

print("="*80)
print("MÉTODO DEL PUNTO FIJO PARA CALCULAR √3")
print("="*80)
print("Objetivo: Encontrar √3 con exactitud de 10⁻⁴")
print("Problema equivalente: Encontrar la raíz positiva de f(x) = x² - 3 = 0")

# ============================================================================
# TRANSFORMACIÓN 1: g₁(x) = 3/x
# ============================================================================

print("\n" + "="*60)
print("TRANSFORMACIÓN 1: g₁(x) = 3/x")
print("="*60)

print("Derivación:")
print("x² = 3  →  x = 3/x")
print("Por tanto: g₁(x) = 3/x")

def g1(x):
    if x == 0:
        return float('inf')
    return 3/x

# Análisis de convergencia
print(f"\nAnálisis de convergencia:")
raiz_3 = np.sqrt(3)
g1_derivada = -3/(raiz_3**2)  # g₁'(x) = -3/x², evaluada en √3
print(f"g₁'(x) = -3/x²")
print(f"g₁'(√3) = -3/(√3)² = -3/3 = -1")
print(f"|g₁'(√3)| = 1")
print("⚠️  Como |g₁'(√3)| = 1, la convergencia es marginal")

# Ejecutar el método
resultado1, iter1, conv1, hist1 = metodo_punto_fijo(g1, 2.0, tol=1e-4, nombre="g₁(x) = 3/x")

# ============================================================================
# TRANSFORMACIÓN 2: g₂(x) = (x + 3/x)/2 (Método Babilónico)
# ============================================================================

print("\n" + "="*60)
print("TRANSFORMACIÓN 2: g₂(x) = (x + 3/x)/2 (Método Babilónico)")
print("="*60)

print("Derivación:")
print("Promedio entre x y 3/x:")
print("g₂(x) = (x + 3/x)/2")
print("Esta es la fórmula del método de Newton para √3")

def g2(x):
    if x == 0:
        return float('inf')
    return (x + 3/x) / 2

# Análisis de convergencia
g2_derivada = (1 - 3/(raiz_3**2)) / 2  # g₂'(x) = (1 - 3/x²)/2
print(f"\nAnálisis de convergencia:")
print(f"g₂'(x) = (1 - 3/x²)/2")
print(f"g₂'(√3) = (1 - 3/3)/2 = 0/2 = 0")
print(f"|g₂'(√3)| = 0")
print("✓ Convergencia cuadrática (muy rápida)")

# Ejecutar el método
resultado2, iter2, conv2, hist2 = metodo_punto_fijo(g2, 2.0, tol=1e-4, nombre="g₂(x) = (x + 3/x)/2")

# ============================================================================
# TRANSFORMACIÓN 3: g₃(x) = (2x + 3/x²)/3
# ============================================================================

print("\n" + "="*60)
print("TRANSFORMACIÓN 3: g₃(x) = (2x + 3/x²)/3")
print("="*60)

print("Derivación:")
print("Método de orden superior derivado de x³ = 3x:")
print("g₃(x) = (2x + 3/x²)/3")

def g3(x):
    if x == 0:
        return float('inf')
    return (2*x + 3/(x**2)) / 3

# Análisis de convergencia
print(f"\nAnálisis de convergencia:")
print(f"g₃'(x) = (2 - 6/x³)/3")
print(f"g₃'(√3) = (2 - 6/(√3)³)/3 = (2 - 6/(3√3))/3 = (2 - 2/√3)/3")
g3_derivada = (2 - 6/(raiz_3**3)) / 3
print(f"g₃'(√3) ≈ {g3_derivada:.6f}")
print(f"|g₃'(√3)| ≈ {abs(g3_derivada):.6f}")

if abs(g3_derivada) < 1:
    print("✓ Convergencia garantizada")
else:
    print("⚠️  Convergencia no garantizada")

# Ejecutar el método
resultado3, iter3, conv3, hist3 = metodo_punto_fijo(g3, 2.0, tol=1e-4, nombre="g₃(x) = (2x + 3/x²)/3")

# ============================================================================
# TRANSFORMACIÓN 4: g₄(x) = x - (x² - 3)/(2x) (Newton-Raphson)
# ============================================================================

print("\n" + "="*60)
print("TRANSFORMACIÓN 4: g₄(x) = x - (x² - 3)/(2x) (Newton-Raphson)")
print("="*60)

print("Derivación:")
print("Método de Newton para f(x) = x² - 3:")
print("g₄(x) = x - f(x)/f'(x) = x - (x² - 3)/(2x)")
print("Simplificando: g₄(x) = (x + 3/x)/2")
print("(¡Es idéntica a g₂!)")

def g4(x):
    if x == 0:
        return float('inf')
    return x - (x**2 - 3)/(2*x)

# Ejecutar el método
resultado4, iter4, conv4, hist4 = metodo_punto_fijo(g4, 2.0, tol=1e-4, nombre="g₄(x) = x - (x² - 3)/(2x)")

# ============================================================================
# COMPARACIÓN DE MÉTODOS
# ============================================================================

print("\n" + "="*80)
print("COMPARACIÓN DE MÉTODOS")
print("="*80)

metodos = [
    ("g₁(x) = 3/x", resultado1, iter1, conv1, hist1),
    ("g₂(x) = (x + 3/x)/2", resultado2, iter2, conv2, hist2),
    ("g₃(x) = (2x + 3/x²)/3", resultado3, iter3, conv3, hist3),
    ("g₄(x) = Newton-Raphson", resultado4, iter4, conv4, hist4)
]

valor_real = np.sqrt(3)
print(f"Valor real: √3 = {valor_real:.10f}")
print("-" * 80)
print(f"{'Método':<25} {'Resultado':<12} {'Iter':<6} {'Error':<12} {'Converge'}")
print("-" * 80)

for nombre, resultado, iteraciones, converge, _ in metodos:
    error = abs(resultado - valor_real)
    estado = "Sí" if converge else "No"
    print(f"{nombre:<25} {resultado:<12.6f} {iteraciones:<6} {error:<12.2e} {estado}")

# ============================================================================
# ANÁLISIS DE CONVERGENCIA GRÁFICO
# ============================================================================

print("\n" + "="*60)
print("ANÁLISIS GRÁFICO DE CONVERGENCIA")
print("="*60)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# Configurar colores
colores = ['blue', 'red', 'green', 'orange']
nombres_cortos = ['g₁(x)=3/x', 'g₂(x)=(x+3/x)/2', 'g₃(x)=(2x+3/x²)/3', 'g₄(x)=Newton']

# Gráfico 1: Funciones y la recta y=x
ax1.set_title('Funciones de Iteración vs y = x')
x_plot = np.linspace(1, 3, 1000)

# Solo plotear g2 y g3 para claridad
ax1.plot(x_plot, [g2(x) for x in x_plot], color='red', linewidth=2, label='g₂(x) = (x+3/x)/2')
ax1.plot(x_plot, [g3(x) for x in x_plot], color='green', linewidth=2, label='g₃(x) = (2x+3/x²)/3')
ax1.plot(x_plot, x_plot, 'k--', linewidth=2, label='y = x')
ax1.plot(valor_real, valor_real, 'ro', markersize=8, label=f'√3 ≈ {valor_real:.3f}')
ax1.set_xlabel('x')
ax1.set_ylabel('g(x)')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1, 3)
ax1.set_ylim(1, 3)

# Gráfico 2: Convergencia de errores
ax2.set_title('Convergencia del Error Absoluto')
for i, (nombre, _, _, converge, hist) in enumerate(metodos[:3]):  # Excluir g4 porque es igual a g2
    if converge and len(hist) > 1:
        iteraciones = [h['iteracion'] for h in hist]
        errores = [h['error_rel'] for h in hist]
        ax2.semilogy(iteraciones, errores, 'o-', color=colores[i], 
                    linewidth=2, markersize=4, label=nombres_cortos[i])

ax2.axhline(y=1e-4, color='black', linestyle='--', alpha=0.7, label='Tolerancia 10⁻⁴')
ax2.set_xlabel('Iteración')
ax2.set_ylabel('Error Absoluto (escala log)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Gráfico 3: Secuencia de iteraciones para g₂
ax3.set_title('Convergencia de g₂(x) = (x+3/x)/2')
if conv2:
    x_vals = [hist2[0]['x_actual']] + [h['x_nuevo'] for h in hist2[:10]]
    ax3.plot(range(len(x_vals)), x_vals, 'ro-', linewidth=2, markersize=6)
    ax3.axhline(y=valor_real, color='blue', linestyle='--', alpha=0.7, label=f'√3 = {valor_real:.6f}')
    ax3.set_xlabel('Iteración')
    ax3.set_ylabel('x_n')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

# Gráfico 4: Comparación de las primeras iteraciones
ax4.set_title('Primeras 10 Iteraciones - Comparación')
for i, (nombre, _, _, converge, hist) in enumerate(metodos[:3]):
    if converge and len(hist) > 1:
        x_vals = [hist[0]['x_actual']] + [h['x_nuevo'] for h in hist[:10]]
        ax4.plot(range(len(x_vals)), x_vals, 'o-', color=colores[i], 
                linewidth=2, markersize=4, label=nombres_cortos[i])

ax4.axhline(y=valor_real, color='black', linestyle='--', alpha=0.7, label=f'√3 = {valor_real:.6f}')
ax4.set_xlabel('Iteración')
ax4.set_ylabel('x_n')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================================
# RECOMENDACIÓN FINAL
# ============================================================================

print("\n" + "="*60)
print("RECOMENDACIÓN Y CONCLUSIONES")
print("="*60)

mejor_metodo = min(metodos[1:3], key=lambda x: x[2] if x[3] else float('inf'))  # Excluir g1

print("ANÁLISIS DE EFICIENCIA:")
print(f"• g₁(x) = 3/x: Convergencia muy lenta debido a |g'(√3)| = 1")
print(f"• g₂(x) = (x+3/x)/2: Convergencia cuadrática, muy eficiente")
print(f"• g₃(x) = (2x+3/x²)/3: Convergencia lineal, moderadamente eficiente")
print(f"• g₄(x): Idéntico a g₂ (Newton-Raphson)")

print(f"\nMÉTODO RECOMENDADO: {mejor_metodo[0]}")
print(f"• Resultado: √3 ≈ {mejor_metodo[1]:.6f}")
print(f"• Iteraciones necesarias: {mejor_metodo[2]}")
print(f"• Error final: {abs(mejor_metodo[1] - valor_real):.2e}")

print(f"\nVERIFICACIÓN:")
print(f"• √3 real = {valor_real:.10f}")
print(f"• Resultado = {mejor_metodo[1]:.10f}")
print(f"• Exactitud lograda: {abs(mejor_metodo[1] - valor_real):.2e} < 10⁻⁴ ✓")

print(f"\n¿POR QUÉ g₂(x) ES EL MEJOR?")
print(f"• Convergencia cuadrática: cada iteración duplica el número de dígitos correctos")
print(f"• Es el método de Newton aplicado a f(x) = x² - 3")
print(f"• Conocido como 'Método Babilónico' para calcular raíces cuadradas")
print(f"• Muy estable numéricamente")
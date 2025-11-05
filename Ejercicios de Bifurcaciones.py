import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Configuración de matplotlib para mejores gráficos
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 10

# Definir los sistemas
def sistema1(x, r):
    return r + x**2

def sistema2(x, r):
    return r*x - x**2

def sistema3(x, r):
    return r*x - x**3

def sistema4(x, r):
    return r + 3*x - x**3

def sistema5(x, r):
    return r - np.exp(x)

def sistema6(x, r):
    return r - x**2

def sistema7(x, r):
    return r*x + x**3

def sistema8(x, r):
    return x**3 - r*x

def sistema9(x, r):
    return (r - 1) - (x - 1)**2

def sistema10(x, r):
    return (r - 2)*x - x**2

def sistema11(x, r):
    return (r - 3)*x - x**3

def sistema12(x, r):
    return r - (x - 2)**2

def sistema13(x, r):
    return (r - 1)*(x - 1) - (x - 1)**2

def sistema14(x, r, k=1, h=1):
    return r*x*(1 - x/k) - h

# Función para encontrar puntos fijos
def encontrar_puntos_fijos(func, r_val, x_range=(-10, 10), num_guesses=50):
    puntos = []
    guesses = np.linspace(x_range[0], x_range[1], num_guesses)
    
    for guess in guesses:
        try:
            sol = fsolve(lambda x: func(x, r_val), guess, full_output=True)
            if sol[2] == 1:  # Solución convergió
                x_sol = sol[0][0]
                if x_range[0] <= x_sol <= x_range[1]:
                    # Evitar duplicados
                    if not any(abs(x_sol - p) < 1e-6 for p in puntos):
                        puntos.append(x_sol)
        except:
            pass
    
    return sorted(puntos)

# Función para determinar estabilidad
def estabilidad(func, x_val, r_val, epsilon=1e-6):
    df_dx = (func(x_val + epsilon, r_val) - func(x_val - epsilon, r_val)) / (2 * epsilon)
    return df_dx < 0  # Estable si df/dx < 0

# Función para analizar un sistema
def analizar_sistema(func, num_sistema, r_range, titulo, x_range=(-5, 5)):
    r_vals = np.linspace(r_range[0], r_range[1], 500)
    
    puntos_estables = []
    puntos_inestables = []
    
    for r in r_vals:
        puntos = encontrar_puntos_fijos(func, r, x_range)
        for x in puntos:
            if estabilidad(func, x, r):
                puntos_estables.append((r, x))
            else:
                puntos_inestables.append((r, x))
    
    # Crear diagrama de bifurcación
    plt.subplot(4, 4, num_sistema)
    
    if puntos_estables:
        r_est, x_est = zip(*puntos_estables)
        plt.plot(r_est, x_est, 'b-', linewidth=2, label='Estable')
    
    if puntos_inestables:
        r_inest, x_inest = zip(*puntos_inestables)
        plt.plot(r_inest, x_inest, 'r--', linewidth=1.5, label='Inestable')
    
    plt.xlabel('r')
    plt.ylabel('x*')
    plt.title(f'{num_sistema}. {titulo}', fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=7)
    
    # Análisis de bifurcación
    return analizar_bifurcacion(puntos_estables, puntos_inestables, r_range)

def analizar_bifurcacion(estables, inestables, r_range):
    info = {}
    
    # Contar cambios en el número de puntos fijos
    r_vals = np.linspace(r_range[0], r_range[1], 100)
    num_puntos_prev = 0
    
    for r in r_vals:
        num_puntos = sum(1 for p in estables if abs(p[0] - r) < 0.05)
        num_puntos += sum(1 for p in inestables if abs(p[0] - r) < 0.05)
        
        if num_puntos != num_puntos_prev and num_puntos_prev > 0:
            info['bifurcacion'] = f"r ≈ {r:.2f}"
            break
        num_puntos_prev = num_puntos
    
    return info

# Crear figura con todos los diagramas
plt.figure(figsize=(20, 20))

# Sistema 1: ẋ = r + x²
analizar_sistema(sistema1, 1, (-2, 2), 'ẋ = r + x²', x_range=(-3, 3))

# Sistema 2: ẋ = rx - x²
analizar_sistema(sistema2, 2, (-1, 3), 'ẋ = rx - x²', x_range=(-1, 4))

# Sistema 3: ẋ = rx - x³
analizar_sistema(sistema3, 3, (-2, 2), 'ẋ = rx - x³', x_range=(-3, 3))

# Sistema 4: ẋ = r + 3x - x³
analizar_sistema(sistema4, 4, (-5, 5), 'ẋ = r + 3x - x³', x_range=(-4, 4))

# Sistema 5: ẋ = r - eˣ
analizar_sistema(sistema5, 5, (-2, 2), 'ẋ = r - eˣ', x_range=(-3, 3))

# Sistema 6: ẋ = r - x²
analizar_sistema(sistema6, 6, (-1, 2), 'ẋ = r - x²', x_range=(-3, 3))

# Sistema 7: ẋ = rx + x³
analizar_sistema(sistema7, 7, (-2, 2), 'ẋ = rx + x³', x_range=(-3, 3))

# Sistema 8: ẋ = x³ - rx
analizar_sistema(sistema8, 8, (-2, 2), 'ẋ = x³ - rx', x_range=(-3, 3))

# Sistema 9: ẋ = (r-1) - (x-1)²
analizar_sistema(sistema9, 9, (0, 3), 'ẋ = (r-1) - (x-1)²', x_range=(-2, 4))

# Sistema 10: ẋ = (r-2)x - x²
analizar_sistema(sistema10, 10, (0, 5), 'ẋ = (r-2)x - x²', x_range=(-1, 5))

# Sistema 11: ẋ = (r-3)x - x³
analizar_sistema(sistema11, 11, (1, 5), 'ẋ = (r-3)x - x³', x_range=(-3, 3))

# Sistema 12: ẋ = r - (x-2)²
analizar_sistema(sistema12, 12, (-1, 2), 'ẋ = r - (x-2)²', x_range=(0, 4))

# Sistema 13: ẋ = (r-1)(x-1) - (x-1)²
analizar_sistema(sistema13, 13, (0, 3), 'ẋ = (r-1)(x-1) - (x-1)²', x_range=(-1, 4))

# Sistema 14: ẋ = rx(1-x/k) - h
def sistema14_especifico(x, r):
    return sistema14(x, r, k=2, h=0.5)

analizar_sistema(sistema14_especifico, 14, (0, 4), 'ẋ = rx(1-x/k) - h', x_range=(-1, 3))

plt.tight_layout()
plt.savefig('diagramas_bifurcacion.png', dpi=300, bbox_inches='tight')
plt.show()

# Análisis detallado impreso
print("=" * 80)
print("ANÁLISIS DE BIFURCACIONES - RESUMEN")
print("=" * 80)

sistemas = [
    (sistema1, "ẋ = r + x²", (-2, 2), "Bifurcación silla-nodo en r=0"),
    (sistema2, "ẋ = rx - x²", (-1, 3), "Bifurcación transcrítica en r=0"),
    (sistema3, "ẋ = rx - x³", (-2, 2), "Bifurcación de horquilla supercrítica en r=0"),
    (sistema4, "ẋ = r + 3x - x³", (-5, 5), "Bifurcaciones múltiples"),
    (sistema5, "ẋ = r - eˣ", (-2, 2), "Bifurcación silla-nodo"),
    (sistema6, "ẋ = r - x²", (-1, 2), "Bifurcación silla-nodo en r=0"),
    (sistema7, "ẋ = rx + x³", (-2, 2), "Bifurcación de horquilla subcrítica en r=0"),
    (sistema8, "ẋ = x³ - rx", (-2, 2), "Bifurcación de horquilla supercrítica en r=0"),
    (sistema9, "ẋ = (r-1) - (x-1)²", (0, 3), "Bifurcación silla-nodo en r=1"),
    (sistema10, "ẋ = (r-2)x - x²", (0, 5), "Bifurcación transcrítica en r=2"),
    (sistema11, "ẋ = (r-3)x - x³", (1, 5), "Bifurcación de horquilla en r=3"),
    (sistema12, "ẋ = r - (x-2)²", (-1, 2), "Bifurcación silla-nodo en r=0"),
    (sistema13, "ẋ = (r-1)(x-1) - (x-1)²", (0, 3), "Bifurcación transcrítica en r=1"),
    (sistema14_especifico, "ẋ = rx(1-x/k) - h", (0, 4), "Bifurcación silla-nodo")
]

for i, (func, nombre, r_range, tipo_bif) in enumerate(sistemas, 1):
    print(f"\n{i}. {nombre}")
    print(f"   Tipo de bifurcación: {tipo_bif}")
    
    # Encontrar puntos fijos para algunos valores de r
    r_test = [r_range[0], (r_range[0] + r_range[1])/2, r_range[1]]
    
    for r in r_test:
        puntos = encontrar_puntos_fijos(func, r)
        if puntos:
            print(f"   r = {r:.2f}: Puntos fijos: {[f'{p:.3f}' for p in puntos]}")
            for p in puntos:
                est = "estable" if estabilidad(func, p, r) else "inestable"
                print(f"            x* = {p:.3f} ({est})")

print("\n" + "=" * 80)
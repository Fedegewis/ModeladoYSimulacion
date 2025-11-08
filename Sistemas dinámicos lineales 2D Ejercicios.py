

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.linalg import eig

# Definir todos los sistemas
sistemas = {
    1: {'eq': 'ẋ = x, ẏ = y', 'A': np.array([[1, 0], [0, 1]])},
    2: {'eq': 'ẋ = -y, ẏ = x', 'A': np.array([[0, -1], [1, 0]])},
    3: {'eq': 'ẋ = x, ẏ = -y', 'A': np.array([[1, 0], [0, -1]])},
    4: {'eq': 'ẋ = y - x, ẏ = -y - x', 'A': np.array([[-1, 1], [-1, -1]])},
    5: {'eq': 'ẋ = x + y, ẏ = x + y', 'A': np.array([[1, 1], [1, 1]])},
    6: {'eq': 'ẋ = -y, ẏ = x', 'A': np.array([[0, -1], [1, 0]])},
    7: {'eq': 'ẋ = 2y, ẏ = 2x', 'A': np.array([[0, 2], [2, 0]])},
    8: {'eq': 'ẋ = -y + x, ẏ = x + y', 'A': np.array([[1, -1], [1, 1]])},
    9: {'eq': 'ẋ = x - 2y, ẏ = -2x + y', 'A': np.array([[1, -2], [-2, 1]])},
    10: {'eq': 'ẋ = x + 2y, ẏ = 4x + 3y', 'A': np.array([[1, 2], [4, 3]])},
    11: {'eq': 'ẋ = x - 2y, ẏ = x + y', 'A': np.array([[1, -2], [1, 1]])},
    12: {'eq': 'ẋ = x - y, ẏ = 3x + 3y', 'A': np.array([[1, -1], [3, 3]])},
    13: {'eq': 'ẋ = -4x + 3y, ẏ = -6x + 5y', 'A': np.array([[-4, 3], [-6, 5]])},
    14: {'eq': 'ẋ = 6x - y, ẏ = 5x + 4y', 'A': np.array([[6, -1], [5, 4]])},
    15: {'eq': 'ẋ = x + 2y, ẏ = 2x - 4y', 'A': np.array([[1, 2], [2, -4]])},
    16: {'eq': 'ẋ = 2x - 5y, ẏ = 4x - 2y', 'A': np.array([[2, -5], [4, -2]])},
    17: {'eq': 'ẋ = -5x + 2y, ẏ = -10x + 3y', 'A': np.array([[-5, 2], [-10, 3]])},
    18: {'eq': 'ẋ = -2x + 3y, ẏ = -6x + 4y', 'A': np.array([[-2, 3], [-6, 4]])},
    19: {'eq': 'ẋ = 5x - 4y, ẏ = x + y', 'A': np.array([[5, -4], [1, 1]])},
    20: {'eq': 'ẋ = 3x + y, ẏ = x + 3y', 'A': np.array([[3, 1], [1, 3]])},
    21: {'eq': 'ẋ = y, ẏ = 6x + y', 'A': np.array([[0, 1], [6, 1]])},
    22: {'eq': 'ẋ = 2x - 2y, ẏ = 4x - 2y', 'A': np.array([[2, -2], [4, -2]])},
    23: {'eq': 'ẋ = x + 2y, ẏ = 2x + y', 'A': np.array([[1, 2], [2, 1]])},
    24: {'eq': 'ẋ = 2x + 3y, ẏ = 2x + y', 'A': np.array([[2, 3], [2, 1]])},
    25: {'eq': 'ẋ = -3x - 4y, ẏ = 2x + y', 'A': np.array([[-3, -4], [2, 1]])},
    26: {'eq': 'ẋ = 3x - y, ẏ = 9x - 3y', 'A': np.array([[3, -1], [9, -3]])},
    27: {'eq': 'ẋ = -2x + y, ẏ = x - 2y', 'A': np.array([[-2, 1], [1, -2]])},
    28: {'eq': 'ẋ = x + 3y, ẏ = x - y', 'A': np.array([[1, 3], [1, -1]])},
}

def clasificar_equilibrio(eigenvalues):
    """Clasificar el punto de equilibrio según los autovalores"""
    lambda1, lambda2 = eigenvalues
    
    # Verificar si son complejos
    if np.iscomplex(lambda1) or np.iscomplex(lambda2):
        parte_real = np.real(lambda1)
        if abs(parte_real) < 1e-10:
            return "Centro (órbitas cerradas)"
        elif parte_real > 0:
            return "Espiral inestable"
        else:
            return "Espiral estable"
    
    # Autovalores reales
    lambda1, lambda2 = np.real(lambda1), np.real(lambda2)
    
    if abs(lambda1) < 1e-10 or abs(lambda2) < 1e-10:
        return "Línea de equilibrios"
    elif lambda1 * lambda2 < 0:
        return "Punto silla (inestable)"
    elif lambda1 > 0 and lambda2 > 0:
        return "Nodo inestable (fuente)"
    else:
        return "Nodo estable (sumidero)"

def sistema_dinamico(X, t, A):
    """Función que define el sistema dinámico"""
    return A @ X

def analizar_sistema(num_sistema, t_max=5, mostrar=True):
    """
    Analizar completamente un sistema dinámico
    
    Parámetros:
    -----------
    num_sistema : int
        Número del sistema (1-28)
    t_max : float
        Tiempo máximo de simulación
    mostrar : bool
        Si True, muestra los gráficos
    """
    
    sistema = sistemas[num_sistema]
    A = sistema['A']
    
    print("="*80)
    print(f"SISTEMA {num_sistema}: {sistema['eq']}")
    print("="*80)
    
    # m) Calcular autovalores y autovectores
    eigenvalues, eigenvectors = eig(A)
    
    print("\n📊 MATRIZ DEL SISTEMA:")
    print(f"A = \n{A}")
    
    print("\n🔢 AUTOVALORES:")
    for i, val in enumerate(eigenvalues, 1):
        if np.iscomplex(val):
            print(f"λ{i} = {val.real:.4f} + {val.imag:.4f}i")
        else:
            print(f"λ{i} = {val.real:.4f}")
    
    print("\n📐 AUTOVECTORES:")
    for i in range(len(eigenvectors)):
        v = eigenvectors[:, i]
        if np.iscomplex(v[0]) or np.iscomplex(v[1]):
            print(f"v{i+1} = [{v[0].real:.4f} + {v[0].imag:.4f}i, {v[1].real:.4f} + {v[1].imag:.4f}i]ᵀ")
        else:
            print(f"v{i+1} = [{v[0].real:.4f}, {v[1].real:.4f}]ᵀ")
    
    # n) Punto de equilibrio y clasificación
    tipo = clasificar_equilibrio(eigenvalues)
    print(f"\n⚖️ PUNTO DE EQUILIBRIO: (0, 0)")
    print(f"📌 TIPO: {tipo}")
    
    # p) y q) Graficar diagrama de fase y soluciones
    if mostrar:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # ===== DIAGRAMA DE FASE =====
        # Condiciones iniciales
        condiciones_iniciales = [
            [1, 0], [0, 1], [-1, 0], [0, -1],
            [0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5], [0.5, -0.5]
        ]
        
        colores = plt.cm.rainbow(np.linspace(0, 1, len(condiciones_iniciales)))
        
        # Tiempo de simulación
        t = np.linspace(0, t_max, 1000)
        
        # Simular trayectorias
        for i, X0 in enumerate(condiciones_iniciales):
            sol = odeint(sistema_dinamico, X0, t, args=(A,))
            ax1.plot(sol[:, 0], sol[:, 1], color=colores[i], linewidth=1.5, alpha=0.7)
            ax1.plot(X0[0], X0[1], 'o', color=colores[i], markersize=8)
        
        # Campo vectorial
        x_range = np.linspace(-2, 2, 20)
        y_range = np.linspace(-2, 2, 20)
        X_grid, Y_grid = np.meshgrid(x_range, y_range)
        
        U = A[0, 0] * X_grid + A[0, 1] * Y_grid
        V = A[1, 0] * X_grid + A[1, 1] * Y_grid
        
        # Normalizar vectores para mejor visualización
        M = np.sqrt(U**2 + V**2)
        M[M == 0] = 1
        U_norm = U / M
        V_norm = V / M
        
        ax1.quiver(X_grid, Y_grid, U_norm, V_norm, M, alpha=0.3, cmap='gray')
        
        # Punto de equilibrio
        ax1.plot(0, 0, 'ko', markersize=12, markerfacecolor='red', 
                label='Equilibrio (0,0)', zorder=5)
        
        # Dibujar autovectores si son reales
        if not np.iscomplex(eigenvalues[0]):
            for i in range(2):
                v = np.real(eigenvectors[:, i])
                # Normalizar para visualización
                v_norm = v / np.linalg.norm(v) * 1.5
                ax1.arrow(0, 0, v_norm[0], v_norm[1], head_width=0.1, 
                         head_length=0.1, fc='blue', ec='blue', 
                         linewidth=2, alpha=0.6, zorder=4)
                ax1.arrow(0, 0, -v_norm[0], -v_norm[1], head_width=0.1, 
                         head_length=0.1, fc='blue', ec='blue', 
                         linewidth=2, alpha=0.6, zorder=4)
        
        ax1.set_xlabel('x', fontsize=12)
        ax1.set_ylabel('y', fontsize=12)
        ax1.set_title(f'Diagrama de Fase - Sistema {num_sistema}\n{tipo}', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axis('equal')
        ax1.legend()
        
        # ===== EVOLUCIÓN TEMPORAL =====
        X0 = [1, 0.5]  # Condición inicial para evolución temporal
        sol = odeint(sistema_dinamico, X0, t, args=(A,))
        
        ax2.plot(t, sol[:, 0], 'r-', linewidth=2, label='x(t)')
        ax2.plot(t, sol[:, 1], 'b-', linewidth=2, label='y(t)')
        ax2.set_xlabel('Tiempo (t)', fontsize=12)
        ax2.set_ylabel('x(t), y(t)', fontsize=12)
        ax2.set_title(f'Evolución Temporal\nCondición inicial: x₀={X0[0]}, y₀={X0[1]}', 
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=11)
        
        plt.tight_layout()
        plt.savefig(f'sistema_{num_sistema}.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # o) Fórmula de solución general
    print("\n📝 SOLUCIÓN GENERAL:")
    if np.iscomplex(eigenvalues[0]):
        alpha = np.real(eigenvalues[0])
        beta = np.imag(eigenvalues[0])
        print(f"Autovalores complejos: λ = {alpha:.4f} ± {beta:.4f}i")
        print(f"x(t) = e^({alpha:.4f}t)[c₁cos({beta:.4f}t) + c₂sin({beta:.4f}t)]")
        print(f"y(t) = e^({alpha:.4f}t)[c₃cos({beta:.4f}t) + c₄sin({beta:.4f}t)]")
    else:
        l1, l2 = np.real(eigenvalues[0]), np.real(eigenvalues[1])
        v1, v2 = np.real(eigenvectors[:, 0]), np.real(eigenvectors[:, 1])
        print(f"x(t) = c₁·e^({l1:.4f}t)·[{v1[0]:.4f}] + c₂·e^({l2:.4f}t)·[{v2[0]:.4f}]")
        print(f"y(t) = c₁·e^({l1:.4f}t)·[{v1[1]:.4f}] + c₂·e^({l2:.4f}t)·[{v2[1]:.4f}]")
    
    print("\n" + "="*80 + "\n")
    
    return eigenvalues, eigenvectors, tipo

# ============================================================================
# EJECUTAR ANÁLISIS PARA TODOS LOS SISTEMAS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🎯 "*20)
    print("ANÁLISIS COMPLETO DE SISTEMAS DINÁMICOS LINEALES 2D")
    print("🎯 "*20 + "\n")
    
    # Analizar un sistema específico (cambiar el número aquí)
    SISTEMA_A_ANALIZAR = 1  # <--- CAMBIA ESTE NÚMERO (1-28)
    
    analizar_sistema(SISTEMA_A_ANALIZAR, t_max=5, mostrar=True)
    
    # Si quieres analizar TODOS los sistemas (solo texto, sin gráficos):
    print("\n" + "📊 "*20)
    print("RESUMEN DE TODOS LOS SISTEMAS")
    print("📊 "*20 + "\n")
    
    resumen = []
    for i in range(1, 29):
        eigenvalues, _, tipo = analizar_sistema(i, mostrar=False)
        resumen.append({
            'Sistema': i,
            'Ecuación': sistemas[i]['eq'],
            'Tipo': tipo,
            'λ1': eigenvalues[0],
            'λ2': eigenvalues[1]
        })
    
    # Imprimir tabla resumen
    print("\n" + "="*100)
    print(f"{'Sist':<6} {'Tipo de Equilibrio':<30} {'λ₁':<25} {'λ₂':<25}")
    print("="*100)
    for item in resumen:
        l1 = f"{item['λ1'].real:.3f}+{item['λ1'].imag:.3f}i" if np.iscomplex(item['λ1']) else f"{item['λ1'].real:.3f}"
        l2 = f"{item['λ2'].real:.3f}+{item['λ2'].imag:.3f}i" if np.iscomplex(item['λ2']) else f"{item['λ2'].real:.3f}"
        print(f"{item['Sistema']:<6} {item['Tipo']:<30} {l1:<25} {l2:<25}")
    print("="*100)
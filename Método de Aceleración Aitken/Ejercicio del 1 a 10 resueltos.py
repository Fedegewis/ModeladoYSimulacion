import numpy as np
import matplotlib.pyplot as plt

def aitken_acceleration(g, x0, max_iter=50, tol=1e-10):
    """
    Implementa el Método de Aceleración de Aitken
    
    Parámetros:
    g: función de iteración g(x)
    x0: valor inicial
    max_iter: número máximo de iteraciones
    tol: tolerancia para convergencia
    
    Retorna:
    x_aitken: aproximación mejorada
    iterations: lista de todas las iteraciones
    converged: True si convergió
    """
    
    # Listas para almacenar los valores
    x_values = [x0]
    x_aitken_values = []
    
    x_n = x0
    
    for i in range(max_iter):
        try:
            # Calculamos tres iteraciones consecutivas del punto fijo
            x_n1 = g(x_n)
            x_n2 = g(x_n1) 
            x_n3 = g(x_n2)
            
            # Aplicamos la fórmula de Aitken
            denominator = x_n3 - 2*x_n2 + x_n1
            
            if abs(denominator) < 1e-15:
                print(f"Denominador muy pequeño en iteración {i+1}, usando punto fijo normal")
                x_aitken = x_n3
            else:
                numerator = (x_n2 - x_n1)**2
                x_aitken = x_n1 - numerator / denominator
            
            x_values.extend([x_n1, x_n2, x_n3])
            x_aitken_values.append(x_aitken)
            
            # Verificar convergencia
            if i > 0 and abs(x_aitken - x_aitken_values[-2]) < tol:
                return x_aitken, x_values, x_aitken_values, True, i+1
                
            # Preparar siguiente iteración
            x_n = x_aitken
            
        except (OverflowError, ValueError, ZeroDivisionError) as e:
            print(f"Error en iteración {i+1}: {e}")
            break
    
    return x_aitken_values[-1] if x_aitken_values else x0, x_values, x_aitken_values, False, max_iter

def punto_fijo_normal(g, x0, max_iter=50, tol=1e-10):
    """Método de punto fijo normal para comparación"""
    x = x0
    values = [x0]
    
    for i in range(max_iter):
        try:
            x_new = g(x)
            values.append(x_new)
            
            if abs(x_new - x) < tol:
                return x_new, values, True, i+1
            x = x_new
        except:
            break
    
    return x, values, False, max_iter

# Definir las funciones para cada ejercicio
def ejercicio_1():
    print("="*60)
    print("EJERCICIO 1: f(x) = π/2 * x² - x - 2, x₀ = 1.4")
    print("Buscamos la raíz, convertimos a g(x) = x + π/2 * x² - x - 2 = π/2 * x² - 2")
    
    def g(x):
        return np.pi/2 * x**2 - 2
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 1.4)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 1.4)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_2():
    print("="*60)
    print("EJERCICIO 2: f(x) = cos(x) - x, x₀ = 0.5")
    print("Convertimos a g(x) = cos(x)")
    
    def g(x):
        return np.cos(x)
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 0.5)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 0.5)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_3():
    print("="*60)
    print("EJERCICIO 3: g(x) = ∛(3x² - 4x + 1), x₀ = 0.3")
    
    def g(x):
        return (3*x**2 - 4*x + 1)**(1/3)
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 0.3)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 0.3)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_4():
    print("="*60)
    print("EJERCICIO 4: g(x) = e^(-x), x₀ = 1")
    
    def g(x):
        return np.exp(-x)
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 1)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 1)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_5():
    print("="*60)
    print("EJERCICIO 5: g(x) = √(3x - 2), x₀ = 2")
    
    def g(x):
        if 3*x - 2 < 0:
            return x  # Evitar raíz de número negativo
        return np.sqrt(3*x - 2)
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 2)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 2)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_6():
    print("="*60)
    print("EJERCICIO 6: g(x) = ln(x + 1), x₀ = 0.5")
    
    def g(x):
        if x <= -1:
            return x  # Evitar ln de número no positivo
        return np.log(x + 1)
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 0.5)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 0.5)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_7():
    print("="*60)
    print("EJERCICIO 7: g(x) = 1 - x³, x₀ = 0.5")
    
    def g(x):
        return 1 - x**3
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 0.5)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 0.5)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_8():
    print("="*60)
    print("EJERCICIO 8: g(x) = 1/2(x² - 3), x₀ = 0.5")
    
    def g(x):
        return 0.5 * (x**2 - 3)
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 0.5)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 0.5)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_9():
    print("="*60)
    print("EJERCICIO 9: g(x) = (sin(x) + 5)/x², x₀ = 2")
    
    def g(x):
        if abs(x) < 1e-10:
            return x  # Evitar división por cero
        return (np.sin(x) + 5) / (x**2)
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 2)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 2)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_10():
    print("="*60)
    print("EJERCICIO 10: g(x) = x², probando x₀ = 0.4, 0.9, 1.5")
    
    def g(x):
        return x**2
    
    for x0 in [0.4, 0.9, 1.5]:
        print(f"\nCon x₀ = {x0}:")
        resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, x0)
        resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, x0)
        
        print(f"  Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
        print(f"  Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
        print(f"  Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def ejercicio_11():
    print("="*60)
    print("EJERCICIO 11: g(x) = 3/2 * x + 1/x², x₀ = 0.25")
    
    def g(x):
        if abs(x) < 1e-10:
            return x  # Evitar división por cero
        return 1.5 * x + 1 / (x**2)
    
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, 0.25)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, 0.25)
    
    print(f"Aitken: x = {resultado_aitken:.10f} en {iter_aitken} iteraciones")
    print(f"Punto fijo normal: x = {resultado_normal:.10f} en {iter_normal} iteraciones")
    print(f"Verificación g({resultado_aitken:.6f}) = {g(resultado_aitken):.10f}")

def graficar_convergencia(ejercicio_num, g, x0, titulo):
    """Función para graficar la convergencia"""
    resultado_aitken, vals_aitken, aitken_vals, conv_aitken, iter_aitken = aitken_acceleration(g, x0, max_iter=20)
    resultado_normal, vals_normal, conv_normal, iter_normal = punto_fijo_normal(g, x0, max_iter=20)
    
    plt.figure(figsize=(12, 5))
    
    # Gráfica de convergencia
    plt.subplot(1, 2, 1)
    if len(vals_normal) > 1:
        plt.semilogy(range(len(vals_normal)), [abs(x - resultado_normal) for x in vals_normal], 
                     'b-o', label='Punto Fijo Normal', markersize=4)
    if len(aitken_vals) > 1:
        plt.semilogy(range(len(aitken_vals)), [abs(x - resultado_aitken) for x in aitken_vals], 
                     'r-s', label='Aitken', markersize=4)
    
    plt.xlabel('Iteración')
    plt.ylabel('Error absoluto')
    plt.title(f'Convergencia - {titulo}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfica de la función
    plt.subplot(1, 2, 2)
    x_range = np.linspace(max(0.1, x0-2), x0+2, 1000)
    try:
        y_range = [g(x) for x in x_range]
        plt.plot(x_range, y_range, 'b-', label='g(x)')
        plt.plot(x_range, x_range, 'k--', alpha=0.5, label='y=x')
        plt.plot(x0, g(x0), 'go', markersize=8, label=f'Inicio x₀={x0}')
        plt.plot(resultado_aitken, resultado_aitken, 'ro', markersize=8, label=f'Aitken: {resultado_aitken:.4f}')
        plt.xlabel('x')
        plt.ylabel('g(x)')
        plt.title(f'Función g(x) - {titulo}')
        plt.legend()
        plt.grid(True, alpha=0.3)
    except:
        plt.text(0.5, 0.5, 'Error al graficar\nla función', 
                ha='center', va='center', transform=plt.gca().transAxes)
    
    plt.tight_layout()
    plt.show()

# Ejecutar todos los ejercicios
if __name__ == "__main__":
    print("MÉTODO DE ACELERACIÓN DE AITKEN")
    print("Resolviendo todos los ejercicios...\n")
    
    # Ejecutar todos los ejercicios
    ejercicio_1()
    ejercicio_2()
    ejercicio_3()
    ejercicio_4()
    ejercicio_5()
    ejercicio_6()
    ejercicio_7()
    ejercicio_8()
    ejercicio_9()
    ejercicio_10()
    ejercicio_11()
    
    print("\n" + "="*60)
    print("ANÁLISIS GRÁFICO DE ALGUNOS EJERCICIOS")
    print("="*60)
    
    # Graficar algunos ejercicios interesantes
    graficar_convergencia(2, lambda x: np.cos(x), 0.5, "cos(x) - x = 0")
    graficar_convergencia(4, lambda x: np.exp(-x), 1, "e^(-x)")
    graficar_convergencia(7, lambda x: 1 - x**3, 0.5, "1 - x³")
    
    print("\n¡Análisis completado!")
import numpy as np
import matplotlib.pyplot as plt

# Función original
def f(x):
    return (x + 2) * (x + 1) * (x - 1)**3 * (x - 2)

# Función para demostrar el concepto de multiplicidad
def demostrar_multiplicidad():
    print("CONCEPTO DE MULTIPLICIDAD")
    print("=" * 50)
    
    # Evaluar la función y sus derivadas en x = 1
    x = 1
    
    # Función original
    f_val = f(x)
    print(f"f(1) = {f_val}")
    
    # Primera derivada (calculada manualmente)
    def f_prima(x):
        # f'(x) usando regla del producto
        # f(x) = (x+2)(x+1)(x-1)³(x-2)
        # Expandimos: f(x) = (x+2)(x+1)(x-2)(x-1)³
        
        # Producto de los primeros 3 términos
        g = lambda t: (t + 2) * (t + 1) * (t - 2)
        h = lambda t: (t - 1)**3
        
        # g'(x) = derivada de (x+2)(x+1)(x-2)
        # g'(x) = (x+1)(x-2) + (x+2)(x-2) + (x+2)(x+1)
        g_prima = lambda t: (t + 1) * (t - 2) + (t + 2) * (t - 2) + (t + 2) * (t + 1)
        
        # h'(x) = 3(x-1)²
        h_prima = lambda t: 3 * (t - 1)**2
        
        # f'(x) = g'(x) * h(x) + g(x) * h'(x)
        return g_prima(x) * h(x) + g(x) * h_prima(x)
    
    f_prima_val = f_prima(x)
    print(f"f'(1) = {f_prima_val}")
    
    # Segunda derivada en x = 1
    def f_segunda(x):
        # Para simplificar, evaluamos numéricamente
        h = 1e-8
        return (f_prima(x + h) - f_prima(x - h)) / (2 * h)
    
    f_segunda_val = f_segunda(x)
    print(f"f''(1) ≈ {f_segunda_val:.6f}")
    
    # Tercera derivada en x = 1
    def f_tercera(x):
        h = 1e-6
        return (f_segunda(x + h) - f_segunda(x - h)) / (2 * h)
    
    f_tercera_val = f_tercera(x)
    print(f"f'''(1) ≈ {f_tercera_val:.6f}")
    
    print("\nINTERPRETACIÓN:")
    print("- f(1) = 0: La función pasa por (1, 0)")
    print("- f'(1) = 0: La tangente es horizontal en x = 1")
    print("- f''(1) = 0: No hay concavidad definida en x = 1")
    print("- f'''(1) ≠ 0: La tercera derivada es la primera no nula")
    print("\n¡Esto confirma que x = 1 es una raíz de multiplicidad 3!")

# Función para explicar el Teorema del Valor Intermedio
def teorema_valor_intermedio():
    print("\n" + "=" * 60)
    print("TEOREMA DEL VALOR INTERMEDIO")
    print("=" * 60)
    
    print("ENUNCIADO:")
    print("Si f es continua en [a,b] y f(a) y f(b) tienen signos opuestos,")
    print("entonces existe al menos un c ∈ (a,b) tal que f(c) = 0")
    
    # Ejemplo con el intervalo [-3, 2.5]
    a, b = -3, 2.5
    fa, fb = f(a), f(b)
    
    print(f"\nEJEMPLO con intervalo [{a}, {b}]:")
    print(f"f({a}) = {fa:.6f}")
    print(f"f({b}) = {fb:.6f}")
    print(f"f({a}) × f({b}) = {fa * fb:.6f}")
    
    if fa * fb < 0:
        print("Como f(a) y f(b) tienen signos opuestos, ¡HAY AL MENOS UNA RAÍZ!")
    else:
        print("f(a) y f(b) tienen el mismo signo, pero puede haber raíces igualmente")
    
    print(f"\nRaíces conocidas en [{a}, {b}]: x = -2, -1, 1, 2")

# Función para mostrar comportamiento gráfico de multiplicidades
def graficar_multiplicidades():
    print("\n" + "=" * 60)
    print("COMPORTAMIENTO GRÁFICO SEGÚN MULTIPLICIDAD")
    print("=" * 60)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Función con raíz simple
    def f1(x):
        return (x - 1)
    
    # Función con raíz doble
    def f2(x):
        return (x - 1)**2
    
    # Función con raíz triple
    def f3(x):
        return (x - 1)**3
    
    # Función con raíz cuádruple
    def f4(x):
        return (x - 1)**4
    
    funciones = [f1, f2, f3, f4]
    titulos = ['Multiplicidad 1: f(x) = (x-1)', 
               'Multiplicidad 2: f(x) = (x-1)²',
               'Multiplicidad 3: f(x) = (x-1)³', 
               'Multiplicidad 4: f(x) = (x-1)⁴']
    
    x = np.linspace(0, 2, 1000)
    
    for i, (func, titulo) in enumerate(zip(funciones, titulos)):
        ax = axes[i//2, i%2]
        y = func(x)
        
        ax.plot(x, y, 'b-', linewidth=2)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.7)
        ax.axvline(x=1, color='r', linestyle='--', alpha=0.7)
        ax.plot(1, 0, 'ro', markersize=8)
        
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(titulo)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0.5, 1.5)
        ax.set_ylim(-0.5, 0.5)
    
    plt.tight_layout()
    plt.show()
    
    print("INTERPRETACIÓN:")
    print("• Multiplicidad IMPAR (1, 3, 5...): La función CRUZA el eje X")
    print("• Multiplicidad PAR (2, 4, 6...): La función TOCA el eje X pero no cruza")
    print("• Mayor multiplicidad → Curva más 'plana' cerca de la raíz")

# Función para verificar convergencia paso a paso
def verificar_convergencia_paso_a_paso():
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE CONVERGENCIA PASO A PASO")
    print("=" * 60)
    
    intervalos = [(-3, 2.5), (-2.5, 3), (-1.75, 1.5), (-1.5, 1.75)]
    nombres = ['a)', 'b)', 'c)', 'd)']
    
    for i, (a, b) in enumerate(intervalos):
        print(f"\n{nombres[i]} Intervalo [{a}, {b}]:")
        print("-" * 30)
        
        # Paso 1: Evaluar en extremos
        fa, fb = f(a), f(b)
        print(f"Paso 1 - Evaluar extremos:")
        print(f"  f({a}) = {fa:.6f}")
        print(f"  f({b}) = {fb:.6f}")
        
        # Paso 2: Verificar cambio de signo
        cambio_signo = fa * fb < 0
        print(f"Paso 2 - Cambio de signo: {'SÍ' if cambio_signo else 'NO'}")
        
        # Paso 3: Identificar raíces en el intervalo
        raices_en_intervalo = []
        raices_conocidas = [-2, -1, 1, 2]
        
        for raiz in raices_conocidas:
            if a <= raiz <= b:
                raices_en_intervalo.append(raiz)
        
        print(f"Paso 3 - Raíces en el intervalo: {raices_en_intervalo}")
        
        # Paso 4: Conclusión
        converge = len(raices_en_intervalo) > 0
        print(f"Paso 4 - ¿Converge a cero?: {'SÍ' if converge else 'NO'}")
        
        if converge:
            print(f"  → La función se anula en x = {raices_en_intervalo}")

# Función principal que ejecuta todas las demostraciones
def main():
    print("EXPLICACIÓN COMPLETA: CONVERGENCIA A CERO Y MULTIPLICIDAD")
    print("=" * 70)
    
    # Demostrar el concepto de multiplicidad
    demostrar_multiplicidad()
    
    # Explicar el Teorema del Valor Intermedio
    teorema_valor_intermedio()
    
    # Mostrar comportamiento gráfico
    graficar_multiplicidades()
    
    # Verificar convergencia paso a paso
    verificar_convergencia_paso_a_paso()
    
    print("\n" + "=" * 70)
    print("RESUMEN CONCEPTUAL:")
    print("=" * 70)
    print("1. RAÍCES: Valores donde f(x) = 0 (usar propiedad producto cero)")
    print("2. MULTIPLICIDAD: Cuántas veces se repite una raíz")
    print("   • Se ve en el exponente: (x-1)³ → multiplicidad 3")
    print("   • Impar: cruza el eje | Par: toca el eje")
    print("3. CONVERGENCIA A CERO: Existe x en el intervalo donde f(x) = 0")
    print("4. TEOREMA VALOR INTERMEDIO: Si f(a) y f(b) tienen signos opuestos,")
    print("   entonces hay al menos una raíz entre a y b")

if __name__ == "__main__":
    main()
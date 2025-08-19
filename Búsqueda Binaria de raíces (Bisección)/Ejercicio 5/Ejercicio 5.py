import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import pandas as pd

# Definir la función f(x) = (x + 2)(x + 1)(x - 1)³(x - 2)
def f(x):
    return (x + 2) * (x + 1) * (x - 1)**3 * (x - 2)

# Definir la derivada de f(x) para análisis
def f_prime(x):
    # Usando la regla del producto y la cadena
    # f'(x) = d/dx[(x+2)(x+1)(x-1)³(x-2)]
    term1 = (x + 1) * (x - 1)**3 * (x - 2)  # derivada de (x+2)
    term2 = (x + 2) * (x - 1)**3 * (x - 2)  # derivada de (x+1)
    term3 = (x + 2) * (x + 1) * 3 * (x - 1)**2 * (x - 2)  # derivada de (x-1)³
    term4 = (x + 2) * (x + 1) * (x - 1)**3  # derivada de (x-2)
    
    return term1 + term2 + term3 + term4

# Encontrar las raíces de la función
def encontrar_raices():
    raices = [-2, -1, 1, 2]  # Raíces evidentes de la función
    print("Raíces de f(x):")
    for raiz in raices:
        print(f"x = {raiz}: f({raiz}) = {f(raiz)}")
    
    # Verificar la multiplicidad en x = 1
    print(f"\nMultiplicidad en x = 1: (x-1)³ indica multiplicidad 3")
    return raices

# Analizar convergencia en cada intervalo
def analizar_convergencia(intervalos):
    resultados = []
    
    for i, (a, b) in enumerate(intervalos):
        print(f"\n{'='*50}")
        print(f"ANÁLISIS INTERVALO {chr(97+i)}: [{a}, {b}]")
        print(f"{'='*50}")
        
        # Evaluar función en los extremos
        fa = f(a)
        fb = f(b)
        
        print(f"f({a}) = {fa:.6f}")
        print(f"f({b}) = {fb:.6f}")
        
        # Verificar si hay cambio de signo
        cambio_signo = fa * fb < 0
        print(f"Cambio de signo: {'Sí' if cambio_signo else 'No'}")
        
        # Buscar raíces en el intervalo usando método numérico
        raices_en_intervalo = []
        
        # Verificar raíces conocidas en el intervalo
        raices_conocidas = [-2, -1, 1, 2]
        for raiz in raices_conocidas:
            if a <= raiz <= b:
                raices_en_intervalo.append(raiz)
        
        # Buscar raíces adicionales si hay cambio de signo
        if cambio_signo and len(raices_en_intervalo) == 0:
            try:
                # Punto medio como estimación inicial
                x_inicial = (a + b) / 2
                raiz_numerica = fsolve(f, x_inicial)[0]
                
                # Verificar que la raíz esté en el intervalo
                if a <= raiz_numerica <= b and abs(f(raiz_numerica)) < 1e-10:
                    raices_en_intervalo.append(raiz_numerica)
            except:
                pass
        
        print(f"Raíces en el intervalo: {raices_en_intervalo}")
        
        # Análisis de convergencia
        converge_a_cero = len(raices_en_intervalo) > 0
        
        # Crear puntos para graficar
        x_vals = np.linspace(a, b, 1000)
        y_vals = f(x_vals)
        
        # Verificar comportamiento cerca de las raíces
        comportamiento = ""
        for raiz in raices_en_intervalo:
            if raiz == 1:
                comportamiento += f"En x={raiz}: raíz de multiplicidad 3 (toca el eje y se inflecta)\n"
            else:
                comportamiento += f"En x={raiz}: raíz simple (cruza el eje)\n"
        
        resultado = {
            'intervalo': f"[{a}, {b}]",
            'f(a)': fa,
            'f(b)': fb,
            'cambio_signo': cambio_signo,
            'raices': raices_en_intervalo,
            'converge_a_cero': converge_a_cero,
            'comportamiento': comportamiento.strip()
        }
        
        resultados.append(resultado)
        
        print(f"¿Converge a cero?: {'Sí' if converge_a_cero else 'No'}")
        if comportamiento:
            print(f"Comportamiento:\n{comportamiento}")
    
    return resultados

# Graficar la función en todos los intervalos
def graficar_funcion(intervalos):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()
    
    nombres_intervalos = ['a) [-3, 2.5]', 'b) [-2.5, 3]', 'c) [-1.75, 1.5]', 'd) [-1.5, 1.75]']
    
    for i, (a, b) in enumerate(intervalos):
        ax = axes[i]
        
        # Crear puntos para el gráfico
        x = np.linspace(a, b, 1000)
        y = f(x)
        
        # Graficar la función
        ax.plot(x, y, 'b-', linewidth=2, label='f(x)')
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.7, label='y = 0')
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        
        # Marcar raíces en el intervalo
        raices_conocidas = [-2, -1, 1, 2]
        for raiz in raices_conocidas:
            if a <= raiz <= b:
                ax.plot(raiz, 0, 'ro', markersize=8, label=f'Raíz en x={raiz}')
        
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(nombres_intervalos[i])
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Ajustar límites del eje y para mejor visualización
        y_min, y_max = np.min(y), np.max(y)
        margen = 0.1 * (y_max - y_min)
        ax.set_ylim(y_min - margen, y_max + margen)
    
    plt.tight_layout()
    plt.show()

# Crear tabla resumen
def crear_tabla_resumen(resultados):
    print(f"\n{'='*80}")
    print("TABLA RESUMEN DE CONVERGENCIA")
    print(f"{'='*80}")
    
    df_data = []
    for i, resultado in enumerate(resultados):
        df_data.append({
            'Opción': chr(97+i),
            'Intervalo': resultado['intervalo'],
            'f(a)': f"{resultado['f(a)']:.3f}",
            'f(b)': f"{resultado['f(b)']:.3f}",
            'Cambio de signo': 'Sí' if resultado['cambio_signo'] else 'No',
            'Número de raíces': len(resultado['raices']),
            'Converge a 0': 'SÍ' if resultado['converge_a_cero'] else 'NO'
        })
    
    df = pd.DataFrame(df_data)
    print(df.to_string(index=False))

# Función principal
def main():
    print("ANÁLISIS DE CONVERGENCIA DE f(x) = (x + 2)(x + 1)(x - 1)³(x - 2)")
    print("="*70)
    
    # Definir los intervalos a analizar
    intervalos = [
        (-3, 2.5),    # a)
        (-2.5, 3),    # b)
        (-1.75, 1.5), # c)
        (-1.5, 1.75)  # d)
    ]
    
    # Encontrar raíces
    encontrar_raices()
    
    # Analizar convergencia en cada intervalo
    resultados = analizar_convergencia(intervalos)
    
    # Crear tabla resumen
    crear_tabla_resumen(resultados)
    
    # Graficar la función
    graficar_funcion(intervalos)
    
    print(f"\n{'='*70}")
    print("CONCLUSIÓN:")
    print("="*70)
    print("La función f(x) = (x + 2)(x + 1)(x - 1)³(x - 2) converge a cero")
    print("(tiene raíces) en TODOS los intervalos dados, ya que cada uno")
    print("contiene al menos una de las raíces: x = -2, -1, 1, 2")

# Ejecutar el análisis
if __name__ == "__main__":
    main()
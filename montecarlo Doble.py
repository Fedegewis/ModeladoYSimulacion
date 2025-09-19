
import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
 
# Establecer una semilla para reproducibilidad
np.random.seed(0)
 
# Definir la función a integrar
def funcion(x, y):
    return np.exp(2*x - y)  # Ejemplo: función gaussiana
 
# Límites de integración
x_min, x_max = 0, 1
y_min, y_max = 1, 2
 
# Número de puntos aleatorios para Montecarlo
N = 10000  # Reducido para mejor visualización en la gráfica
 
# Generar puntos aleatorios dentro del dominio
x_random = np.random.uniform(x_min, x_max, N)
y_random = np.random.uniform(y_min, y_max, N)
 
# Evaluar la función en los puntos aleatorios
valores = funcion(x_random, y_random)
 
# Calcular el área del dominio
area = (x_max - x_min) * (y_max - y_min)
 
# Estimar la integral con Montecarlo
integral_montecarlo = area * np.mean(valores)
 
# Calcular la integral con cuadratura de Gauss
integral_exacta_nquad, _ = spi.nquad(funcion, [[x_min, x_max], [y_min, y_max]])
 
# Cálculos estadísticos
media = np.mean(valores)
varianza = np.var(valores, ddof=1)  # Varianza muestral (ddof=1 para muestra)
desviacion_estandar = np.std(valores, ddof=1)  # Desviación estándar muestral
error_estandar = desviacion_estandar / np.sqrt(N)  # Error estándar
 
# Intervalo de confianza al 95%
z_score = 1.96  # Aproximación para nivel de confianza 95%
intervalo_confianza = (integral_montecarlo - z_score * error_estandar,
                       integral_montecarlo + z_score * error_estandar)
 
# Encontrar valores mínimo y máximo generados para x y y
x_min_generated = np.min(x_random)
x_max_generated = np.max(x_random)
y_min_generated = np.min(y_random)
y_max_generated = np.max(y_random)
 
# Imprimir resultados
print(f"Estimación de la integral (Montecarlo): {integral_montecarlo}")
print(f"Valor exacto (Cuadratura de Gauss nquad): {integral_exacta_nquad}")
print(f"Media muestral: {media}")
print(f"Varianza muestral: {varianza}")
print(f"Desviación estándar muestral: {desviacion_estandar}")
print(f"Error estándar: {error_estandar}")
print(f"Intervalo de confianza al 95%: {intervalo_confianza}")
print(f"Valor mínimo generado para x: {x_min_generated}")
print(f"Valor máximo generado para x: {x_max_generated}")
print(f"Valor mínimo generado para y: {y_min_generated}")
print(f"Valor máximo generado para y: {y_max_generated}")
 
# Gráfica de dispersión de los puntos aleatorios generados
plt.figure(figsize=(8, 6))
plt.scatter(x_random, y_random, s=10, alpha=0.5, color='blue')
plt.xlabel("Valores de x generados")
plt.ylabel("Valores de y generados")
plt.title("Distribución aleatoria de puntos Montecarlo")
plt.grid(True)
plt.show()
 
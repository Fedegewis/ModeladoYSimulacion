import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.stats import norm
import random

print("=" * 60)
print("EJERCICIOS DE INTEGRACIÓN NUMÉRICA")
print("=" * 60)

# Ejercicio 2: Estimación por muestreo aleatorio (Monte Carlo)
print("\n2. ESTIMACIÓN POR MUESTREO ALEATORIO (MONTE CARLO)")
print("-" * 50)

def monte_carlo_integration(func, a, b, n_samples, max_y):
    """
    Integración por método Monte Carlo
    func: función a integrar
    a, b: límites de integración
    n_samples: número de muestras
    max_y: valor máximo de la función en el intervalo
    """
    count_inside = 0
    
    for _ in range(n_samples):
        x = random.uniform(a, b)
        y = random.uniform(0, max_y)
        if y <= func(x):
            count_inside += 1
    
    area = (b - a) * max_y * (count_inside / n_samples)
    error = 1/100  # Error máximo de 1/100
    
    return area, error

# Función de ejemplo para Monte Carlo
def f_ejemplo(x):
    return x**2

# Parámetros
a, b = 0, 2
max_y = 4  # máximo de x^2 en [0,2]
n_samples = 10000

area_mc, error_mc = monte_carlo_integration(f_ejemplo, a, b, n_samples, max_y)
integral_exacta = (2**3)/3  # Integral exacta de x^2 de 0 a 2

print(f"Integral por Monte Carlo: {area_mc:.4f}")
print(f"Integral exacta: {integral_exacta:.4f}")
print(f"Error máximo permitido: {error_mc}")

# Ejercicio 3: Integración de ln(x) usando Monte Carlo
print("\n3. INTEGRACIÓN DE ln(x) CON MONTE CARLO")
print("-" * 50)

def ln_monte_carlo(n_samples=10000):
    """Integrar ln(x) usando Monte Carlo con 95% confianza y error 0.01"""
    a, b = 1, np.e  # de 1 a e
    
    # Método de muestreo directo
    total = 0
    for _ in range(n_samples):
        x = random.uniform(a, b)
        total += np.log(x)
    
    integral = (b - a) * total / n_samples
    
    # Error estándar estimado
    variance = 0
    for _ in range(1000):  # muestra más pequeña para calcular varianza
        x = random.uniform(a, b)
        variance += (np.log(x) - integral/(b-a))**2
    variance /= 999
    
    error_std = np.sqrt(variance / n_samples) * (b - a)
    
    return integral, error_std

integral_ln, error_ln = ln_monte_carlo()
integral_ln_exacta = 1  # La integral de ln(x) de 1 a e es 1

print(f"Integral de ln(x) por Monte Carlo: {integral_ln:.4f}")
print(f"Integral exacta: {integral_ln_exacta:.4f}")
print(f"Error estimado: {error_ln:.4f}")

# Ejercicio 4: Integración de sqrt(x) con n=5000
print("\n4. INTEGRACIÓN DE √x CON MONTE CARLO (n=5000)")
print("-" * 50)

def sqrt_monte_carlo(a, b, n_samples):
    """Integrar sqrt(x) usando Monte Carlo"""
    total = 0
    values = []
    
    for _ in range(n_samples):
        x = random.uniform(a, b)
        val = np.sqrt(x)
        total += val
        values.append(val)
    
    integral = (b - a) * total / n_samples
    
    # Calcular desviación estándar
    mean_val = total / n_samples
    variance = sum((v - mean_val)**2 for v in values) / (n_samples - 1)
    std_dev = np.sqrt(variance)
    error_std = std_dev * np.sqrt(b - a) / np.sqrt(n_samples)
    
    return integral, std_dev, error_std

# Parámetros para sqrt(x)
a_sqrt, b_sqrt = 0, 4
n_sqrt = 5000

integral_sqrt, std_sqrt, error_sqrt = sqrt_monte_carlo(a_sqrt, b_sqrt, n_sqrt)
integral_sqrt_exacta = (2/3) * (4**(3/2) - 0**(3/2))  # (2/3)[x^(3/2)]_0^4

print(f"a) Desviación estándar: {std_sqrt:.4f}")
print(f"   Error estándar: {error_sqrt:.4f}")

# Intervalo de confianza del 90%
z_90 = 1.645  # valor z para 90% confianza
intervalo_90 = z_90 * error_sqrt
z_95 = 1.96   # z_0.05 = 2.576 (parece ser un error en el problema)

print(f"b) Intervalo de confianza 90%: [{integral_sqrt - intervalo_90:.4f}, {integral_sqrt + intervalo_90:.4f}]")
print(f"   Integral calculada: {integral_sqrt:.4f}")
print(f"   Integral exacta: {integral_sqrt_exacta:.4f}")

# Ejercicio 5: Integración de sin(x) con muestra uniforme
print("\n5. INTEGRACIÓN DE sin(x) CON MUESTRA UNIFORME")
print("-" * 50)

def sin_monte_carlo_uniform(n_samples, conf_level=0.95):
    """Integrar sin(x) de 0 a π usando muestra uniforme"""
    a, b = 0, np.pi
    total = 0
    values = []
    
    for _ in range(n_samples):
        x = random.uniform(a, b)
        val = np.sin(x)
        total += val
        values.append(val)
    
    integral = (b - a) * total / n_samples
    
    # Calcular intervalo de confianza
    mean_val = total / n_samples
    variance = sum((v - mean_val)**2 for v in values) / (n_samples - 1)
    std_error = np.sqrt(variance / n_samples) * (b - a)
    
    return integral, std_error

n_sin = 10000
integral_sin, error_sin = sin_monte_carlo_uniform(n_sin)
integral_sin_exacta = 2  # La integral de sin(x) de 0 a π es 2

print(f"Integral de sin(x): {integral_sin:.4f}")
print(f"Error estándar: {error_sin:.4f}")
print(f"Intervalo de confianza 95%: [{integral_sin - 1.96*error_sin:.4f}, {integral_sin + 1.96*error_sin:.4f}]")
print(f"Integral exacta: {integral_sin_exacta:.4f}")

# Ejercicio 6: Integral doble con Monte Carlo
print("\n6. INTEGRAL DOBLE ∫∫ e^(x+y) dx dy")
print("-" * 50)

def double_integral_monte_carlo(n_samples, conf_level=0.90):
    """Calcular integral doble de e^(x+y) en región [0,1]x[0,1]"""
    total = 0
    values = []
    
    for _ in range(n_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        val = np.exp(x + y)
        total += val
        values.append(val)
    
    # Área de la región es 1 (1*1)
    integral = total / n_samples
    
    # Intervalo de confianza
    mean_val = total / n_samples
    variance = sum((v - mean_val)**2 for v in values) / (n_samples - 1)
    std_error = np.sqrt(variance / n_samples)
    
    return integral, std_error

n_double = 50000
integral_double, error_double = double_integral_monte_carlo(n_double)
integral_double_exacta = (np.e - 1)**2  # Resultado exacto

print(f"Integral doble: {integral_double:.4f}")
print(f"Error estándar: {error_double:.4f}")
print(f"Intervalo de confianza 90%: [{integral_double - 1.645*error_double:.4f}, {integral_double + 1.645*error_double:.4f}]")
print(f"Integral exacta: {integral_double_exacta:.4f}")

# Ejercicio 7: Integral doble de x² + y²
print("\n7. INTEGRAL DOBLE ∫∫ (x² + y²) dx dy")
print("-" * 50)

def double_integral_x2_y2(n_samples):
    """Calcular integral doble de x² + y² en región [0,1]x[0,1]"""
    total = 0
    values = []
    
    for _ in range(n_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        val = x**2 + y**2
        total += val
        values.append(val)
    
    integral = total / n_samples
    
    # Intervalo de confianza
    mean_val = total / n_samples
    variance = sum((v - mean_val)**2 for v in values) / (n_samples - 1)
    std_error = np.sqrt(variance / n_samples)
    
    return integral, std_error

n_x2y2 = 100000
integral_x2y2, error_x2y2 = double_integral_x2_y2(n_x2y2)
integral_x2y2_exacta = 2/3  # Resultado exacto

print(f"Integral de x² + y²: {integral_x2y2:.4f}")
print(f"Error estándar: {error_x2y2:.4f}")
print(f"Intervalo de confianza 95%: [{integral_x2y2 - 1.96*error_x2y2:.4f}, {integral_x2y2 + 1.96*error_x2y2:.4f}]")
print(f"Integral exacta: {integral_x2y2_exacta:.4f}")

# Ejercicio 8: Integral con muestra de n=5000
print("\n8. INTEGRAL ∫₀¹ 1/√x dx CON n=5000")
print("-" * 50)

def integral_inv_sqrt(n_samples):
    """Calcular integral de 1/√x de 0 a 1 (usando límite ε→0)"""
    epsilon = 1e-6  # Para evitar división por cero
    total = 0
    values = []
    
    for _ in range(n_samples):
        x = random.uniform(epsilon, 1)
        val = 1/np.sqrt(x)
        total += val
        values.append(val)
    
    integral = (1 - epsilon) * total / n_samples
    
    # Intervalo de confianza
    mean_val = total / n_samples
    variance = sum((v - mean_val)**2 for v in values) / (n_samples - 1)
    std_error = np.sqrt(variance / n_samples) * (1 - epsilon)
    
    return integral, std_error

n_inv_sqrt = 5000
integral_inv_sqrt_val, error_inv_sqrt = integral_inv_sqrt(n_inv_sqrt)
integral_inv_sqrt_exacta = 2  # La integral exacta es 2

print(f"Integral de 1/√x: {integral_inv_sqrt_val:.4f}")
print(f"Intervalo de confianza 95%: [{integral_inv_sqrt_val - 1.96*error_inv_sqrt:.4f}, {integral_inv_sqrt_val + 1.96*error_inv_sqrt:.4f}]")
print(f"Integral exacta: {integral_inv_sqrt_exacta:.4f}")

# Ejercicio 9: Integral con n=10000
print("\n9. INTEGRAL ∫₀^(π/2) sin²x dx CON n=10000")
print("-" * 50)

def integral_sin_squared(n_samples):
    """Calcular integral de sin²x de 0 a π/2"""
    a, b = 0, np.pi/2
    total = 0
    values = []
    
    for _ in range(n_samples):
        x = random.uniform(a, b)
        val = np.sin(x)**2
        total += val
        values.append(val)
    
    integral = (b - a) * total / n_samples
    
    # Intervalo de confianza
    mean_val = total / n_samples
    variance = sum((v - mean_val)**2 for v in values) / (n_samples - 1)
    std_error = np.sqrt(variance / n_samples) * (b - a)
    
    return integral, std_error

n_sin2 = 10000
integral_sin2, error_sin2 = integral_sin_squared(n_sin2)
integral_sin2_exacta = np.pi/4  # La integral exacta es π/4

print(f"Integral de sin²x: {integral_sin2:.4f}")
print(f"Intervalo de confianza 95%: [{integral_sin2 - 1.96*error_sin2:.4f}, {integral_sin2 + 1.96*error_sin2:.4f}]")
print(f"Integral exacta: {integral_sin2_exacta:.4f}")

# Ejercicio 10: Método gráfico para modelar el rechazo
print("\n10. MÉTODO GRÁFICO PARA MODELAR RECHAZO POR MUESTREO")
print("-" * 50)

def rejection_sampling_visualization():
    """Visualizar el método de rechazo para f(x) = x² y g(x) = √x en [0,1]"""
    
    # Definir las funciones
    x = np.linspace(0, 1, 1000)
    f_x = x**2
    g_x = np.sqrt(x)
    
    # Crear la gráfica
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(x, f_x, 'b-', linewidth=2, label='f(x) = x²')
    plt.plot(x, g_x, 'r-', linewidth=2, label='g(x) = √x')
    plt.fill_between(x, 0, f_x, alpha=0.3, color='blue', label='Área bajo f(x)')
    plt.fill_between(x, 0, g_x, alpha=0.3, color='red', label='Área bajo g(x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Comparación de f(x) = x² y g(x) = √x')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Simulación del método de rechazo para f(x) = x²
    plt.subplot(2, 2, 2)
    n_points = 1000
    x_samples = []
    y_samples = []
    accepted = []
    
    for _ in range(n_points):
        x_rand = random.uniform(0, 1)
        y_rand = random.uniform(0, 1)  # máximo de x² en [0,1] es 1
        
        if y_rand <= x_rand**2:
            accepted.append(True)
            x_samples.append(x_rand)
            y_samples.append(y_rand)
        else:
            accepted.append(False)
            x_samples.append(x_rand)
            y_samples.append(y_rand)
    
    # Puntos aceptados y rechazados
    x_accept = [x_samples[i] for i in range(len(x_samples)) if accepted[i]]
    y_accept = [y_samples[i] for i in range(len(y_samples)) if accepted[i]]
    x_reject = [x_samples[i] for i in range(len(x_samples)) if not accepted[i]]
    y_reject = [y_samples[i] for i in range(len(y_samples)) if not accepted[i]]
    
    plt.scatter(x_accept, y_accept, c='green', s=1, alpha=0.6, label='Aceptados')
    plt.scatter(x_reject, y_reject, c='red', s=1, alpha=0.6, label='Rechazados')
    plt.plot(x, x**2, 'b-', linewidth=2, label='f(x) = x²')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Método de Rechazo para f(x) = x²\n{len(x_accept)}/{n_points} aceptados')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Histograma de puntos aceptados
    plt.subplot(2, 2, 3)
    plt.hist(x_accept, bins=30, density=True, alpha=0.7, color='green', label='Muestra generada')
    x_theory = np.linspace(0, 1, 1000)
    # La distribución teórica proporcional a x²
    y_theory = 3 * x_theory**2  # 3x² es la PDF normalizada
    plt.plot(x_theory, y_theory, 'r-', linewidth=2, label='Distribución teórica 3x²')
    plt.xlabel('x')
    plt.ylabel('Densidad')
    plt.title('Distribución de puntos aceptados')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Estimación de la integral
    plt.subplot(2, 2, 4)
    integral_estimate = len(x_accept) / n_points  # Área del cuadrado [0,1]x[0,1]
    integral_exact = 1/3  # Integral exacta de x² de 0 a 1
    
    plt.bar(['Estimado', 'Exacto'], [integral_estimate, integral_exact], 
            color=['lightblue', 'lightgreen'], alpha=0.7)
    plt.ylabel('Valor de la integral')
    plt.title(f'Comparación de resultados\nError: {abs(integral_estimate - integral_exact):.4f}')
    plt.grid(True, alpha=0.3)
    
    # Añadir valores en las barras
    plt.text(0, integral_estimate + 0.01, f'{integral_estimate:.4f}', 
             ha='center', va='bottom')
    plt.text(1, integral_exact + 0.01, f'{integral_exact:.4f}', 
             ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    print(f"Método de rechazo para f(x) = x²:")
    print(f"Puntos aceptados: {len(x_accept)} de {n_points}")
    print(f"Eficiencia: {len(x_accept)/n_points:.2%}")
    print(f"Integral estimada: {integral_estimate:.4f}")
    print(f"Integral exacta: {integral_exact:.4f}")
    print(f"Error absoluto: {abs(integral_estimate - integral_exact):.4f}")

# Ejecutar visualización
rejection_sampling_visualization()

print("\n" + "="*60)
print("RESUMEN DE RESULTADOS")
print("="*60)
print("Todos los ejercicios han sido resueltos usando métodos de Monte Carlo")
print("Los intervalos de confianza se calculan usando la distribución normal")
print("Los errores se estiman usando la desviación estándar muestral")
print("="*60)
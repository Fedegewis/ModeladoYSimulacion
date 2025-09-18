import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import math

# Configuración para gráficos
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class RungeKuttaSolver:
    def __init__(self):
        pass
    
    def euler_method(self, f, t_span, y0, h):
        """Método de Euler"""
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + h, h)
        y = np.zeros(len(t))
        y[0] = y0
        
        for i in range(len(t) - 1):
            y[i + 1] = y[i] + h * f(t[i], y[i])
        
        return t, y
    
    def heun_method(self, f, t_span, y0, h):
        """Método de Heun (RK2)"""
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + h, h)
        y = np.zeros(len(t))
        y[0] = y0
        
        for i in range(len(t) - 1):
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h, y[i] + k1)
            y[i + 1] = y[i] + 0.5 * (k1 + k2)
        
        return t, y
    
    def rk4_method(self, f, t_span, y0, h):
        """Método de Runge-Kutta de 4to orden"""
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + h, h)
        y = np.zeros(len(t))
        y[0] = y0
        
        for i in range(len(t) - 1):
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            k3 = h * f(t[i] + h/2, y[i] + k2/2)
            k4 = h * f(t[i] + h, y[i] + k3)
            y[i + 1] = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6
        
        return t, y

def define_equations():
    """Define todas las ecuaciones diferenciales del problema"""
    
    equations = {
        1: {
            'f': lambda t, y: y + t**2,
            'y0': 1,
            't_span': (0, 1),
            'h': 0.1,
            'title': r"$\frac{dy}{dt} = y + t^2$",
            'exact': lambda t: 2*np.exp(t) - t**2 - 2*t - 2  # Solución exacta
        },
        2: {
            'f': lambda t, y: y * np.sin(t),
            'y0': 2,
            't_span': (0, np.pi),
            'h': np.pi/10,
            'title': r"$\frac{dy}{dt} = y \sin(t)$",
            'exact': lambda t: 2 * np.exp(1 - np.cos(t))  # Solución exacta
        },
        3: {
            'f': lambda t, y: 2*t + 3*y,
            'y0': 0,
            't_span': (0, 1),
            'h': 0.2,
            'title': r"$\frac{dy}{dt} = 2t + 3y$",
            'exact': lambda t: (2/9) * (3*np.exp(3*t) - 2 - 6*t)  # Solución exacta
        },
        4: {
            'f': lambda t, y: t - y**2,
            'y0': 1,
            't_span': (0, 2),
            'h': 0.2,
            'title': r"$\frac{dy}{dt} = t - y^2$",
            'exact': None  # No tiene solución analítica simple
        },
        5: {
            'f': lambda t, y: np.exp(-t) - y,
            'y0': 0,
            't_span': (0, 1),
            'h': 0.1,
            'title': r"$\frac{dy}{dt} = e^{-t} - y$",
            'exact': lambda t: t * np.exp(-t)  # Solución exacta
        },
        6: {
            'f': lambda t, y: 1/(1+t**2) - y,
            'y0': 1,
            't_span': (0, 2),
            'h': 0.5,
            'title': r"$\frac{dy}{dt} = \frac{1}{1+t^2} - y$",
            'exact': None  # Solución compleja
        },
        7: {
            'f': lambda t, y: (t**2 - 1)/y**2 if y != 0 else 0,
            'y0': 2,
            't_span': (0, 2),
            'h': 0.5,
            'title': r"$\frac{dy}{dx} = \frac{x^2-1}{y^2}$",
            'exact': None  # Solución implícita
        },
        8: {
            'f': lambda t, y: y - t**2 + 1,
            'y0': 0.5,
            't_span': (0, 1),
            'h': 0.2,
            'title': r"$\frac{dy}{dt} = y - t^2 + 1$",
            'exact': lambda t: (t + 1)**2 - 0.5 * np.exp(t)  # Solución exacta
        }
    }
    
    return equations

def solve_and_plot_equation(eq_num, eq_data, solver):
    """Resuelve y grafica una ecuación específica"""
    
    f = eq_data['f']
    y0 = eq_data['y0']
    t_span = eq_data['t_span']
    h = eq_data['h']
    title = eq_data['title']
    exact_func = eq_data.get('exact', None)
    
    # Resolver con diferentes métodos
    t_euler, y_euler = solver.euler_method(f, t_span, y0, h)
    t_heun, y_heun = solver.heun_method(f, t_span, y0, h)
    t_rk4, y_rk4 = solver.rk4_method(f, t_span, y0, h)
    
    # Crear figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfico principal con comparación de métodos
    ax1.plot(t_euler, y_euler, 'r--', marker='o', markersize=4, label='Euler', linewidth=2)
    ax1.plot(t_heun, y_heun, 'g--', marker='s', markersize=4, label='Heun (RK2)', linewidth=2)
    ax1.plot(t_rk4, y_rk4, 'b-', marker='^', markersize=4, label='RK4', linewidth=2)
    
    # Solución exacta si está disponible
    if exact_func is not None:
        t_exact = np.linspace(t_span[0], t_span[1], 200)
        y_exact = exact_func(t_exact)
        ax1.plot(t_exact, y_exact, 'k-', label='Solución Exacta', linewidth=1, alpha=0.8)
        
        # Calcular errores
        y_exact_points = exact_func(t_rk4)
        error_euler = np.abs(y_euler - exact_func(t_euler))
        error_heun = np.abs(y_heun - exact_func(t_heun))
        error_rk4 = np.abs(y_rk4 - y_exact_points)
        
        # Gráfico de errores
        ax2.semilogy(t_euler, error_euler, 'r--', marker='o', markersize=4, label='Error Euler')
        ax2.semilogy(t_heun, error_heun, 'g--', marker='s', markersize=4, label='Error Heun')
        ax2.semilogy(t_rk4, error_rk4, 'b-', marker='^', markersize=4, label='Error RK4')
        ax2.set_title('Errores Absolutos')
        ax2.set_xlabel('t')
        ax2.set_ylabel('|Error|')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Mostrar errores máximos
        print(f"\nEcuación {eq_num}: {title}")
        print(f"Error máximo Euler: {np.max(error_euler):.2e}")
        print(f"Error máximo Heun: {np.max(error_heun):.2e}")
        print(f"Error máximo RK4: {np.max(error_rk4):.2e}")
    else:
        ax2.text(0.5, 0.5, 'Solución exacta\nno disponible', 
                ha='center', va='center', transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Comparación numérica')
    
    ax1.set_title(f'Ecuación {eq_num}: {title}')
    ax1.set_xlabel('t')
    ax1.set_ylabel('y(t)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Crear tabla de resultados
    print(f"\nTabla de resultados para la Ecuación {eq_num}:")
    print("-" * 80)
    print(f"{'t':>8} {'Euler':>12} {'Heun':>12} {'RK4':>12}", end="")
    if exact_func:
        print(f" {'Exacta':>12} {'Error RK4':>12}")
    else:
        print()
    print("-" * 80)
    
    for i in range(0, len(t_rk4), max(1, len(t_rk4)//10)):  # Mostrar cada 10 puntos aproximadamente
        print(f"{t_rk4[i]:8.2f} {y_euler[i]:12.6f} {y_heun[i]:12.6f} {y_rk4[i]:12.6f}", end="")
        if exact_func:
            exact_val = exact_func(t_rk4[i])
            error = abs(y_rk4[i] - exact_val)
            print(f" {exact_val:12.6f} {error:12.2e}")
        else:
            print()

def main():
    """Función principal"""
    print("=" * 80)
    print("RESOLUCIÓN DE ECUACIONES DIFERENCIALES")
    print("Métodos: Euler, Heun (RK2), y Runge-Kutta 4to orden")
    print("=" * 80)
    
    solver = RungeKuttaSolver()
    equations = define_equations()
    
    # Resolver todas las ecuaciones
    for eq_num in range(1, 9):
        if eq_num in equations:
            solve_and_plot_equation(eq_num, equations[eq_num], solver)
            print("\n" + "="*80 + "\n")
    
    # Resumen de métodos
    print("\nRESUMEN DE MÉTODOS:")
    print("-" * 50)
    print("1. Método de Euler (orden 1):")
    print("   y_{n+1} = y_n + h * f(t_n, y_n)")
    print("\n2. Método de Heun (RK2, orden 2):")
    print("   k1 = h * f(t_n, y_n)")
    print("   k2 = h * f(t_n + h, y_n + k1)")
    print("   y_{n+1} = y_n + (k1 + k2)/2")
    print("\n3. Método de Runge-Kutta 4to orden:")
    print("   k1 = h * f(t_n, y_n)")
    print("   k2 = h * f(t_n + h/2, y_n + k1/2)")
    print("   k3 = h * f(t_n + h/2, y_n + k2/2)")
    print("   k4 = h * f(t_n + h, y_n + k3)")
    print("   y_{n+1} = y_n + (k1 + 2*k2 + 2*k3 + k4)/6")

if __name__ == "__main__":
    main()
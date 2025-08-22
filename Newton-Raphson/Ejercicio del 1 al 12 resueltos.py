# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 11:38:03 2025

@author: fedeg
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    import numpy as np
except Exception:
    FigureCanvasTkAgg = None
    plt = None
    np = None

def safe_eval(expr, x_val):
    """Evaluación segura de expresiones matemáticas"""
    # Crear un contexto seguro con funciones matemáticas
    safe_dict = {
        'x': x_val,
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'exp': math.exp, 'log': math.log, 'ln': math.log,
        'sqrt': math.sqrt, 'abs': abs, 'pow': pow,
        'pi': math.pi, 'e': math.e,
        '__builtins__': {}
    }
    
    try:
        return eval(expr, safe_dict)
    except:
        raise ValueError(f"Error al evaluar la expresión: {expr}")

def numerical_derivative(f_expr, x, h=1e-8):
    """Calcula la derivada numérica usando diferencias centradas"""
    return (safe_eval(f_expr, x + h) - safe_eval(f_expr, x - h)) / (2 * h)

def newton_raphson_method(f_expr, df_expr, x0, tol=1e-10, max_iter=50):
    """Implementa el método de Newton-Raphson"""
    history = []
    x = x0
    
    for i in range(max_iter):
        try:
            # Evaluar f(x) y f'(x)
            fx = safe_eval(f_expr, x)
            
            if df_expr.strip():  # Si se proporciona derivada
                dfx = safe_eval(df_expr, x)
            else:  # Derivada numérica
                dfx = numerical_derivative(f_expr, x)
            
            # Verificar si la derivada es muy pequeña
            if abs(dfx) < 1e-14:
                history.append((i, x, fx, dfx, float('inf'), float('inf'), "Derivada ≈ 0"))
                return None, history, "Derivada muy pequeña - método falla"
            
            # Calcular siguiente aproximación
            x_new = x - fx / dfx
            
            # Calcular errores
            abs_error = abs(x_new - x)
            rel_error = abs_error / abs(x_new) if x_new != 0 else float('inf')
            
            history.append((i, x, fx, dfx, abs_error, rel_error, x_new))
            
            # Verificar convergencia
            if abs_error < tol:
                return x_new, history, f"Convergió en {i+1} iteraciones"
            
            x = x_new
            
        except Exception as e:
            history.append((i, x, "Error", "Error", "Error", "Error", str(e)))
            return None, history, f"Error en iteración {i}: {str(e)}"
    
    return x, history, f"No convergió en {max_iter} iteraciones"

class NewtonRaphsonGUI:
    def __init__(self, master):
        self.master = master
        master.title("Método Newton-Raphson - Ejercicios Resueltos")
        master.geometry("1000x800")
        self.exercises = self.load_exercises()
        self._build_widgets()

    def load_exercises(self):
        """Carga todos los ejercicios predefinidos"""
        return {
            "1. f(x) = (x-1)², x₀ = 0": {
                "f": "(x - 1)**2",
                "df": "2*(x - 1)",
                "x0": "0",
                "descripcion": "Función cuadrática con raíz doble en x = 1"
            },
            "2. f(x) = x³ - 2x - 5, x₀ = 1.5": {
                "f": "x**3 - 2*x - 5",
                "df": "3*x**2 - 2",
                "x0": "1.5",
                "descripcion": "Función cúbica"
            },
            "3. f(x) = x⁵ - x - 1, x₀ = 1": {
                "f": "x**5 - x - 1",
                "df": "5*x**4 - 1",
                "x0": "1",
                "descripcion": "Función quíntica"
            },
            "4. Aproximar 6√2 (8 cifras)": {
                "f": "x**2 - 72",
                "df": "2*x",
                "x0": "8",
                "descripcion": "6√2 ≈ √72, resolver x² - 72 = 0"
            },
            "5. f(x) = eˣ + x² - 4, x₀ = 0.5": {
                "f": "exp(x) + x**2 - 4",
                "df": "exp(x) + 2*x",
                "x0": "0.5",
                "descripcion": "Función exponencial + cuadrática"
            },
            "6. f(x) = x² - 3x - 4, x₀ = 8": {
                "f": "x**2 - 3*x - 4",
                "df": "2*x - 3",
                "x0": "8",
                "descripcion": "Función cuadrática con raíces en x = -1, x = 4"
            },
            "7. f(x) = ln(x) - 1, x₀ = 2": {
                "f": "log(x) - 1",
                "df": "1/x",
                "x0": "2",
                "descripcion": "Función logarítmica, raíz en x = e"
            },
            "8. f(x) = x⁴ - 16, x₀ = 2": {
                "f": "x**4 - 16",
                "df": "4*x**3",
                "x0": "2",
                "descripcion": "Función cuártica, raíces en x = ±2"
            },
            "9. f(x) = x³ - 2x + 1, x₀ = -1.5": {
                "f": "x**3 - 2*x + 1",
                "df": "3*x**2 - 2",
                "x0": "-1.5",
                "descripcion": "Función cúbica"
            },
            "10. f(x) = e^(3x) - 4, x₀ = 0": {
                "f": "exp(3*x) - 4",
                "df": "3*exp(3*x)",
                "x0": "0",
                "descripcion": "Función exponencial"
            },
            "11. f(x) = x² - 2x + 1, x₀ = 0": {
                "f": "x**2 - 2*x + 1",
                "df": "2*x - 2",
                "x0": "0",
                "descripcion": "f(x) = (x-1)², raíz doble en x = 1"
            },
            "12. x = xe^(-x), x₀ = -1": {
                "f": "x - x*exp(-x)",
                "df": "1 - exp(-x) + x*exp(-x)",
                "x0": "-1",
                "descripcion": "Ecuación transcendental"
            }
        }

    def _build_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Título
        title_label = ttk.Label(main_frame, text="MÉTODO NEWTON-RAPHSON - EJERCICIOS RESUELTOS", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 15))
        
        # Selector de ejercicios
        exercise_frame = ttk.LabelFrame(main_frame, text="Seleccionar Ejercicio", padding=10)
        exercise_frame.grid(row=1, column=0, columnspan=4, sticky='ew', pady=(0, 10))
        
        ttk.Label(exercise_frame, text="Ejercicio:").grid(row=0, column=0, sticky='w')
        self.exercise_var = tk.StringVar()
        self.exercise_combo = ttk.Combobox(exercise_frame, textvariable=self.exercise_var,
                                          values=list(self.exercises.keys()), width=50, state='readonly')
        self.exercise_combo.grid(row=0, column=1, padx=10, sticky='ew')
        self.exercise_combo.bind('<<ComboboxSelected>>', self.load_selected_exercise)
        
        ttk.Button(exercise_frame, text="Cargar Ejercicio", 
                  command=self.load_selected_exercise).grid(row=0, column=2, padx=5)
        
        # Descripción del ejercicio
        self.description_var = tk.StringVar(value="Selecciona un ejercicio...")
        desc_label = ttk.Label(exercise_frame, textvariable=self.description_var, 
                              font=('Arial', 10), foreground='blue')
        desc_label.grid(row=1, column=0, columnspan=3, sticky='ew', pady=5)
        
        # Entradas manuales
        input_frame = ttk.LabelFrame(main_frame, text="Entrada Manual", padding=10)
        input_frame.grid(row=2, column=0, columnspan=4, sticky='ew', pady=(0, 10))
        
        ttk.Label(input_frame, text="f(x):").grid(row=0, column=0, sticky='w')
        self.f_var = tk.StringVar()
        self.f_entry = ttk.Entry(input_frame, textvariable=self.f_var, width=40)
        self.f_entry.grid(row=0, column=1, columnspan=2, padx=5, sticky='ew')
        
        ttk.Label(input_frame, text="f'(x):").grid(row=1, column=0, sticky='w')
        self.df_var = tk.StringVar()
        self.df_entry = ttk.Entry(input_frame, textvariable=self.df_var, width=40)
        self.df_entry.grid(row=1, column=1, columnspan=2, padx=5, sticky='ew')
        
        ttk.Label(input_frame, text="x₀:").grid(row=2, column=0, sticky='w')
        self.x0_var = tk.StringVar()
        self.x0_entry = ttk.Entry(input_frame, textvariable=self.x0_var, width=15)
        self.x0_entry.grid(row=2, column=1, padx=5, sticky='w')
        
        ttk.Label(input_frame, text="Tolerancia:").grid(row=2, column=2, sticky='w')
        self.tol_var = tk.StringVar(value="1e-10")
        self.tol_entry = ttk.Entry(input_frame, textvariable=self.tol_var, width=15)
        self.tol_entry.grid(row=2, column=3, padx=5, sticky='w')
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Resolver", command=self.solve_newton,
                  style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Resolver Todos", command=self.solve_all_exercises).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_all).pack(side='left', padx=5)
        
        # Resultado
        self.result_var = tk.StringVar(value="Resultado: (selecciona y resuelve un ejercicio)")
        result_label = ttk.Label(main_frame, textvariable=self.result_var, 
                                font=('Arial', 12, 'bold'), foreground='blue')
        result_label.grid(row=4, column=0, columnspan=4, pady=10)
        
        # Tabla de iteraciones
        table_frame = ttk.LabelFrame(main_frame, text="Iteraciones", padding=10)
        table_frame.grid(row=5, column=0, columnspan=4, sticky='nsew', pady=(0, 10))
        
        # Crear Treeview con scrollbars
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill='both', expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("iter", "x_n", "f_x", "df_x", "error_abs", "error_rel", "x_new"),
                                show='headings', height=8)
        
        # Configurar columnas
        columns = [
            ("iter", "Iter", 50),
            ("x_n", "xₙ", 120),
            ("f_x", "f(xₙ)", 120),
            ("df_x", "f'(xₙ)", 120),
            ("error_abs", "Error Abs", 100),
            ("error_rel", "Error Rel", 100),
            ("x_new", "xₙ₊₁", 120)
        ]
        
        for col, heading, width in columns:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor="center")
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        
        # Gráfico (si matplotlib disponible)
        if FigureCanvasTkAgg and plt and np:
            graph_frame = ttk.LabelFrame(main_frame, text="Visualización", padding=5)
            graph_frame.grid(row=6, column=0, columnspan=4, sticky='ew')
            
            self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
            self.canvas.get_tk_widget().pack()
        else:
            self.canvas = None
        
        # Configurar redimensionamiento
        main_frame.columnconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

    def load_selected_exercise(self, event=None):
        """Carga el ejercicio seleccionado"""
        exercise_name = self.exercise_var.get()
        if exercise_name in self.exercises:
            ex = self.exercises[exercise_name]
            self.f_var.set(ex["f"])
            self.df_var.set(ex["df"])
            self.x0_var.set(ex["x0"])
            self.description_var.set(ex["descripcion"])

    def solve_newton(self):
        """Resuelve usando Newton-Raphson"""
        try:
            f_expr = self.f_var.get()
            df_expr = self.df_var.get()
            x0 = float(self.x0_var.get())
            tol = float(self.tol_var.get())
            
            if not f_expr:
                messagebox.showerror("Error", "Ingresa la función f(x)")
                return
            
            # Resolver
            result, history, message = newton_raphson_method(f_expr, df_expr, x0, tol)
            
            # Mostrar resultado
            if result is not None:
                if "6√2" in self.exercise_var.get():  # Caso especial para aproximar 6√2
                    theoretical = 6 * math.sqrt(2)
                    self.result_var.set(f"6√2 ≈ {result:.10f} (teórico: {theoretical:.10f})")
                else:
                    self.result_var.set(f"Raíz encontrada: {result:.10f} - {message}")
            else:
                self.result_var.set(f"No convergió - {message}")
            
            # Llenar tabla
            self.populate_table(history)
            
            # Graficar si es posible
            if self.canvas:
                self.plot_function_and_convergence(f_expr, history, result)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")

    def solve_all_exercises(self):
        """Resuelve todos los ejercicios y muestra un resumen"""
        results_window = tk.Toplevel(self.master)
        results_window.title("Resultados de Todos los Ejercicios")
        results_window.geometry("800x600")
        
        results_frame = ttk.Frame(results_window, padding=10)
        results_frame.pack(fill='both', expand=True)
        
        results_text = tk.Text(results_frame, font=('Courier', 10))
        results_text.pack(fill='both', expand=True)
        
        scrollbar_r = ttk.Scrollbar(results_frame, orient="vertical", command=results_text.yview)
        results_text.configure(yscrollcommand=scrollbar_r.set)
        scrollbar_r.pack(side="right", fill="y")
        
        results_text.insert(tk.END, "RESULTADOS DE TODOS LOS EJERCICIOS NEWTON-RAPHSON\n")
        results_text.insert(tk.END, "=" * 70 + "\n\n")
        
        for exercise_name, exercise_data in self.exercises.items():
            try:
                x0 = float(exercise_data["x0"])
                result, history, message = newton_raphson_method(
                    exercise_data["f"], exercise_data["df"], x0, 1e-10
                )
                
                results_text.insert(tk.END, f"{exercise_name}\n")
                results_text.insert(tk.END, f"  f(x) = {exercise_data['f']}\n")
                results_text.insert(tk.END, f"  x₀ = {x0}\n")
                
                if result is not None:
                    if "6√2" in exercise_name:
                        theoretical = 6 * math.sqrt(2)
                        error = abs(result - theoretical)
                        results_text.insert(tk.END, f"  ✓ Resultado: {result:.10f}\n")
                        results_text.insert(tk.END, f"  ✓ 6√2 teórico: {theoretical:.10f}\n")
                        results_text.insert(tk.END, f"  ✓ Error: {error:.2e}\n")
                    else:
                        # Verificación
                        verification = safe_eval(exercise_data["f"], result)
                        results_text.insert(tk.END, f"  ✓ Resultado: {result:.10f}\n")
                        results_text.insert(tk.END, f"  ✓ f({result:.6f}) = {verification:.2e}\n")
                    results_text.insert(tk.END, f"  ✓ Iteraciones: {len(history)}\n")
                else:
                    results_text.insert(tk.END, f"  ✗ No convergió: {message}\n")
                
                results_text.insert(tk.END, "\n" + "-" * 50 + "\n\n")
                
            except Exception as e:
                results_text.insert(tk.END, f"  ✗ Error: {str(e)}\n\n")
        
        results_text.config(state='disabled')

    def populate_table(self, history):
        """Llena la tabla con el historial de iteraciones"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar datos
        for record in history:
            # Formatear valores para mostrar
            formatted_record = []
            for i, value in enumerate(record):
                if isinstance(value, float):
                    if i in [4, 5]:  # Errores
                        formatted_record.append(f"{value:.2e}")
                    else:
                        formatted_record.append(f"{value:.8f}")
                else:
                    formatted_record.append(str(value))
            
            self.tree.insert('', 'end', values=formatted_record)

    def plot_function_and_convergence(self, f_expr, history, result):
        """Grafica la función y la convergencia"""
        try:
            # Limpiar gráficos
            self.ax1.clear()
            self.ax2.clear()
            
            # Extraer valores x de la historia
            x_values = [record[1] for record in history if isinstance(record[1], (int, float))]
            if not x_values:
                return
            
            # Gráfico 1: Función y raíz
            x_min, x_max = min(x_values + [result]) - 1, max(x_values + [result]) + 1
            x_plot = np.linspace(x_min, x_max, 400)
            y_plot = [safe_eval(f_expr, x) for x in x_plot]
            
            self.ax1.plot(x_plot, y_plot, 'b-', label='f(x)')
            self.ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
            self.ax1.axvline(x=result, color='r', linestyle='--', alpha=0.7, label=f'Raíz: {result:.6f}')
            self.ax1.plot(x_values, [safe_eval(f_expr, x) for x in x_values], 'ro-', label='Iteraciones')
            self.ax1.set_xlabel('x')
            self.ax1.set_ylabel('f(x)')
            self.ax1.set_title('Función y Convergencia')
            self.ax1.legend()
            self.ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Convergencia del error
            if len(history) > 1:
                iterations = list(range(len(history)))
                errors = [record[4] for record in history if isinstance(record[4], (int, float))]
                
                self.ax2.semilogy(iterations, errors, 'go-', label='Error absoluto')
                self.ax2.set_xlabel('Iteración')
                self.ax2.set_ylabel('Error (log)')
                self.ax2.set_title('Convergencia del Error')
                self.ax2.legend()
                self.ax2.grid(True, alpha=0.3)
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error en gráfico: {e}")

    def clear_all(self):
        """Limpia todos los campos"""
        self.f_var.set("")
        self.df_var.set("")
        self.x0_var.set("")
        self.exercise_var.set("")
        self.description_var.set("Selecciona un ejercicio...")
        self.result_var.set("Resultado: (selecciona y resuelve un ejercicio)")
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Limpiar gráfico
        if self.canvas:
            self.ax1.clear()
            self.ax2.clear()
            self.canvas.draw()

def main():
    root = tk.Tk()
    
    # Configurar estilo
    style = ttk.Style()
    style.theme_use('clam')
    
    app = NewtonRaphsonGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
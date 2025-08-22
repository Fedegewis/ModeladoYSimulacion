import ast
import math
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Tuple
import sympy as sp

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    import numpy as np
except Exception:
    FigureCanvasTkAgg = None
    plt = None
    np = None


def _make_safe_func(expr: str) -> Callable[[float], float]:
    """Convierte expresión string a función evaluable de forma segura"""
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed_names.update({"abs": abs, "pow": pow})
    
    expr_ast = ast.parse(expr, mode='eval')
    for node in ast.walk(expr_ast):
        if isinstance(node, ast.Name):
            if node.id != 'x' and node.id not in allowed_names:
                raise ValueError(f"Nombre no permitido en expresión: {node.id}")
        elif isinstance(node, (ast.Call, ast.BinOp, ast.UnaryOp, ast.Expression,
                               ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div,
                               ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.Constant,
                               ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.Gt,
                               ast.LtE, ast.GtE, ast.And, ast.Or, ast.BoolOp)):
            continue
        else:
            raise ValueError(f"Nodo AST no permitido: {type(node).__name__}")
    
    code = compile(expr_ast, '<string>', 'eval')
    def f(x: float) -> float:
        return eval(code, {'__builtins__': {}}, {**allowed_names, 'x': x})
    return f


def numerical_derivative(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    """Calcula derivada numérica usando diferencias centrales"""
    return (f(x + h) - f(x - h)) / (2 * h)


def symbolic_derivative(expr: str) -> str:
    """Calcula derivada simbólica usando SymPy"""
    try:
        # Definir la variable simbólica
        x = sp.Symbol('x')
        
        # Convertir la expresión a SymPy
        # Reemplazar funciones comunes por equivalentes de SymPy
        expr_sympy = expr.replace('sqrt', 'sp.sqrt')
        expr_sympy = expr_sympy.replace('sin', 'sp.sin')
        expr_sympy = expr_sympy.replace('cos', 'sp.cos')
        expr_sympy = expr_sympy.replace('tan', 'sp.tan')
        expr_sympy = expr_sympy.replace('log', 'sp.log')
        expr_sympy = expr_sympy.replace('exp', 'sp.exp')
        expr_sympy = expr_sympy.replace('asin', 'sp.asin')
        expr_sympy = expr_sympy.replace('acos', 'sp.acos')
        expr_sympy = expr_sympy.replace('atan', 'sp.atan')
        expr_sympy = expr_sympy.replace('sinh', 'sp.sinh')
        expr_sympy = expr_sympy.replace('cosh', 'sp.cosh')
        expr_sympy = expr_sympy.replace('tanh', 'sp.tanh')
        
        # Evaluar la expresión simbólica
        func = eval(expr_sympy, {'x': x, 'sp': sp, 'pi': sp.pi, 'e': sp.E})
        
        # Calcular la derivada
        derivative = sp.diff(func, x)
        
        # Simplificar y convertir a string
        derivative_simplified = sp.simplify(derivative)
        return str(derivative_simplified)
    
    except Exception as e:
        raise ValueError(f"Error en derivada simbólica: {str(e)}")


def evaluate_derivative_at_points(f_expr: str, df_expr: str, x_points: List[float]) -> List[Tuple[float, float, float, float]]:
    """Evalúa función y derivada en puntos específicos"""
    try:
        f = _make_safe_func(f_expr)
        df = _make_safe_func(df_expr.replace('sp.', '').replace('sqrt', 'math.sqrt').replace('log', 'math.log'))
        
        results = []
        for x in x_points:
            try:
                f_val = f(x)
                df_val = df(x)
                df_num = numerical_derivative(f, x)
                error = abs(df_val - df_num) if not math.isnan(df_num) else float('inf')
                results.append((x, f_val, df_val, df_num, error))
            except:
                results.append((x, float('nan'), float('nan'), float('nan'), float('inf')))
        
        return results
    except Exception as e:
        raise ValueError(f"Error evaluando derivada: {str(e)}")


class DerivativasGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Calculadora de Derivadas")
        master.geometry("900x700")
        self._build_widgets()

    def _build_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configurar el grid
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="CALCULADORA DE DERIVADAS", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 15))
        
        # Entrada de función
        ttk.Label(main_frame, text="f(x) =", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=(0, 5))
        self.expr_var = tk.StringVar(value="x**2 + 3*x + 2")
        expr_entry = ttk.Entry(main_frame, textvariable=self.expr_var, width=50, font=('Arial', 10))
        expr_entry.grid(row=1, column=1, columnspan=2, sticky='we', padx=(0, 5))
        
        # Botón calcular derivada
        calc_button = ttk.Button(main_frame, text="Calcular f'(x)", command=self.calculate_derivative)
        calc_button.grid(row=1, column=3, padx=(5, 0))        
        # Resultado de derivada simbólica
        ttk.Label(main_frame, text="f'(x) =", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=(0, 5), pady=(10, 5))
        self.derivative_var = tk.StringVar(value="Presiona 'Calcular f'(x)' para obtener la derivada")        
        derivative_entry = ttk.Entry(main_frame, textvariable=self.derivative_var, width=50, 
                                   font=('Arial', 10), state='readonly')
        derivative_entry.grid(row=2, column=1, columnspan=2, sticky='we', padx=(0, 5), pady=(10, 5))
        
        # Botón copiar derivada
        copy_button = ttk.Button(main_frame, text="Copiar", command=self.copy_derivative)
        copy_button.grid(row=2, column=3, padx=(5, 0), pady=(10, 5))
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=4, sticky='we', pady=15)
        
        # Sección de evaluación
        eval_label = ttk.Label(main_frame, text="EVALUAR EN PUNTOS ESPECÍFICOS", 
                              font=('Arial', 12, 'bold'))
        eval_label.grid(row=4, column=0, columnspan=4, pady=(0, 10))
        
        # Entrada de puntos
        ttk.Label(main_frame, text="Puntos x (separados por comas):").grid(row=5, column=0, sticky='w')
        self.points_var = tk.StringVar(value="0, 1, 2, -1, 0.5")
        points_entry = ttk.Entry(main_frame, textvariable=self.points_var, width=30)
        points_entry.grid(row=5, column=1, sticky='we', padx=(5, 5))
        
        # Botón evaluar
        eval_button = ttk.Button(main_frame, text="Evaluar", command=self.evaluate_points)
        eval_button.grid(row=5, column=2, padx=(5, 0))
        
        # Botón limpiar todo
        clear_button = ttk.Button(main_frame, text="Limpiar Todo", command=self.clear_all)
        clear_button.grid(row=5, column=3, padx=(5, 0))
        
        # Tabla de resultados
        columns = ('x', 'f(x)', "f'(x) simbólica", "f'(x) numérica", "Error")
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        
        self.tree.grid(row=6, column=0, columnspan=4, pady=15, sticky='nsew')
        main_frame.rowconfigure(6, weight=1)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=6, column=4, sticky='ns', pady=15)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame para información adicional
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding=5)
        info_frame.grid(row=7, column=0, columnspan=4, sticky='we', pady=(10, 0))
        
        # Mensaje informativo
        info_text = ("Funciones soportadas: +, -, *, /, **, sqrt(), sin(), cos(), tan(), "
                    "log(), exp(), asin(), acos(), atan(), sinh(), cosh(), tanh(), "
                    "constantes: pi, e")
        info_label = ttk.Label(info_frame, text=info_text, wraplength=800, justify='left')
        info_label.grid(row=0, column=0, sticky='w')
        
        # Ejemplos
        examples_text = ("Ejemplos: x**2 + 3*x + 1, sin(x)*cos(x), exp(x)/x, sqrt(x**2 + 1), "
                        "log(x), tan(x), x**3 - 2*x**2 + x - 1")
        examples_label = ttk.Label(info_frame, text=f"Ejemplos: {examples_text}", 
                                  wraplength=800, justify='left', font=('Arial', 8))
        examples_label.grid(row=1, column=0, sticky='w', pady=(5, 0))
        
        # Gráfico (si matplotlib está disponible)
        if FigureCanvasTkAgg and plt and np:
            self.setup_plot()
        else:
            no_plot_label = ttk.Label(main_frame, 
                                    text="matplotlib/numpy no disponible - gráficos deshabilitados")
            no_plot_label.grid(row=8, column=0, columnspan=4, pady=10)
            self.fig = None
            self.ax = None
            self.canvas = None

    def setup_plot(self):
        """Configura el área de gráficos"""
        plot_frame = ttk.LabelFrame(self.master, text="Gráfico de f(x) y f'(x)", padding=5)
        plot_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        self.master.columnconfigure(1, weight=1)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)

    def calculate_derivative(self):
        """Calcula la derivada simbólica de la función"""
        try:
            expr = self.expr_var.get().strip()
            if not expr:
                messagebox.showerror("Error", "Por favor ingresa una función")
                return
            
            # Calcular derivada simbólica
            derivative = symbolic_derivative(expr)
            self.derivative_var.set(derivative)
            
            # Actualizar gráfico si está disponible
            if self.canvas:
                self.update_plot()
                
            messagebox.showinfo("Éxito", "Derivada calculada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la derivada: {str(e)}")
            self.derivative_var.set("Error en el cálculo")

    def copy_derivative(self):
        """Copia la derivada al portapapeles"""
        derivative = self.derivative_var.get()
        if derivative and derivative != "Presiona 'Calcular f'(x)' para obtener la derivada":
            self.master.clipboard_clear()
            self.master.clipboard_append(derivative)
            messagebox.showinfo("Copiado", "Derivada copiada al portapapeles")
        else:
            messagebox.showwarning("Advertencia", "No hay derivada para copiar")

    def evaluate_points(self):
        """Evalúa la función y su derivada en puntos específicos"""
        try:
            # Verificar que hay una derivada calculada
            derivative = self.derivative_var.get()
            if not derivative or derivative == "Presiona 'Calcular f'(x)' para obtener la derivada":
                messagebox.showerror("Error", "Primero calcula la derivada")
                return
            
            # Obtener puntos
            points_str = self.points_var.get().strip()
            if not points_str:
                messagebox.showerror("Error", "Por favor ingresa algunos puntos")
                return
            
            # Parsear puntos
            points = [float(p.strip()) for p in points_str.split(',')]
            
            # Evaluar
            expr = self.expr_var.get()
            results = evaluate_derivative_at_points(expr, derivative, points)
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Llenar tabla
            for x, fx, dfx_sym, dfx_num, error in results:
                values = (
                    f"{x:.6g}",
                    f"{fx:.6g}" if not math.isnan(fx) else "NaN",
                    f"{dfx_sym:.6g}" if not math.isnan(dfx_sym) else "NaN",
                    f"{dfx_num:.6g}" if not math.isnan(dfx_num) else "NaN",
                    f"{error:.2e}" if error < float('inf') else "Inf"
                )
                self.tree.insert('', 'end', values=values)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los puntos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error evaluando: {str(e)}")

    def update_plot(self):
        """Actualiza los gráficos de f(x) y f'(x)"""
        if not self.canvas:
            return
            
        try:
            expr = self.expr_var.get()
            derivative = self.derivative_var.get()
            
            if not expr or not derivative or derivative.startswith("Presiona"):
                return
            
            # Crear funciones
            f = _make_safe_func(expr)
            df_str = derivative.replace('sp.', '').replace('sqrt', 'math.sqrt').replace('log', 'math.log')
            df = _make_safe_func(df_str)
            
            # Generar puntos para graficar
            x_vals = np.linspace(-5, 5, 1000)
            
            # Evaluar funciones
            f_vals = []
            df_vals = []
            
            for x in x_vals:
                try:
                    f_val = f(x)
                    df_val = df(x)
                    if abs(f_val) > 100:  # Limitar valores extremos
                        f_val = np.nan
                    if abs(df_val) > 100:
                        df_val = np.nan
                    f_vals.append(f_val)
                    df_vals.append(df_val)
                except:
                    f_vals.append(np.nan)
                    df_vals.append(np.nan)
            
            # Limpiar y graficar
            self.ax1.clear()
            self.ax2.clear()
            
            # Gráfico de f(x)
            self.ax1.plot(x_vals, f_vals, 'b-', linewidth=2, label='f(x)')
            self.ax1.grid(True, alpha=0.3)
            self.ax1.set_title('Función f(x)', fontsize=10)
            self.ax1.set_xlabel('x')
            self.ax1.set_ylabel('f(x)')
            self.ax1.legend()
            
            # Gráfico de f'(x)
            self.ax2.plot(x_vals, df_vals, 'r-', linewidth=2, label="f'(x)")
            self.ax2.grid(True, alpha=0.3)
            self.ax2.set_title("Derivada f'(x)", fontsize=10)
            self.ax2.set_xlabel('x')
            self.ax2.set_ylabel("f'(x)")
            self.ax2.legend()
            
            # Ajustar layout y actualizar
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error actualizando gráfico: {e}")

    def clear_all(self):
        """Limpia todos los campos y resultados"""
        # Limpiar campos
        self.expr_var.set("")
        self.derivative_var.set("Presiona 'Calcular f'(x)' para obtener la derivada")
        self.points_var.set("0, 1, 2, -1, 0.5")
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Limpiar gráficos
        if self.canvas:
            self.ax1.clear()
            self.ax2.clear()
            self.ax1.text(0.5, 0.5, 'Ingresa una función para graficar', 
                         transform=self.ax1.transAxes, ha='center', va='center')
            self.ax2.text(0.5, 0.5, 'Calcula la derivada para graficar', 
                         transform=self.ax2.transAxes, ha='center', va='center')
            self.canvas.draw()


def main():
    """Función principal"""
    root = tk.Tk()
    try:
        app = DerivativasGUI(root)
        root.mainloop()
    except ImportError as e:
        messagebox.showerror("Error", f"Faltan dependencias: {e}\n"
                                    "Instala: pip install sympy matplotlib numpy")
    except Exception as e:
        messagebox.showerror("Error", f"Error iniciando aplicación: {e}")


if __name__ == "__main__":
    main()
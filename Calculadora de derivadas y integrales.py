import ast
import math
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Tuple, Optional
import sympy as sp

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import integrate
except Exception:
    FigureCanvasTkAgg = None
    plt = None
    np = None
    integrate = None


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


def numerical_integral(f: Callable[[float], float], a: float, b: float, method: str = 'quad') -> Tuple[float, float]:
    """Calcula integral numérica usando diferentes métodos"""
    if not integrate:
        raise ImportError("SciPy no disponible para integración numérica")
    
    try:
        if method == 'quad':
            result, error = integrate.quad(f, a, b)
        elif method == 'simpson':
            # Simpson con 1000 puntos
            n = 1000
            x = np.linspace(a, b, n+1)
            y = [f(xi) for xi in x]
            result = integrate.simpson(y, x)
            error = 1e-8  # Estimación del error
        elif method == 'trapz':
            # Trapezoidal con 1000 puntos
            n = 1000
            x = np.linspace(a, b, n+1)
            y = [f(xi) for xi in x]
            result = integrate.trapz(y, x)
            error = 1e-6  # Estimación del error
        else:
            raise ValueError(f"Método no reconocido: {method}")
            
        return result, error
    except Exception as e:
        raise ValueError(f"Error en integración numérica: {str(e)}")


def symbolic_derivative(expr: str) -> str:
    """Calcula derivada simbólica usando SymPy"""
    try:
        x = sp.Symbol('x')
        expr_sympy = _convert_to_sympy(expr)
        func = eval(expr_sympy, {'x': x, 'sp': sp, 'pi': sp.pi, 'e': sp.E})
        derivative = sp.diff(func, x)
        derivative_simplified = sp.simplify(derivative)
        return str(derivative_simplified)
    except Exception as e:
        raise ValueError(f"Error en derivada simbólica: {str(e)}")


def symbolic_integral(expr: str, definite: bool = False, a: Optional[float] = None, b: Optional[float] = None) -> str:
    """Calcula integral simbólica usando SymPy"""
    try:
        x = sp.Symbol('x')
        expr_sympy = _convert_to_sympy(expr)
        func = eval(expr_sympy, {'x': x, 'sp': sp, 'pi': sp.pi, 'e': sp.E})
        
        if definite and a is not None and b is not None:
            # Integral definida
            result = sp.integrate(func, (x, a, b))
        else:
            # Integral indefinida
            result = sp.integrate(func, x)
            
        result_simplified = sp.simplify(result)
        
        if not definite:
            return str(result_simplified) + " + C"
        else:
            return str(result_simplified)
            
    except Exception as e:
        raise ValueError(f"Error en integral simbólica: {str(e)}")


def _convert_to_sympy(expr: str) -> str:
    """Convierte expresión a formato SymPy"""
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
    expr_sympy = expr_sympy.replace('pi', 'sp.pi')
    expr_sympy = expr_sympy.replace('e', 'sp.E')
    return expr_sympy


def evaluate_derivative_at_points(f_expr: str, df_expr: str, x_points: List[float]) -> List[Tuple[float, float, float, float, float]]:
    """Evalúa función y derivada en puntos específicos"""
    try:
        f = _make_safe_func(f_expr)
        df_str = df_expr.replace('sp.', '').replace('sqrt', 'math.sqrt').replace('log', 'math.log')
        df = _make_safe_func(df_str)
        
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


class CalculadoraGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Calculadora de Derivadas e Integrales")
        master.geometry("1200x800")
        self.current_mode = "derivative"  # "derivative" o "integral"
        self._build_widgets()

    def _build_widgets(self):
        # Notebook para pestañas
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de Derivadas
        self.derivative_frame = ttk.Frame(notebook)
        notebook.add(self.derivative_frame, text="Derivadas")
        self._build_derivative_tab()
        
        # Pestaña de Integrales
        self.integral_frame = ttk.Frame(notebook)
        notebook.add(self.integral_frame, text="Integrales")
        self._build_integral_tab()

    def _build_derivative_tab(self):
        """Construye la pestaña de derivadas"""
        main_frame = ttk.Frame(self.derivative_frame, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Configurar el grid
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
        eval_button = ttk.Button(main_frame, text="Evaluar", command=self.evaluate_derivative_points)
        eval_button.grid(row=5, column=2, padx=(5, 0))
        
        # Botón limpiar
        clear_button = ttk.Button(main_frame, text="Limpiar", command=self.clear_derivative)
        clear_button.grid(row=5, column=3, padx=(5, 0))
        
        # Tabla de resultados
        columns = ('x', 'f(x)', "f'(x) simbólica", "f'(x) numérica", "Error")
        self.derivative_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.derivative_tree.heading(col, text=col)
            self.derivative_tree.column(col, width=120, anchor='center')
        
        self.derivative_tree.grid(row=6, column=0, columnspan=4, pady=15, sticky='nsew')
        main_frame.rowconfigure(6, weight=1)
        
        # Scrollbar
        scrollbar_der = ttk.Scrollbar(main_frame, orient='vertical', command=self.derivative_tree.yview)
        scrollbar_der.grid(row=6, column=4, sticky='ns', pady=15)
        self.derivative_tree.configure(yscrollcommand=scrollbar_der.set)

    def _build_integral_tab(self):
        """Construye la pestaña de integrales"""
        main_frame = ttk.Frame(self.integral_frame, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="CALCULADORA DE INTEGRALES", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 15))
        
        # Entrada de función
        ttk.Label(main_frame, text="f(x) =", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=(0, 5))
        self.integral_expr_var = tk.StringVar(value="x**2")
        expr_entry = ttk.Entry(main_frame, textvariable=self.integral_expr_var, width=50, font=('Arial', 10))
        expr_entry.grid(row=1, column=1, columnspan=3, sticky='we', padx=(0, 5))
        
        # Tipo de integral
        integral_type_frame = ttk.Frame(main_frame)
        integral_type_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky='w')
        
        self.integral_type_var = tk.StringVar(value="indefinite")
        indefinite_rb = ttk.Radiobutton(integral_type_frame, text="Integral Indefinida ∫f(x)dx", 
                                       variable=self.integral_type_var, value="indefinite",
                                       command=self.toggle_integral_limits)
        indefinite_rb.grid(row=0, column=0, padx=(0, 20))
        
        definite_rb = ttk.Radiobutton(integral_type_frame, text="Integral Definida", 
                                     variable=self.integral_type_var, value="definite",
                                     command=self.toggle_integral_limits)
        definite_rb.grid(row=0, column=1)
        
        # Límites de integración
        limits_frame = ttk.Frame(main_frame)
        limits_frame.grid(row=3, column=0, columnspan=4, pady=5, sticky='w')
        
        ttk.Label(limits_frame, text="Límites:").grid(row=0, column=0, padx=(0, 5))
        ttk.Label(limits_frame, text="a =").grid(row=0, column=1, padx=(10, 5))
        self.limit_a_var = tk.StringVar(value="0")
        self.limit_a_entry = ttk.Entry(limits_frame, textvariable=self.limit_a_var, width=10)
        self.limit_a_entry.grid(row=0, column=2, padx=(0, 10))
        
        ttk.Label(limits_frame, text="b =").grid(row=0, column=3, padx=(0, 5))
        self.limit_b_var = tk.StringVar(value="1")
        self.limit_b_entry = ttk.Entry(limits_frame, textvariable=self.limit_b_var, width=10)
        self.limit_b_entry.grid(row=0, column=4)
        
        # Inicialmente ocultar límites
        self.limit_a_entry.configure(state='disabled')
        self.limit_b_entry.configure(state='disabled')
        
        # Botones de cálculo
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=4, pady=15)
        
        calc_symbolic_button = ttk.Button(buttons_frame, text="Calcular Simbólicamente", 
                                         command=self.calculate_symbolic_integral)
        calc_symbolic_button.grid(row=0, column=0, padx=(0, 10))
        
        calc_numeric_button = ttk.Button(buttons_frame, text="Calcular Numéricamente", 
                                        command=self.calculate_numeric_integral)
        calc_numeric_button.grid(row=0, column=1, padx=(0, 10))
        
        clear_integral_button = ttk.Button(buttons_frame, text="Limpiar", command=self.clear_integral)
        clear_integral_button.grid(row=0, column=2)
        
        # Resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        results_frame.grid(row=5, column=0, columnspan=4, pady=15, sticky='we')
        results_frame.columnconfigure(1, weight=1)
        
        # Resultado simbólico
        ttk.Label(results_frame, text="Simbólico:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.symbolic_result_var = tk.StringVar(value="Presiona 'Calcular Simbólicamente'")
        symbolic_entry = ttk.Entry(results_frame, textvariable=self.symbolic_result_var, width=60, 
                                  font=('Arial', 10), state='readonly')
        symbolic_entry.grid(row=0, column=1, sticky='we', padx=(5, 5))
        
        copy_symbolic_button = ttk.Button(results_frame, text="Copiar", command=self.copy_symbolic_integral)
        copy_symbolic_button.grid(row=0, column=2, padx=(5, 0))
        
        # Resultado numérico
        ttk.Label(results_frame, text="Numérico:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=(0, 5), pady=(10, 0))
        self.numeric_result_var = tk.StringVar(value="Presiona 'Calcular Numéricamente'")
        numeric_entry = ttk.Entry(results_frame, textvariable=self.numeric_result_var, width=60, 
                                 font=('Arial', 10), state='readonly')
        numeric_entry.grid(row=1, column=1, sticky='we', padx=(5, 5), pady=(10, 0))
        
        # Método numérico
        method_frame = ttk.Frame(results_frame)
        method_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky='w')
        
        ttk.Label(method_frame, text="Método numérico:").grid(row=0, column=0, padx=(0, 5))
        self.numeric_method_var = tk.StringVar(value="quad")
        method_combo = ttk.Combobox(method_frame, textvariable=self.numeric_method_var, 
                                   values=["quad", "simpson", "trapz"], width=10, state='readonly')
        method_combo.grid(row=0, column=1)
        
        # Información
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding=5)
        info_frame.grid(row=6, column=0, columnspan=4, sticky='we', pady=(10, 0))
        
        info_text = ("Funciones soportadas: +, -, *, /, **, sqrt(), sin(), cos(), tan(), "
                    "log(), exp(), asin(), acos(), atan(), sinh(), cosh(), tanh(), "
                    "constantes: pi, e")
        info_label = ttk.Label(info_frame, text=info_text, wraplength=800, justify='left')
        info_label.grid(row=0, column=0, sticky='w')
        
        examples_text = ("Ejemplos: x**2, sin(x), exp(x), 1/x, sqrt(x), x*sin(x), "
                        "1/(1+x**2), exp(-x**2)")
        examples_label = ttk.Label(info_frame, text=f"Ejemplos: {examples_text}", 
                                  wraplength=800, justify='left', font=('Arial', 8))
        examples_label.grid(row=1, column=0, sticky='w', pady=(5, 0))

    def toggle_integral_limits(self):
        """Activa/desactiva los campos de límites según el tipo de integral"""
        if self.integral_type_var.get() == "definite":
            self.limit_a_entry.configure(state='normal')
            self.limit_b_entry.configure(state='normal')
        else:
            self.limit_a_entry.configure(state='disabled')
            self.limit_b_entry.configure(state='disabled')

    def calculate_derivative(self):
        """Calcula la derivada simbólica de la función"""
        try:
            expr = self.expr_var.get().strip()
            if not expr:
                messagebox.showerror("Error", "Por favor ingresa una función")
                return
            
            derivative = symbolic_derivative(expr)
            self.derivative_var.set(derivative)
            messagebox.showinfo("Éxito", "Derivada calculada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la derivada: {str(e)}")
            self.derivative_var.set("Error en el cálculo")

    def calculate_symbolic_integral(self):
        """Calcula la integral simbólica"""
        try:
            expr = self.integral_expr_var.get().strip()
            if not expr:
                messagebox.showerror("Error", "Por favor ingresa una función")
                return
            
            is_definite = self.integral_type_var.get() == "definite"
            
            if is_definite:
                try:
                    a = float(self.limit_a_var.get())
                    b = float(self.limit_b_var.get())
                except ValueError:
                    messagebox.showerror("Error", "Los límites deben ser números válidos")
                    return
                
                result = symbolic_integral(expr, definite=True, a=a, b=b)
            else:
                result = symbolic_integral(expr, definite=False)
            
            self.symbolic_result_var.set(result)
            messagebox.showinfo("Éxito", "Integral simbólica calculada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la integral simbólica: {str(e)}")
            self.symbolic_result_var.set("Error en el cálculo")

    def calculate_numeric_integral(self):
        """Calcula la integral numéricamente"""
        try:
            expr = self.integral_expr_var.get().strip()
            if not expr:
                messagebox.showerror("Error", "Por favor ingresa una función")
                return
            
            if self.integral_type_var.get() != "definite":
                messagebox.showwarning("Advertencia", "La integración numérica requiere límites definidos")
                return
            
            try:
                a = float(self.limit_a_var.get())
                b = float(self.limit_b_var.get())
            except ValueError:
                messagebox.showerror("Error", "Los límites deben ser números válidos")
                return
            
            f = _make_safe_func(expr)
            method = self.numeric_method_var.get()
            
            result, error = numerical_integral(f, a, b, method)
            
            if method == "quad":
                result_text = f"{result:.10g} ± {error:.2e}"
            else:
                result_text = f"{result:.10g} (error estimado: {error:.2e})"
                
            self.numeric_result_var.set(result_text)
            messagebox.showinfo("Éxito", "Integral numérica calculada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la integral numérica: {str(e)}")
            self.numeric_result_var.set("Error en el cálculo")

    def copy_derivative(self):
        """Copia la derivada al portapapeles"""
        derivative = self.derivative_var.get()
        if derivative and not derivative.startswith("Presiona"):
            self.master.clipboard_clear()
            self.master.clipboard_append(derivative)
            messagebox.showinfo("Copiado", "Derivada copiada al portapapeles")
        else:
            messagebox.showwarning("Advertencia", "No hay derivada para copiar")

    def copy_symbolic_integral(self):
        """Copia la integral simbólica al portapapeles"""
        integral = self.symbolic_result_var.get()
        if integral and not integral.startswith("Presiona"):
            self.master.clipboard_clear()
            self.master.clipboard_append(integral)
            messagebox.showinfo("Copiado", "Integral copiada al portapapeles")
        else:
            messagebox.showwarning("Advertencia", "No hay integral para copiar")

    def evaluate_derivative_points(self):
        """Evalúa la función y su derivada en puntos específicos"""
        try:
            derivative = self.derivative_var.get()
            if not derivative or derivative.startswith("Presiona"):
                messagebox.showerror("Error", "Primero calcula la derivada")
                return
            
            points_str = self.points_var.get().strip()
            if not points_str:
                messagebox.showerror("Error", "Por favor ingresa algunos puntos")
                return
            
            points = [float(p.strip()) for p in points_str.split(',')]
            expr = self.expr_var.get()
            results = evaluate_derivative_at_points(expr, derivative, points)
            
            # Limpiar tabla
            for item in self.derivative_tree.get_children():
                self.derivative_tree.delete(item)
            
            # Llenar tabla
            for x, fx, dfx_sym, dfx_num, error in results:
                values = (
                    f"{x:.6g}",
                    f"{fx:.6g}" if not math.isnan(fx) else "NaN",
                    f"{dfx_sym:.6g}" if not math.isnan(dfx_sym) else "NaN",
                    f"{dfx_num:.6g}" if not math.isnan(dfx_num) else "NaN",
                    f"{error:.2e}" if error < float('inf') else "Inf"
                )
                self.derivative_tree.insert('', 'end', values=values)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los puntos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error evaluando: {str(e)}")

    def clear_derivative(self):
        """Limpia los campos de derivadas"""
        self.expr_var.set("")
        self.derivative_var.set("Presiona 'Calcular f'(x)' para obtener la derivada")
        self.points_var.set("0, 1, 2, -1, 0.5")
        
        for item in self.derivative_tree.get_children():
            self.derivative_tree.delete(item)

    def clear_integral(self):
        """Limpia los campos de integrales"""
        self.integral_expr_var.set("")
        self.symbolic_result_var.set("Presiona 'Calcular Simbólicamente'")
        self.numeric_result_var.set("Presiona 'Calcular Numéricamente'")
        self.limit_a_var.set("0")
        self.limit_b_var.set("1")
        self.integral_type_var.set("indefinite")
        self.toggle_integral_limits()


def main():
    """Función principal"""
    root = tk.Tk()
    try:
        app = CalculadoraGUI(root)
        root.mainloop()
    except ImportError as e:
        messagebox.showerror("Error", f"Faltan dependencias: {e}\n"
                                    "Instala: pip install sympy matplotlib numpy scipy")
    except Exception as e:
        messagebox.showerror("Error", f"Error iniciando aplicación: {e}")


if __name__ == "__main__":
    main()
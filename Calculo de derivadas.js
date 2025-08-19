import ast
import math
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

try:
    import numpy as np
except ImportError:
    np = None

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    # Intentar establecer un estilo, si falla usar default
    try:
        plt.style.use('seaborn-v0_8')
    except:
        try:
            plt.style.use('seaborn')
        except:
            pass  # Usar estilo por defecto
except ImportError:
    FigureCanvasTkAgg = None
    plt = None


def _make_safe_func(expr: str) -> Callable[[float], float]:
    """Crear función segura desde expresión string"""
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed_names.update({"abs": abs, "pow": pow, "min": min, "max": max})
    
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


def derivada_adelante(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Derivada usando diferencias hacia adelante"""
    return (f(x + h) - f(x)) / h


def derivada_atras(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Derivada usando diferencias hacia atrás"""
    return (f(x) - f(x - h)) / h


def derivada_centrada(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Derivada usando diferencias centrales"""
    return (f(x + h) - f(x - h)) / (2 * h)


def derivada_cinco_puntos(f: Callable[[float], float], x: float, h: float = 1e-3) -> float:
    """Derivada usando fórmula de 5 puntos"""
    return (-f(x + 2*h) + 8*f(x + h) - 8*f(x - h) + f(x - 2*h)) / (12 * h)


def segunda_derivada(f: Callable[[float], float], x: float, h: float = 1e-4) -> float:
    """Segunda derivada"""
    return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)


def crear_puntos(x_min, x_max, num_puntos):
    """Crear lista de puntos"""
    if np is not None:
        return np.linspace(x_min, x_max, num_puntos)
    else:
        step = (x_max - x_min) / (num_puntos - 1)
        return [x_min + i * step for i in range(num_puntos)]


def calcular_derivadas_rango(f: Callable[[float], float], x_min: float, x_max: float, 
                           num_puntos: int = 100, h: float = 1e-5):
    """Calcular derivadas en un rango de valores"""
    x_vals = crear_puntos(x_min, x_max, num_puntos)
    resultados = []
    
    for x in x_vals:
        try:
            fx = f(x)
            df_adelante = derivada_adelante(f, x, h)
            df_atras = derivada_atras(f, x, h)
            df_centrada = derivada_centrada(f, x, h)
            df_cinco_pts = derivada_cinco_puntos(f, x, h)
            d2f = segunda_derivada(f, x, h)
            
            resultados.append((x, fx, df_adelante, df_atras, df_centrada, 
                             df_cinco_pts, d2f))
        except:
            continue
    
    return resultados


class DerivadasGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Calculadora de Derivadas Numéricas")
        master.geometry("1000x700")
        self._build_widgets()
        
    def _build_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Entrada de función
        ttk.Label(main_frame, text="Función f(x):").grid(row=0, column=0, sticky='w', pady=5)
        self.expr_var = tk.StringVar(value="x**2 + 2*x + 1")
        ttk.Entry(main_frame, textvariable=self.expr_var, width=50).grid(row=0, column=1, columnspan=3, sticky='we', pady=5)
        
        # Parámetros para punto específico
        params_frame = ttk.LabelFrame(main_frame, text="Cálculo en punto específico", padding=10)
        params_frame.grid(row=1, column=0, columnspan=4, sticky='we', pady=10)
        
        ttk.Label(params_frame, text="x:").grid(row=0, column=0, padx=5)
        self.x_var = tk.StringVar(value="1.0")
        ttk.Entry(params_frame, textvariable=self.x_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(params_frame, text="h:").grid(row=0, column=2, padx=5)
        self.h_var = tk.StringVar(value="1e-5")
        ttk.Entry(params_frame, textvariable=self.h_var, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Button(params_frame, text="Calcular en Punto", 
                  command=self.calcular_punto).grid(row=0, column=4, padx=10)
        
        # Parámetros para rango
        rango_frame = ttk.LabelFrame(main_frame, text="Cálculo en rango", padding=10)
        rango_frame.grid(row=2, column=0, columnspan=4, sticky='we', pady=10)
        
        ttk.Label(rango_frame, text="x_min:").grid(row=0, column=0, padx=5)
        self.x_min_var = tk.StringVar(value="-2")
        ttk.Entry(rango_frame, textvariable=self.x_min_var, width=8).grid(row=0, column=1, padx=5)
        
        ttk.Label(rango_frame, text="x_max:").grid(row=0, column=2, padx=5)
        self.x_max_var = tk.StringVar(value="2")
        ttk.Entry(rango_frame, textvariable=self.x_max_var, width=8).grid(row=0, column=3, padx=5)
        
        ttk.Label(rango_frame, text="Puntos:").grid(row=0, column=4, padx=5)
        self.puntos_var = tk.StringVar(value="50")
        ttk.Entry(rango_frame, textvariable=self.puntos_var, width=8).grid(row=0, column=5, padx=5)
        
        ttk.Button(rango_frame, text="Calcular Rango", 
                  command=self.calcular_rango).grid(row=0, column=6, padx=10)
        
        # Botones adicionales
        botones_frame = ttk.Frame(main_frame)
        botones_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(botones_frame, text="Limpiar Todo", 
                  command=self.limpiar_todo).grid(row=0, column=0, padx=5)
        ttk.Button(botones_frame, text="Exportar Datos", 
                  command=self.exportar_datos).grid(row=0, column=1, padx=5)
        
        # Resultado de punto específico
        self.resultado_punto = tk.StringVar(value="Selecciona una función y un punto para calcular")
        result_frame = ttk.LabelFrame(main_frame, text="Resultado en punto específico", padding=10)
        result_frame.grid(row=4, column=0, columnspan=4, sticky='we', pady=10)
        ttk.Label(result_frame, textvariable=self.resultado_punto, wraplength=800).grid(row=0, column=0, sticky='w')
        
        # Tabla de resultados
        tabla_frame = ttk.LabelFrame(main_frame, text="Tabla de resultados", padding=10)
        tabla_frame.grid(row=5, column=0, columnspan=4, sticky='nsew', pady=10)
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Treeview con scrollbars
        tree_frame = ttk.Frame(tabla_frame)
        tree_frame.grid(row=0, column=0, sticky='nsew')
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame, show='headings', height=8)
        scrollbar_v = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        # Configurar gráfico
        if FigureCanvasTkAgg and plt:
            grafico_frame = ttk.LabelFrame(main_frame, text="Gráfico", padding=10)
            grafico_frame.grid(row=6, column=0, columnspan=4, sticky='nsew', pady=10)
            main_frame.rowconfigure(6, weight=1)
            
            self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 6))
            self.fig.tight_layout(pad=3.0)
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=grafico_frame)
            self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
            grafico_frame.columnconfigure(0, weight=1)
            grafico_frame.rowconfigure(0, weight=1)
        else:
            ttk.Label(main_frame, text="matplotlib no disponible - No se pueden mostrar gráficos").grid(
                row=6, column=0, columnspan=4, pady=20)
            self.canvas = None
            self.ax1 = None
            self.ax2 = None
    
    def _configurar_tabla(self, columnas):
        """Configurar columnas de la tabla"""
        self.tree["columns"] = columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
    
    def _llenar_tabla(self, datos):
        """Llenar tabla con datos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar datos
        for fila in datos:
            valores = [f"{v:.6g}" if isinstance(v, (float, int)) else str(v) for v in fila]
            self.tree.insert('', 'end', values=valores)
    
    def calcular_punto(self):
        """Calcular derivadas en un punto específico"""
        try:
            f = _make_safe_func(self.expr_var.get())
            x = float(self.x_var.get())
            h = float(self.h_var.get())
            
            # Calcular todas las derivadas
            fx = f(x)
            df_adelante = derivada_adelante(f, x, h)
            df_atras = derivada_atras(f, x, h)
            df_centrada = derivada_centrada(f, x, h)
            df_cinco_pts = derivada_cinco_puntos(f, x, h)
            d2f = segunda_derivada(f, x, h)
            
            # Mostrar resultado
            resultado = f"""Función: {self.expr_var.get()}
Punto x = {x}, h = {h}

f({x}) = {fx:.8g}
f'({x}) ≈ {df_centrada:.8g} (diferencias centrales - recomendado)

Comparación de métodos:
• Diferencias adelante:    {df_adelante:.8g}
• Diferencias atrás:       {df_atras:.8g}  
• Diferencias centrales:   {df_centrada:.8g}
• Fórmula 5 puntos:        {df_cinco_pts:.8g}
• Segunda derivada f''(x): {d2f:.8g}"""
            
            self.resultado_punto.set(resultado)
            
            # Configurar tabla para punto específico
            columnas = ["Método", "Valor"]
            self._configurar_tabla(columnas)
            
            datos = [
                ("f(x)", fx),
                ("Diff. Adelante", df_adelante),
                ("Diff. Atrás", df_atras),
                ("Diff. Centrales", df_centrada),
                ("5 Puntos", df_cinco_pts),
                ("Segunda derivada", d2f)
            ]
            
            self._llenar_tabla(datos)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def calcular_rango(self):
        """Calcular derivadas en un rango de valores"""
        try:
            f = _make_safe_func(self.expr_var.get())
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())
            num_puntos = int(self.puntos_var.get())
            h = float(self.h_var.get())
            
            # Calcular derivadas en el rango
            resultados = calcular_derivadas_rango(f, x_min, x_max, num_puntos, h)
            
            if not resultados:
                messagebox.showwarning("Advertencia", "No se pudieron calcular derivadas en el rango especificado")
                return
            
            # Configurar tabla
            columnas = ["x", "f(x)", "f'(x) Adel.", "f'(x) Atrás", "f'(x) Centr.", "f'(x) 5pts", "f''(x)"]
            self._configurar_tabla(columnas)
            self._llenar_tabla(resultados)
            
            # Actualizar resultado
            self.resultado_punto.set(f"Calculadas derivadas para {len(resultados)} puntos en [{x_min}, {x_max}]")
            
            # Crear gráficos
            if self.canvas and self.ax1 and self.ax2:
                self._crear_graficos(resultados, f)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def _crear_graficos(self, resultados, f):
        """Crear gráficos de función y derivadas"""
        try:
            x_vals = [r[0] for r in resultados]
            f_vals = [r[1] for r in resultados]
            df_vals = [r[4] for r in resultados]  # Diferencias centrales
            d2f_vals = [r[6] for r in resultados]  # Segunda derivada
            
            # Limpiar gráficos
            self.ax1.clear()
            self.ax2.clear()
            
            # Gráfico 1: Función y primera derivada
            self.ax1.plot(x_vals, f_vals, 'b-', label='f(x)', linewidth=2)
            self.ax1.plot(x_vals, df_vals, 'r--', label="f'(x)", linewidth=2)
            self.ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            self.ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            self.ax1.set_xlabel('x')
            self.ax1.set_ylabel('y')
            self.ax1.set_title(f'Función: {self.expr_var.get()}')
            self.ax1.legend()
            self.ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Primera y segunda derivada
            self.ax2.plot(x_vals, df_vals, 'r-', label="f'(x)", linewidth=2)
            self.ax2.plot(x_vals, d2f_vals, 'g-', label="f''(x)", linewidth=2)
            self.ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            self.ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            self.ax2.set_xlabel('x')
            self.ax2.set_ylabel('y')
            self.ax2.set_title('Derivadas')
            self.ax2.legend()
            self.ax2.grid(True, alpha=0.3)
            
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error creando gráficos: {e}")
    
    def limpiar_todo(self):
        """Limpiar todos los resultados"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Limpiar resultado
        self.resultado_punto.set("Selecciona una función y un punto para calcular")
        
        # Limpiar gráficos
        if self.canvas and self.ax1 and self.ax2:
            self.ax1.clear()
            self.ax2.clear()
            self.canvas.draw()
    
    def exportar_datos(self):
        """Exportar datos de la tabla a archivo CSV"""
        try:
            from tkinter import filedialog
            import csv
            
            if not self.tree.get_children():
                messagebox.showwarning("Advertencia", "No hay datos para exportar")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Escribir encabezados
                    headers = [self.tree.heading(col)['text'] for col in self.tree['columns']]
                    writer.writerow(headers)
                    
                    # Escribir datos
                    for item in self.tree.get_children():
                        values = self.tree.item(item)['values']
                        writer.writerow(values)
                
                messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando datos: {str(e)}")


def main():
    root = tk.Tk()
    app = DerivadasGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
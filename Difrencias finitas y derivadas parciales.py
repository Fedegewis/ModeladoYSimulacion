import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np
import sympy as sp
from sympy import symbols, sin, cos, tan, log, ln, exp, sqrt, pi, E
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DiferenciasFinitasCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Diferencias Finitas y Derivadas Parciales")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        
        # Variables
        self.metodo = tk.StringVar(value='progresiva')
        self.tipo_derivada = tk.StringVar(value='simple')
        self.funcion_str = tk.StringVar(value='x**2 + 3*x + 1')
        self.punto_x = tk.DoubleVar(value=2.0)
        self.h_value = tk.DoubleVar(value=0.1)
        self.funcion_parcial_str = tk.StringVar(value='x**2 + y**2 + x*y')
        self.punto_y = tk.DoubleVar(value=1.0)
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text="🧮 Calculadora de Diferencias Finitas", 
                              font=('Arial', 16, 'bold'), bg='#f0f8ff', fg='#1e40af')
        title_label.pack(pady=(0, 20))
        
        # Frame para opciones
        options_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Tipo de derivada
        tipo_frame = ttk.Frame(options_frame)
        tipo_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(tipo_frame, text="Tipo de Derivada:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        tipo_buttons_frame = ttk.Frame(tipo_frame)
        tipo_buttons_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Radiobutton(tipo_buttons_frame, text="Derivada Ordinaria f'(x)", 
                       variable=self.tipo_derivada, value='simple',
                       command=self.cambiar_tipo).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(tipo_buttons_frame, text="Derivadas Parciales ∂f/∂x, ∂f/∂y", 
                       variable=self.tipo_derivada, value='parcial',
                       command=self.cambiar_tipo).pack(side=tk.LEFT)
        
        # Método de diferencias finitas
        metodo_frame = ttk.Frame(options_frame)
        metodo_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(metodo_frame, text="Método:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        metodo_buttons_frame = ttk.Frame(metodo_frame)
        metodo_buttons_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Radiobutton(metodo_buttons_frame, text="→ Progresiva", 
                       variable=self.metodo, value='progresiva').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(metodo_buttons_frame, text="← Regresiva", 
                       variable=self.metodo, value='regresiva').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(metodo_buttons_frame, text="↕ Central", 
                       variable=self.metodo, value='central').pack(side=tk.LEFT)
        
        # Frame para inputs (se creará dinámicamente)
        self.input_frame = ttk.LabelFrame(main_frame, text="Parámetros", padding="10")
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.calc_button = tk.Button(button_frame, text="🧮 Calcular", 
                                    command=self.calcular, bg='#3b82f6', fg='white',
                                    font=('Arial', 12, 'bold'), pady=8)
        self.calc_button.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="🗑️ Limpiar", 
                 command=self.limpiar, bg='#ef4444', fg='white',
                 font=('Arial', 12, 'bold'), pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="📊 Graficar", 
                 command=self.graficar, bg='#10b981', fg='white',
                 font=('Arial', 12, 'bold'), pady=8).pack(side=tk.LEFT)
        
        # Área de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, 
                                                    font=('Consolas', 10),
                                                    bg='#f8fafc', fg='#1e293b')
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Crear inputs iniciales
        self.cambiar_tipo()
        
    def cambiar_tipo(self):
        # Limpiar frame de inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
            
        if self.tipo_derivada.get() == 'simple':
            self.crear_inputs_simple()
        else:
            self.crear_inputs_parcial()
            
    def crear_inputs_simple(self):
        # Función
        func_frame = ttk.Frame(self.input_frame)
        func_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(func_frame, text="Función f(x):", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        func_entry = ttk.Entry(func_frame, textvariable=self.funcion_str, font=('Consolas', 10))
        func_entry.pack(fill=tk.X, pady=(5, 0))
        
        tk.Label(func_frame, text="Ejemplos: x**2 + 3*x + 1, sin(x), exp(x), sqrt(x)", 
                font=('Arial', 8), fg='#6b7280').pack(anchor=tk.W, pady=(2, 0))
        
        # Punto y h
        params_frame = ttk.Frame(self.input_frame)
        params_frame.pack(fill=tk.X)
        
        # Punto x
        punto_frame = ttk.Frame(params_frame)
        punto_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(punto_frame, text="Punto x:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Entry(punto_frame, textvariable=self.punto_x, font=('Consolas', 10)).pack(fill=tk.X, pady=(5, 0))
        
        # Paso h
        h_frame = ttk.Frame(params_frame)
        h_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(h_frame, text="Paso h:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Entry(h_frame, textvariable=self.h_value, font=('Consolas', 10)).pack(fill=tk.X, pady=(5, 0))
        
    def crear_inputs_parcial(self):
        # Función de dos variables
        func_frame = ttk.Frame(self.input_frame)
        func_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(func_frame, text="Función f(x,y):", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        func_entry = ttk.Entry(func_frame, textvariable=self.funcion_parcial_str, font=('Consolas', 10))
        func_entry.pack(fill=tk.X, pady=(5, 0))
        
        tk.Label(func_frame, text="Ejemplos: x**2 + y**2, x*y + sin(x), exp(x+y)", 
                font=('Arial', 8), fg='#6b7280').pack(anchor=tk.W, pady=(2, 0))
        
        # Puntos y h
        params_frame = ttk.Frame(self.input_frame)
        params_frame.pack(fill=tk.X)
        
        # Punto x
        x_frame = ttk.Frame(params_frame)
        x_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Label(x_frame, text="Punto x:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Entry(x_frame, textvariable=self.punto_x, font=('Consolas', 10)).pack(fill=tk.X, pady=(5, 0))
        
        # Punto y
        y_frame = ttk.Frame(params_frame)
        y_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        tk.Label(y_frame, text="Punto y:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Entry(y_frame, textvariable=self.punto_y, font=('Consolas', 10)).pack(fill=tk.X, pady=(5, 0))
        
        # Paso h
        h_frame = ttk.Frame(params_frame)
        h_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        tk.Label(h_frame, text="Paso h:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Entry(h_frame, textvariable=self.h_value, font=('Consolas', 10)).pack(fill=tk.X, pady=(5, 0))
        
    def evaluar_funcion(self, expr_str, x_val, y_val=None):
        """Evalúa una función usando sympy"""
        try:
            x, y = symbols('x y')
            expr = sp.sympify(expr_str)
            
            if y_val is not None:
                return float(expr.subs([(x, x_val), (y, y_val)]))
            else:
                return float(expr.subs(x, x_val))
        except Exception as e:
            raise ValueError(f"Error al evaluar la función: {str(e)}")
    
    def calcular(self):
        try:
            self.result_text.delete(1.0, tk.END)
            
            metodo = self.metodo.get()
            h = self.h_value.get()
            
            resultado = ""
            resultado += f"{'='*60}\n"
            resultado += f"CÁLCULO DE DIFERENCIAS FINITAS\n"
            resultado += f"{'='*60}\n\n"
            
            if self.tipo_derivada.get() == 'simple':
                # Derivadas ordinarias
                funcion = self.funcion_str.get()
                x_punto = self.punto_x.get()
                
                resultado += f"Función: f(x) = {funcion}\n"
                resultado += f"Punto: x = {x_punto}\n"
                resultado += f"Paso: h = {h}\n"
                resultado += f"Método: {metodo.upper()}\n\n"
                
                # PASO 1: Evaluar función en todos los puntos necesarios
                resultado += "PASO 1 - EVALUACIÓN DE LA FUNCIÓN:\n"
                resultado += "-" * 40 + "\n"
                
                f_x = self.evaluar_funcion(funcion, x_punto)
                resultado += f"f({x_punto}) = {f_x:.8f}\n"
                
                if metodo == 'progresiva':
                    f_x_plus_h = self.evaluar_funcion(funcion, x_punto + h)
                    resultado += f"f({x_punto + h}) = f({x_punto} + {h}) = {f_x_plus_h:.8f}\n\n"
                    
                    resultado += "PASO 2 - APLICAR FÓRMULA DE DIFERENCIA PROGRESIVA:\n"
                    resultado += "-" * 50 + "\n"
                    derivada = (f_x_plus_h - f_x) / h
                    resultado += f"f'({x_punto}) ≈ [f({x_punto + h}) - f({x_punto})] / {h}\n"
                    resultado += f"f'({x_punto}) ≈ [{f_x_plus_h:.8f} - {f_x:.8f}] / {h}\n"
                    resultado += f"f'({x_punto}) ≈ {(f_x_plus_h - f_x):.8f} / {h}\n"
                    resultado += f"f'({x_punto}) ≈ {derivada:.8f}\n\n"
                    
                elif metodo == 'regresiva':
                    f_x_minus_h = self.evaluar_funcion(funcion, x_punto - h)
                    resultado += f"f({x_punto - h}) = f({x_punto} - {h}) = {f_x_minus_h:.8f}\n\n"
                    
                    resultado += "PASO 2 - APLICAR FÓRMULA DE DIFERENCIA REGRESIVA:\n"
                    resultado += "-" * 50 + "\n"
                    derivada = (f_x - f_x_minus_h) / h
                    resultado += f"f'({x_punto}) ≈ [f({x_punto}) - f({x_punto - h})] / {h}\n"
                    resultado += f"f'({x_punto}) ≈ [{f_x:.8f} - {f_x_minus_h:.8f}] / {h}\n"
                    resultado += f"f'({x_punto}) ≈ {(f_x - f_x_minus_h):.8f} / {h}\n"
                    resultado += f"f'({x_punto}) ≈ {derivada:.8f}\n\n"
                    
                elif metodo == 'central':
                    f_x_plus_h = self.evaluar_funcion(funcion, x_punto + h)
                    f_x_minus_h = self.evaluar_funcion(funcion, x_punto - h)
                    resultado += f"f({x_punto + h}) = f({x_punto} + {h}) = {f_x_plus_h:.8f}\n"
                    resultado += f"f({x_punto - h}) = f({x_punto} - {h}) = {f_x_minus_h:.8f}\n\n"
                    
                    resultado += "PASO 2 - APLICAR FÓRMULA DE DIFERENCIA CENTRAL:\n"
                    resultado += "-" * 50 + "\n"
                    derivada = (f_x_plus_h - f_x_minus_h) / (2 * h)
                    resultado += f"f'({x_punto}) ≈ [f({x_punto + h}) - f({x_punto - h})] / (2 × {h})\n"
                    resultado += f"f'({x_punto}) ≈ [{f_x_plus_h:.8f} - {f_x_minus_h:.8f}] / {2 * h}\n"
                    resultado += f"f'({x_punto}) ≈ {(f_x_plus_h - f_x_minus_h):.8f} / {2 * h}\n"
                    resultado += f"f'({x_punto}) ≈ {derivada:.8f}\n\n"
                
                # Calcular derivada exacta si es posible
                try:
                    x = symbols('x')
                    expr = sp.sympify(funcion)
                    derivada_exacta = sp.diff(expr, x)
                    valor_exacto = float(derivada_exacta.subs(x, x_punto))
                    error = abs(derivada - valor_exacto)
                    
                    resultado += "COMPARACIÓN CON DERIVADA EXACTA:\n"
                    resultado += f"f'(x) = {derivada_exacta}\n"
                    resultado += f"f'({x_punto}) exacto = {valor_exacto:.8f}\n"
                    resultado += f"Error absoluto = {error:.8f}\n"
                    resultado += f"Error relativo = {(error/abs(valor_exacto)*100):.6f}%\n"
                except:
                    resultado += "No se pudo calcular la derivada exacta.\n"
                    
            else:
                # Derivadas parciales
                funcion = self.funcion_parcial_str.get()
                x_punto = self.punto_x.get()
                y_punto = self.punto_y.get()
                
                resultado += f"Función: f(x,y) = {funcion}\n"
                resultado += f"Punto: ({x_punto}, {y_punto})\n"
                resultado += f"Paso: h = {h}\n"
                resultado += f"Método: {metodo.upper()}\n\n"
                
                # PASO 1: Evaluar función en todos los puntos necesarios
                resultado += "PASO 1 - EVALUACIÓN DE LA FUNCIÓN:\n"
                resultado += "-" * 40 + "\n"
                
                f_xy = self.evaluar_funcion(funcion, x_punto, y_punto)
                resultado += f"f({x_punto},{y_punto}) = {f_xy:.8f}\n"
                
                if metodo == 'progresiva':
                    f_x_plus_h_y = self.evaluar_funcion(funcion, x_punto + h, y_punto)
                    f_x_y_plus_h = self.evaluar_funcion(funcion, x_punto, y_punto + h)
                    resultado += f"f({x_punto + h},{y_punto}) = {f_x_plus_h_y:.8f}\n"
                    resultado += f"f({x_punto},{y_punto + h}) = {f_x_y_plus_h:.8f}\n\n"
                    
                    resultado += "PASO 2 - APLICAR FÓRMULAS DE DIFERENCIAS PROGRESIVAS:\n"
                    resultado += "-" * 55 + "\n"
                    
                    derivada_x = (f_x_plus_h_y - f_xy) / h
                    derivada_y = (f_x_y_plus_h - f_xy) / h
                    
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ [f({x_punto + h},{y_punto}) - f({x_punto},{y_punto})] / {h}\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ [{f_x_plus_h_y:.8f} - {f_xy:.8f}] / {h}\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ {(f_x_plus_h_y - f_xy):.8f} / {h}\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ {derivada_x:.8f}\n\n"
                    
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ [f({x_punto},{y_punto + h}) - f({x_punto},{y_punto})] / {h}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ [{f_x_y_plus_h:.8f} - {f_xy:.8f}] / {h}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ {(f_x_y_plus_h - f_xy):.8f} / {h}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ {derivada_y:.8f}\n\n"
                    
                elif metodo == 'regresiva':
                    f_x_minus_h_y = self.evaluar_funcion(funcion, x_punto - h, y_punto)
                    f_x_y_minus_h = self.evaluar_funcion(funcion, x_punto, y_punto - h)
                    resultado += f"f({x_punto - h},{y_punto}) = {f_x_minus_h_y:.8f}\n"
                    resultado += f"f({x_punto},{y_punto - h}) = {f_x_y_minus_h:.8f}\n\n"
                    
                    resultado += "PASO 2 - APLICAR FÓRMULAS DE DIFERENCIAS REGRESIVAS:\n"
                    resultado += "-" * 55 + "\n"
                    
                    derivada_x = (f_xy - f_x_minus_h_y) / h
                    derivada_y = (f_xy - f_x_y_minus_h) / h
                    
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ [f({x_punto},{y_punto}) - f({x_punto - h},{y_punto})] / {h}\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ [{f_xy:.8f} - {f_x_minus_h_y:.8f}] / {h}\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ {(f_xy - f_x_minus_h_y):.8f} / {h}\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ {derivada_x:.8f}\n\n"
                    
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ [f({x_punto},{y_punto}) - f({x_punto},{y_punto - h})] / {h}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ [{f_xy:.8f} - {f_x_y_minus_h:.8f}] / {h}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ {(f_xy - f_x_y_minus_h):.8f} / {h}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ {derivada_y:.8f}\n\n"
                    
                elif metodo == 'central':
                    f_x_plus_h_y = self.evaluar_funcion(funcion, x_punto + h, y_punto)
                    f_x_minus_h_y = self.evaluar_funcion(funcion, x_punto - h, y_punto)
                    f_x_y_plus_h = self.evaluar_funcion(funcion, x_punto, y_punto + h)
                    f_x_y_minus_h = self.evaluar_funcion(funcion, x_punto, y_punto - h)
                    
                    resultado += f"f({x_punto + h},{y_punto}) = {f_x_plus_h_y:.8f}\n"
                    resultado += f"f({x_punto - h},{y_punto}) = {f_x_minus_h_y:.8f}\n"
                    resultado += f"f({x_punto},{y_punto + h}) = {f_x_y_plus_h:.8f}\n"
                    resultado += f"f({x_punto},{y_punto - h}) = {f_x_y_minus_h:.8f}\n\n"
                    
                    resultado += "PASO 2 - APLICAR FÓRMULAS DE DIFERENCIAS CENTRALES:\n"
                    resultado += "-" * 55 + "\n"
                    
                    derivada_x = (f_x_plus_h_y - f_x_minus_h_y) / (2 * h)
                    derivada_y = (f_x_y_plus_h - f_x_y_minus_h) / (2 * h)
                    
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ [f({x_punto + h},{y_punto}) - f({x_punto - h},{y_punto})] / (2 × {h})\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ [{f_x_plus_h_y:.8f} - {f_x_minus_h_y:.8f}] / {2 * h}\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ {(f_x_plus_h_y - f_x_minus_h_y):.8f} / {2 * h}\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) ≈ {derivada_x:.8f}\n\n"
                    
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ [f({x_punto},{y_punto + h}) - f({x_punto},{y_punto - h})] / (2 × {h})\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ [{f_x_y_plus_h:.8f} - {f_x_y_minus_h:.8f}] / {2 * h}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ {(f_x_y_plus_h - f_x_y_minus_h):.8f} / {2 * h}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) ≈ {derivada_y:.8f}\n\n"
                
                # Calcular derivadas exactas si es posible
                try:
                    x, y = symbols('x y')
                    expr = sp.sympify(funcion)
                    derivada_x_exacta = sp.diff(expr, x)
                    derivada_y_exacta = sp.diff(expr, y)
                    
                    valor_exacto_x = float(derivada_x_exacta.subs([(x, x_punto), (y, y_punto)]))
                    valor_exacto_y = float(derivada_y_exacta.subs([(x, x_punto), (y, y_punto)]))
                    
                    error_x = abs(derivada_x - valor_exacto_x)
                    error_y = abs(derivada_y - valor_exacto_y)
                    
                    resultado += "COMPARACIÓN CON DERIVADAS EXACTAS:\n"
                    resultado += f"∂f/∂x = {derivada_x_exacta}\n"
                    resultado += f"∂f/∂y = {derivada_y_exacta}\n\n"
                    resultado += f"∂f/∂x({x_punto},{y_punto}) exacto = {valor_exacto_x:.8f}\n"
                    resultado += f"∂f/∂y({x_punto},{y_punto}) exacto = {valor_exacto_y:.8f}\n\n"
                    resultado += f"Error absoluto en ∂f/∂x = {error_x:.8f}\n"
                    resultado += f"Error absoluto en ∂f/∂y = {error_y:.8f}\n"
                except:
                    resultado += "No se pudieron calcular las derivadas exactas.\n"
            
            self.result_text.insert(tk.END, resultado)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo:\n{str(e)}")
    
    def limpiar(self):
        self.result_text.delete(1.0, tk.END)
        
    def graficar(self):
        """Grafica la función y muestra los puntos usados en el cálculo"""
        try:
            if self.tipo_derivada.get() == 'simple':
                self.graficar_simple()
            else:
                self.graficar_parcial()
        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar:\n{str(e)}")
    
    def graficar_simple(self):
        funcion = self.funcion_str.get()
        x_punto = self.punto_x.get()
        h = self.h_value.get()
        metodo = self.metodo.get()
        
        # Crear ventana para el gráfico
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Gráfico de la Función")
        graph_window.geometry("800x600")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Rango para el gráfico
        x_min = x_punto - 3*h
        x_max = x_punto + 3*h
        x_vals = np.linspace(x_min, x_max, 1000)
        
        # Evaluar función
        y_vals = []
        for x in x_vals:
            try:
                y_vals.append(self.evaluar_funcion(funcion, x))
            except:
                y_vals.append(np.nan)
        
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {funcion}')
        
        # Marcar puntos según el método
        f_x = self.evaluar_funcion(funcion, x_punto)
        ax.plot(x_punto, f_x, 'ro', markersize=8, label=f'f({x_punto})')
        
        if metodo == 'progresiva':
            f_x_plus_h = self.evaluar_funcion(funcion, x_punto + h)
            ax.plot(x_punto + h, f_x_plus_h, 'go', markersize=8, label=f'f({x_punto + h})')
            ax.plot([x_punto, x_punto + h], [f_x, f_x_plus_h], 'r--', alpha=0.7)
            
        elif metodo == 'regresiva':
            f_x_minus_h = self.evaluar_funcion(funcion, x_punto - h)
            ax.plot(x_punto - h, f_x_minus_h, 'go', markersize=8, label=f'f({x_punto - h})')
            ax.plot([x_punto - h, x_punto], [f_x_minus_h, f_x], 'r--', alpha=0.7)
            
        elif metodo == 'central':
            f_x_plus_h = self.evaluar_funcion(funcion, x_punto + h)
            f_x_minus_h = self.evaluar_funcion(funcion, x_punto - h)
            ax.plot(x_punto + h, f_x_plus_h, 'go', markersize=8, label=f'f({x_punto + h})')
            ax.plot(x_punto - h, f_x_minus_h, 'mo', markersize=8, label=f'f({x_punto - h})')
            ax.plot([x_punto - h, x_punto + h], [f_x_minus_h, f_x_plus_h], 'r--', alpha=0.7)
        
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Diferencia Finita {metodo.capitalize()} - f(x) = {funcion}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def graficar_parcial(self):
        messagebox.showinfo("Gráfico 3D", "Para derivadas parciales, el gráfico 3D requiere librerías adicionales.\nLos resultados numéricos están en el área de texto.")

def main():
    root = tk.Tk()
    app = DiferenciasFinitasCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
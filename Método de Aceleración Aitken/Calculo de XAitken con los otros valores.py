# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 20:11:01 2025

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

class AitkenCalculatorGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Calculadora de Aceleración de Aitken")
        master.geometry("800x700")
        self._build_widgets()
        self.calculation_history = []

    def _build_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding=15)
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Título
        title_label = ttk.Label(main_frame, text="CALCULADORA DE ACELERACIÓN DE AITKEN", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=6, pady=(0, 20))
        
        # Descripción de la fórmula
        formula_frame = ttk.LabelFrame(main_frame, text="Fórmula de Aitken", padding=10)
        formula_frame.grid(row=1, column=0, columnspan=6, sticky='ew', pady=(0, 15))
        
        formula_text = "x̂ = x₀ - (x₁ - x₀)² / (x₂ - 2x₁ + x₀)"
        ttk.Label(formula_frame, text=formula_text, font=('Courier', 12)).pack()
        
        # Frame para inputs
        input_frame = ttk.LabelFrame(main_frame, text="Valores de Entrada", padding=10)
        input_frame.grid(row=2, column=0, columnspan=6, sticky='ew', pady=(0, 15))
        
        # Entradas para x0, x1, x2
        ttk.Label(input_frame, text="x₀:", font=('Arial', 11, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        self.x0_var = tk.StringVar(value="1.0")
        self.x0_entry = ttk.Entry(input_frame, textvariable=self.x0_var, width=15, font=('Arial', 11))
        self.x0_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="x₁:", font=('Arial', 11, 'bold')).grid(row=0, column=2, padx=5, pady=5)
        self.x1_var = tk.StringVar(value="0.367879")
        self.x1_entry = ttk.Entry(input_frame, textvariable=self.x1_var, width=15, font=('Arial', 11))
        self.x1_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="x₂:", font=('Arial', 11, 'bold')).grid(row=0, column=4, padx=5, pady=5)
        self.x2_var = tk.StringVar(value="0.692201")
        self.x2_entry = ttk.Entry(input_frame, textvariable=self.x2_var, width=15, font=('Arial', 11))
        self.x2_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=6, pady=(0, 15))
        
        ttk.Button(button_frame, text="Calcular Aitken", command=self.calculate_aitken,
                  style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Agregar a Historial", command=self.add_to_history).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpiar Todo", command=self.clear_all).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Ejemplos", command=self.show_examples).pack(side='left', padx=5)
        
        # Frame de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados del Cálculo", padding=10)
        result_frame.grid(row=4, column=0, columnspan=6, sticky='ew', pady=(0, 15))
        
        # Resultado principal
        self.result_var = tk.StringVar(value="x̂_Aitken = (presiona 'Calcular Aitken')")
        result_label = ttk.Label(result_frame, textvariable=self.result_var, 
                                font=('Arial', 12, 'bold'), foreground='blue')
        result_label.pack(pady=5)
        
        # Detalles del cálculo
        self.details_text = tk.Text(result_frame, height=6, width=80, font=('Courier', 10))
        self.details_text.pack(pady=5)
        
        # Scrollbar para detalles
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)
        
        # Frame del historial
        history_frame = ttk.LabelFrame(main_frame, text="Historial de Cálculos", padding=10)
        history_frame.grid(row=5, column=0, columnspan=6, sticky='ew', pady=(0, 15))
        
        # Tabla del historial
        self.history_tree = ttk.Treeview(history_frame, 
                                        columns=("x0", "x1", "x2", "x_aitken", "mejora"),
                                        show='headings', height=6)
        
        self.history_tree.heading("x0", text="x₀")
        self.history_tree.heading("x1", text="x₁") 
        self.history_tree.heading("x2", text="x₂")
        self.history_tree.heading("x_aitken", text="x̂_Aitken")
        self.history_tree.heading("mejora", text="Mejora vs x₂")
        
        for col in self.history_tree["columns"]:
            self.history_tree.column(col, width=120, anchor="center")
        
        self.history_tree.pack(fill='both', expand=True)
        
        # Gráfico (si matplotlib está disponible)
        if FigureCanvasTkAgg and plt and np:
            graph_frame = ttk.LabelFrame(main_frame, text="Visualización de Convergencia", padding=10)
            graph_frame.grid(row=6, column=0, columnspan=6, sticky='ew', pady=(0, 15))
            
            self.fig, self.ax = plt.subplots(figsize=(8, 4))
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
            self.canvas.get_tk_widget().pack()
        else:
            self.canvas = None
            self.ax = None

    def calculate_aitken(self):
        try:
            # Obtener valores
            x0 = float(self.x0_var.get())
            x1 = float(self.x1_var.get())
            x2 = float(self.x2_var.get())
            
            # Calcular Aitken
            numerator = (x1 - x0) ** 2
            denominator = x2 - 2 * x1 + x0
            
            # Verificar denominador
            if abs(denominator) < 1e-15:
                x_aitken = x2  # Usar x2 si denominador es muy pequeño
                warning_msg = " (Denominador ≈ 0, usando x₂)"
            else:
                x_aitken = x0 - numerator / denominator
                warning_msg = ""
            
            # Calcular errores y mejoras
            error_x2 = abs(x2 - x1)
            error_aitken = abs(x_aitken - x0) if abs(denominator) >= 1e-15 else float('inf')
            
            # Mejora relativa
            if error_x2 != 0:
                mejora_percent = ((error_x2 - error_aitken) / error_x2) * 100
            else:
                mejora_percent = 0
            
            # Mostrar resultado principal
            self.result_var.set(f"x̂_Aitken = {x_aitken:.10f}{warning_msg}")
            
            # Mostrar detalles del cálculo
            details = f"""DETALLES DEL CÁLCULO:
════════════════════════════════════════════════════════════════

Valores de entrada:
  x₀ = {x0:.10f}
  x₁ = {x1:.10f} 
  x₂ = {x2:.10f}

Cálculo paso a paso:
  Numerador   = (x₁ - x₀)² = ({x1:.6f} - {x0:.6f})² = {numerator:.10f}
  Denominador = x₂ - 2x₁ + x₀ = {x2:.6f} - 2({x1:.6f}) + {x0:.6f} = {denominator:.10f}
  
  x̂_Aitken = x₀ - (numerador/denominador)
  x̂_Aitken = {x0:.6f} - ({numerator:.6f}/{denominator:.6f})
  x̂_Aitken = {x0:.6f} - {numerator/denominator if abs(denominator) >= 1e-15 else 0:.6f}
  x̂_Aitken = {x_aitken:.10f}

Análisis de convergencia:
  Error punto fijo normal: |x₂ - x₁| = {error_x2:.6f}
  Error Aitken estimado:   |x̂ - x₀|  = {error_aitken:.6f}
  Mejora relativa: {mejora_percent:.2f}%
  
{'  ⚠️  Denominador muy pequeño - convergencia lenta' if abs(denominator) < 1e-10 else '  ✓  Aceleración exitosa'}
"""
            
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, details)
            
            # Guardar cálculo actual para posible adición al historial
            self.current_calculation = {
                'x0': x0, 'x1': x1, 'x2': x2, 
                'x_aitken': x_aitken, 'mejora': mejora_percent
            }
            
        except ValueError as e:
            messagebox.showerror("Error", f"Valores inválidos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {e}")

    def add_to_history(self):
        if hasattr(self, 'current_calculation'):
            calc = self.current_calculation
            self.calculation_history.append(calc)
            
            # Agregar a la tabla
            self.history_tree.insert('', 'end', values=(
                f"{calc['x0']:.6f}",
                f"{calc['x1']:.6f}", 
                f"{calc['x2']:.6f}",
                f"{calc['x_aitken']:.6f}",
                f"{calc['mejora']:.2f}%"
            ))
            
            # Actualizar gráfico si disponible
            self.update_graph()
            
            messagebox.showinfo("Éxito", "Cálculo agregado al historial")
        else:
            messagebox.showwarning("Aviso", "Primero realiza un cálculo")

    def update_graph(self):
        if not (self.canvas and self.ax and self.calculation_history):
            return
            
        # Preparar datos para graficar
        iterations = list(range(len(self.calculation_history)))
        x_values = [calc['x_aitken'] for calc in self.calculation_history]
        
        # Limpiar y crear nuevo gráfico
        self.ax.clear()
        self.ax.plot(iterations, x_values, 'ro-', label='Valores Aitken', markersize=8)
        self.ax.set_xlabel('Iteración')
        self.ax.set_ylabel('Valor x̂_Aitken')
        self.ax.set_title('Convergencia con Aceleración de Aitken')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
        # Si hay suficientes puntos, mostrar línea de convergencia
        if len(x_values) > 1:
            self.ax.axhline(y=x_values[-1], color='green', linestyle='--', alpha=0.7, 
                           label=f'Último valor: {x_values[-1]:.6f}')
            self.ax.legend()
        
        self.canvas.draw()

    def clear_all(self):
        # Limpiar entradas
        self.x0_var.set("1.0")
        self.x1_var.set("0.367879") 
        self.x2_var.set("0.692201")
        
        # Limpiar resultado
        self.result_var.set("x̂_Aitken = (presiona 'Calcular Aitken')")
        self.details_text.delete(1.0, tk.END)
        
        # Limpiar historial
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        self.calculation_history.clear()
        
        # Limpiar gráfico
        if self.ax and self.canvas:
            self.ax.clear()
            self.canvas.draw()

    def show_examples(self):
        examples_window = tk.Toplevel(self.master)
        examples_window.title("Ejemplos de Ejercicios")
        examples_window.geometry("600x500")
        
        examples_frame = ttk.Frame(examples_window, padding=15)
        examples_frame.pack(fill='both', expand=True)
        
        ttk.Label(examples_frame, text="EJEMPLOS DE LOS EJERCICIOS", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 15))
        
        examples_text = tk.Text(examples_frame, height=25, width=70, font=('Courier', 10))
        examples_text.pack(fill='both', expand=True)
        
        examples_content = """EJERCICIO 2: g(x) = cos(x), x₀ = 0.5
  x₀ = 0.5
  x₁ = cos(0.5) = 0.877583
  x₂ = cos(0.877583) = 0.639012
  ➤ Pega estos valores y calcula

EJERCICIO 4: g(x) = e^(-x), x₀ = 1
  x₀ = 1.0
  x₁ = e^(-1) = 0.367879
  x₂ = e^(-0.367879) = 0.692201
  ➤ Ya están cargados por defecto

EJERCICIO 5: g(x) = √(3x-2), x₀ = 2
  x₀ = 2.0
  x₁ = √(3×2-2) = √4 = 2.0
  x₂ = √(3×2-2) = 2.0
  ➤ Punto fijo inmediato

EJERCICIO 7: g(x) = 1-x³, x₀ = 0.5
  x₀ = 0.5
  x₁ = 1-(0.5)³ = 1-0.125 = 0.875
  x₂ = 1-(0.875)³ = 1-0.669873 = 0.330127
  ➤ Oscila, Aitken ayuda mucho

EJERCICIO 10: g(x) = x², x₀ = 0.4
  x₀ = 0.4
  x₁ = (0.4)² = 0.16
  x₂ = (0.16)² = 0.0256
  ➤ Converge a 0 rápidamente

CÓMO USAR:
1. Copia los valores x₀, x₁, x₂ de cualquier ejercicio
2. Pégalos en los campos correspondientes  
3. Presiona 'Calcular Aitken'
4. Agrega al historial para comparar ejercicios
"""
        
        examples_text.insert(tk.END, examples_content)
        examples_text.config(state='disabled')  # Solo lectura

def main():
    root = tk.Tk()
    
    # Configurar estilo
    style = ttk.Style()
    style.theme_use('clam')
    
    app = AitkenCalculatorGUI(root)
    
    # Hacer la ventana redimensionable
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()
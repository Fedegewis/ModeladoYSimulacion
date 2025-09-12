import tkinter as tk
from tkinter import ttk, messagebox
import math
from scipy.stats import norm
import numpy as np

class ZCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Z(α/2) - Intervalos de Confianza")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.confidence_var = tk.StringVar(value="95")
        self.alpha_var = tk.StringVar()
        self.alpha_half_var = tk.StringVar()
        self.percentile_var = tk.StringVar()
        self.z_var = tk.StringVar()
        
        self.setup_ui()
        self.calculate()  # Cálculo inicial
    
    def setup_ui(self):
        # Título
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=10)
        
        tk.Label(title_frame, text="Calculadora Z(α/2)", 
                font=("Arial", 18, "bold"), bg='#f0f0f0', fg='#2c3e50').pack()
        tk.Label(title_frame, text="Intervalos de Confianza", 
                font=("Arial", 12), bg='#f0f0f0', fg='#7f8c8d').pack()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='white', relief='raised', bd=2)
        main_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Entrada del nivel de confianza
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Nivel de Confianza (%):", 
                font=("Arial", 12, "bold"), bg='white').grid(row=0, column=0, sticky='e', padx=10)
        
        confidence_entry = tk.Entry(input_frame, textvariable=self.confidence_var, 
                                   font=("Arial", 12), width=10, justify='center')
        confidence_entry.grid(row=0, column=1, padx=10)
        confidence_entry.bind('<KeyRelease>', self.on_confidence_change)
        
        # Botones para valores comunes
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        tk.Label(buttons_frame, text="Valores Comunes:", 
                font=("Arial", 11, "bold"), bg='white').pack()
        
        button_frame = tk.Frame(buttons_frame, bg='white')
        button_frame.pack(pady=5)
        
        common_values = [90, 95, 99]
        for value in common_values:
            btn = tk.Button(button_frame, text=f"{value}%", 
                          command=lambda v=value: self.set_confidence(v),
                          bg='#3498db', fg='white', font=("Arial", 10, "bold"),
                          width=8, height=1)
            btn.pack(side='left', padx=5)
        
        # Resultados
        results_frame = tk.LabelFrame(main_frame, text="Resultados", 
                                    font=("Arial", 12, "bold"), bg='white', fg='#2c3e50')
        results_frame.pack(pady=20, padx=20, fill='x')
        
        # Grid de resultados
        results_grid = tk.Frame(results_frame, bg='white')
        results_grid.pack(pady=10, padx=10, fill='x')
        
        # Labels y valores
        labels = ["α (alfa):", "α/2:", "Percentil necesario:", "Z(α/2):"]
        variables = [self.alpha_var, self.alpha_half_var, self.percentile_var, self.z_var]
        colors = ['#34495e', '#34495e', '#34495e', '#e74c3c']
        fonts = [("Arial", 11), ("Arial", 11), ("Arial", 11), ("Arial", 14, "bold")]
        
        for i, (label, var, color, font) in enumerate(zip(labels, variables, colors, fonts)):
            tk.Label(results_grid, text=label, font=("Arial", 11, "bold"), 
                    bg='white', anchor='w').grid(row=i, column=0, sticky='w', pady=5)
            tk.Label(results_grid, textvariable=var, font=font, 
                    bg='white', fg=color, anchor='e').grid(row=i, column=1, sticky='e', pady=5, padx=20)
        
        # Configurar columnas
        results_grid.columnconfigure(0, weight=1)
        results_grid.columnconfigure(1, weight=1)
        
        # Frame de fórmulas
        formula_frame = tk.LabelFrame(main_frame, text="Fórmulas", 
                                    font=("Arial", 11, "bold"), bg='white', fg='#2c3e50')
        formula_frame.pack(pady=10, padx=20, fill='x')
        
        formulas = [
            "1. α = 1 - (Nivel de Confianza / 100)",
            "2. α/2 = α ÷ 2", 
            "3. Percentil = (1 - α/2) × 100",
            "4. Z(α/2) = Percentil inverso de la distribución normal"
        ]
        
        for formula in formulas:
            tk.Label(formula_frame, text=formula, font=("Arial", 9), 
                    bg='white', anchor='w').pack(anchor='w', padx=10, pady=2)
        
        # Tabla de valores comunes
        table_frame = tk.LabelFrame(main_frame, text="Valores de Referencia", 
                                  font=("Arial", 11, "bold"), bg='white', fg='#2c3e50')
        table_frame.pack(pady=10, padx=20, fill='x')
        
        # Headers
        headers = ["IC (%)", "α", "α/2", "Percentil", "Z(α/2)"]
        for j, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Arial", 9, "bold"), 
                    bg='#ecf0f1', relief='ridge', bd=1, width=12).grid(row=0, column=j, sticky='ew')
        
        # Datos
        data = [
            ["90%", "0.10", "0.05", "95%", "1.645"],
            ["95%", "0.05", "0.025", "97.5%", "1.960"],
            ["99%", "0.01", "0.005", "99.5%", "2.576"]
        ]
        
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                bg_color = '#f8f9fa' if i % 2 == 0 else 'white'
                tk.Label(table_frame, text=value, font=("Arial", 9), 
                        bg=bg_color, relief='ridge', bd=1, width=12).grid(row=i+1, column=j, sticky='ew')
        
        # Configurar columnas de la tabla
        for j in range(len(headers)):
            table_frame.columnconfigure(j, weight=1)
    
    def set_confidence(self, value):
        self.confidence_var.set(str(value))
        self.calculate()
    
    def on_confidence_change(self, event=None):
        self.calculate()
    
    def calculate(self):
        try:
            confidence = float(self.confidence_var.get())
            
            if confidence <= 0 or confidence >= 100:
                raise ValueError("El nivel de confianza debe estar entre 0 y 100")
            
            # Cálculos
            alpha = 1 - (confidence / 100)
            alpha_half = alpha / 2
            percentile = (1 - alpha_half) * 100
            z_value = norm.ppf(1 - alpha_half)  # Percentil inverso
            
            # Actualizar variables
            self.alpha_var.set(f"{alpha:.4f}")
            self.alpha_half_var.set(f"{alpha_half:.4f}")
            self.percentile_var.set(f"{percentile:.2f}%")
            self.z_var.set(f"{z_value:.4f}")
            
        except ValueError as e:
            # En caso de error, limpiar resultados
            self.alpha_var.set("Error")
            self.alpha_half_var.set("Error")
            self.percentile_var.set("Error")
            self.z_var.set("Error")

def main():
    root = tk.Tk()
    app = ZCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
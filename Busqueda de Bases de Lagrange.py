import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp

class LagrangeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Bases de Lagrange")
        self.root.geometry("1200x800")
        
        # Variables - Sin puntos por defecto
        self.points = []  
        self.selected_basis = 0
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Mostrar mensaje inicial
        self.show_initial_message()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo (controles)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Frame derecho (gráfica)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # === CONTROLES ===
        # Título
        title_label = ttk.Label(left_frame, text="Calculadora de Bases\nde Lagrange", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Sección de puntos
        points_frame = ttk.LabelFrame(left_frame, text="Puntos de Interpolación", 
                                     padding=10)
        points_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Lista de puntos
        self.points_listbox = tk.Listbox(points_frame, height=6)
        self.points_listbox.pack(fill=tk.X, pady=(0, 10))
        
        # Agregar punto
        add_frame = ttk.Frame(points_frame)
        add_frame.pack(fill=tk.X)
        
        ttk.Label(add_frame, text="x:").pack(side=tk.LEFT)
        self.x_entry = ttk.Entry(add_frame, width=8)
        self.x_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(add_frame, text="y:").pack(side=tk.LEFT)
        self.y_entry = ttk.Entry(add_frame, width=8)
        self.y_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(add_frame, text="Agregar", command=self.add_point).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_frame, text="Eliminar", command=self.remove_point).pack(side=tk.LEFT)
        
        # Instrucciones iniciales
        instructions_frame = ttk.Frame(points_frame)
        instructions_frame.pack(fill=tk.X, pady=(10, 0))
        
        instructions_label = ttk.Label(instructions_frame, 
                                     text="💡 Agrega al menos 2 puntos para comenzar", 
                                     font=("Arial", 9), foreground="blue")
        instructions_label.pack()
        
        # Selector de base
        basis_frame = ttk.LabelFrame(left_frame, text="Seleccionar Base", padding=10)
        basis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.basis_var = tk.IntVar(value=0)
        self.basis_buttons = []
        self.basis_buttons_frame = ttk.Frame(basis_frame)
        self.basis_buttons_frame.pack()
        
        # Fórmulas
        formulas_frame = ttk.LabelFrame(left_frame, text="Fórmulas", padding=10)
        formulas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Base específica
        ttk.Label(formulas_frame, text="Base seleccionada:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.basis_formula = scrolledtext.ScrolledText(formulas_frame, height=3, 
                                                      wrap=tk.WORD, font=("Courier", 9))
        self.basis_formula.pack(fill=tk.X, pady=(0, 10))
        
        # Polinomio completo
        ttk.Label(formulas_frame, text="Polinomio completo P(x):", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.poly_formula = scrolledtext.ScrolledText(formulas_frame, height=3, 
                                                     wrap=tk.WORD, font=("Courier", 9))
        self.poly_formula.pack(fill=tk.X, pady=(0, 10))
        
        # Verificación
        ttk.Label(formulas_frame, text="Verificación:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.verification_text = scrolledtext.ScrolledText(formulas_frame, height=4, 
                                                          wrap=tk.WORD, font=("Courier", 9))
        self.verification_text.pack(fill=tk.X)
        
        # === GRÁFICA ===
        # Configurar matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Botón de actualizar gráfica
        update_btn = ttk.Button(right_frame, text="Actualizar Gráfica", 
                               command=self.update_graph)
        update_btn.pack(pady=5)
    
    def show_initial_message(self):
        """Mostrar mensaje inicial cuando no hay puntos"""
        self.basis_formula.delete(1.0, tk.END)
        self.basis_formula.insert(tk.END, "Agrega al menos 2 puntos para comenzar")
        
        self.poly_formula.delete(1.0, tk.END)
        self.poly_formula.insert(tk.END, "El polinomio aparecerá aquí")
        
        self.verification_text.delete(1.0, tk.END)
        self.verification_text.insert(tk.END, "La verificación aparecerá aquí")
        
        # Limpiar gráfica
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'Agrega puntos para ver la gráfica', 
                    transform=self.ax.transAxes, ha='center', va='center',
                    fontsize=14, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        self.ax.set_title("Bases de Lagrange")
        self.canvas.draw()
        
    def calculate_lagrange_basis(self, points, i):
        """Calcula la base Li(x) de Lagrange"""
        n = len(points)
        x = sp.Symbol('x')
        
        numerator_terms = []
        denominator_value = 1
        
        for j in range(n):
            if i != j:
                numerator_terms.append(f"(x - {points[j][0]})")
                denominator_value *= (points[i][0] - points[j][0])
        
        numerator_str = "".join(numerator_terms)
        
        # Crear expresión simbólica
        numerator_expr = 1
        for j in range(n):
            if i != j:
                numerator_expr *= (x - points[j][0])
        
        basis_expr = numerator_expr / denominator_value
        
        # Para mostrar con factor fuera, expandir solo el numerador
        numerator_expanded = sp.expand(numerator_expr)
        if denominator_value == 1:
            basis_factored = str(numerator_expanded)
        elif denominator_value == -1:
            basis_factored = f"-({numerator_expanded})"
        else:
            basis_factored = f"({1/denominator_value})*({numerator_expanded})"
        
        return {
            'expression': f"L{i}(x) = {numerator_str} / {denominator_value}",
            'simplified': basis_factored,
            'symbolic': basis_expr
        }
    
    def evaluate_lagrange_basis(self, points, i, x_val):
        """Evalúa Li(x) en un punto específico"""
        result = 1
        n = len(points)
        
        for j in range(n):
            if i != j:
                result *= (x_val - points[j][0]) / (points[i][0] - points[j][0])
        
        return result
    
    def calculate_full_polynomial(self, points):
        """Calcula el polinomio interpolante completo"""
        x = sp.Symbol('x')
        polynomial = 0
        
        for i in range(len(points)):
            basis = self.calculate_lagrange_basis(points, i)
            polynomial += points[i][1] * basis['symbolic']
        
        polynomial_simplified = sp.expand(polynomial)
        return f"P(x) = {polynomial_simplified}"
    
    def add_point(self):
        """Agregar un nuevo punto"""
        try:
            x_val = float(self.x_entry.get())
            y_val = float(self.y_entry.get())
            
            # Verificar que no exista ya un punto con la misma x
            if any(point[0] == x_val for point in self.points):
                messagebox.showerror("Error", "Ya existe un punto con esa coordenada x")
                return
            
            self.points.append((x_val, y_val))
            self.points.sort(key=lambda p: p[0])  # Ordenar por x
            
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
            
            self.update_display()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos")
    
    def remove_point(self):
        """Eliminar el punto seleccionado"""
        selection = self.points_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un punto para eliminar")
            return
        
        if len(self.points) <= 1:
            messagebox.showwarning("Advertencia", "Necesitas al menos 2 puntos para eliminar")
            return
        
        index = selection[0]
        del self.points[index]
        
        # Ajustar la base seleccionada si es necesario
        if self.selected_basis >= len(self.points):
            self.selected_basis = len(self.points) - 1
            self.basis_var.set(self.selected_basis)
        
        self.update_display()
    
    def on_basis_change(self):
        """Callback cuando cambia la base seleccionada"""
        self.selected_basis = self.basis_var.get()
        self.update_display()
    
    def update_display(self):
        """Actualizar toda la interfaz"""
        if len(self.points) < 2:
            # Si hay menos de 2 puntos, mostrar mensaje
            self.show_initial_message()
            
            # Limpiar lista de puntos pero mostrar los que hay
            self.points_listbox.delete(0, tk.END)
            for i, (x, y) in enumerate(self.points):
                self.points_listbox.insert(tk.END, f"P{i}: ({x}, {y})")
            
            # Limpiar botones de bases
            for btn in self.basis_buttons:
                btn.destroy()
            self.basis_buttons = []
            
            return
        
        # Actualizar lista de puntos
        self.points_listbox.delete(0, tk.END)
        for i, (x, y) in enumerate(self.points):
            self.points_listbox.insert(tk.END, f"P{i}: ({x}, {y})")
        
        # Actualizar botones de bases
        for btn in self.basis_buttons:
            btn.destroy()
        
        self.basis_buttons = []
        for i in range(len(self.points)):
            btn = ttk.Radiobutton(self.basis_buttons_frame, text=f"L{i}(x)", 
                                 variable=self.basis_var, value=i,
                                 command=self.on_basis_change)
            btn.pack(side=tk.LEFT, padx=2)
            self.basis_buttons.append(btn)
        
        # Asegurar que la base seleccionada sea válida
        if self.selected_basis >= len(self.points):
            self.selected_basis = 0
            self.basis_var.set(0)
        
        # Actualizar fórmulas
        self.update_formulas()
        
        # Actualizar gráfica
        self.update_graph()
    
    def update_formulas(self):
        """Actualizar las fórmulas mostradas"""
        if len(self.points) < 2:
            return
        
        # Base específica
        basis_info = self.calculate_lagrange_basis(self.points, self.selected_basis)
        self.basis_formula.delete(1.0, tk.END)
        self.basis_formula.insert(tk.END, f"{basis_info['expression']}\n\n")
        self.basis_formula.insert(tk.END, f"Factorizado: L{self.selected_basis}(x) = {basis_info['simplified']}\n\n")
        self.basis_formula.insert(tk.END, f"Punto asociado: {self.points[self.selected_basis]}")
        
        # Polinomio completo
        full_poly = self.calculate_full_polynomial(self.points)
        self.poly_formula.delete(1.0, tk.END)
        self.poly_formula.insert(tk.END, full_poly)
        
        # Verificación
        self.verification_text.delete(1.0, tk.END)
        self.verification_text.insert(tk.END, f"Verificación para L{self.selected_basis}(x):\n\n")
        
        for j, (x_val, y_val) in enumerate(self.points):
            basis_value = self.evaluate_lagrange_basis(self.points, self.selected_basis, x_val)
            expected = 1 if j == self.selected_basis else 0
            check = "✓" if abs(basis_value - expected) < 1e-10 else "✗"
            
            self.verification_text.insert(tk.END, 
                f"L{self.selected_basis}({x_val}) = {basis_value:.6f} {check}\n")
    
    def update_graph(self):
        """Actualizar la gráfica"""
        if len(self.points) < 2:
            return
        
        self.ax.clear()
        
        # Generar datos para la gráfica
        x_vals = [p[0] for p in self.points]
        x_min, x_max = min(x_vals) - 1, max(x_vals) + 1
        x_plot = np.linspace(x_min, x_max, 1000)
        
        # Evaluar la base seleccionada
        y_plot = [self.evaluate_lagrange_basis(self.points, self.selected_basis, x) 
                  for x in x_plot]
        
        # Graficar la base
        self.ax.plot(x_plot, y_plot, 'b-', linewidth=2, 
                    label=f'L{self.selected_basis}(x)')
        
        # Marcar los puntos de interpolación
        for i, (x_val, y_val) in enumerate(self.points):
            basis_val = self.evaluate_lagrange_basis(self.points, self.selected_basis, x_val)
            
            if i == self.selected_basis:
                # Punto donde la base vale 1 (rojo)
                self.ax.plot(x_val, basis_val, 'ro', markersize=10, 
                           label=f'L{self.selected_basis}({x_val}) = 1')
            else:
                # Puntos donde la base vale 0 (verde)
                self.ax.plot(x_val, basis_val, 'go', markersize=8)
        
        # Línea en y=0 y y=1 para referencia
        self.ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        self.ax.axhline(y=1, color='r', linestyle='--', alpha=0.3)
        
        # Configurar la gráfica
        self.ax.set_xlabel('x')
        self.ax.set_ylabel(f'L{self.selected_basis}(x)')
        self.ax.set_title(f'Base de Lagrange L{self.selected_basis}(x)')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
        # Ajustar límites
        if y_plot:  # Verificar que hay datos
            y_min, y_max = min(y_plot), max(y_plot)
            y_range = y_max - y_min
            if y_range > 0:
                self.ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
        
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = LagrangeCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
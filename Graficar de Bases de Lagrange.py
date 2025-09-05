# -*- coding: utf-8 -*-
"""
Simulador: Reconstrucción de función desde datos discretos
- Interpolación de Lagrange (1D): construcción simbólica con SymPy, evaluación y gráfico
- Errores: locales (punto a punto) y global (máximo en malla fina)
- Opción de función verdadera f(x) para comparar (eval segura)
- Derivación numérica (1D): adelante/atrás/centrada con paso h (desde datos o desde f si está)
- Gradiente (2D) opcional: pegar matriz de temperaturas/valores y calcular fx, fy, |∇f| con quiver

Requisitos: numpy, sympy, matplotlib

Ejecutar: python simulador_lagrange.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import numpy as np
import sympy as sp
from typing import List, Tuple, Optional

# Matplotlib en Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ========================= Utilidades seguras ========================= #

ALLOWED_NAMES = {
    # builtins seguros
    'abs': abs, 'min': min, 'max': max, 'pow': pow, 'round': round,
    # math
    'pi': math.pi, 'e': math.e, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan, 'atan2': math.atan2,
    'sinh': math.sin, 'cosh': math.cosh, 'tanh': math.tanh,
    'exp': math.exp, 'log': math.log, 'log10': math.log10, 'sqrt': math.sqrt,
}


def safe_eval(expr: str, xval: float) -> float:
    """Evalúa f(x) de forma acotada: expr puede usar funciones en ALLOWED_NAMES y variable x."""
    if expr.strip() == "":
        raise ValueError("No hay expresión de función.")
    scope = dict(ALLOWED_NAMES)
    scope['x'] = xval
    return float(eval(expr, {"__builtins__": {}}, scope))


# ========================= Interpolación Lagrange ========================= #

def lagrange_symbolic(xs: List[float], ys: List[float]) -> sp.Expr:
    x = sp.Symbol('x', real=True)
    n = len(xs)
    poly = 0
    for i in range(n):
        xi, yi = xs[i], ys[i]
        Li = 1
        for j in range(n):
            if j == i:
                continue
            Li *= (x - xs[j]) / (xi - xs[j])
        poly += yi * Li
    return sp.simplify(sp.expand(poly))


def interp_eval(xs: List[float], ys: List[float], xq: np.ndarray) -> np.ndarray:
    """Evalúa el polinomio de Lagrange en un vector xq (versión numérica estable con barycentric)."""
    # Pesos baricéntricos
    xs_arr = np.array(xs, dtype=float)
    ys_arr = np.array(ys, dtype=float)
    n = len(xs_arr)
    w = np.ones(n)
    for j in range(n):
        for k in range(n):
            if k != j:
                w[j] /= (xs_arr[j] - xs_arr[k])
    # Evaluación baricéntrica
    xq = np.array(xq, dtype=float)
    p = np.zeros_like(xq)
    for idx, xv in enumerate(xq):
        # Si coincide con un nodo
        diff = xv - xs_arr
        if np.any(np.isclose(diff, 0.0)):
            j = int(np.where(np.isclose(diff, 0.0))[0][0])
            p[idx] = ys_arr[j]
        else:
            num = np.sum(w * ys_arr / diff)
            den = np.sum(w / diff)
            p[idx] = num / den
    return p


# ========================= GUI ========================= #

class LagrangeApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        master.title("Simulador – Lagrange, Errores y Derivación (1D) + Gradiente (2D)")
        self._build_ui()
        self.last_grid = None

    # ---------- UI ---------- #
    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        self.tab1 = ttk.Frame(nb)
        self.tab2 = ttk.Frame(nb)
        self.tab3 = ttk.Frame(nb)
        nb.add(self.tab1, text="Interpolación 1D")
        nb.add(self.tab2, text="Derivación 1D")
        nb.add(self.tab3, text="Gradiente 2D")

        self._build_tab1()
        self._build_tab2()
        self._build_tab3()

    # ---------- TAB 1: Interpolación ---------- #
    def _build_tab1(self):
        left = ttk.Frame(self.tab1)
        left.pack(side="left", fill="y", padx=6, pady=6)
        right = ttk.Frame(self.tab1)
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        # Tabla de puntos
        lbl = ttk.Label(left, text="Puntos (x, y)")
        lbl.pack(anchor="w")
        self.tree = ttk.Treeview(left, columns=("x", "y"), show="headings", height=8)
        self.tree.heading("x", text="x")
        self.tree.heading("y", text="f(x)")
        self.tree.column("x", width=80)
        self.tree.column("y", width=90)
        self.tree.pack()

        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=4)
        self.x_entry = ttk.Entry(btns, width=10)
        self.y_entry = ttk.Entry(btns, width=10)
        self.x_entry.insert(0, "0")
        self.y_entry.insert(0, "0")
        ttk.Label(btns, text="x:").grid(row=0, column=0)
        self.x_entry.grid(row=0, column=1)
        ttk.Label(btns, text="y:").grid(row=0, column=2)
        self.y_entry.grid(row=0, column=3)
        ttk.Button(btns, text="Agregar", command=self.add_point).grid(row=0, column=4, padx=4)
        ttk.Button(btns, text="Quitar sel.", command=self.remove_selected).grid(row=0, column=5)
        ttk.Button(btns, text="Limpiar", command=self.clear_points).grid(row=0, column=6, padx=4)

        # Función verdadera y derivada para error teórico
        ttk.Label(left, text="f(x) opcional (para errores):").pack(anchor="w", pady=(8, 0))
        self.fx_entry = ttk.Entry(left, width=28)
        self.fx_entry.insert(0, "")
        self.fx_entry.pack(anchor="w")
        ex = ttk.Label(left, text="Ej: sin(x) + 0.2*x**2")
        ex.pack(anchor="w")
        
        ttk.Label(left, text="f^(n+1)(x) para error teórico:").pack(anchor="w", pady=(8, 0))
        self.fx_der_entry = ttk.Entry(left, width=28)
        self.fx_der_entry.insert(0, "")
        self.fx_der_entry.pack(anchor="w")

        # Rango y malla
        rng = ttk.Frame(left)
        rng.pack(anchor="w", pady=6)
        ttk.Label(rng, text="x_min").grid(row=0, column=0)
        ttk.Label(rng, text="x_max").grid(row=0, column=2)
        ttk.Label(rng, text="#malla").grid(row=0, column=4)
        self.xmin_e = ttk.Entry(rng, width=8)
        self.xmax_e = ttk.Entry(rng, width=8)
        self.npts_e = ttk.Entry(rng, width=6)
        self.xmin_e.insert(0, "0")
        self.xmax_e.insert(0, "10")
        self.npts_e.insert(0, "400")
        self.xmin_e.grid(row=0, column=1)
        self.xmax_e.grid(row=0, column=3)
        self.npts_e.grid(row=0, column=5)


        # Acciones
        ttk.Button(left, text="Construir Lagrange y Graficar", command=self.build_and_plot).pack(fill="x", pady=6)
        ttk.Button(left, text="Ver Tabla de Malla", command=self.show_mesh_table).pack(fill="x", pady=2)
        ttk.Button(left, text="Exportar CSV (malla)", command=self.export_csv).pack(fill="x")

        # Resultado simbólico + errores
        self.poly_text = tk.Text(left, height=6, width=40)
        self.poly_text.pack(pady=6)
        self.err_label = ttk.Label(left, text="Errores:")
        self.err_label.pack(anchor="w")

        # Figura
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True, ls=':')
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- TAB 2: Derivación ---------- #
    def _build_tab2(self):
        frm = ttk.Frame(self.tab2)
        frm.pack(fill="both", expand=True, padx=6, pady=6)

        row = 0
        ttk.Label(frm, text="x0").grid(row=row, column=0)
        self.dx_x0 = ttk.Entry(frm, width=10)
        self.dx_x0.insert(0, "1.0")
        self.dx_x0.grid(row=row, column=1)
        ttk.Label(frm, text="h").grid(row=row, column=2)
        self.dx_h = ttk.Entry(frm, width=10)
        self.dx_h.insert(0, "0.1")
        self.dx_h.grid(row=row, column=3)
        ttk.Label(frm, text="Método").grid(row=row, column=4)
        self.dx_method = ttk.Combobox(frm, values=["adelante", "atras", "centrada"], width=10, state="readonly")
        self.dx_method.current(2)
        self.dx_method.grid(row=row, column=5)

        row += 1
        ttk.Label(frm, text="f(x) (si hay):").grid(row=row, column=0, sticky="w", pady=(8, 0))
        self.dx_fx = ttk.Entry(frm, width=40)
        self.dx_fx.insert(0, "")
        self.dx_fx.grid(row=row, column=1, columnspan=5, sticky="we", pady=(8, 0))

        row += 1
        ttk.Button(frm, text="Derivar numéricamente", command=self.compute_derivative).grid(row=row, column=0, columnspan=2, pady=8)
        self.dx_out = ttk.Label(frm, text="")
        self.dx_out.grid(row=row, column=2, columnspan=4, sticky="w")

        # Nota sobre uso de datos si no hay f(x)
        note = ("Si no especificás f(x), el simulador intentará usar los puntos de la pestaña Interpolación\n"
                  "construyendo el polinomio de Lagrange para evaluar f(x±h).")
        ttk.Label(frm, text=note).grid(row=row+1, column=0, columnspan=6, sticky="w", pady=8)

    # ---------- TAB 3: Gradiente 2D ---------- #
    def _build_tab3(self):
        left = ttk.Frame(self.tab3)
        left.pack(side="left", fill="y", padx=6, pady=6)
        right = ttk.Frame(self.tab3)
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        ttk.Label(left, text="Pegá matriz de valores (filas separadas por\nlinea, columnas por coma):").pack(anchor="w")
        self.txt_mat = tk.Text(left, width=30, height=12)
        self.txt_mat.insert('1.0', "20,21.5,23\n19.5,22,24.5\n18,20,22.5")
        self.txt_mat.pack()

        frm = ttk.Frame(left)
        frm.pack(anchor="w", pady=6)
        ttk.Label(frm, text="h_x").grid(row=0, column=0)
        ttk.Label(frm, text="h_y").grid(row=0, column=2)
        self.hx_e = ttk.Entry(frm, width=8)
        self.hy_e = ttk.Entry(frm, width=8)
        self.hx_e.insert(0, "1.0")
        self.hy_e.insert(0, "1.0")
        self.hx_e.grid(row=0, column=1)
        self.hy_e.grid(row=0, column=3)

        ttk.Button(left, text="Calcular gradiente y graficar", command=self.compute_gradient).pack(fill="x", pady=6)
        self.grad_info = ttk.Label(left, text="")
        self.grad_info.pack(anchor="w")

        self.fig2 = Figure(figsize=(5.2, 4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.grid(True, ls=':')
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=right)
        self.canvas2.get_tk_widget().pack(fill="both", expand=True)

    # ---------- Funciones de apoyo ---------- #
    def get_points(self) -> Tuple[List[float], List[float]]:
        xs, ys = [], []
        for item in self.tree.get_children():
            x = float(self.tree.item(item, 'values')[0])
            y = float(self.tree.item(item, 'values')[1])
            xs.append(x); ys.append(y)
        # ordenar por x
        if len(xs) != len(set(xs)):
            raise ValueError("Hay valores de x duplicados.")
        ord_idx = np.argsort(xs)
        xs = [xs[i] for i in ord_idx]
        ys = [ys[i] for i in ord_idx]
        return xs, ys

    def add_point(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
        except Exception:
            messagebox.showerror("Error", "x e y deben ser numéricos.")
            return
        self.tree.insert('', 'end', values=(x, y))

    def remove_selected(self):
        for sel in self.tree.selection():
            self.tree.delete(sel)

    def clear_points(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.poly_text.delete('1.0', 'end')
        self.err_label.config(text="Errores:")
        self.ax.clear(); self.ax.grid(True, ls=':'); self.canvas.draw()
        self.last_grid = None
    
    def show_mesh_table(self):
        if self.last_grid is None:
            messagebox.showinfo("Info", "Primero generá la malla con 'Construir Lagrange y Graficar'.")
            return
        
        xq, yq, fx_vals = self.last_grid
        
        table_window = tk.Toplevel(self)
        table_window.title("Datos de la Malla")
        
        columns = ("x", "P(x)")
        if fx_vals is not None:
            columns = ("x", "P(x)", "f(x)", "Error")
            
        tree = ttk.Treeview(table_window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
            
        if fx_vals is not None:
            for xv, pv, fv in zip(xq, yq, fx_vals):
                error = abs(fv - pv)
                tree.insert("", "end", values=(f"{xv:.6g}", f"{pv:.6g}", f"{fv:.6g}", f"{error:.6g}"))
        else:
            for xv, pv in zip(xq, yq):
                tree.insert("", "end", values=(f"{xv:.6g}", f"{pv:.6g}"))
                
        tree.pack(expand=True, fill="both")

    # ---------- Acciones principales ---------- #
    def build_and_plot(self):
        try:
            xs, ys = self.get_points()
            if len(xs) < 2:
                raise ValueError("Ingresá al menos dos puntos.")
            x_min = float(self.xmin_e.get()); x_max = float(self.xmax_e.get()); npts = int(self.npts_e.get())
            if x_max <= x_min:
                raise ValueError("x_max debe ser mayor que x_min.")
            xq = np.linspace(x_min, x_max, npts)

            # Polinomio simbólico
            poly = lagrange_symbolic(xs, ys)
            self.poly_text.delete('1.0', 'end')
            self.poly_text.insert('end', f"Polinomio de Lagrange (grado {len(xs)-1}):\nP(x) = {sp.simplify(poly)}\n")

            # Evaluación numérica estable
            yq = interp_eval(xs, ys, xq)

            # Posible función verdadera y derivada para errores
            fx_expr = self.fx_entry.get().strip()
            fx_vals = None
            err_global_malla = None
            err_global_teorico = None
            
            if fx_expr:
                try:
                    fx_vals = np.array([safe_eval(fx_expr, xv) for xv in xq])
                    err_malla = fx_vals - yq
                    err_global_malla = np.max(np.abs(err_malla))
                    
                    self.poly_text.insert('end', f"\nError Global (malla {npts}): {err_global_malla:.6g}\n")
                    
                    fx_der_expr = self.fx_der_entry.get().strip()
                    if fx_der_expr:
                        x = sp.Symbol('x', real=True)
                        f_der_sym = sp.sympify(fx_der_expr)
                        f_der_lamb = sp.lambdify(x, f_der_sym, 'numpy')

                        # Calcular el término del producto de las diferencias
                        prod_term = np.ones_like(xq)
                        for xi in xs:
                            prod_term *= (xq - xi)
                        
                        # Calcular la derivada en la malla
                        der_vals = f_der_lamb(xq)
                        max_der_abs = np.max(np.abs(der_vals))
                        
                        # Calcular el error teórico máximo
                        n = len(xs) - 1
                        theo_error = (max_der_abs / math.factorial(n + 1)) * np.abs(prod_term)
                        err_global_teorico = np.max(theo_error)
                        
                        self.poly_text.insert('end', f"Error Global Teórico (cota): {err_global_teorico:.6g}\n")
                        self.ax.plot(xq, theo_error, 'r--', label='Cota de Error Teórico')
                        
                except Exception as e:
                    messagebox.showwarning("Aviso", f"No se pudo evaluar f(x) o su derivada: {e}")

            # Graficar
            self.ax.clear(); self.ax.grid(True, ls=':')
            self.ax.plot(xq, yq, label='Interpolación P(x)')
            self.ax.plot(xs, ys, 'o', label='Datos (x_i, y_i)')
            if fx_vals is not None:
                self.ax.plot(xq, fx_vals, '--', label='f(x) verdadera')
            self.ax.set_xlabel('x'); self.ax.set_ylabel('y')
            self.ax.set_title('Reconstrucción por Lagrange')
            self.ax.legend(loc='best')
            self.canvas.draw()

            # Errores locales (en los nodos de malla xq si hay f)
            if fx_vals is not None:
                idx_mid = np.linspace(0, len(xq)-1, min(10, len(xq)), dtype=int)
                resumen = [f"x={xq[i]:.3g}, |err|={abs(fx_vals[i]-yq[i]):.3g}" for i in idx_mid]
                self.err_label.config(text="Errores (muestra):\n" + "\n".join(resumen))
            else:
                self.err_label.config(text="Errores: (ingresá f(x) para calcular)")

            self.last_grid = (xq, yq, fx_vals)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_csv(self):
        if not hasattr(self, 'last_grid'):
            messagebox.showinfo("Info", "Primero generá la malla con 'Construir y Graficar'.")
            return
        xq, yq, fx_vals = self.last_grid
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV', '*.csv')])
        if not path:
            return
        with open(path, 'w', encoding='utf-8') as f:
            if fx_vals is not None:
                f.write('x,P(x),f(x),error\n')
                for xv, pv, fv in zip(xq, yq, fx_vals):
                    f.write(f"{xv},{pv},{fv},{fv-pv}\n")
            else:
                f.write('x,P(x)\n')
                for xv, pv in zip(xq, yq):
                    f.write(f"{xv},{pv}\n")
        messagebox.showinfo("Listo", f"Archivo guardado en:\n{path}")

    # ---------- Derivación ---------- #
    def compute_derivative(self):
        try:
            x0 = float(self.dx_x0.get()); h = float(self.dx_h.get()); method = self.dx_method.get()
            if h <= 0: raise ValueError('h debe ser positivo')

            fx_expr = self.dx_fx.get().strip()
            # función para evaluar f
            def f_num(xv: float) -> float:
                if fx_expr:
                    return safe_eval(fx_expr, xv)
                # usar Lagrange de la pestaña 1
                xs, ys = self.get_points()
                if len(xs) < 2:
                    raise ValueError("Sin f(x) ni puntos suficientes para interpolar.")
                return float(interp_eval(xs, ys, np.array([xv]))[0])

            if method == 'adelante':
                der = (f_num(x0+h) - f_num(x0)) / h
                orden = 'O(h)'
            elif method == 'atras':
                der = (f_num(x0) - f_num(x0-h)) / h
                orden = 'O(h)'
            else:
                der = (f_num(x0+h) - f_num(x0-h)) / (2*h)
                orden = 'O(h^2)'

            self.dx_out.config(text=f"f'(x0) ≈ {der:.8g}   ({orden})")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Gradiente 2D ---------- #
    def compute_gradient(self):
        try:
            mat_str = self.txt_mat.get('1.0', 'end').strip()
            rows = [r for r in mat_str.splitlines() if r.strip()]
            M = [list(map(float, r.split(','))) for r in rows]
            T = np.array(M, dtype=float)
            ny, nx = T.shape
            hx = float(self.hx_e.get()); hy = float(self.hy_e.get())
            if hx <= 0 or hy <= 0: raise ValueError('h_x y h_y deben ser positivos')

            fx = np.zeros_like(T)
            fy = np.zeros_like(T)
            # d/dx
            for j in range(ny):
                for i in range(nx):
                    if 0 < i < nx-1:
                        fx[j, i] = (T[j, i+1] - T[j, i-1]) / (2*hx)
                    elif i == 0:
                        fx[j, i] = (T[j, i+1] - T[j, i]) / hx
                    else:
                        fx[j, i] = (T[j, i] - T[j, i-1]) / hx
            # d/dy (índice de fila aumenta hacia abajo)
            for j in range(ny):
                for i in range(nx):
                    if 0 < j < ny-1:
                        fy[j, i] = (T[j+1, i] - T[j-1, i]) / (2*hy)
                    elif j == 0:
                        fy[j, i] = (T[j+1, i] - T[j, i]) / hy
                    else:
                        fy[j, i] = (T[j, i] - T[j-1, i]) / hy

            mag = np.sqrt(fx**2 + fy**2)
            info = f"|∇f| min={mag.min():.4g}, max={mag.max():.4g}"
            self.grad_info.config(text=info)

            # plot
            self.ax2.clear(); self.ax2.grid(True, ls=':')
            X, Y = np.meshgrid(np.arange(nx), np.arange(ny))
            self.ax2.quiver(X, Y, fx, fy)
            self.ax2.set_title('Campo de gradiente (quiver)')
            self.ax2.set_xlabel('x index'); self.ax2.set_ylabel('y index')
            self.ax2.invert_yaxis()
            self.canvas2.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ========================= main ========================= #
if __name__ == '__main__':
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use('clam')
    except Exception:
        pass
    app = LagrangeApp(root)
    root.mainloop()
# -*- coding: utf-8 -*-
"""
Simulador Unificado: Raíces, Integración, Interpolación de Lagrange y Dif. Finitas
- Módulos: Raíces | Integración | Interpolación (Lagrange) | Dif. Finitas (1D/2D)
- Evaluación segura de expresiones (math.*) con soporte para arrays (np.vectorize)
- Tablas y resultados con 8 decimales, gráficas opcionales
Requisitos: tkinter, numpy, sympy, matplotlib
"""

import ast
import math
from typing import Callable, Optional, List
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


# ==== Helper: Teclado de Funciones genérico ====
class _FunctionKeypad:
    DEFAULT_BUTTONS = [
        ['sin(', 'cos(', 'tan(', 'exp(', 'log(', 'sqrt(', 'pi', 'E', '**', '(', ')'],
        ['x', 'y', 'z', '+', '-', '*', '/', 'abs(', 'asin(', 'acos(', 'atan('],
        ['sinh(', 'cosh(', 'tanh(', 'asinh(', 'acosh(', 'atanh(', 'floor(', 'ceiling(', 'sign(']
    ]

    def __init__(self, parent, target_entry, title="Teclado de Funciones", buttons=None, max_cols=8):
        self.win = tk.Toplevel(parent)
        self.win.title(title)
        self.target_entry = target_entry
        self.buttons = buttons if buttons else self.DEFAULT_BUTTONS
        self._build(max_cols=max_cols)

    def _insert(self, text):
        try:
            self.target_entry.insert(tk.END, text)
        except Exception:
            pass

    def _build(self, max_cols=8):
        r = 0
        for row in self.buttons:
            c = 0
            for bt in row:
                ttk.Button(self.win, text=bt, width=8, command=lambda t=bt: self._insert(t)).grid(row=r, column=c, padx=2, pady=2, sticky="w")
                c += 1
                if c >= max_cols:
                    r += 1
                    c = 0
            r += 1
        # acciones
        ttk.Button(self.win, text="Borrar", width=12, command=self._backspace).grid(row=r, column=0, columnspan=2, pady=6)
        ttk.Button(self.win, text="Limpiar", width=12, command=self._clear).grid(row=r, column=2, columnspan=2, pady=6)

    def _backspace(self):
        w = self.target_entry
        try:
            cur = w.index(tk.INSERT)
            if cur > 0:
                w.delete(cur-1, cur)
        except Exception:
            # fallback: borrar último
            try:
                txt = w.get()
                if txt:
                    w.delete(len(txt)-1, tk.END)
            except Exception:
                pass

    def _clear(self):
        try:
            self.target_entry.delete(0, tk.END)
        except Exception:
            pass


def open_function_keypad(parent, target_entry, title="Teclado de Funciones"):
    """
    Abre un teclado de funciones matemáticas para el Entry destino.
    Uso: open_function_keypad(self, self.entry_f) o similar.
    """
    _FunctionKeypad(parent, target_entry, title=title)



# === Monte Carlo integrado ===
class MonteCarloSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Monte Carlo + Teclado Avanzado")
        self.root.geometry("1100x760")

        # -------------------- Entradas --------------------
        frame_inputs = ttk.LabelFrame(root, text="Parámetros")
        frame_inputs.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame_inputs, text="f(x) =").grid(row=0, column=0)
        self.entry_func = ttk.Entry(frame_inputs, width=20)
        self.entry_func.insert(0, "sin(x)+1")
        self.entry_func.grid(row=0, column=1)

        ttk.Button(frame_inputs, text="Teclado Funciones", command=self.teclado_funciones_1d).grid(row=0, column=2, padx=5)

        ttk.Label(frame_inputs, text="a =").grid(row=0, column=3)
        self.entry_a = ttk.Entry(frame_inputs, width=7)
        self.entry_a.insert(0, "0")
        self.entry_a.grid(row=0, column=4)

        ttk.Label(frame_inputs, text="b =").grid(row=0, column=5)
        self.entry_b = ttk.Entry(frame_inputs, width=7)
        self.entry_b.insert(0, "3.1416")
        self.entry_b.grid(row=0, column=6)

        ttk.Label(frame_inputs, text="N =").grid(row=0, column=7)
        self.entry_N = ttk.Entry(frame_inputs, width=8)
        self.entry_N.insert(0, "1000")
        self.entry_N.grid(row=0, column=8)

        ttk.Label(frame_inputs, text="Gauss pts =").grid(row=0, column=9)
        self.entry_gauss = ttk.Entry(frame_inputs, width=5)
        self.entry_gauss.insert(0, "5")
        self.entry_gauss.grid(row=0, column=10)

        
# Botones principales (re-layout en múltiples filas)
        frame_actions = ttk.Frame(frame_inputs)
        frame_actions.grid(row=1, column=0, columnspan=12, sticky="w", pady=6)

        actions = [
            ("Simular (hit-or-miss)", self.simular),
            ("Método Promedio", self.ventana_metodo_promedio),
            ("Convergencia", self.ventana_convergencia),
            ("Análisis Estadístico", self.ventana_estadistica),
            ("Integrales Dobles", self.ventana_integrales_dobles),
            ("Integrales Triples", self.ventana_integrales_triples),
            ("Ayuda", self.mostrar_ayuda),
        ]
        max_cols = 3  # botones por fila
        r = c = 0
        for (txt, cmd) in actions:
            ttk.Button(frame_actions, text=txt, command=cmd).grid(row=r, column=c, padx=5, pady=4, sticky="w")
            c += 1
            if c >= max_cols:
                c = 0
                r += 1
# -------------------- Tabla --------------------
        frame_table = ttk.LabelFrame(root, text="Muestras Monte Carlo")
        frame_table.pack(side="left", fill="y", padx=5, pady=5)

        cols = ("x", "y", "f(x)", "Éxito")
        self.tree = ttk.Treeview(frame_table, columns=cols, show="headings", height=30)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80, anchor="center")
        self.tree.pack(side="left", fill="y")

        scroll = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        # -------------------- Gráfico --------------------
        frame_plot = ttk.LabelFrame(root, text="Gráfico")
        frame_plot.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # -------------------- Resultados --------------------
        self.label_result = ttk.Label(root, text="Resultados: ")
        self.label_result.pack(fill="x", padx=5, pady=5)

        # datos para ventanas dependientes
        self.fxs_samples = None
        self.volume = None
        self.convergencia_data = None

    # -------------------- Simulación MC hit-or-miss --------------------
    def simular(self):
        try:
            func_str = self.entry_func.get()
            a, b = float(self.entry_a.get()), float(self.entry_b.get())
            N = int(self.entry_N.get())
            n_gauss = int(self.entry_gauss.get())

            x = sp.Symbol('x')
            f_expr = sp.sympify(func_str)
            f = sp.lambdify(x, f_expr, "numpy")

            xs_dense = np.linspace(a, b, 1000)
            ys_dense = np.nan_to_num(f(xs_dense))
            y_min, y_max = min(0, np.min(ys_dense)), max(0, np.max(ys_dense))

            np.random.seed(0)
            xs = np.random.uniform(a, b, N)
            ys = np.random.uniform(y_min, y_max, N)
            fx_vals_samples = np.nan_to_num(f(xs))
            success_mask = ((ys >= 0) & (ys <= fx_vals_samples)) | ((ys <= 0) & (ys >= fx_vals_samples))
            count = np.sum(success_mask)

            rect_area = (b - a) * (y_max - y_min)
            mc_estimate = count / N * rect_area
            mc_prom = (b - a) * np.mean(fx_vals_samples)

            nodes, weights = leggauss(n_gauss)
            trans_nodes = 0.5*(nodes+1)*(b-a)+a
            gauss_val = 0.5*(b-a)*np.sum(weights * f(trans_nodes))

            self.fxs_samples = fx_vals_samples
            self.volume = b - a  # Guardar volumen para análisis estadístico
            self.convergencia_data = (xs, self.fxs_samples, b - a, gauss_val)

            # Tabla
            for i in self.tree.get_children():
                self.tree.delete(i)
            for i in range(min(N, 5000)):
                self.tree.insert("", "end",
                                 values=(f"{xs[i]:.6f}", f"{ys[i]:.6f}", f"{fx_vals_samples[i]:.6f}",
                                         "✔" if success_mask[i] else "✘"))

            # Gráfico
            self.ax.clear()
            self.ax.fill_between(xs_dense, 0, ys_dense, color='lightblue', alpha=0.3, label='Área bajo la curva')
            self.ax.plot(xs_dense, ys_dense, label=f"f(x)={func_str}", color="blue", linewidth=2)
            self.ax.scatter(xs[~success_mask], ys[~success_mask], s=20, alpha=0.6, color="red", label="Fallidos")
            self.ax.scatter(xs[success_mask], ys[success_mask], s=20, alpha=0.6, color="green", label="Éxitos")
            self.ax.axhline(0, color="black", linewidth=0.8)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y=f(x)")
            self.ax.set_title(f"MC: {mc_estimate:.6f} | MC promedio: {mc_prom:.6f} | Gauss: {gauss_val:.6f}")
            self.ax.legend()
            self.ax.grid(True)
            self.ax.set_xlim(a, b)
            self.ax.set_ylim(y_min - 0.1*abs(y_min), y_max + 0.1*abs(y_max))
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------- Limpiar --------------------
    def limpiar(self):
        self.ax.clear()
        self.canvas.draw()
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.label_result.config(text="Resultados: ")
        self.fxs_samples = None
        self.volume = None
        self.convergencia_data = None

    # -------------------- Ventana Convergencia --------------------
    def ventana_convergencia(self):
        if not hasattr(self, 'convergencia_data') or self.convergencia_data is None:
            messagebox.showwarning("Atención", "Primero ejecute una simulación.")
            return

        xs, fxs, L, gauss_val = self.convergencia_data
        cum_avg = np.cumsum(fxs)/np.arange(1, len(fxs)+1)
        std_accum = np.array([np.std(fxs[:i+1], ddof=1) if i>0 else 0 for i in range(len(fxs))])

        # Ajustar por volumen
        cum_avg_vol = cum_avg * L
        std_accum_vol = std_accum * L

        win = tk.Toplevel(self.root)
        win.title("Convergencia Monte Carlo")

        fig, ax = plt.subplots(figsize=(7,4))
        ax.plot(cum_avg_vol, label="MC promedio acumulado")
        ax.fill_between(range(len(cum_avg)), cum_avg_vol - std_accum_vol, cum_avg_vol + std_accum_vol,
                        color='gray', alpha=0.3, label='±1 std')
        ax.axhline(gauss_val, color="red", linestyle="--", label="Gauss-Legendre")
        ax.set_xlabel("Número de muestras")
        ax.set_ylabel("Estimación")
        ax.legend()
        ax.grid(True)

        canvas_conv = FigureCanvasTkAgg(fig, master=win)
        canvas_conv.get_tk_widget().pack(fill="both", expand=True)
        canvas_conv.draw()

    # -------------------- Análisis Estadístico --------------------
    def ventana_estadistica(self):
        if self.fxs_samples is None:
            messagebox.showwarning("Atención", "Primero ejecute una simulación.")
            return

        data = self.fxs_samples
        n = len(data)
        volumen = getattr(self, "volume", 1)

        # Ajustar por volumen
        media = np.mean(data) * volumen
        std = np.std(data, ddof=1) * volumen
        stderr = std / np.sqrt(n)

        win = tk.Toplevel(self.root)
        win.title("Análisis Estadístico")

        ttk.Label(win, text="Nivel de confianza:").pack(padx=5, pady=5, anchor="w")
        confidence_var = tk.DoubleVar(value=95)
        conf_box = ttk.Combobox(win, textvariable=confidence_var, values=[90,95,99], width=5)
        conf_box.pack(padx=5, pady=5, anchor="w")

        lbl = tk.Label(win, justify="left", font=("Arial",12))
        lbl.pack(padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(5,3))
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        def actualizar(event=None):
            conf = confidence_var.get()/100
            t_val = stats.t.ppf(0.5+conf/2, n-1)
            ic_lower = media - t_val*stderr
            ic_upper = media + t_val*stderr
            lbl.config(text=f"Muestras: {n}\nMedia: {media:.6f}\nDesviación estándar: {std:.6f}\n"
                            f"Error estándar: {stderr:.6f}\nIntervalo de confianza {int(conf*100)}%: [{ic_lower:.6f}, {ic_upper:.6f}]")
            ax.clear()
            ax.hist(data*volumen, bins=min(30,max(5,n//5)), edgecolor='black', alpha=0.7, density=True)
            x_vals = np.linspace(min(data)*volumen, max(data)*volumen, 200)
            y_norm = stats.norm.pdf(x_vals, media, std)
            ax.plot(x_vals, y_norm, color='orange', linewidth=2, label='Distribución Normal')
            ax.axvline(media, color='blue', linestyle='-', linewidth=2, label='Media')
            ax.axvline(ic_lower, color='red', linestyle='--', linewidth=2, label=f'IC {int(conf*100)}%')
            ax.axvline(ic_upper, color='red', linestyle='--', linewidth=2)
            ax.set_title("Distribución muestral f(x) ajustada por volumen")
            ax.set_xlabel("f(x) * (b-a)")
            ax.set_ylabel("Densidad")
            ax.grid(True)
            ax.legend()
            canvas.draw()

        conf_box.bind("<<ComboboxSelected>>", actualizar)
        actualizar()

    # -------------------- Ayuda --------------------
    def mostrar_ayuda(self):
        texto = (
            "Este simulador aproxima integrales definidas usando Monte Carlo.\n\n"
            "1. Método de 'puntos de éxito' (hit-or-miss): se genera un rectángulo que contiene a la curva. Se cuentan los puntos dentro de la región bajo la curva y se estima el área.\n\n"
            "2. Método Monte Carlo promedio: se toma el promedio de f(x) evaluada en puntos aleatorios de [a,b] y se multiplica por la longitud del intervalo.\n\n"
            "3. Gauss-Legendre: método de cuadratura determinista de alta precisión que se toma como valor de referencia.\n\n"
            "Usa los botones 'Integrales Dobles' o 'Integrales Triples' para abrir ventanas con teclado matemático avanzado y vista previa."
        )
        win = tk.Toplevel(self.root)
        win.title("Ayuda teórica")
        msg = tk.Message(win, text=texto, width=700)
        msg.pack(padx=10, pady=10)

    # -------------------- Método Promedio 1D (ventana) --------------------
    def ventana_metodo_promedio(self):
        try:
            func_str = self.entry_func.get()
            a, b = float(self.entry_a.get()), float(self.entry_b.get())
            N = int(self.entry_N.get())

            x = sp.Symbol('x')
            f_expr = sp.sympify(func_str)
            f = sp.lambdify(x, f_expr, "numpy")

            xs = np.random.uniform(a, b, N)
            fx_vals = np.nan_to_num(f(xs))
            integral_prom = (b-a)*np.mean(fx_vals)

            win = tk.Toplevel(self.root)
            win.title("Método Promedio 1D")

            tree = ttk.Treeview(win, columns=("x","f(x)"), show="headings")
            tree.heading("x", text="x")
            tree.heading("f(x)", text="f(x)")
            tree.pack(side="left", fill="y")

            scroll = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scroll.set)
            scroll.pack(side="left", fill="y")

            for i in range(min(N,5000)):
                tree.insert("", "end", values=(f"{xs[i]:.6f}", f"{fx_vals[i]:.6f}"))

            # Gráfico
            fig, ax = plt.subplots(figsize=(6,4))
            canvas = FigureCanvasTkAgg(fig, master=win)
            canvas.get_tk_widget().pack(fill="both", expand=True)

            ax.hist(fx_vals*(b-a), bins=min(30,max(5,N//5)), edgecolor='black', alpha=0.7)
            ax.axhline(np.mean(fx_vals)*(b-a), color='red', linestyle='--', label='Media f(x)*(b-a)')
            ax.set_title(f"Integral aproximada: {integral_prom:.6f}")
            ax.set_xlabel("f(x) * (b-a)")
            ax.set_ylabel("Frecuencia")
            ax.grid(True)
            ax.legend()
            canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------- Integrales Dobles (con teclado avanzado) --------------------
    def ventana_integrales_dobles(self):
        try:
            win = tk.Toplevel(self.root)
            win.title("Integral Doble Monte Carlo")

            ttk.Label(win, text="f(x,y) =").grid(row=0,column=0)
            entry_f = ttk.Entry(win, width=50)
            entry_f.insert(0,"x*y")
            entry_f.grid(row=0,column=1, columnspan=6, padx=5, pady=5)

            ttk.Label(win, text="a =").grid(row=1,column=0)
            entry_a = ttk.Entry(win, width=8); entry_a.insert(0,"0"); entry_a.grid(row=1,column=1)
            ttk.Label(win, text="b =").grid(row=1,column=2)
            entry_b = ttk.Entry(win, width=8); entry_b.insert(0,"1"); entry_b.grid(row=1,column=3)

            ttk.Label(win, text="c =").grid(row=2,column=0)
            entry_c = ttk.Entry(win, width=8); entry_c.insert(0,"0"); entry_c.grid(row=2,column=1)
            ttk.Label(win, text="d =").grid(row=2,column=2)
            entry_d = ttk.Entry(win, width=8); entry_d.insert(0,"1"); entry_d.grid(row=2,column=3)

            ttk.Label(win, text="N =").grid(row=3,column=0)
            entry_N = ttk.Entry(win, width=8); entry_N.insert(0,"500"); entry_N.grid(row=3,column=1)

            # -------- Teclado avanzado --------
            def agregar_texto(txt):
                entry_f.insert(tk.END, txt)

            frame_teclado = tk.LabelFrame(win, text="Teclado Matemático Avanzado")
            frame_teclado.grid(row=4, column=0, columnspan=8, pady=10)

            botones = [
                ["x", "y", "(", ")", "+", "-", "*", "/", "**"],
                ["sqrt(", "exp(", "log(", "log10(", "abs(", "sign(", "floor(", "ceiling("],
                ["sin(", "cos(", "tan(", "asin(", "acos(", "atan(", "atan2(", "pi"],
                ["sinh(", "cosh(", "tanh(", "asinh(", "acosh(", "atanh(", "E", "gamma("]
            ]

            for i, fila in enumerate(botones):
                for j, btxt in enumerate(fila):
                    tk.Button(
                        frame_teclado,
                        text=btxt,
                        width=7,
                        command=lambda t=btxt: agregar_texto(t)
                    ).grid(row=i, column=j, padx=2, pady=2)

            # -------- Cálculo --------
            def calcular():
                try:
                    f_str = entry_f.get()
                    a,b = float(entry_a.get()), float(entry_b.get())
                    c,d = float(entry_c.get()), float(entry_d.get())
                    N = int(entry_N.get())

                    x,y = sp.symbols('x y')
                    f_expr = sp.sympify(f_str)
                    f = sp.lambdify((x,y), f_expr, "numpy")

                    xs = np.random.uniform(a,b,N)
                    ys = np.random.uniform(c,d,N)
                    fx_vals = np.nan_to_num(f(xs,ys))
                    area = (b-a)*(d-c)
                    integral = area*np.mean(fx_vals)

                    fig, ax = plt.subplots(figsize=(6,4))
                    canvas = FigureCanvasTkAgg(fig, master=win)
                    canvas.get_tk_widget().grid(row=7,column=0,columnspan=8)
                    sc = ax.scatter(xs, ys, c=fx_vals, cmap='viridis', s=12)
                    fig.colorbar(sc, ax=ax, label='f(x,y)')
                    ax.set_title(f"Integral Doble ≈ {integral:.6f}")
                    ax.set_xlabel("x")
                    ax.set_ylabel("y")
                    canvas.draw()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            ttk.Button(win,text="Calcular", command=calcular).grid(row=6,column=0,columnspan=3, pady=10)
            ttk.Button(win,text="Limpiar entrada", command=lambda: entry_f.delete(0, tk.END)).grid(row=6,column=3,columnspan=2)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------- Integrales Triples (con teclado avanzado) --------------------
    def ventana_integrales_triples(self):
        try:
            win = tk.Toplevel(self.root)
            win.title("Integral Triple Monte Carlo")

            ttk.Label(win, text="f(x,y,z) =").grid(row=0, column=0)
            entry_f = ttk.Entry(win, width=60)
            entry_f.insert(0, "x*y*z")
            entry_f.grid(row=0, column=1, columnspan=8, padx=5, pady=5)

            ttk.Label(win, text="a =").grid(row=1, column=0)
            entry_a = ttk.Entry(win, width=8); entry_a.insert(0,"0"); entry_a.grid(row=1,column=1)
            ttk.Label(win, text="b =").grid(row=1, column=2)
            entry_b = ttk.Entry(win, width=8); entry_b.insert(0,"1"); entry_b.grid(row=1,column=3)

            ttk.Label(win, text="c =").grid(row=2, column=0)
            entry_c = ttk.Entry(win, width=8); entry_c.insert(0,"0"); entry_c.grid(row=2,column=1)
            ttk.Label(win, text="d =").grid(row=2, column=2)
            entry_d = ttk.Entry(win, width=8); entry_d.insert(0,"1"); entry_d.grid(row=2,column=3)

            ttk.Label(win, text="e =").grid(row=3, column=0)
            entry_e = ttk.Entry(win, width=8); entry_e.insert(0,"0"); entry_e.grid(row=3,column=1)
            ttk.Label(win, text="f =").grid(row=3, column=2)
            entry_fz = ttk.Entry(win, width=8); entry_fz.insert(0,"1"); entry_fz.grid(row=3,column=3)

            ttk.Label(win, text="N =").grid(row=4, column=0)
            entry_N = ttk.Entry(win, width=8); entry_N.insert(0,"2000"); entry_N.grid(row=4,column=1)

            # -------- Teclado avanzado (mismo que en dobles) --------
            def agregar_texto(txt):
                entry_f.insert(tk.END, txt)

            frame_teclado = tk.LabelFrame(win, text="Teclado Matemático Avanzado")
            frame_teclado.grid(row=5, column=0, columnspan=9, pady=10)

            botones = [
                ["x", "y", "z", "(", ")", "+", "-", "*", "/", "**"],
                ["sqrt(", "exp(", "log(", "log10(", "abs(", "sign(", "floor(", "ceiling("],
                ["sin(", "cos(", "tan(", "asin(", "acos(", "atan(", "atan2(", "pi"],
                ["sinh(", "cosh(", "tanh(", "asinh(", "acosh(", "atanh(", "E", "gamma("]
            ]

            for i, fila in enumerate(botones):
                for j, btxt in enumerate(fila):
                    tk.Button(
                        frame_teclado,
                        text=btxt,
                        width=7,
                        command=lambda t=btxt: agregar_texto(t)
                    ).grid(row=i, column=j, padx=2, pady=2)

            # -------- Cálculo triple --------
            def calcular():
                try:
                    f_str = entry_f.get()
                    a,b = float(entry_a.get()), float(entry_b.get())
                    c,d = float(entry_c.get()), float(entry_d.get())
                    e,fz = float(entry_e.get()), float(entry_fz.get())
                    N = int(entry_N.get())

                    x,y,z = sp.symbols('x y z')
                    f_expr = sp.sympify(f_str)
                    f = sp.lambdify((x,y,z), f_expr, "numpy")

                    xs = np.random.uniform(a,b,N)
                    ys = np.random.uniform(c,d,N)
                    zs = np.random.uniform(e,fz,N)
                    fx_vals = np.nan_to_num(f(xs,ys,zs))
                    volume = (b-a)*(d-c)*(fz-e)
                    integral = volume * np.mean(fx_vals)

                    fig = plt.figure(figsize=(5,4))
                    ax = fig.add_subplot(111, projection='3d')
                    canvas = FigureCanvasTkAgg(fig, master=win)
                    canvas.get_tk_widget().grid(row=7,column=0,columnspan=9)
                    sc = ax.scatter(xs, ys, zs, c=fx_vals, cmap='viridis', s=10)
                    fig.colorbar(sc, ax=ax, label='f(x,y,z)')
                    ax.set_title(f"Integral Triple ≈ {integral:.6f}")
                    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
                    canvas.draw()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            ttk.Button(win, text="Calcular", command=calcular).grid(row=6,column=0,columnspan=3, pady=10)
            ttk.Button(win, text="Limpiar entrada", command=lambda: entry_f.delete(0, tk.END)).grid(row=6,column=3,columnspan=2)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------- Teclado para entrada 1D (ventana) --------------------
    def teclado_funciones_1d(self):
        win = tk.Toplevel(self.root)
        win.title("Teclado de Funciones Avanzado (1D)")

        botones = [
            'sin(','cos(','tan(','exp(','log(','sqrt(','pi','E','**','(',')',
            'x','+','-','*','/','abs(','asin(','acos(','atan(',
            'sinh(','cosh(','tanh(','asinh(','acosh(','atanh('
        ]

        entry_target = self.entry_func

        def insertar(texto):
            entry_target.insert(tk.END, texto)

        r, c = 0, 0
        for b in botones:
            tk.Button(win, text=b, width=8, command=lambda bt=b: insertar(bt)).grid(row=r,column=c,padx=2,pady=2)
            c += 1
            if c > 6:
                c = 0
                r += 1

        tk.Button(win, text="Borrar", width=10, command=lambda: entry_target.delete(len(entry_target.get())-1, tk.END)).grid(row=r+1,column=0,columnspan=3,pady=5)
        tk.Button(win, text="Limpiar Todo", width=12, command=lambda: entry_target.delete(0, tk.END)).grid(row=r+1,column=3,columnspan=3,pady=5)

import numpy as np
import sympy as sp

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
except Exception:
    FigureCanvasTkAgg = None
    plt = None


# ==========================
# Utilidades seguras y parsing
# ==========================
def _compile_safe(expr: str, allowed_names: dict, varnames: List[str]):
    expr_ast = ast.parse(expr, mode='eval')
    for node in ast.walk(expr_ast):
        if isinstance(node, ast.Name):
            if node.id not in allowed_names and node.id not in varnames:
                raise ValueError(f"Nombre no permitido en expresión: {node.id}")
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Importaciones no permitidas.")
    return compile(expr_ast, "<expr>", "eval")


def make_safe_func_1v(expr: str) -> Callable[[float], float]:
    """
    Compila f(x) segura.
    - Escalar -> float
    - Array/lista/tupla -> np.array aplicando elemento a elemento
    """
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed.update({"abs": abs, "pow": pow})
    code = _compile_safe(expr, allowed, ["x"])

    def f_eval(x):
        if isinstance(x, (np.ndarray, list, tuple)):
            def scalar(t):
                return float(eval(code, {"__builtins__": {}}, {**allowed, "x": float(t)}))
            return np.vectorize(scalar, otypes=[float])(x)
        return float(eval(code, {"__builtins__": {}}, {**allowed, "x": float(x)}))
    return f_eval


def make_safe_func_2v(expr: str) -> Callable[[float, float], float]:
    """
    Compila f(x,y) segura.
    - Soporta evaluación escalar y vectorizada (broadcast con numpy)
    """
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed.update({"abs": abs, "pow": pow})
    code = _compile_safe(expr, allowed, ["x", "y"])

    def f_eval(x, y):
        def scalar(a, b):
            return float(eval(code, {"__builtins__": {}}, {**allowed, "x": float(a), "y": float(b)}))
        return np.vectorize(scalar, otypes=[float])(x, y)
    return f_eval


def parse_num(s: str) -> float:
    """Acepta 'pi' y 'E'."""
    s = s.replace("pi", str(math.pi)).replace("E", str(math.e))
    return float(eval(s, {"__builtins__": {}}, {}))


def parse_csv_numbers(s: str) -> List[float]:
    s = s.strip()
    if not s:
        return []
    parts = [p.strip() for p in s.split(",")]
    return [parse_num(p) for p in parts]


# ==========================
# Derivada numérica (para Newton)
# ==========================
def numerical_derivative(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)


# ==========================
# MÓDULO: Raíces
# Métodos: newtonrhapson, punto fijo, Aitken Δ²
# ==========================
def newtonrhapson(f: Callable[[float], float], x0: float,
                  df: Optional[Callable[[float], float]] = None,
                  tol: float = 1e-8, max_iter: int = 50):
    hist = []
    x = x0
    for n in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x) if df is not None else numerical_derivative(f, x)
        if abs(dfx) < 1e-14:
            raise ValueError("Derivada ~0; Newton puede fallar.")
        x_new = x - fx / dfx
        abs_err = abs(x_new - x)
        rel_err = abs_err / abs(x_new) if x_new != 0 else float('inf')
        hist.append((n, x, fx, dfx, x_new, abs_err, rel_err))
        x = x_new
        if abs_err < tol or abs(fx) < tol:
            return x, hist
    return None, hist


def punto_fijo(g: Callable[[float], float], x0: float,
               tol: float = 1e-8, max_iter: int = 200):
    hist = []
    x = x0
    for n in range(1, max_iter + 1):
        gx = g(x)
        x_new = gx
        abs_err = abs(x_new - x)
        rel_err = abs_err / abs(x_new) if x_new != 0 else float('inf')
        hist.append((n, x, gx, x_new, abs_err, rel_err))
        x = x_new
        if abs_err < tol:
            return x, hist
    return None, hist


def aitken_delta2(g: Callable[[float], float], x0: float,
                  tol: float = 1e-8, max_iter: int = 100):
    hist = []
    x = x0
    for n in range(1, max_iter + 1):
        x1 = g(x)
        x2 = g(x1)
        dx = x1 - x
        d2x = x2 - 2.0 * x1 + x
        if abs(d2x) < 1e-14:
            x_hat = x1  # no se puede acelerar este paso
        else:
            x_hat = x - (dx * dx) / d2x
        abs_err = abs(x_hat - x)
        rel_err = abs_err / abs(x_hat) if x_hat != 0 else float('inf')
        hist.append((n, x, x1, x2, x_hat, abs_err, rel_err))
        x = x_hat
        if abs_err < tol:
            return x, hist
    return None, hist


# ==========================
# MÓDULO: Integración numérica
# ==========================
def rectangulo_medio(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    mid = (x[:-1] + x[1:]) / 2
    I = h * np.sum(f(mid))
    tabla = [(i, mid[i], f(mid[i])) for i in range(n)]
    nodos = mid
    return I, tabla, nodos

def trapecio(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    fx = f(x)
    I = h * (0.5 * fx[0] + np.sum(fx[1:-1]) + 0.5 * fx[-1])
    tabla = [(i, x[i], fx[i]) for i in range(n + 1)]
    return I, tabla, x

def simpson_13(f, a, b, n):
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    fx = f(x)
    I = (h / 3) * (fx[0] + fx[-1] + 4 * np.sum(fx[1:-1:2]) + 2 * np.sum(fx[2:-2:2]))
    tabla = [(i, x[i], fx[i]) for i in range(n + 1)]
    return I, tabla, x

def simpson_38(f, a, b, n):
    r = n % 3
    if r != 0:
        n += (3 - r)
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    fx = f(x)
    idx = np.arange(1, n)
    I = (3 * h / 8) * (fx[0] + fx[-1] +
                       3 * np.sum(fx[idx[idx % 3 != 0]]) +
                       2 * np.sum(fx[3:-1:3]))
    tabla = [(i, x[i], fx[i]) for i in range(n + 1)]
    return I, tabla, x

def boole(f, a, b, n):
    r = n % 4
    if r != 0:
        n += (4 - r)
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    fx = f(x)
    I = (2 * h / 45) * (7 * (fx[0] + fx[-1]) +
                        32 * np.sum(fx[1:-1:2]) +
                        12 * np.sum(fx[2:-2:4]) +
                        14 * np.sum(fx[4:-1:4]))
    tabla = [(i, x[i], fx[i]) for i in range(n + 1)]
    return I, tabla, x

def gauss_legendre(f, a, b, n):
    if n not in (1, 2, 3, 4, 5):
        raise ValueError("Cuadratura Gauss-Legendre soportada para n=1..5")
    nodes, weights = np.polynomial.legendre.leggauss(n)  # en [-1,1]
    t = (b - a) / 2.0
    m = (b + a) / 2.0
    x = m + t * nodes
    I = t * np.sum(weights * f(x))
    tabla = [(i, x[i], f(x[i]), weights[i]) for i in range(n)]
    return I, tabla, x


# ==========================
# MÓDULO: Interpolación de Lagrange
# ==========================
def lagrange_bases_and_poly(xs: List[float], ys: List[float]):
    """
    Devuelve:
      - lista de polinomios base L_i(x) como np.poly1d
      - polinomio interpolante P(x) = sum y_i * L_i(x)
    """
    n = len(xs)
    if n != len(ys):
        raise ValueError("xs y ys deben tener la misma longitud.")
    if n == 0:
        raise ValueError("Debe ingresar al menos un punto.")
    polys = []
    for i in range(n):
        Li = np.poly1d([1.0])
        denom = 1.0
        for j in range(n):
            if j == i:
                continue
            Li *= np.poly1d([1.0, -xs[j]])   # (x - xj)
            denom *= (xs[i] - xs[j])
        Li = Li / denom
        polys.append(Li)
    P = np.poly1d([0.0])
    for i in range(n):
        P += ys[i] * polys[i]
    return polys, P


def poly_to_str(P: np.poly1d, decimals: int = 8) -> str:
    """
    Convierte un np.poly1d en un string legible con 'decimals' decimales.
    Ej: 1.23456789*x**3 - 0.50000000*x + 2.00000000
    """
    coeffs = P.c  # mayor a menor grado
    deg = len(coeffs) - 1
    terms = []
    eps = 10**(-(decimals + 2))  # umbral para cero

    for i, a in enumerate(coeffs):
        power = deg - i
        if abs(a) < eps:
            continue
        coef = float(a)
        abscoef = abs(round(coef, decimals))

        if power == 0:
            term_core = f"{abscoef:.{decimals}f}"
        elif power == 1:
            if abs(abscoef - 1.0) < eps:
                term_core = "x"
            else:
                term_core = f"{abscoef:.{decimals}f}*x"
        else:
            if abs(abscoef - 1.0) < eps:
                term_core = f"x**{power}"
            else:
                term_core = f"{abscoef:.{decimals}f}*x**{power}"

        sign = "-" if coef < 0 else "+"
        terms.append((sign, term_core))

    if not terms:
        return "0"

    first_sign, first_term = terms[0]
    s = f"- {first_term}" if first_sign == "-" else first_term
    for sign, term in terms[1:]:
        s += f" {sign} {term}"
    return s


# ==========================
# MÓDULO: Diferencias Finitas y Derivadas Parciales
# ==========================
def fd_forward_1(f, x0, h):
    return (f(x0 + h) - f(x0)) / h

def fd_backward_1(f, x0, h):
    return (f(x0) - f(x0 - h)) / h

def fd_central_1(f, x0, h):
    return (f(x0 + h) - f(x0 - h)) / (2*h)

def fd_central_2(f, x0, h):
    return (f(x0 + h) - 2*f(x0) + f(x0 - h)) / (h*h)

# 2D (centrales, O(h^2))
def fx_central(fxy, x0, y0, hx):
    return (fxy(x0 + hx, y0) - fxy(x0 - hx, y0)) / (2*hx)

def fy_central(fxy, x0, y0, hy):
    return (fxy(x0, y0 + hy) - fxy(x0, y0 - hy)) / (2*hy)

def fxx_central(fxy, x0, y0, hx):
    return (fxy(x0 + hx, y0) - 2*fxy(x0, y0) + fxy(x0 - hx, y0)) / (hx*hx)

def fyy_central(fxy, x0, y0, hy):
    return (fxy(x0, y0 + hy) - 2*fxy(x0, y0) + fxy(x0, y0 - hy)) / (hy*hy)

def fxy_central(fxy, x0, y0, hx, hy):
    # (f(x+h,y+h)-f(x+h,y-h)-f(x-h,y+h)+f(x-h,y-h))/(4hxhy)
    return (fxy(x0+hx, y0+hy) - fxy(x0+hx, y0-hy) - fxy(x0-hx, y0+hy) + fxy(x0-hx, y0-hy)) / (4*hx*hy)


# ==========================
# UI: Frames por módulo
# ==========================
class RootFrame(ttk.Frame):
    """Raíces: newtonrhapson, punto fijo, Aitken Δ²"""
    def __init__(self, master):
        super().__init__(master)
        self._build()

    def _build(self):
        frm_algo = ttk.Frame(self)
        ttk.Label(frm_algo, text="Algoritmo:").pack(side=tk.LEFT)
        self.cb_algo = ttk.Combobox(
            frm_algo, state="readonly",
            values=["newtonrhapson", "punto fijo", "Aitken Δ²"]
        )
        self.cb_algo.current(0)
        self.cb_algo.pack(side=tk.LEFT, padx=5)
        self.cb_algo.bind("<<ComboboxSelected>>", lambda e: self._render_params())
        frm_algo.pack(fill=tk.X, pady=5)

        self.params = ttk.Frame(self); self.params.pack(fill=tk.X, pady=5)

        self.tree = ttk.Treeview(self, show="headings", height=12)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        frm_btn = ttk.Frame(self)
        ttk.Button(frm_btn, text="Calcular", command=self._run).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_btn, text="Graficar función", command=self._plot).pack(side=tk.LEFT, padx=5)
        frm_btn.pack(pady=5)

        self.var_res = tk.StringVar(value="Resultado: —")
        ttk.Label(self, textvariable=self.var_res).pack(anchor="w", pady=3)

        self.fig = None
        self.canvas = None

        self._render_params()

    def _clear_tree(self):
        for c in self.tree.get_children():
            self.tree.delete(c)

    def _render_params(self):
        for w in self.params.winfo_children():
            w.destroy()
        algo = self.cb_algo.get()
        self.entries = {}

        # Tolerancia y máx iter
        frm_tol = ttk.Frame(self.params)
        ttk.Label(frm_tol, text="Tol=").pack(side=tk.LEFT)
        e_tol = ttk.Entry(frm_tol, width=10); e_tol.insert(0, "1e-8"); e_tol.pack(side=tk.LEFT)
        ttk.Label(frm_tol, text="   Máx it=").pack(side=tk.LEFT)
        e_it = ttk.Entry(frm_tol, width=6); e_it.insert(0, "100"); e_it.pack(side=tk.LEFT)
        frm_tol.pack(anchor="w", pady=2)
        self.entries["tol"] = e_tol
        self.entries["max_iter"] = e_it

        if algo == "newtonrhapson":
            frm_fx = ttk.Frame(self.params)
            ttk.Label(frm_fx, text="f(x) = ").pack(side=tk.LEFT)
            e_fx = ttk.Entry(frm_fx, width=40); e_fx.insert(0, "x**3 - x - 2"); e_fx.pack(side=tk.LEFT, fill=tk.X, expand=True)
            frm_fx.pack(fill=tk.X, pady=2)
            frm_dfx = ttk.Frame(self.params)
            ttk.Label(frm_dfx, text="f'(x) (opcional) = ").pack(side=tk.LEFT)
            e_dfx = ttk.Entry(frm_dfx, width=40); e_dfx.insert(0, ""); e_dfx.pack(side=tk.LEFT, fill=tk.X, expand=True)
            frm_dfx.pack(fill=tk.X, pady=2)
            frm_x0 = ttk.Frame(self.params)
            ttk.Label(frm_x0, text="x0=").pack(side=tk.LEFT)
            e_x0 = ttk.Entry(frm_x0, width=12); e_x0.insert(0, "1.5"); e_x0.pack(side=tk.LEFT)
            frm_x0.pack(anchor="w", pady=2)

            self.entries["fx"] = e_fx
            self.entries["dfx"] = e_dfx
            self.entries["x0"] = e_x0

            self._clear_tree()
            cols = ("n", "x", "f(x)", "f'(x)", "x_new", "|Δ|", "rel")
            self.tree["columns"] = cols
            for c in cols:
                self.tree.heading(c, text=c); self.tree.column(c, width=100, anchor="center")

        elif algo in ("punto fijo", "Aitken Δ²"):
            frm_gx = ttk.Frame(self.params)
            ttk.Label(frm_gx, text="g(x) = ").pack(side=tk.LEFT)
            e_gx = ttk.Entry(frm_gx, width=40); e_gx.insert(0, "cos(x)"); e_gx.pack(side=tk.LEFT, fill=tk.X, expand=True)
            frm_gx.pack(fill=tk.X, pady=2)
            frm_x0 = ttk.Frame(self.params)
            ttk.Label(frm_x0, text="x0=").pack(side=tk.LEFT)
            e_x0 = ttk.Entry(frm_x0, width=12); e_x0.insert(0, "0.5"); e_x0.pack(side=tk.LEFT)
            frm_x0.pack(anchor="w", pady=2)
            self.entries["gx"] = e_gx
            self.entries["x0"] = e_x0

            self._clear_tree()
            cols = ("n", "x", "g(x)", "x_new", "|Δ|", "rel") if algo=="punto fijo" else ("n", "x", "x1", "x2", "x_hat", "|Δ|", "rel")
            self.tree["columns"] = cols
            for c in cols:
                self.tree.heading(c, text=c); self.tree.column(c, width=100, anchor="center")

    def _run(self):
        algo = self.cb_algo.get()
        try:
            tol = float(self.entries["tol"].get())
            max_iter = int(self.entries["max_iter"].get())
        except Exception:
            messagebox.showerror("Parámetros", "Tol o Máx it no válidos."); return

        try:
            if algo == "newtonrhapson":
                f = make_safe_func_1v(self.entries["fx"].get())
                dfx_expr = self.entries["dfx"].get().strip()
                df = make_safe_func_1v(dfx_expr) if dfx_expr else None
                x0 = float(self.entries["x0"].get())
                root, hist = newtonrhapson(f, x0, df=df, tol=tol, max_iter=max_iter)
                self._clear_tree()
                for row in hist:
                    self.tree.insert("", tk.END, values=[f"{v:.8f}" if isinstance(v,(int,float)) else v for v in row])
                self.var_res.set("Resultado: no convergió." if root is None else f"Resultado: x* = {root:.8f}, f(x*) = {f(root):.8f}")

            elif algo == "punto fijo":
                g = make_safe_func_1v(self.entries["gx"].get())
                x0 = float(self.entries["x0"].get())
                root, hist = punto_fijo(g, x0, tol=tol, max_iter=max_iter)
                self._clear_tree()
                for row in hist:
                    self.tree.insert("", tk.END, values=[f"{v:.8f}" if isinstance(v,(int,float)) else v for v in row])
                self.var_res.set("Resultado: no convergió." if root is None else f"Resultado: x* = {root:.8f}, |g(x*)-x*| = {abs(g(root)-root):.8f}")

            elif algo == "Aitken Δ²":
                g = make_safe_func_1v(self.entries["gx"].get())
                x0 = float(self.entries["x0"].get())
                root, hist = aitken_delta2(g, x0, tol=tol, max_iter=max_iter)
                self._clear_tree()
                for row in hist:
                    self.tree.insert("", tk.END, values=[f"{v:.8f}" if isinstance(v,(int,float)) else v for v in row])
                self.var_res.set("Resultado: no convergió." if root is None else f"Resultado: x* = {root:.8f}, |g(x*)-x*| = {abs(g(root)-root):.8f}")
            else:
                raise ValueError("Algoritmo no implementado.")
        except Exception as e:
            messagebox.showerror("Ejecución", str(e)); return

    def _plot(self):
        if FigureCanvasTkAgg is None or plt is None:
            messagebox.showinfo("Gráfica", "matplotlib no disponible."); return
        algo = self.cb_algo.get()
        try:
            if algo == "newtonrhapson":
                f = make_safe_func_1v(self.entries["fx"].get())
                func = f; ttl = "f(x)"
            else:
                g = make_safe_func_1v(self.entries["gx"].get())
                func = g; ttl = "g(x)"
        except Exception as e:
            messagebox.showerror("Error en función", str(e)); return

        xs = np.linspace(-5, 5, 400)
        ys = np.array([func(x) for x in xs])

        if self.fig is None:
            self.fig = plt.Figure(figsize=(5, 3), dpi=100)
            self.ax = self.fig.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.clear()
        self.ax.axhline(0, lw=1)
        self.ax.plot(xs, ys, label=ttl)
        if algo != "newtonrhapson":
            self.ax.plot(xs, xs, linestyle="--", label="y=x")
        self.ax.set_title(ttl)
        self.ax.grid(True, ls=":")
        self.ax.legend()
        self.canvas.draw_idle()


class IntegrationFrame(ttk.Frame):
    """Integración numérica"""
    def __init__(self, master):
        super().__init__(master)
        self._build()

    def _build(self):
        frm_f = ttk.Frame(self)
        ttk.Label(frm_f, text="f(x) = ").pack(side=tk.LEFT)
        self.entry_fx = ttk.Entry(frm_f, width=40); self.entry_fx.insert(0, "sin(x)")
        ttk.Button(frm_f, text="Teclado Funciones", command=lambda: open_function_keypad(self, self.entry_fx, "Teclado - f(x)")).pack(side=tk.LEFT, padx=4)
        self.entry_fx.pack(side=tk.LEFT, fill=tk.X, expand=True)
        frm_f.pack(fill=tk.X, pady=5)

        frm_abn = ttk.Frame(self)
        ttk.Label(frm_abn, text="a=").pack(side=tk.LEFT)
        self.ea = ttk.Entry(frm_abn, width=10); self.ea.insert(0, "0"); self.ea.pack(side=tk.LEFT)
        ttk.Label(frm_abn, text="   b=").pack(side=tk.LEFT)
        self.eb = ttk.Entry(frm_abn, width=10); self.eb.insert(0, "pi"); self.eb.pack(side=tk.LEFT)
        ttk.Label(frm_abn, text="   n=").pack(side=tk.LEFT)
        self.en = ttk.Entry(frm_abn, width=8); self.en.insert(0, "10"); self.en.pack(side=tk.LEFT)
        frm_abn.pack(anchor="w", pady=2)

        frm_algo = ttk.Frame(self)
        ttk.Label(frm_algo, text="Regla:").pack(side=tk.LEFT)
        self.cb_algo = ttk.Combobox(frm_algo, state="readonly",
            values=["Rectángulo medio", "Trapecio", "Simpson 1/3", "Simpson 3/8", "Boole", "Gauss-Legendre"])
        self.cb_algo.current(1)
        self.cb_algo.pack(side=tk.LEFT, padx=5)
        self.cb_algo.bind("<<ComboboxSelected>>", lambda e: self._toggle_gauss())
        frm_algo.pack(fill=tk.X, pady=5)

        frm_btn = ttk.Frame(self)
        ttk.Button(frm_btn, text="Integrar", command=self._run).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_btn, text="Graficar f(x)", command=self._plot).pack(side=tk.LEFT, padx=5)
        frm_btn.pack(pady=5)

        self.tree = ttk.Treeview(self, show="headings", height=12)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        self.var_res = tk.StringVar(value="Resultado: —")
        ttk.Label(self, textvariable=self.var_res).pack(anchor="w", pady=3)

        self.fig = None
        self.canvas = None

        self._toggle_gauss()

    def _clear_tree(self):
        for c in self.tree.get_children(): self.tree.delete(c)

    def _toggle_gauss(self):
        algo = self.cb_algo.get()
        self._clear_tree()
        if algo == "Gauss-Legendre":
            cols = ("i", "x_i", "f(x_i)", "w_i")
        elif algo == "Rectángulo medio":
            cols = ("i", "x_mid", "f(x_mid)")
        else:
            cols = ("i", "x_i", "f(x_i)")
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c); self.tree.column(c, width=100, anchor="center")

    def _run(self):
        try:
            f = make_safe_func_1v(self.entry_fx.get())
            a = parse_num(self.ea.get()); b = parse_num(self.eb.get()); n = int(self.en.get())
            if n <= 0: raise ValueError("n debe ser > 0")
        except Exception as e:
            messagebox.showerror("Parámetros", f"Error: {e}"); return

        algo = self.cb_algo.get()
        try:
            if algo == "Rectángulo medio":
                I, tabla, nodos = rectangulo_medio(f, a, b, n)
            elif algo == "Trapecio":
                I, tabla, nodos = trapecio(f, a, b, n)
            elif algo == "Simpson 1/3":
                I, tabla, nodos = simpson_13(f, a, b, n)
            elif algo == "Simpson 3/8":
                I, tabla, nodos = simpson_38(f, a, b, n)
            elif algo == "Boole":
                I, tabla, nodos = boole(f, a, b, n)
            elif algo == "Gauss-Legendre":
                I, tabla, nodos = gauss_legendre(f, a, b, n)
            else:
                raise ValueError("Regla no implementada.")
        except Exception as e:
            messagebox.showerror("Ejecución", str(e)); return

        self._clear_tree()
        for row in tabla:
            self.tree.insert("", tk.END, values=[f"{v:.8f}" if isinstance(v,(int,float)) else v for v in row])
        self.var_res.set(f"Resultado: I ≈ {I:.8f}")

        self._last_nodes = nodos
        self._last_f = f
        self._last_a = a
        self._last_b = b

    def _plot(self):
        if FigureCanvasTkAgg is None or plt is None:
            messagebox.showinfo("Gráfica", "matplotlib no disponible."); return
        try:
            f = make_safe_func_1v(self.entry_fx.get())
            a = parse_num(self.ea.get()); b = parse_num(self.eb.get())
        except Exception as e:
            messagebox.showerror("Error", str(e)); return

        xs = np.linspace(a, b, 400)
        ys = np.array([f(x) for x in xs])

        if self.fig is None:
            self.fig = plt.Figure(figsize=(5, 3), dpi=100)
            self.ax = self.fig.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.clear()
        self.ax.plot(xs, ys)
        self.ax.set_title("f(x)")
        self.ax.grid(True, ls=":")
        if hasattr(self, "_last_nodes"):
            xn = self._last_nodes
            yn = np.array([f(x) for x in np.atleast_1d(xn)])
            self.ax.scatter(np.atleast_1d(xn), yn, marker='o')
        self.canvas.draw_idle()



class LagrangeFrame(ttk.Frame):
    """Interpolación de Lagrange: bases L_i(x), cálculo paso a paso y polinomio P(x)."""
    def __init__(self, master):
        super().__init__(master)
        self._build()

    def _build(self):
        # Entradas de nodos
        frm_pts = ttk.Frame(self)
        ttk.Label(frm_pts, text="x (coma-separado):").pack(side=tk.LEFT)
        self.ex = ttk.Entry(frm_pts, width=40); self.ex.insert(0, "0, 1, 2")
        self.ex.pack(side=tk.LEFT, padx=4)
        ttk.Label(frm_pts, text="y:").pack(side=tk.LEFT)
        self.ey = ttk.Entry(frm_pts, width=40); self.ey.insert(0, "1, 2, 0")
        self.ey.pack(side=tk.LEFT, padx=4)
        frm_pts.pack(fill=tk.X, pady=5)

        # x de evaluación y opciones
        frm_opts = ttk.Frame(self)
        ttk.Label(frm_opts, text="x_eval (opcional):").pack(side=tk.LEFT)
        self.ex_eval = ttk.Entry(frm_opts, width=16); self.ex_eval.insert(0, "")
        self.ex_eval.pack(side=tk.LEFT, padx=4)
        self.var_show = tk.StringVar(value="Bases L_i(x) (expresiones)")
        self.cb_show = ttk.Combobox(frm_opts, width=34, state="readonly",
                                    values=["Tabla (x_i, y_i)",
                                            "Bases L_i(x) (expresiones)",
                                            "Bases L_i(x) (valores en x_eval)",
                                            "Términos y_i·L_i(x)",
                                            "Coeficientes del polinomio P(x)"])
        self.cb_show.current(1)
        self.cb_show.pack(side=tk.LEFT, padx=6)
        ttk.Button(frm_opts, text="Calcular", command=self._compute).pack(side=tk.LEFT, padx=6)
        ttk.Button(frm_opts, text="Graficar", command=self._plot).pack(side=tk.LEFT, padx=6)
        frm_opts.pack(fill=tk.X, pady=5)

        # Resultado breve
        self.var_res = tk.StringVar(value="Resultado:")
        ttk.Label(self, textvariable=self.var_res).pack(anchor="w", padx=4)

        # Tabla
        cols = ("i","dato")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150 if c=="i" else 600, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # Texto con detalle y polinomio
        frm_text = ttk.LabelFrame(self, text="Detalle / Polinomio")
        self.txt = ScrolledText(frm_text, height=12, wrap="word")
        self.txt.pack(fill=tk.BOTH, expand=True)
        frm_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Copiar polinomio
        ttk.Button(self, text="Copiar P(x)", command=self._copy_poly).pack(pady=4)

        # Área de gráfico (on demand)
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib.pyplot as plt
            self._mpl_ok = True
        except Exception:
            self._mpl_ok = False

    def _parse_xy(self):
        try:
            xs = [float(s.strip()) for s in self.ex.get().split(",") if s.strip()!=""]
            ys = [float(s.strip()) for s in self.ey.get().split(",") if s.strip()!=""]
            if len(xs) != len(ys):
                raise ValueError("x e y deben tener la misma longitud.")
            if len(set(xs)) != len(xs):
                raise ValueError("Los x_i deben ser todos distintos.")
            return xs, ys
        except Exception as e:
            messagebox.showerror("Entradas", str(e))
            return None, None

    def _poly_to_string(self, poly, var='x', decimals=8):
        # poly es un objeto sympy (expandido). Convertimos a string bonito
        import sympy as sp
        x = sp.Symbol(var)
        poly = sp.expand(poly)
        coeffs = sp.Poly(poly, x).all_coeffs()
        coeffs = [float(c) for c in coeffs]
        deg = len(coeffs)-1
        parts = []
        eps = 10**(-(decimals+2))
        for i,a in enumerate(coeffs):
            p = deg - i
            if abs(a) < eps: 
                continue
            coef = f"{a:.{decimals}f}".rstrip('0').rstrip('.')
            if p==0:
                term = f"{coef}"
            elif p==1:
                term = f"{coef}·{var}"
            else:
                term = f"{coef}·{var}^{p}"
            parts.append(term)
        if not parts:
            return "0"
        # Unir con signos adecuados (coef ya tiene signo)
        s = parts[0]
        for t in parts[1:]:
            s += (" + " if not t.startswith("-") else " - ") + (t.lstrip("-"))
        return s

    def _compute(self):
        xs, ys = self._parse_xy()
        if xs is None: return
        import sympy as sp, numpy as np
        x = sp.Symbol('x')
        n = len(xs)

        # Construcción de bases L_i(x)
        bases = []
        detail_lines = []
        for i in range(n):
            xi = xs[i]
            den = 1.0
            num = 1
            num_factors = []
            for j in range(n):
                if j==i: continue
                num *= (x - xs[j])
                num_factors.append(f"(x - {xs[j]:.8f})")
                den *= (xi - xs[j])
            Li = sp.expand(num/den)
            bases.append(Li)
            detail_lines.append(f"L_{i}(x) = " + " * ".join(num_factors) + f"  /  " + " * ".join([f"({xi:.8f} - {xs[j]:.8f})" for j in range(n) if j!=i]))
            detail_lines.append(f"       = {self._poly_to_string(Li)}")
            detail_lines.append("")

        # Polinomio P(x)
        P = sp.expand(sum(ys[i]*bases[i] for i in range(n)))

        # Poblado de tabla según modo
        mode = self.cb_show.get()
        self.tree.delete(*self.tree.get_children())
        if mode == "Tabla (x_i, y_i)":
            self.tree["columns"] = ("i","x_i","y_i")
            for c in ("i","x_i","y_i"):
                self.tree.heading(c, text=c); self.tree.column(c, width=140, anchor="center")
            for i,(xi,yi) in enumerate(zip(xs,ys)):
                self.tree.insert("", "end", values=(i, f"{xi:.8f}", f"{yi:.8f}"))
        elif mode == "Bases L_i(x) (valores en x_eval)":
            self.tree["columns"] = ("i","L_i(x_eval)")
            for c in ("i","L_i(x_eval)"):
                self.tree.heading(c, text=c); self.tree.column(c, width=200 if c=="i" else 500, anchor="center")
            xv_str = self.ex_eval.get().strip()
            if not xv_str:
                messagebox.showinfo("x_eval", "Ingresá un x_eval para evaluar las bases."); 
            try:
                xv = float(xv_str)
                for i,Li in enumerate(bases):
                    val = float(sp.N(Li.subs({x:xv})))
                    self.tree.insert("", "end", values=(i, f"{val:.8f}"))
            except Exception as e:
                messagebox.showerror("x_eval", str(e))
        elif mode == "Términos y_i·L_i(x)":
            self.tree["columns"] = ("i","y_i·L_i(x)")
            for c in ("i","y_i·L_i(x)"):
                self.tree.heading(c, text=c); self.tree.column(c, width=200 if c=="i" else 600, anchor="center")
            for i,Li in enumerate(bases):
                term = sp.expand(ys[i]*Li)
                self.tree.insert("", "end", values=(i, self._poly_to_string(term)))
        elif mode == "Coeficientes del polinomio P(x)":
            self.tree["columns"] = ("grado","coeficiente")
            for c in ("grado","coeficiente"):
                self.tree.heading(c, text=c); self.tree.column(c, width=200, anchor="center")
            coeffs = sp.Poly(P, x).all_coeffs()
            deg = len(coeffs)-1
            for k,c in enumerate(coeffs):
                self.tree.insert("", "end", values=(deg-k, f"{float(c):.8f}"))
        else: # Bases expresiones
            self.tree["columns"] = ("i","L_i(x)")
            for c in ("i","L_i(x)"):
                self.tree.heading(c, text=c); self.tree.column(c, width=140 if c=="i" else 640, anchor="center")
            for i,Li in enumerate(bases):
                self.tree.insert("", "end", values=(i, self._poly_to_string(Li)))

        # Texto detallado y polinomio
        detail = "Cálculo de bases de Lagrange:\n" + "\n".join(detail_lines)
        detail += "\nPolinomio interpolante:\nP(x) = " + self._poly_to_string(P)
        self._set_text(detail)

        # Resultado breve (y evaluación si corresponde)
        xv = self.ex_eval.get().strip()
        if xv:
            try:
                xv = float(xv)
                Pv = float(sp.N(P.subs({x:xv})))
                self.var_res.set(f"Resultado: P({xv}) = {Pv:.8f}")
            except Exception:
                self.var_res.set("Resultado: P(x) construido.")
        else:
            self.var_res.set("Resultado: P(x) construido.")

        # Guardar para graficar
        self._last = {"xs": xs, "ys": ys, "P": P}

    def _set_text(self, s):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, s)
        self.txt.configure(state="disabled")

    def _copy_poly(self):
        try:
            import re
            s = self.txt.get("1.0", tk.END)
            # extrae última línea P(x) = ...
            m = [line for line in s.splitlines() if line.startswith("P(x) = ")]
            poly_line = m[-1] if m else s
            self.clipboard_clear()
            self.clipboard_append(poly_line)
            messagebox.showinfo("Copiado", "P(x) copiado al portapapeles.")
        except Exception as e:
            messagebox.showerror("Copiar", str(e))

    def _plot(self):
        if not self._mpl_ok:
            messagebox.showinfo("Gráfico","matplotlib no disponible en este entorno.")
            return
        data = getattr(self, "_last", None)
        if not data:
            messagebox.showinfo("Info","Primero calcule para generar el polinomio.")
            return
        import numpy as np, sympy as sp, matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        x = sp.Symbol('x')
        xs = np.array(data["xs"]); ys = np.array(data["ys"])
        P = data["P"]
        xv = np.linspace(min(xs)-1, max(xs)+1, 400)
        yv = np.array([float(sp.N(P.subs({x:t}))) for t in xv])

        top = tk.Toplevel(self); top.title("Interpolación de Lagrange - Gráfico")
        fig, ax = plt.subplots(figsize=(6,4))
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        ax.plot(xv, yv, label="P(x)")
        ax.scatter(xs, ys, color="red", label="Nodos")
        ax.grid(True, ls=":")
        ax.legend()
        canvas.draw_idle()

class FiniteDiffFrame(ttk.Frame):
    """Diferencias Finitas 1D y Derivadas Parciales 2D"""
    def __init__(self, master):
        super().__init__(master)
        self._build()

    def _build(self):
        frm_dim = ttk.Frame(self)
        ttk.Label(frm_dim, text="Dimensión:").pack(side=tk.LEFT)
        self.cb_dim = ttk.Combobox(frm_dim, state="readonly", values=["1D", "2D"])
        self.cb_dim.current(0); self.cb_dim.pack(side=tk.LEFT, padx=5)
        self.cb_dim.bind("<<ComboboxSelected>>", lambda e: self._render_params())
        frm_dim.pack(fill=tk.X, pady=5)

        self.params = ttk.Frame(self); self.params.pack(fill=tk.X, pady=5)

        frm_btn = ttk.Frame(self)
        ttk.Button(frm_btn, text="Calcular", command=self._run).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_btn, text="Graficar", command=self._plot).pack(side=tk.LEFT, padx=5)
        frm_btn.pack(pady=5)

        self.tree = ttk.Treeview(self, show="headings", height=12)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        self.var_res = tk.StringVar(value="Resultado: —")
        ttk.Label(self, textvariable=self.var_res).pack(anchor="w", pady=3)

        self.fig = None
        self.canvas = None

        self._render_params()

    def _clear_tree(self):
        for c in self.tree.get_children(): self.tree.delete(c)

    def _render_params(self):
        for w in self.params.winfo_children(): w.destroy()
        self.entries = {}
        dim = self.cb_dim.get()

        if dim == "1D":
            frm_fx = ttk.Frame(self.params)
            ttk.Label(frm_fx, text="f(x) = ").pack(side=tk.LEFT)
            e_fx = ttk.Entry(frm_fx, width=40); e_fx.insert(0, "sin(x)")
            ttk.Button(frm_fx, text="Teclado Funciones", command=lambda: open_function_keypad(self, e_fx, "Teclado - f(x)")).pack(side=tk.LEFT, padx=4)
            e_fx.pack(side=tk.LEFT, fill=tk.X, expand=True); frm_fx.pack(fill=tk.X, pady=2)

            frm_x0h = ttk.Frame(self.params)
            ttk.Label(frm_x0h, text="x0=").pack(side=tk.LEFT)
            e_x0 = ttk.Entry(frm_x0h, width=10); e_x0.insert(0, "1.0"); e_x0.pack(side=tk.LEFT)
            ttk.Label(frm_x0h, text="   h=").pack(side=tk.LEFT)
            e_h = ttk.Entry(frm_x0h, width=10); e_h.insert(0, "1e-3"); e_h.pack(side=tk.LEFT)
            frm_x0h.pack(anchor="w", pady=2)

            frm_esq = ttk.Frame(self.params)
            ttk.Label(frm_esq, text="Esquema:").pack(side=tk.LEFT)
            self.cb_esq = ttk.Combobox(frm_esq, state="readonly", values=[
                "Adelante O(h)", "Atrás O(h)", "Centrada O(h^2)", "Segunda derivada centrada O(h^2)"
            ])
            self.cb_esq.current(2); self.cb_esq.pack(side=tk.LEFT, padx=5)
            frm_esq.pack(anchor="w", pady=2)

            self.entries["fx"] = e_fx; self.entries["x0"] = e_x0; self.entries["h"] = e_h

            self._clear_tree()
            cols = ("derivada", "valor")
            self.tree["columns"] = cols
            for c in cols:
                self.tree.heading(c, text=c); self.tree.column(c, width=160, anchor="center")

        else:  # 2D
            frm_fxy = ttk.Frame(self.params)
            ttk.Label(frm_fxy, text="f(x,y) = ").pack(side=tk.LEFT)
            e_fxy = ttk.Entry(frm_fxy, width=60); e_fxy.insert(0, "sin(x*y) + x**2")
            e_fxy.pack(side=tk.LEFT, fill=tk.X, expand=True); frm_fxy.pack(fill=tk.X, pady=2)

            frm_xyh = ttk.Frame(self.params)
            ttk.Label(frm_xyh, text="x0=").pack(side=tk.LEFT)
            e_x0 = ttk.Entry(frm_xyh, width=10); e_x0.insert(0, "1.0"); e_x0.pack(side=tk.LEFT)
            ttk.Label(frm_xyh, text="   y0=").pack(side=tk.LEFT)
            e_y0 = ttk.Entry(frm_xyh, width=10); e_y0.insert(0, "2.0"); e_y0.pack(side=tk.LEFT)
            ttk.Label(frm_xyh, text="   hx=").pack(side=tk.LEFT)
            e_hx = ttk.Entry(frm_xyh, width=10); e_hx.insert(0, "1e-3"); e_hx.pack(side=tk.LEFT)
            ttk.Label(frm_xyh, text="   hy=").pack(side=tk.LEFT)
            e_hy = ttk.Entry(frm_xyh, width=10); e_hy.insert(0, "1e-3"); e_hy.pack(side=tk.LEFT)
            frm_xyh.pack(anchor="w", pady=2)

            frm_chk = ttk.Frame(self.params)
            self.var_fx = tk.BooleanVar(value=True)
            self.var_fy = tk.BooleanVar(value=True)
            self.var_fxx = tk.BooleanVar(value=True)
            self.var_fyy = tk.BooleanVar(value=False)
            self.var_fxy = tk.BooleanVar(value=True)
            ttk.Checkbutton(frm_chk, text="f_x", variable=self.var_fx).pack(side=tk.LEFT, padx=4)
            ttk.Checkbutton(frm_chk, text="f_y", variable=self.var_fy).pack(side=tk.LEFT, padx=4)
            ttk.Checkbutton(frm_chk, text="f_xx", variable=self.var_fxx).pack(side=tk.LEFT, padx=4)
            ttk.Checkbutton(frm_chk, text="f_yy", variable=self.var_fyy).pack(side=tk.LEFT, padx=4)
            ttk.Checkbutton(frm_chk, text="f_xy", variable=self.var_fxy).pack(side=tk.LEFT, padx=4)
            frm_chk.pack(anchor="w", pady=2)

            self.entries["fxy"] = e_fxy; self.entries["x0"] = e_x0; self.entries["y0"] = e_y0
            self.entries["hx"] = e_hx; self.entries["hy"] = e_hy

            self._clear_tree()
            cols = ("derivada", "valor")
            self.tree["columns"] = cols
            for c in cols:
                self.tree.heading(c, text=c); self.tree.column(c, width=160, anchor="center")

    def _run(self):
        dim = self.cb_dim.get()
        self._clear_tree()
        try:
            if dim == "1D":
                f = make_safe_func_1v(self.entries["fx"].get())
                x0 = parse_num(self.entries["x0"].get()); h = parse_num(self.entries["h"].get())
                esquema = self.cb_esq.get()
                if esquema == "Adelante O(h)":
                    val = fd_forward_1(f, x0, h); self.tree.insert("", tk.END, values=("f'(x0) adelante", f"{val:.8f}"))
                elif esquema == "Atrás O(h)":
                    val = fd_backward_1(f, x0, h); self.tree.insert("", tk.END, values=("f'(x0) atrás", f"{val:.8f}"))
                elif esquema == "Centrada O(h^2)":
                    val = fd_central_1(f, x0, h); self.tree.insert("", tk.END, values=("f'(x0) centrada", f"{val:.8f}"))
                elif esquema == "Segunda derivada centrada O(h^2)":
                    val = fd_central_2(f, x0, h); self.tree.insert("", tk.END, values=("f''(x0) centrada", f"{val:.8f}"))
                self.var_res.set("Cálculo 1D completado.")
            else:
                fxy = make_safe_func_2v(self.entries["fxy"].get())
                x0 = parse_num(self.entries["x0"].get()); y0 = parse_num(self.entries["y0"].get())
                hx = parse_num(self.entries["hx"].get()); hy = parse_num(self.entries["hy"].get())
                if self.var_fx.get():
                    val = fx_central(fxy, x0, y0, hx); self.tree.insert("", tk.END, values=("f_x", f"{val:.8f}"))
                if self.var_fy.get():
                    val = fy_central(fxy, x0, y0, hy); self.tree.insert("", tk.END, values=("f_y", f"{val:.8f}"))
                if self.var_fxx.get():
                    val = fxx_central(fxy, x0, y0, hx); self.tree.insert("", tk.END, values=("f_xx", f"{val:.8f}"))
                if self.var_fyy.get():
                    val = fyy_central(fxy, x0, y0, hy); self.tree.insert("", tk.END, values=("f_yy", f"{val:.8f}"))
                if self.var_fxy.get():
                    val = fxy_central(fxy, x0, y0, hx, hy); self.tree.insert("", tk.END, values=("f_xy", f"{val:.8f}"))
                self.var_res.set("Cálculo 2D completado.")
        except Exception as e:
            messagebox.showerror("Error", str(e)); return

    def _plot(self):
        if FigureCanvasTkAgg is None or plt is None:
            messagebox.showinfo("Gráfica", "matplotlib no disponible."); return
        dim = self.cb_dim.get()
        if dim == "1D":
            try:
                f = make_safe_func_1v(self.entries["fx"].get())
                x0 = parse_num(self.entries["x0"].get())
            except Exception as e:
                messagebox.showerror("Error", str(e)); return
            xs = np.linspace(x0 - 5, x0 + 5, 400)
            ys = np.array([f(x) for x in xs])
            if self.fig is None:
                self.fig = plt.Figure(figsize=(5, 3), dpi=100)
                self.ax = self.fig.add_subplot(111)
                self.canvas = FigureCanvasTkAgg(self.fig, master=self)
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.ax.clear()
            self.ax.axhline(0, lw=1)
            self.ax.plot(xs, ys)
            self.ax.scatter([x0], [f(x0)], marker='o')
            self.ax.set_title("f(x) alrededor de x0")
            self.ax.grid(True, ls=":")
            self.canvas.draw_idle()
        else:
            try:
                fxy = make_safe_func_2v(self.entries["fxy"].get())
                x0 = parse_num(self.entries["x0"].get()); y0 = parse_num(self.entries["y0"].get())
            except Exception as e:
                messagebox.showerror("Error", str(e)); return
            xs = np.linspace(x0 - 2, x0 + 2, 80)
            ys = np.linspace(y0 - 2, y0 + 2, 80)
            XX, YY = np.meshgrid(xs, ys)
            ZZ = fxy(XX, YY)
            if self.fig is None:
                self.fig = plt.Figure(figsize=(5, 3), dpi=100)
                self.ax = self.fig.add_subplot(111)
                self.canvas = FigureCanvasTkAgg(self.fig, master=self)
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.ax.clear()
            cs = self.ax.contourf(XX, YY, ZZ, levels=20)
            self.ax.set_title("f(x,y) alrededor de (x0,y0)")
            self.ax.grid(True, ls=":")
            self.canvas.draw_idle()


# ==========================
# App principal
# ==========================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador Unificado: Raíces, Integración, Lagrange y Dif. Finitas")
        self.geometry("980x720")
        try:
            self.style = ttk.Style(self)
            self.style.theme_use("clam")
        except Exception:
            pass

        top = ttk.Frame(self)
        ttk.Label(top, text="Módulo:").pack(side=tk.LEFT)
        self.cb_mod = ttk.Combobox(top, state="readonly",
                                   values=["Raíces", "Integración", "Interpolación (Lagrange)", "Dif. Finitas (1D/2D)"])
        ttk.Button(top, text="Abrir Monte Carlo", command=self._open_mc).pack(side=tk.LEFT, padx=8)
        self.cb_mod.current(0)
        self.cb_mod.pack(side=tk.LEFT, padx=5)
        self.cb_mod.bind("<<ComboboxSelected>>", lambda e: self._swap())
        top.pack(fill=tk.X, pady=8)

        self.container = ttk.Frame(self); self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {
            "Raíces": RootFrame(self.container),
            "Integración": IntegrationFrame(self.container),
            "Interpolación (Lagrange)": LagrangeFrame(self.container),
            "Dif. Finitas (1D/2D)": FiniteDiffFrame(self.container),
        }
        for f in self.frames.values(): f.pack_forget()
        self.frames["Raíces"].pack(fill=tk.BOTH, expand=True)

    def _open_mc(self):
        win = tk.Toplevel(self); win.title('Simulador Monte Carlo')
        MonteCarloSimulator(win)

    def _swap(self):
        sel = self.cb_mod.get()
        for name, frame in self.frames.items():
            frame.pack_forget()
        self.frames[sel].pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    App().mainloop()
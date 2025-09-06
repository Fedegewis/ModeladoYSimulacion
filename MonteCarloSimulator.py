# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy.polynomial.legendre import leggauss
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D  # necesario para gráficos 3D (incluso si no se usa explícitamente)

class MonteCarloSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Monte Carlo + Teclado Avanzado")
        self.root.geometry("1300x780")

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

        # Botones principales
        ttk.Button(frame_inputs, text="Simular (hit-or-miss)", command=self.simular).grid(row=0, column=11, padx=5)
        ttk.Button(frame_inputs, text="Método Promedio", command=self.ventana_metodo_promedio).grid(row=0, column=12, padx=5)
        ttk.Button(frame_inputs, text="Convergencia", command=self.ventana_convergencia).grid(row=0, column=13, padx=5)
        ttk.Button(frame_inputs, text="Análisis Estadístico", command=self.ventana_estadistica).grid(row=0, column=14, padx=5)
        ttk.Button(frame_inputs, text="Integrales Dobles", command=self.ventana_integrales_dobles).grid(row=0, column=15, padx=5)
        ttk.Button(frame_inputs, text="Integrales Triples", command=self.ventana_integrales_triples).grid(row=0, column=16, padx=5)
        ttk.Button(frame_inputs, text="Ayuda", command=self.mostrar_ayuda).grid(row=0, column=17, padx=5)

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

if __name__=="__main__":
    root = tk.Tk()
    app = MonteCarloSimulator(root)
    root.mainloop()

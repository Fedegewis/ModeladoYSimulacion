# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class RungeKuttaPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Runge-Kutta Profesional")
        self.root.geometry("1500x900")
        self.solution_expr = None
        self.show_rk4_table = tk.BooleanVar(value=False)

        # Variables
        self.func_str = tk.StringVar(value="t - y")
        self.t0 = tk.DoubleVar(value=0.0)
        self.y0 = tk.DoubleVar(value=1.0)
        self.t_end = tk.DoubleVar(value=5.0)
        self.h = tk.DoubleVar(value=0.1)
        self.method = tk.StringVar(value="RK4")

        self.create_widgets()

    def create_widgets(self):
        # --- Frame Entrada ---
        frame_in = tk.LabelFrame(self.root, text="Parámetros de Entrada", padx=5, pady=5)
        frame_in.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_in, text="f(t,y)=").grid(row=0,column=0)
        tk.Entry(frame_in,textvariable=self.func_str,width=15).grid(row=0,column=1)
        tk.Label(frame_in, text="t0").grid(row=0,column=2)
        tk.Entry(frame_in,textvariable=self.t0,width=6).grid(row=0,column=3)
        tk.Label(frame_in, text="y0").grid(row=0,column=4)
        tk.Entry(frame_in,textvariable=self.y0,width=6).grid(row=0,column=5)
        tk.Label(frame_in, text="t_end").grid(row=0,column=6)
        tk.Entry(frame_in,textvariable=self.t_end,width=6).grid(row=0,column=7)
        tk.Label(frame_in, text="h").grid(row=0,column=8)
        tk.Entry(frame_in,textvariable=self.h,width=6).grid(row=0,column=9)
        tk.Label(frame_in, text="Método").grid(row=0,column=10)
        ttk.Combobox(frame_in,textvariable=self.method, values=["Euler","Heun","Midpoint","RK2","Ralston","RK4"],width=10).grid(row=0,column=11)
        tk.Checkbutton(frame_in,text="Mostrar Pendientes RK4",variable=self.show_rk4_table).grid(row=0,column=12)

        tk.Button(frame_in,text="Calcular",bg="#4CAF50",fg="white",command=self.solve).grid(row=0,column=13,padx=3)
        tk.Button(frame_in,text="Ayuda",bg="#2196F3",fg="white",command=self.show_help).grid(row=0,column=14,padx=3)
        tk.Button(frame_in,text="Comparar Métodos",bg="#FF9800",fg="white",command=self.compare_methods).grid(row=0,column=15,padx=3)
        tk.Button(frame_in,text="Calcular Solución Analítica",bg="#9C27B0",fg="white",command=self.calc_analytical).grid(row=0,column=16,padx=3)
        tk.Button(frame_in,text="Graficar Todos los Métodos",bg="#FF5722",fg="white",command=self.compare_methods).grid(row=0,column=17,padx=3)
        tk.Button(frame_in,text="Tabla Comparativa",bg="#9E9E9E",fg="white",command=self.generate_comparative_table).grid(row=0,column=18,padx=3)

        # --- PanedWindow principal ---
        self.paned = tk.PanedWindow(self.root, orient="horizontal", sashrelief="sunken")
        self.paned.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Panel Tablas ---
        self.tab_frame = ttk.Notebook(self.paned)
        self.paned.add(self.tab_frame, stretch="always")

        # Tabla normal
        self.table_frame = tk.Frame(self.tab_frame)
        self.tab_frame.add(self.table_frame,text="Tabla Normal")
        self.table_scroll = ttk.Scrollbar(self.table_frame, orient="horizontal")
        self.table_scroll.pack(side="bottom",fill="x")
        self.table = ttk.Treeview(self.table_frame, columns=("n","t","y_num","y_exact","Error"),
                                  show="headings", height=12, xscrollcommand=self.table_scroll.set)
        self.table.pack(fill="both", expand=True)
        self.table_scroll.config(command=self.table.xview)
        headers = ["n","t","y_num","y_exact","Error"]
        for h in headers: self.table.heading(h,text=h); self.table.column(h,width=100,anchor="center")

        # Tabla Euler detallada
        self.euler_frame = tk.Frame(self.tab_frame)
        self.tab_frame.add(self.euler_frame,text="Euler Detallado")
        self.euler_scroll = ttk.Scrollbar(self.euler_frame, orient="horizontal")
        self.euler_scroll.pack(side="bottom",fill="x")
        self.euler_table = ttk.Treeview(self.euler_frame, show="headings", height=12, xscrollcommand=self.euler_scroll.set)
        self.euler_table.pack(fill="both", expand=True)
        self.euler_table.configure(xscrollcommand=self.euler_scroll.set)
        self.euler_scroll.config(command=self.euler_table.xview)

        # Tabla Heun detallada
        self.heun_frame = tk.Frame(self.tab_frame)
        self.tab_frame.add(self.heun_frame,text="Heun Detallado")
        self.heun_scroll = ttk.Scrollbar(self.heun_frame, orient="horizontal")
        self.heun_scroll.pack(side="bottom",fill="x")
        self.heun_table = ttk.Treeview(self.heun_frame, show="headings", height=12, xscrollcommand=self.heun_scroll.set)
        self.heun_table.pack(fill="both", expand=True)
        self.heun_table.configure(xscrollcommand=self.heun_scroll.set)
        self.heun_scroll.config(command=self.heun_table.xview)

        # Tabla comparativa
        self.comp_frame = tk.Frame(self.tab_frame)
        self.tab_frame.add(self.comp_frame,text="Tabla Comparativa")
        self.comp_scroll = ttk.Scrollbar(self.comp_frame, orient="horizontal")
        self.comp_scroll.pack(side="bottom",fill="x")
        self.comp_table = ttk.Treeview(self.comp_frame, show="headings", height=12, xscrollcommand=self.comp_scroll.set)
        self.comp_table.pack(fill="both", expand=True)
        self.comp_table.configure(xscrollcommand=self.comp_scroll.set)
        self.comp_scroll.config(command=self.comp_table.xview)

        # Tabla RK4 pendientes
        self.rk4_frame = tk.Frame(self.tab_frame)
        self.tab_frame.add(self.rk4_frame,text="Pendientes RK4")
        self.rk4_scroll = ttk.Scrollbar(self.rk4_frame, orient="horizontal")
        self.rk4_scroll.pack(side="bottom",fill="x")
        self.rk4_table = ttk.Treeview(self.rk4_frame, show="headings", height=12, xscrollcommand=self.rk4_scroll.set)
        self.rk4_table.pack(fill="both", expand=True)
        self.rk4_table.configure(xscrollcommand=self.rk4_scroll.set)
        self.rk4_scroll.config(command=self.rk4_table.xview)

        # --- Panel Gráfica ---
        self.plot_frame = tk.Frame(self.paned)
        self.paned.add(self.plot_frame, stretch="always")
        self.fig, self.ax = plt.subplots(figsize=(3,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(fill="both", expand=True)

        # --- Panel Solución Analítica con renderizado LaTeX ---
        self.analytic_frame = tk.LabelFrame(self.root, text="Solución Analítica (LaTeX)", padx=5, pady=5)
        self.analytic_frame.pack(fill="both", padx=10, pady=5)
        self.fig_analytic, self.ax_analytic = plt.subplots(figsize=(12,1.5))
        self.ax_analytic.axis("off")
        self.canvas_analytic = FigureCanvasTkAgg(self.fig_analytic, master=self.analytic_frame)
        self.canvas_analytic.get_tk_widget().pack(fill="both", expand=True)

    # --- Funciones ---
    def f(self,t,y):
        t_sym,y_sym = sp.symbols("t y")
        expr = sp.sympify(self.func_str.get())
        f_lamb = sp.lambdify((t_sym,y_sym),expr,"numpy")
        return f_lamb(t,y)

    def solve(self):
        self.table.delete(*self.table.get_children())
        t0, y0, t_end, h = self.t0.get(), self.y0.get(), self.t_end.get(), self.h.get()
        n_steps = int((t_end-t0)/h)
        t_values = [t0]; y_values = [y0]
        rk4_pendientes = []
        
        # Para tablas detalladas - SIEMPRE generar ambas
        euler_details = []
        heun_details = []

        # Generar tabla Euler detallada
        t_euler, y_euler = t0, y0
        for i in range(n_steps):
            yn = y_euler
            slope = self.f(t_euler, y_euler)
            y_next = y_euler + h*slope
            euler_details.append([i, f"{t_euler:.3f}", f"{yn:.6f}", f"{slope:.6f}", f"{y_next:.6f}"])
            y_euler = y_next
            t_euler += h

        # Generar tabla Heun detallada
        t_heun, y_heun = t0, y0
        for i in range(n_steps):
            yn = y_heun
            k1 = self.f(t_heun, y_heun)
            y_star = yn + h*k1
            k2 = self.f(t_heun+h, y_star)
            y_next = yn + h*(k1+k2)/2
            heun_details.append([i, f"{t_heun:.3f}", f"{yn:.6f}", f"{k1:.6f}", f"{y_star:.6f}", f"{k2:.6f}", f"{y_next:.6f}"])
            y_heun = y_next
            t_heun += h

        # Calcular con el método seleccionado para la tabla principal
        t,y = t0,y0
        for i in range(n_steps):
            if self.method.get()=="Euler": 
                y += h*self.f(t,y)
                
            elif self.method.get()=="Heun": 
                k1=self.f(t,y)
                k2=self.f(t+h,y+h*k1)
                y += h*(k1+k2)/2
                
            elif self.method.get()=="Midpoint": k1=self.f(t,y); k2=self.f(t+h/2,y+h*k1/2); y+=h*k2
            elif self.method.get()=="RK2": k1=self.f(t,y); k2=self.f(t+h/2,y+h*k1/2); y+=h*k2
            elif self.method.get()=="Ralston": k1=self.f(t,y); k2=self.f(t+3*h/4, y+3*h*k1/4); y+=h*(k1+k2/3)
            elif self.method.get()=="RK4":
                k1=self.f(t,y); k2=self.f(t+h/2, y+h*k1/2)
                k3=self.f(t+h/2, y+h*k2/2); k4=self.f(t+h, y+h*k3)
                y_next = y + (h/6)*(k1+2*k2+2*k3+k4)
                if self.show_rk4_table.get(): rk4_pendientes.append([i,t,y,k1,k2,k3,k4,y_next])
                y = y_next
            t+=h; t_values.append(t); y_values.append(y)

        # Tabla normal
        for i,(ti,yi) in enumerate(zip(t_values,y_values)):
            y_exact_str, err_str = "-", "-"
            if self.solution_expr is not None:
                try:
                    y_exact_val = float(self.solution_expr.subs("t",ti))
                    err_val = abs(yi-y_exact_val)
                    y_exact_str = f"{y_exact_val:.6f}"
                    err_str = f"{err_val:.6e}" if err_val<1e-6 else f"{err_val:.6f}"
                except: pass
            self.table.insert("", "end", values=(i,f"{ti:.3f}",f"{yi:.6f}",y_exact_str,err_str))

        # Tabla Euler detallada - SIEMPRE llenar
        self.euler_table.delete(*self.euler_table.get_children())
        cols = ["n", "t_n", "Y_n", "f(t_n,Y_n)", "Y_{n+1}"]
        self.euler_table["columns"] = cols
        for c in cols:
            self.euler_table.heading(c, text=c)
            self.euler_table.column(c, width=120, anchor="center")
        for row in euler_details:
            self.euler_table.insert("", "end", values=row)

        # Tabla Heun detallada - SIEMPRE llenar
        self.heun_table.delete(*self.heun_table.get_children())
        cols = ["n", "t_n", "Y_n", "k1", "Y*", "k2", "Y_{n+1}"]
        self.heun_table["columns"] = cols
        for c in cols:
            self.heun_table.heading(c, text=c)
            self.heun_table.column(c, width=120, anchor="center")
        for row in heun_details:
            self.heun_table.insert("", "end", values=row)

        # Tabla RK4 pendientes
        if self.show_rk4_table.get() and rk4_pendientes:
            self.rk4_table.delete(*self.rk4_table.get_children())
            cols = ["n","t_n","y_n","k1","k2","k3","k4","y_{n+1}"]
            self.rk4_table["columns"] = cols
            for c in cols:
                self.rk4_table.heading(c,text=c)
                self.rk4_table.column(c,width=100,anchor="center")
            for row in rk4_pendientes:
                self.rk4_table.insert("", "end", values=[f"{v:.6f}" if isinstance(v,float) else v for v in row])

        # Gráfica
        self.ax.clear()
        self.ax.plot(t_values,y_values,label=self.method.get(),marker="o",markersize=3)
        if self.solution_expr is not None:
            t_dense = np.linspace(t0,t_end,200)
            y_dense = [float(self.solution_expr.subs("t",tt)) for tt in t_dense]
            self.ax.plot(t_dense, y_dense, "k--", label="Exacta")
        self.ax.set_title("Solución Numérica vs Analítica")
        self.ax.set_xlabel("t")
        self.ax.set_ylabel("y(t)")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def calc_analytical(self):
        self.ax_analytic.clear()
        t_sym = sp.symbols("t")
        y_func = sp.Function("y")
        try:
            ode = sp.Eq(sp.Derivative(y_func(t_sym),t_sym), sp.sympify(self.func_str.get()).subs({"y":y_func(t_sym)}))
            sol = sp.dsolve(ode,ics={y_func(self.t0.get()):self.y0.get()})
            self.solution_expr = sol.rhs
            sol_latex = sp.latex(sol)
            self.ax_analytic.text(0.01,0.5,r"$"+sol_latex+"$",fontsize=16,verticalalignment="center",horizontalalignment="left")
        except:
            self.solution_expr = None
            self.ax_analytic.text(0.5,0.5,"No tiene solución analítica",fontsize=16,verticalalignment="center",horizontalalignment="center")
        self.ax_analytic.axis("off")
        self.canvas_analytic.draw()

    def show_help(self):
        help_text = """
Métodos disponibles:

1. Euler: y_{n+1} = y_n + h*f(t_n,y_n)
   - Y_n: valor actual
   - Y_{n+1}: siguiente valor

2. Heun (Euler Mejorado): Predictor-Corrector
   - Y_n: valor actual
   - Y*: valor predicho
   - Y_{n+1}: valor corregido

3. Midpoint: y_{n+1} = y_n + h*f(t_n + h/2, y_n + h*k1/2)
4. RK2: y_{n+1} = y_n + h*k2
5. Ralston: y_{n+1} = y_n + h*(k1 + k2/3)
6. RK4: y_{n+1} = y_n + h*(k1+2k2+2k3+k4)/6

Donde k1,k2,k3,k4 son pendientes intermedias.
"""
        messagebox.showinfo("Ayuda - Métodos Runge-Kutta", help_text)

    def compare_methods(self):
        methods = ["Euler","Heun","Midpoint","RK2","Ralston","RK4"]
        t0,y0,t_end,h = self.t0.get(),self.y0.get(),self.t_end.get(),self.h.get()
        self.ax.clear()
        for method in methods:
            t,y = t0,y0; t_vals=[t0]; y_vals=[y0]
            n_steps = int((t_end-t0)/h)
            for _ in range(n_steps):
                if method=="Euler": y+=h*self.f(t,y)
                elif method=="Heun": k1=self.f(t,y); k2=self.f(t+h,y+h*k1); y+=h*(k1+k2)/2
                elif method=="Midpoint": k1=self.f(t,y); k2=self.f(t+h/2,y+h*k1/2); y+=h*k2
                elif method=="RK2": k1=self.f(t,y); k2=self.f(t+h/2,y+h*k1/2); y+=h*k2
                elif method=="Ralston": k1=self.f(t,y); k2=self.f(t+3*h/4, y+3*h*k1/4); y+=h*(k1+k2/3)
                elif method=="RK4": k1=self.f(t,y); k2=self.f(t+h/2, y+h*k1/2); k3=self.f(t+h/2, y+h*k2/2); k4=self.f(t+h, y+h*k3); y+=h*(k1+2*k2+2*k3+k4)/6
                t+=h; t_vals.append(t); y_vals.append(y)
            self.ax.plot(t_vals,y_vals,label=method,marker="o",markersize=3)
        if self.solution_expr is not None:
            t_dense = np.linspace(t0,t_end,200)
            y_dense = [float(self.solution_expr.subs("t",tt)) for tt in t_dense]
            self.ax.plot(t_dense,y_dense,"k--",label="Exacta")
        self.ax.set_title("Soluciones Numéricas de Todos los Métodos")
        self.ax.set_xlabel("t")
        self.ax.set_ylabel("y(t)")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def generate_comparative_table(self):
        self.comp_table.delete(*self.comp_table.get_children())
        cols=["n","t","Euler","Error_Euler","Heun","Error_Heun","Midpoint","Error_Midpoint",
              "RK2","Error_RK2","Ralston","Error_Ralston","RK4","Error_RK4","Exacta"]
        self.comp_table["columns"]=cols
        for c in cols:
            self.comp_table.heading(c,text=c)
            self.comp_table.column(c,width=100,anchor="center")

        t0,y0,t_end,h=self.t0.get(),self.y0.get(),self.t_end.get(),self.h.get()
        n_steps=int((t_end-t0)/h)
        t_values=[t0 + i*h for i in range(n_steps+1)]
        exact_values=[float(self.solution_expr.subs("t",ti)) if self.solution_expr else "-" for ti in t_values]
        methods=["Euler","Heun","Midpoint","RK2","Ralston","RK4"]
        results={m:[] for m in methods}

        for method in methods:
            t,y=t0,y0
            ys=[y0]
            for _ in range(n_steps):
                if method=="Euler": y+=h*self.f(t,y)
                elif method=="Heun": k1=self.f(t,y); k2=self.f(t+h,y+h*k1); y+=h*(k1+k2)/2
                elif method=="Midpoint": k1=self.f(t,y); k2=self.f(t+h/2,y+h*k1/2); y+=h*k2
                elif method=="RK2": k1=self.f(t,y); k2=self.f(t+h/2,y+h*k1/2); y+=h*k2
                elif method=="Ralston": k1=self.f(t,y); k2=self.f(t+3*h/4, y+3*h*k1/4); y+=h*(k1+k2/3)
                elif method=="RK4": k1=self.f(t,y); k2=self.f(t+h/2,y+h*k1/2); k3=self.f(t+h/2,y+h*k2/2); k4=self.f(t+h,y+h*k3); y+=h*(k1+2*k2+2*k3+k4)/6
                t+=h; ys.append(y)
            results[method]=ys

        for i,ti in enumerate(t_values):
            row=[i,f"{ti:.3f}"]
            for m in methods:
                yi=results[m][i]
                row.append(f"{yi:.6f}")
                if exact_values[i]!="-":
                    err=abs(yi-exact_values[i])
                    row.append(f"{err:.6e}" if err<1e-6 else f"{err:.6f}")
                else:
                    row.append("-")
            row.append(f"{exact_values[i]}" if exact_values[i]!="- " else "-")
            self.comp_table.insert("", "end", values=row)

if __name__=="__main__":
    root = tk.Tk()
    app = RungeKuttaPro(root)
    root.mainloop()
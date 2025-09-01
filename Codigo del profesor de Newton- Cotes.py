# -*- coding: utf-8 -*-
"""
Simulador de Integración Numérica Final
- Métodos: Rectángulo Medio, Trapecio, Simpson 1/3, Simpson 3/8, Boole, Gauss-Legendre
- Tabla compacta, no redimensionable
- Teclado siempre visible
- Gráfica con nodos y opción de mostrar áreas
- Cálculo simbólico y error de truncamiento
- Entrada de constantes simbólicas pi y E
- Botón de ayuda con explicación de fórmulas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- FUNCIONES AUXILIARES ---------------- #
def f_expr(expr_str):
    x = sp.symbols('x')
    expr_str = expr_str.replace("^","**").replace("pi","sp.pi").replace("π","sp.pi").replace("E","sp.E")
    try:
        return sp.sympify(expr_str), x
    except:
        raise ValueError("Función inválida")

def f_num(expr_str):
    expr, x = f_expr(expr_str)
    return sp.lambdify(x, expr, 'numpy')

def valor_entry(s):
    # Convierte a float, admite pi y E
    s = s.replace("pi","np.pi").replace("π","np.pi").replace("E","np.e")
    return float(eval(s))

# ---------------- MÉTODOS DE INTEGRACIÓN ---------------- #
def regla_rectangulo_medio(f,a,b,n):
    h=(b-a)/n
    xi=a+h/2+np.arange(n)*h
    I=h*np.sum(f(xi))
    tabla=[(i, xi[i], f(xi[i]), "") for i in range(n)]   # i desde 0
    return I,tabla,xi

def regla_trapecio(f,a,b,n):
    h=(b-a)/n
    x=np.linspace(a,b,n+1)
    I=h*(0.5*f(x[0])+np.sum(f(x[1:-1]))+0.5*f(x[-1]))
    tabla=[(i, x[i], f(x[i]), "") for i in range(n+1)]   # i desde 0
    return I,tabla,x

def regla_simpson13(f,a,b,n):
    if n%2!=0: n+=1
    h=(b-a)/n
    x=np.linspace(a,b,n+1)
    I=h/3*(f(x[0])+2*np.sum(f(x[2:-1:2]))+4*np.sum(f(x[1::2]))+f(x[-1]))
    tabla=[(i, x[i], f(x[i]), "") for i in range(n+1)]   # i desde 0
    return I,tabla,x

def regla_simpson38(f,a,b,n):
    if n%3!=0: n+=(3-n%3)
    h=(b-a)/n
    x=np.linspace(a,b,n+1)
    s=f(x[0])+f(x[-1])+3*np.sum(f(x[1:-1][np.arange(1,n)%3!=0]))+2*np.sum(f(x[3:-1:3]))
    I=3*h/8*s
    tabla=[(i, x[i], f(x[i]), "") for i in range(n+1)]   # i desde 0
    return I,tabla,x

def regla_boole(f,a,b,n):
    if n%4!=0: n+=(4-n%4)
    h=(b-a)/n
    x=np.linspace(a,b,n+1)
    s=7*(f(x[0])+f(x[-1])) + 32*np.sum(f(x[1:-1:2])) + 12*np.sum(f(x[2:-2:4])) + 14*np.sum(f(x[4:-1:4]))
    I=2*h/45*s
    tabla=[(i, x[i], f(x[i]), "") for i in range(n+1)]   # i desde 0
    return I,tabla,x

def cuadratura_gauss(f,a,b,n):
    xk,wk=np.polynomial.legendre.leggauss(n)
    x_mapped=0.5*(b-a)*xk + 0.5*(a+b)
    fx=f(x_mapped)
    I=0.5*(b-a)*np.dot(wk,fx)
    tabla=[(i, x_mapped[i], fx[i], wk[i]) for i in range(n)]   # i desde 0
    return I,tabla,x_mapped

# ---------------- ERROR DE TRUNCAMIENTO ---------------- #
def error_truncamiento(expr_str, regla, a, b, n):
    x=sp.symbols('x')
    expr,_=f_expr(expr_str)
    orden={"Trapecio":2,"Simpson 1/3":4,"Simpson 3/8":4,"Boole":6,"Rectángulo Medio":2}
    if regla not in orden: return "No disponible", None
    deriv=sp.diff(expr,x,orden[regla])
    deriv_max=sp.lambdify(x,sp.Abs(deriv),"numpy")
    xs=np.linspace(a,b,200)
    M=np.max(deriv_max(xs))
    h=(b-a)/n
    if regla=="Trapecio": return "-(b-a)/12*h²*f''(ξ)", -((b-a)/12)*h**2*M
    elif regla=="Simpson 1/3": return "-(b-a)/180*h⁴*f''''(ξ)", -((b-a)/180)*h**4*M
    elif regla=="Simpson 3/8": return "-(b-a)/80*h⁴*f''''(ξ)", -((b-a)/80)*h**4*M
    elif regla=="Boole": return "-(b-a)/9450*h⁶*f⁶(ξ)", -((b-a)/9450)*h**6*M
    elif regla=="Rectángulo Medio": return "-(b-a)/24*h²*f''(ξ)", -((b-a)/24)*h**2*M
    else: return "No disponible", None

# ---------------- INTERFAZ ---------------- #
class Simulador:
    def __init__(self,root):
        self.root=root
        self.root.title("Simulador Integración Numérica Final")
        self.root.geometry("1150x650")

        panel_left=ttk.Frame(root,padding=10)
        panel_left.pack(side="left",fill="y")

        # Entradas
        ttk.Label(panel_left,text="f(x):").grid(row=0,column=0)
        self.funcion_entry=ttk.Entry(panel_left,width=25); self.funcion_entry.grid(row=0,column=1); self.funcion_entry.insert(0,"sin(x)")

        ttk.Label(panel_left,text="a:").grid(row=1,column=0)
        self.a_entry=ttk.Entry(panel_left,width=10); self.a_entry.grid(row=1,column=1); self.a_entry.insert(0,"0")
        ttk.Label(panel_left,text="b:").grid(row=2,column=0)
        self.b_entry=ttk.Entry(panel_left,width=10); self.b_entry.grid(row=2,column=1); self.b_entry.insert(0,"pi")
        ttk.Label(panel_left,text="n:").grid(row=3,column=0)
        self.n_entry=ttk.Entry(panel_left,width=10); self.n_entry.grid(row=3,column=1); self.n_entry.insert(0,"5")

        ttk.Label(panel_left,text="Método:").grid(row=4,column=0)
        self.metodo_combo=ttk.Combobox(panel_left,values=["Rectángulo Medio","Trapecio","Simpson 1/3","Simpson 3/8","Boole","Gauss-Legendre"])
        self.metodo_combo.grid(row=4,column=1)
        self.metodo_combo.current(0)

        ttk.Button(panel_left,text="Calcular",command=self.calcular).grid(row=5,column=0,columnspan=2,pady=5)
        ttk.Button(panel_left,text="Graficar",command=self.graficar).grid(row=6,column=0,columnspan=2,pady=5)
        self.show_area_var=tk.IntVar()
        ttk.Checkbutton(panel_left,text="Mostrar áreas",variable=self.show_area_var,command=self.graficar).grid(row=7,column=0,columnspan=2)
        ttk.Button(panel_left,text="Ayuda",command=self.mostrar_ayuda).grid(row=8,column=0,columnspan=2,pady=5)

        # Teclado
        teclado_frame=ttk.LabelFrame(panel_left,text="Teclado")
        teclado_frame.grid(row=9,column=0,columnspan=2,pady=5)
        botones=["sin","cos","tan","exp","log","sqrt","pi","E","^","(",")","x"]
        for i,b in enumerate(botones):
            ttk.Button(teclado_frame,text=b,command=lambda b=b:self.insertar(b)).grid(row=i//3,column=i%3,padx=2,pady=2)

        # PANEL DERECHO
        panel_right=ttk.Frame(root)
        panel_right.pack(side="right",fill="both",expand=True)

        self.result_label=ttk.Label(panel_right,text="Resultado: "); self.result_label.pack(anchor="w")
        self.simbol_label=ttk.Label(panel_right,text="Integral simbólica: "); self.simbol_label.pack(anchor="w")
        self.error_label=ttk.Label(panel_right,text="Error: "); self.error_label.pack(anchor="w")

        # Tabla compacta y fija
        self.tree=ttk.Treeview(panel_right,columns=("i","x","f(x)","w"),show="headings",height=12)
        for c,t in zip(("i","x","f(x)","w"),("i","x","f(x)","Peso w_i")):
            self.tree.heading(c,text=t)
            self.tree.column(c,width=90,anchor="center")
        self.tree.pack(fill="x",pady=5)

        # Gráfica
        self.fig, self.ax=plt.subplots(figsize=(6,4))
        self.canvas=FigureCanvasTkAgg(self.fig,panel_right)
        self.canvas.get_tk_widget().pack(fill="both",expand=True)

    def insertar(self,texto):
        self.funcion_entry.insert(tk.END,texto)

    def mostrar_ayuda(self):
        ayuda_win=tk.Toplevel(self.root)
        ayuda_win.title("Ayuda: Métodos de Integración")
        ayuda_win.geometry("500x400")
        texto=("Métodos disponibles:\n\n"
               "Rectángulo Medio:\n  I ≈ h * Σ f(x_i*), h=(b-a)/n, x_i* = centro de subintervalo\n\n"
               "Trapecio:\n  I ≈ h*(f(x0)/2 + Σ f(xi) + f(xn)/2), h=(b-a)/n\n\n"
               "Simpson 1/3:\n  I ≈ h/3*(f0 + 4f1 + 2f2 + 4f3 + ... + fn), n par\n\n"
               "Simpson 3/8:\n  I ≈ 3h/8*(f0 + 3f1 + 3f2 + 2f3 + ... + fn), n múltiplo de 3\n\n"
               "Boole:\n  I ≈ 2h/45*(7f0 + 32f1 + 12f2 + 32f3 + 14f4 + ... + 7fn), n múltiplo de 4\n\n"
               "Gauss-Legendre:\n  I ≈ Σ w_i * f(x_i), x_i y w_i son los nodos y pesos de Gauss\n\n"
               "Nota: puede ingresar 'pi' o 'π' como valor de a o b.")
        label=ttk.Label(ayuda_win,text=texto,justify="left")
        label.pack(padx=10,pady=10)

    def calcular(self):
        try:
            f=f_num(self.funcion_entry.get())
            a=valor_entry(self.a_entry.get())
            b=valor_entry(self.b_entry.get())
            n=int(self.n_entry.get())
            metodo=self.metodo_combo.get()

            if metodo=="Rectángulo Medio": I,tabla,xs=regla_rectangulo_medio(f,a,b,n); regla="Rectángulo Medio"
            elif metodo=="Trapecio": I,tabla,xs=regla_trapecio(f,a,b,n); regla="Trapecio"
            elif metodo=="Simpson 1/3": I,tabla,xs=regla_simpson13(f,a,b,n); regla="Simpson 1/3"
            elif metodo=="Simpson 3/8": I,tabla,xs=regla_simpson38(f,a,b,n); regla="Simpson 3/8"
            elif metodo=="Boole": I,tabla,xs=regla_boole(f,a,b,n); regla="Boole"
            elif metodo=="Gauss-Legendre": I,tabla,xs=cuadratura_gauss(f,a,b,n); regla="Gauss"
            else: raise ValueError("Método no válido")

            expr,_=f_expr(self.funcion_entry.get())
            integral_simbol=sp.integrate(expr,(sp.symbols('x'),a,b))
            self.simbol_label.config(text=f"Integral simbólica: {integral_simbol}")

            formula,err=error_truncamiento(self.funcion_entry.get(),regla,a,b,n)
            self.result_label.config(text=f"Resultado numérico: {I:.6f}")
            if err is not None: self.error_label.config(text=f"Error: {formula}, Valor ≈ {err:.6e}")
            else: self.error_label.config(text="Error: No disponible")

            for row in self.tree.get_children(): self.tree.delete(row)
            for t in tabla: 
                self.tree.insert("", "end", values=(t[0], f"{t[1]:.6f}", f"{t[2]:.6f}", f"{t[3]}" if t[3]!="" else ""))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def graficar(self):
        try:
            self.ax.clear()
            f=f_num(self.funcion_entry.get())
            a=valor_entry(self.a_entry.get())
            b=valor_entry(self.b_entry.get())
            n=int(self.n_entry.get())
            xs_plot=np.linspace(a,b,400)
            ys_plot=f(xs_plot)
            self.ax.plot(xs_plot,ys_plot,label="f(x)",color="blue")
            self.ax.axhline(0,color="black")
            self.ax.axvline(0,color="black")
            self.ax.grid(True)
            self.ax.legend()
            self.ax.set_title("Gráfico de f(x) con nodos y áreas")

            metodo=self.metodo_combo.get()
            if metodo=="Rectángulo Medio":
                xi=a+(b-a)/(2*n)+np.arange(n)*(b-a)/n
            elif metodo in ["Trapecio","Simpson 1/3","Simpson 3/8","Boole"]:
                xi=np.linspace(a,b,n+1)
            elif metodo=="Gauss-Legendre":
                xi,_=cuadratura_gauss(f,a,b,n)[2],None
            self.ax.scatter(xi,f(xi),color="red",zorder=5,label="Nodos")

            if self.show_area_var.get() and metodo!="Gauss-Legendre":
                h=(b-a)/n
                for i in range(len(xi)-1):
                    x_fill=np.linspace(xi[i],xi[i+1],20)
                    y_fill=f(x_fill)
                    color="orange"
                    if metodo=="Trapecio": color="orange"
                    elif metodo=="Simpson 1/3": color="green"
                    elif metodo=="Simpson 3/8": color="purple"
                    elif metodo=="Boole": color="pink"
                    elif metodo=="Rectángulo Medio":
                        x_fill=[xi[i]-h/2,xi[i]+h/2]
                        y_fill=[f(xi[i]),f(xi[i])]
                    self.ax.fill_between(x_fill,0,y_fill,color=color,alpha=0.3)

            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__=="__main__":
    root=tk.Tk()
    app=Simulador(root)
    root.mainloop()



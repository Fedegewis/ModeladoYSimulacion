import ast
import math
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
except Exception:
    FigureCanvasTkAgg = None
    plt = None


def _make_safe_func(expr: str) -> Callable[[float], float]:
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed_names.update({"abs": abs, "pow": pow})
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


def numerical_derivative(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)


def newton_raphson(f: Callable[[float], float], x0: float, df: Optional[Callable[[float], float]] = None,
                   tol: float = 1e-8, max_iter: int = 50):
    history = []
    x = x0
    for n in range(max_iter):
        fx = f(x)
        dfx = df(x) if df is not None else numerical_derivative(f, x)
        if abs(dfx) < 1e-14:
            raise RuntimeError("Derivada cerca de cero; Newton puede fallar")
        x_next = x - fx / dfx
        abs_err = abs(x_next - x)
        rel_err = abs_err / abs(x_next) if x_next != 0 else float('inf')
        history.append((n, x, fx, dfx, abs_err, rel_err))
        if abs_err < tol:
            history.append((n + 1, x_next, f(x_next),
                            df(x_next) if df else numerical_derivative(f, x_next), 0.0, 0.0))
            return x_next, history
        x = x_next
    return None, history


def punto_fijo(g: Callable[[float], float], x0: float, tol: float = 1e-8, max_iter: int = 50):
    history = []
    x = x0
    for n in range(max_iter):
        x_next = g(x)
        abs_err = abs(x_next - x)
        rel_err = abs_err / abs(x_next) if x_next != 0 else float('inf')
        history.append((n, x, x_next, abs_err, rel_err))
        if abs_err < tol:
            history.append((n + 1, x_next, g(x_next), 0.0, 0.0))
            return x_next, history
        x = x_next
    return None, history


def punto_fijo_aitken(g: Callable[[float], float], x0: float, tol: float = 1e-8, max_iter: int = 50):
    history = []
    x = x0
    for n in range(max_iter):
        x1 = g(x)
        x2 = g(x1)
        denom = x2 - 2 * x1 + x
        if denom != 0:
            x_acc = x2 - (x2 - x1) ** 2 / denom
        else:
            x_acc = x2
        abs_err = abs(x_acc - x)
        rel_err = abs_err / abs(x_acc) if x_acc != 0 else float('inf')
        history.append((n, x, x_acc, abs_err, rel_err))
        if abs_err < tol:
            return x_acc, history
        x = x_acc
    return None, history


class RaicesGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Métodos Numéricos - Raíces")
        self._build_widgets()

    def _build_widgets(self):
        frm = ttk.Frame(self.master, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')

        # f(x) y g(x)
        ttk.Label(frm, text="f(x):").grid(row=0, column=0, sticky='w')
        self.expr_var = tk.StringVar(value="x**2 - 2")
        ttk.Entry(frm, textvariable=self.expr_var, width=40).grid(row=0, column=1, columnspan=2, sticky='we')

        ttk.Label(frm, text="g(x) (Punto Fijo):").grid(row=1, column=0, sticky='w')
        self.gexpr_var = tk.StringVar(value="(x + 2/x)/2")
        ttk.Entry(frm, textvariable=self.gexpr_var, width=40).grid(row=1, column=1, columnspan=2, sticky='we')

        # Derivada opcional
        ttk.Label(frm, text="f'(x) (opcional):").grid(row=2, column=0, sticky='w')
        self.dexpr_var = tk.StringVar(value="")
        ttk.Entry(frm, textvariable=self.dexpr_var, width=40).grid(row=2, column=1, columnspan=2, sticky='we')

        # Parámetros
        ttk.Label(frm, text="x0:").grid(row=3, column=0)
        self.x0_var = tk.StringVar(value="1.5")
        ttk.Entry(frm, textvariable=self.x0_var, width=10).grid(row=3, column=1)

        ttk.Label(frm, text="tol:").grid(row=3, column=2)
        self.tol_var = tk.StringVar(value="1e-8")
        ttk.Entry(frm, textvariable=self.tol_var, width=10).grid(row=3, column=3)

        ttk.Label(frm, text="max iter:").grid(row=3, column=4)
        self.max_var = tk.StringVar(value="50")
        ttk.Entry(frm, textvariable=self.max_var, width=10).grid(row=3, column=5)

        # Botones
        ttk.Button(frm, text="Newton", command=self.run_newton).grid(row=4, column=0)
        ttk.Button(frm, text="Punto Fijo", command=self.run_punto_fijo).grid(row=4, column=1)
        ttk.Button(frm, text="Punto Fijo + Aitken", command=self.run_aitken).grid(row=4, column=2)
        ttk.Button(frm, text="Limpiar", command=self.clear_all).grid(row=4, column=3)  # Nuevo botón

        # Tabla
        cols = ("n", "x_n", "aprox", "err_abs", "err_rel")
        self.tree = ttk.Treeview(frm, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, anchor='center')
        self.tree.grid(row=5, column=0, columnspan=6, pady=10)

        self.result_var = tk.StringVar(value="Resultado: -")
        ttk.Label(frm, textvariable=self.result_var).grid(row=6, column=0, columnspan=6, sticky='w')

        if FigureCanvasTkAgg and plt:
            self.fig, self.ax = plt.subplots(figsize=(5, 3))
            self.canvas = FigureCanvasTkAgg(self.fig, master=frm)
            self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=6)
        else:
            self.canvas = None
            self.ax = None
            ttk.Label(frm, text="matplotlib no disponible").grid(row=7, column=0, columnspan=6)

    def _populate_table(self, history):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for rec in history:
            self.tree.insert('', 'end', values=tuple(f"{v:.6g}" if isinstance(v, float) else v for v in rec))

    def _plot(self, history, func):
        if not history:
            return
        xs_plot = [h[1] for h in history if isinstance(h[1], float)]
        if not xs_plot:
            return
        xmin, xmax = min(xs_plot) - 1, max(xs_plot) + 1
        X = [xmin + i*(xmax-xmin)/400 for i in range(401)]
        Y = [func(x) for x in X]
        self.ax.clear()
        self.ax.plot(X, Y, label='Función')
        self.ax.axhline(0, color='k', ls='--')
        self.ax.plot(xs_plot, [func(x) for x in xs_plot], 'o-', label='Iteraciones')
        self.ax.legend()
        self.canvas.draw()

    def clear_all(self):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Reiniciar resultado
        self.result_var.set("Resultado: -")
        # Limpiar gráfico
        if self.ax and self.canvas:
            self.ax.clear()
            self.canvas.draw()

    def run_newton(self):
        try:
            f = _make_safe_func(self.expr_var.get())
            df = _make_safe_func(self.dexpr_var.get()) if self.dexpr_var.get() else None
            x0 = float(self.x0_var.get())
            tol = float(self.tol_var.get())
            max_iter = int(self.max_var.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        root, hist = newton_raphson(f, x0, df, tol, max_iter)
        self._populate_table(hist)
        self.result_var.set(f"Resultado: {root}" if root else "No convergió")
        if FigureCanvasTkAgg and plt:
            self._plot(hist, f)

    def run_punto_fijo(self):
        try:
            g = _make_safe_func(self.gexpr_var.get())
            x0 = float(self.x0_var.get())
            tol = float(self.tol_var.get())
            max_iter = int(self.max_var.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        root, hist = punto_fijo(g, x0, tol, max_iter)
        self._populate_table(hist)
        self.result_var.set(f"Resultado: {root}" if root else "No convergió")

    def run_aitken(self):
        try:
            g = _make_safe_func(self.gexpr_var.get())
            x0 = float(self.x0_var.get())
            tol = float(self.tol_var.get())
            max_iter = int(self.max_var.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        root, hist = punto_fijo_aitken(g, x0, tol, max_iter)
        self._populate_table(hist)
        self.result_var.set(f"Resultado (Aitken): {root}" if root else "No convergió")


def main():
    root = tk.Tk()
    RaicesGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

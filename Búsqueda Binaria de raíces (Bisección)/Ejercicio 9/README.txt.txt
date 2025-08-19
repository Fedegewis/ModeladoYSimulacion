

# 1) Planteo

La iteración de punto fijo es $x = g(x)$ con

$$
g(x)=\frac{5}{x^{2}}+2 .
$$

Derivada:

$$
g'(x) = -\frac{10}{x^{3}},\qquad |g'(x)|=\frac{10}{|x|^{3}}.
$$

Para que la iteración converja por el teorema del punto fijo en un intervalo $[a,b]$ necesitamos dos cosas:

1. $g([a,b])\subset [a,b]$ (la función lleva el intervalo en sí mismo).
2. Existe $k<1$ tal que $\max_{x\in[a,b]}|g'(x)|\le k$.

Como $|g'(x)|=10/x^{3}$ en $x>0$, la condición $|g'(x)|<1$ da

$$
x^{3}>10\quad\Rightarrow\quad x> \sqrt[3]{10}\approx 2.1544.
$$

Nuestro punto fijo real (solución de $x = 5/x^2 + 2$) es aproximadamente $2.690647448$ (un único fijo real positivo).

# 2) Elegir un intervalo que funcione

Elegimos por ejemplo $[a,b]=[2.3,\,3]$.

Comprobaciones:

* Para $x\in[2.3,3]$: $\max |g'(x)|$ ocurre en $x=a=2.3$:

  $$
  k=\frac{10}{2.3^{3}}\approx 0.8219<1.
  $$
* $g$ es decreciente en $x>0$. Calculamos los extremos:

  * $g(2.3)=\dfrac{5}{2.3^2}+2\approx 2.945\le 3$.
  * $g(3)=\dfrac{5}{9}+2\approx 2.555\ge 2.3$.
    Por tanto $g([2.3,3])\subset[2.3,3]$.

Entonces $[2.3,3]$ cumple las hipótesis del teorema del punto fijo y la iteración converge a la solución con tasa de contracción $k\approx0.8219$.

# 3) Cota teórica de iteraciones (opcional)

Usando la cota de contracción,

$$
|x_n - p| \le \frac{k^n}{1-k}\,|x_1-x_0|.
$$

Si tomas $x_0=3$, $x_1=g(3)$ y la tolerancia $10^{-3}$, la cota teórica da que podrían necesitarse hasta \~40 iteraciones en el peor caso. En la práctica suele converger antes.


# 5) Resultado numérico (si lo corres ahora)

Si ejecutás el código obtendrás la convergencia al punto fijo aproximadamente:

$$
x \approx 2.690647448\ \text{(aprox.)}
$$

y el número real de iteraciones dependerá de la tolerancia; con tol $=10^{-3}$ normalmente converge en pocas decenas de pasos (mucho menos que la cota teórica de 40 en la práctica).

---

Si querés, lo corro yo aquí y te muestro la salida exacta, o te doy otra opción de intervalo (por ejemplo $[2.25,3]$ también funciona) o cambio el criterio de parada (por ejemplo usar $|x_{n+1}-x_n|<\text{tol}$ o $|g(x_n)-x_n|<\text{tol}$). ¿Querés que lo ejecute y te pegue la salida?

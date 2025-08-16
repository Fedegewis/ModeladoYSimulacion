¿Qué hace el código y cómo calcula cada valor?
🔍 1. BÚSQUEDA DE INTERVALOS (buscar_intervalos_con_raices)
python# Para f(x) = e^x - 2 - x, evalúa:
f(-3) = e^(-3) - 2 - (-3) = 0.05 + 1 = 1.05      (positivo)
f(-2) = e^(-2) - 2 - (-2) = 0.14 + 0 = 0.14      (positivo) 
f(-1) = e^(-1) - 2 - (-1) = 0.37 - 1 = -0.63     (negativo)
# ¡Cambio de signo entre -2 y -1! → Hay una raíz en [-2,-1]
Aplica el Teorema de Bolzano: Si f(a) y f(b) tienen signos opuestos, existe al menos una raíz en [a,b].
📊 2. MÉTODO DE BISECCIÓN (biseccion)
Ejemplo paso a paso para intervalo [-2, -1]:
| Iteración | a    | b    | c = (a+b)/2 | f(c)   | Error = |b-a|/2 | Acción |
|-----------|------|------|-------------|--------|---------------|---------|
| 1         | -2   | -1   | -1.5        | -0.276 | 0.5          | b = c   |
| 2         | -2   | -1.5 | -1.75       | -0.067 | 0.25         | b = c   |
| 3         | -2   | -1.75| -1.875      | 0.037  | 0.125        | a = c   |
| 4         | -1.875| -1.75| -1.8125     | -0.015 | 0.0625       | b = c   |
Proceso en cada iteración:

Calcula punto medio: c = (a + b) / 2
Evalúa función: f(c)
Calcula error: |b - a| / 2
Decide nuevo intervalo:

Si f(a) × f(c) < 0 → raíz en [a,c] → b = c
Si no → raíz en [c,b] → a = c


Repite hasta que |f(c)| < tolerancia o error < tolerancia

📈 3. GRAFICACIÓN (graficar_multiples_raices)

Crea 1000 puntos en el rango [-3, 3]
Evalúa f(x) para cada punto
Dibuja la curva en azul
Marca cada raíz con un círculo de color diferente
Sombrea intervalos donde se buscó cada raíz

🎯 4. RESULTADOS ESPERADOS:
a) f(x) = e^x - 2 - x: 2 raíces

Raíz 1: x ≈ -1.841 (intervalo [-2,-1])
Raíz 2: x ≈ 1.146 (intervalo [1,2])

b) f(x) = cos(x) + x: 1 raíz

Raíz: x ≈ -0.739 (intervalo [-1,0])

c) f(x) = ln(x) - 5 - x: 1 raíz

Raíz: x ≈ 3.594 (intervalo [3,4])

d) f(x) = x² - 10x + 23: 2 raíces

Raíz 1: x ≈ 3.764 (intervalo [3,4])
Raíz 2: x ≈ 6.236 (intervalo [6,7])

El código ejecuta automáticamente los 4 ejercicios en orden y muestra todos los cálculos paso a paso.
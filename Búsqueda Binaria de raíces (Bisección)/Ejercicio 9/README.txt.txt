

1. ¿Qué es una iteración de punto fijo?

Tenemos una función g(x) = x²/2 + 2
Buscamos un valor x* tal que x* = g(x*) (punto fijo)
El método iterativo es: x_{n+1} = g(x_n)

2. Condición teórica de convergencia
Para que la iteración converja, necesitamos:

|g'(x)| < 1 en todo el intervalo [a,b]
En nuestro caso: g'(x) = x
Por tanto: |x| < 1, es decir, x ∈ (-1, 1)

3. Análisis matemático

Puntos fijos: Resolvemos x = x²/2 + 2
Reordenando: x² - 2x + 4 = 0
Discriminante: Δ = 4 - 16 = -12 < 0
Resultado: No hay puntos fijos reales (solo complejos: 1 ± i√3)

4. Respuesta al ejercicio

Intervalo de convergencia teórica: [-1, 1]
Exactitud: 10⁻¹³
Paradoja: Aunque la iteración es contractiva en [-1, 1], no converge porque no existe punto fijo real

5. ¿Por qué es importante esto?

Demuestra que la condición |g'(x)| < 1 es necesaria pero no suficiente
También necesitamos que exista un punto fijo real
En aplicaciones prácticas, siempre verificar ambas condiciones



Explicación del error:

La función g(x) = x²/2 + 2 hace que los valores crezcan exponencialmente

Si empezamos con x₀ = 3:
x₁ = g(3) = 9/2 + 2 = 6.5
x₂ = g(6.5) = 42.25/2 + 2 = 23.125
x₃ = g(23.125) ≈ 267.06...
En pocas iteraciones, el número se vuelve enorme


Por eso la condición |g'(x)| < 1 es crucial:

Cuando |g'(x)| ≥ 1, la función es "expansiva"
Los valores se alejan del punto fijo en lugar de acercarse
Eventualmente causan overflow



Lo que demuestra el código corregido:

Intervalo [-1, 1]: Aquí |g'(x)| = |x| < 1, pero aún diverge porque no hay punto fijo real
Fuera de [-1, 1]: Los valores explotan rápidamente (overflow)

Conceptos importantes:

Convergencia teórica ≠ convergencia práctica
La condición |g'(x)| < 1 es necesaria pero no suficiente
También necesitamos que exista un punto fijo real

Ejecuta el código corregido - ahora maneja los overflows y te mostrará claramente:

Dónde diverge por overflow (fuera de [-1,1])
Dónde diverge pero de forma controlada (dentro de [-1,1])
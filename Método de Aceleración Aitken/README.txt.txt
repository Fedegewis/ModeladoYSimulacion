Explicación detallada de cada ejercicio:
¿Qué es el Método de Aceleración de Aitken?
Es una técnica que mejora la velocidad de convergencia de secuencias que convergen linealmente. La fórmula es:
x̂ = x₁ - (x₂ - x₁)² / (x₃ - 2x₂ + x₁)
Donde x₁, x₂, x₃ son tres iteraciones consecutivas del método de punto fijo.
Análisis de cada ejercicio:
Ejercicio 1: f(x) = π/2 x² - x - 2

Convertimos a punto fijo: g(x) = π/2 x² - 2
Este es un caso donde el método puede diverger si |g'(x)| > 1

Ejercicio 2: f(x) = cos(x) - x

Punto fijo: g(x) = cos(x)
Es el clásico ejemplo, converge muy bien porque |cos'(x)| = |sin(x)| < 1

Ejercicio 3: g(x) = ∛(3x² - 4x + 1)

Función cúbica, necesitamos que el argumento sea positivo
La convergencia depende de la derivada en el punto fijo

Ejercicio 4: g(x) = e^(-x)

Función exponencial decreciente
Converge bien porque la derivada es siempre negativa y menor que 1 en valor absoluto

Ejercicio 5: g(x) = √(3x - 2)

Requiere que 3x - 2 ≥ 0, es decir x ≥ 2/3
Con x₀ = 2, está en el dominio válido

Ejercicios 6-11: Siguen patrones similares, cada uno con sus propias consideraciones de dominio y convergencia.
Ventajas del Método de Aitken:

Acelera la convergencia: Convierte convergencia lineal en casi cuadrática
No requiere derivadas: Solo necesita evaluaciones de la función
Mejora automáticamente: Funciona con cualquier secuencia convergente

Limitaciones:

Puede ser inestable: Si el denominador es muy pequeño
No garantiza convergencia: Si el método base no converge, Aitken tampoco
Requiere más evaluaciones: Necesita 3 iteraciones por cada mejora
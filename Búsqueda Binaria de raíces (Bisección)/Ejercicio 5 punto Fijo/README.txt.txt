Te explico paso a paso el Método del Punto Fijo y cómo resolví cada ejercicio:
¿Qué es el Método del Punto Fijo?
El método del punto fijo es una técnica iterativa para encontrar raíces de ecuaciones. La idea es transformar una ecuación f(x) = 0 en una forma equivalente x = g(x), donde el valor que buscamos es un "punto fijo" de la función g(x).
Pasos del Método:

Transformación: Convertir f(x) = 0 a x = g(x)
Iteración: x_{n+1} = g(x_n), comenzando con x₀
Convergencia: Repetir hasta que |x_{n+1} - x_n| < tolerancia

Explicación de cada Problema:
Problema 1: f(x) = 2e^(x²) - 5x = 0

Transformación: 2e^(x²) = 5x → x = (2e^(x²))/5
Función g₁(x): (2e^(x²))/5
Convergencia: Depende de que |g'(x)| < 1 en el punto fijo

Problema 2: f(x) = cos(x) = 0

Transformación: Ya está en forma de punto fijo: x = cos(x)
Función g₂(x): cos(x)
Punto fijo famoso: ≈ 0.739085 (constante de Dottie)

Problema 3: f(x) = e^(-x) - x = 0

Transformación: e^(-x) = x → x = e^(-x)
Función g₃(x): e^(-x)
Convergencia: Rápida porque g'(x) = -e^(-x) tiene magnitud pequeña

Problema 4: f(x) = x³ - x - 1 = 0

Transformación: x³ = x + 1 → x = ∛(x + 1)
Función g₄(x): (x + 1)^(1/3)
Alternativas: También podríamos usar x = x³ - 1, pero convergería más lento

Problema 5: f(x) = π + 0.5sin(x/2) - x = 0

Transformación: x = π + 0.5sin(x/2)
Función g₅(x): π + 0.5sin(x/2)

Criterio de Convergencia:
El método converge si |g'(x)| < 1* en el punto fijo x*. Esto garantiza convergencia local:

Si |g'(x*)| < 1: Converge
Si |g'(x*)| > 1: Diverge
Si |g'(x*)| = 1: Indeterminado

Ventajas y Desventajas:
Ventajas:

Simple de implementar
No requiere calcular derivadas de f(x)
Convergencia lineal cuando funciona

Desventajas:

Convergencia depende de la transformación elegida
Puede ser lento comparado con Newton-Raphson
Sensible al valor inicial x₀
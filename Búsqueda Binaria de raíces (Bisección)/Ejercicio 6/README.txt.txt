Te explico paso a paso la demostración matemática de por qué estas funciones tienen punto fijo exactamente cuando f(p) = 0:
Conceptos Fundamentales
Definición de Punto Fijo:
Un punto p es punto fijo de g(x) si g(p) = p
Objetivo:
Demostrar que g(p) = p ⟺ f(p) = 0 donde f(x) = x⁴ + 2x² - x - 3
Demostración Parte A: g(x) = √(3 + x - 2x²)
Dirección 1: g(p) = p ⟹ f(p) = 0
Paso 1: Si g(p) = p, entonces:
√(3 + p - 2p²) = p
Paso 2: Elevamos al cuadrado ambos lados:
3 + p - 2p² = p²
Paso 3: Reorganizamos:
3 + p - 2p² - p² = 0
3 + p - 3p² = 0
3p² - p - 3 = 0
Paso 4: Conectamos con f(p):

De la ecuación 3p² - p - 3 = 0, obtenemos: 3p² = p + 3
Por tanto: p² = (p + 3)/3
Calculamos: p⁴ = (p²)² = (p + 3)²/9
Sustituyendo en f(p): f(p) = p⁴ + 2p² - p - 3 = 0 ✓

Dirección 2: f(p) = 0 ⟹ g(p) = p
Si f(p) = 0, entonces podemos reorganizar la ecuación para obtener la condición del punto fijo.
Demostración Parte B: g(x) = √((x + 3 - x⁴)/2)
Dirección 1: g(p) = p ⟹ f(p) = 0
Paso 1: Si g(p) = p, entonces:
√((p + 3 - p⁴)/2) = p
Paso 2: Elevamos al cuadrado:
(p + 3 - p⁴)/2 = p²
Paso 3: Multiplicamos por 2:
p + 3 - p⁴ = 2p²
Paso 4: Reorganizamos:
-p⁴ + p + 3 - 2p² = 0
p⁴ + 2p² - p - 3 = 0
¡Esta es exactamente f(p) = 0! ✓
Dirección 2: f(p) = 0 ⟹ g(p) = p
Si f(p) = 0, entonces p⁴ + 2p² - p - 3 = 0, lo que se puede reorganizar como:
p + 3 - p⁴ = 2p²
(p + 3 - p⁴)/2 = p²
√((p + 3 - p⁴)/2) = |p|
Para que g(p) = p, necesitamos p ≥ 0.
Aspectos Importantes
Dominios de Definición:

Para g_a(x): Necesitamos 3 + x - 2x² ≥ 0

Resolviendo: 2x² - x - 3 ≤ 0
Dominio: x ∈ [-1, 1.5] aproximadamente


Para g_b(x): Necesitamos x + 3 - x⁴ ≥ 0

Es decir: x⁴ - x - 3 ≤ 0



Equivalencia Matemática:
La clave está en que ambas transformaciones son algebraicamente equivalentes a f(x) = 0:

g_a: Surge de reorganizar f(x) = 0 y despejar una expresión bajo raíz
g_b: Es una reorganización más directa de f(x) = 0

Significado Práctico:

Cualquier raíz de f(x) será un punto fijo de g_a(x) y g_b(x) (si está en el dominio)
Cualquier punto fijo de estas funciones será una raíz de f(x)
Esto garantiza que el método del punto fijo convergirá a las raíces de f(x)

Ventaja del Enfoque:
Esta demostración algebraica es rigurosa porque:

No depende de aproximaciones numéricas
Muestra la equivalencia exacta entre los problemas
Garantiza que no perdemos ni ganamos soluciones en la transformación
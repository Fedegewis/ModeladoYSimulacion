Te explico paso a paso la demostración matemática de que g(x) = 2^(-x) tiene un punto fijo en [1/3, 1]:
Método 1: Teorema del Valor Intermedio 🎯
Paso 1: Definir la función auxiliar
Definimos h(x) = g(x) - x = 2^(-x) - x
Si h(x) tiene una raíz en [1/3, 1], entonces g(x) tiene un punto fijo.
Paso 2: Evaluar en los extremos

h(1/3) = 2^(-1/3) - 1/3 ≈ 0.794 - 0.333 = 0.461 > 0
h(1) = 2^(-1) - 1 = 1/2 - 1 = -0.5 < 0

Paso 3: Aplicar el teorema
Como:

h(x) es continua (composición de funciones continuas)
h(1/3) > 0 y h(1) < 0
Por tanto h(1/3) · h(1) < 0

Por el Teorema del Valor Intermedio: ∃ p ∈ (1/3, 1) tal que h(p) = 0
Por lo tanto: g(p) = p ✓
Método 2: Teorema del Punto Fijo de Brouwer 📐
Condiciones del teorema:
Si g: [a,b] → [a,b] es continua, entonces g tiene al menos un punto fijo.
Verificación:
1. Continuidad: g(x) = 2^(-x) es continua en [1/3, 1] ✓
2. g mapea el intervalo en sí mismo:

g(1/3) = 2^(-1/3) ≈ 0.794 ∈ [1/3, 1] ✓
g(1) = 2^(-1) = 0.5 ∈ [1/3, 1] ✓
Como g es monótona decreciente, g([1/3, 1]) = [0.5, 0.794] ⊆ [1/3, 1] ✓

Conclusión: Por el Teorema del Punto Fijo, ∃ p ∈ [1/3, 1] tal que g(p) = p ✓
Método 3: Análisis de Monotonía 📊
Derivada de g(x):
g'(x) = d/dx[2^(-x)] = -ln(2) · 2^(-x)
Propiedades:

ln(2) > 0 y 2^(-x) > 0 para todo x
Por tanto: g'(x) < 0 para todo x ∈ ℝ
g(x) es estrictamente decreciente

Implicaciones:

El punto fijo es único (si existe)
Como g(1/3) > 1/3 y g(1) < 1, debe existir exactamente un punto donde g(x) = x

Análisis de Convergencia 🔄
Punto fijo numérico:
p ≈ 0.641186
Derivada en el punto fijo:
g'(p) = -ln(2) · 2^(-p) ≈ -0.429
Condición de convergencia:
|g'(p)| ≈ 0.429 < 1 ✓
Por tanto: El punto fijo es atractivo y el método iterativo convergerá.
Demostración Visual 👁️
La gráfica muestra claramente:

Intersección única entre g(x) = 2^(-x) y y = x en [1/3, 1]
h(x) cambia de signo en el intervalo
Convergencia iterativa hacia el punto fijo
La región [1/3, 1] × [1/3, 1] contiene la gráfica de g(x)

Resumen de la Demostración 📝
Hemos demostrado la existencia del punto fijo mediante tres métodos independientes:

Teorema del Valor Intermedio: Cambio de signo de h(x)
Teorema del Punto Fijo: g mapea el intervalo en sí mismo
Análisis de monotonía: Función decreciente con valores apropiados

Propiedades adicionales:

Unicidad: g'(x) < 0 garantiza un único punto fijo
Convergencia: |g'(p)| < 1 asegura convergencia del método iterativo
Estabilidad: El punto fijo es atractivo

Conclusión final: g(x) = 2^(-x) tiene exactamente un punto fijo en [1/3, 1], localizado aproximadamente en p ≈ 0.641186.
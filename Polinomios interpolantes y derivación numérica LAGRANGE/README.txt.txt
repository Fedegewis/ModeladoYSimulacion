# Explicación Detallada: Polinomios Interpolantes de Lagrange

## Teoría Base

La **fórmula de interpolación de Lagrange** para n+1 puntos (x₀,y₀), (x₁,y₁), ..., (xₙ,yₙ) es:

```
P(x) = Σ(i=0 hasta n) yᵢ · Lᵢ(x)
```

Donde cada **base de Lagrange** Lᵢ(x) se define como:

```
Lᵢ(x) = ∏(j=0 hasta n, j≠i) [(x - xⱼ)/(xᵢ - xⱼ)]
```

**Propiedad clave**: Lᵢ(xᵢ) = 1 y Lᵢ(xⱼ) = 0 para i ≠ j

---

## Ejercicio 1: Puntos (1,1), (2,4), (3,9)

**Paso 1**: Identificar los datos
- x₀ = 1, y₀ = 1
- x₁ = 2, y₁ = 4  
- x₂ = 3, y₂ = 9

**Paso 2**: Calcular las bases de Lagrange

L₀(x) = [(x-2)(x-3)]/[(1-2)(1-3)] = [(x-2)(x-3)]/[(-1)(-2)] = [(x-2)(x-3)]/2

L₁(x) = [(x-1)(x-3)]/[(2-1)(2-3)] = [(x-1)(x-3)]/[(1)(-1)] = -[(x-1)(x-3)]

L₂(x) = [(x-1)(x-2)]/[(3-1)(3-2)] = [(x-1)(x-2)]/[(2)(1)] = [(x-1)(x-2)]/2

**Paso 3**: Construir el polinomio
P(x) = 1·L₀(x) + 4·L₁(x) + 9·L₂(x)

P(x) = [(x-2)(x-3)]/2 - 4[(x-1)(x-3)] + 9[(x-1)(x-2)]/2

**Paso 4**: Expandir y simplificar
P(x) = (x² - 5x + 6)/2 - 4(x² - 4x + 3) + 9(x² - 3x + 2)/2
P(x) = (x² - 5x + 6)/2 - 4x² + 16x - 12 + 9(x² - 3x + 2)/2
P(x) = x²

**Resultado**: P(x) = x² (¡Es exactamente la función cuadrática!)

---

## Ejercicio 2: Puntos (0,1), (1,3), (2,2), (3,5)

**Paso 1**: Datos
- x₀ = 0, y₀ = 1
- x₁ = 1, y₁ = 3
- x₂ = 2, y₂ = 2
- x₃ = 3, y₃ = 5

**Paso 2**: Bases de Lagrange (4 puntos = polinomio grado 3)

L₀(x) = [(x-1)(x-2)(x-3)]/[(0-1)(0-2)(0-3)] = [(x-1)(x-2)(x-3)]/[(-1)(-2)(-3)] = -[(x-1)(x-2)(x-3)]/6

L₁(x) = [(x-0)(x-2)(x-3)]/[(1-0)(1-2)(1-3)] = [x(x-2)(x-3)]/[(1)(-1)(-2)] = [x(x-2)(x-3)]/2

L₂(x) = [(x-0)(x-1)(x-3)]/[(2-0)(2-1)(2-3)] = [x(x-1)(x-3)]/[(2)(1)(-1)] = -[x(x-1)(x-3)]/2

L₃(x) = [(x-0)(x-1)(x-2)]/[(3-0)(3-1)(3-2)] = [x(x-1)(x-2)]/[(3)(2)(1)] = [x(x-1)(x-2)]/6

**Paso 3**: P(x) = 1·L₀(x) + 3·L₁(x) + 2·L₂(x) + 5·L₃(x)

**Resultado**: P(x) = (11x³ - 36x² + 38x - 6)/6

---

## Ejercicio 9: Aproximar sin(x) en [0,π] con 3 puntos

**Paso 1**: Elegir puntos estratégicos
- x₀ = 0, y₀ = sin(0) = 0
- x₁ = π/2, y₁ = sin(π/2) = 1
- x₂ = π, y₂ = sin(π) = 0

**Paso 2**: Calcular bases de Lagrange

L₀(x) = [(x - π/2)(x - π)]/[(0 - π/2)(0 - π)] = [(x - π/2)(x - π)]/[(-π/2)(-π)] = [2(x - π/2)(x - π)]/π²

L₁(x) = [(x - 0)(x - π)]/[(π/2 - 0)(π/2 - π)] = [x(x - π)]/[(π/2)(-π/2)] = [-4x(x - π)]/π²

L₂(x) = [(x - 0)(x - π/2)]/[(π - 0)(π - π/2)] = [x(x - π/2)]/[π(π/2)] = [2x(x - π/2)]/π²

**Paso 3**: Construir polinomio
P(x) = 0·L₀(x) + 1·L₁(x) + 0·L₂(x) = L₁(x) = [-4x(x - π)]/π²

**Simplificando**: P(x) = (4x/π²)(π - x) = (4x/π) - (4x²/π²)

**Resultado**: P(x) ≈ 1.273x - 0.405x²

---

## Ejercicio 12: f(x) = 2sin(πx/6), aproximar f(4) y f(1.5)

**Paso 1**: Evaluar función en nodos dados
- x₀ = 1, y₀ = 2sin(π/6) = 2(1/2) = 1
- x₁ = 2, y₁ = 2sin(π/3) = 2(√3/2) = √3 ≈ 1.732
- x₂ = 3, y₂ = 2sin(π/2) = 2(1) = 2

**Paso 2**: Construir bases de Lagrange

L₀(x) = [(x-2)(x-3)]/[(1-2)(1-3)] = [(x-2)(x-3)]/2

L₁(x) = [(x-1)(x-3)]/[(2-1)(2-3)] = -[(x-1)(x-3)]

L₂(x) = [(x-1)(x-2)]/[(3-1)(3-2)] = [(x-1)(x-2)]/2

**Paso 3**: P(x) = 1·L₀(x) + √3·L₁(x) + 2·L₂(x)

**Paso 4**: Evaluar
- P(4) = 1·[(4-2)(4-3)]/2 + √3·[-((4-1)(4-3))] + 2·[(4-1)(4-2)]/2
- P(4) = 1·(2·1)/2 - √3·(3·1) + 2·(3·2)/2
- P(4) = 1 - 3√3 + 6 = 7 - 3√3 ≈ 1.804

**Verificación**: f(4) = 2sin(2π/3) = 2(√3/2) = √3 ≈ 1.732

---

## Ejercicio 13a: Aproximar cos(0.45) con nodos 0, 0.6, 0.9

**Paso 1**: Evaluar cos(x) en los nodos
- x₀ = 0, y₀ = cos(0) = 1
- x₁ = 0.6, y₁ = cos(0.6) ≈ 0.8253
- x₂ = 0.9, y₂ = cos(0.9) ≈ 0.6216

**Paso 2**: Calcular bases de Lagrange

L₀(x) = [(x-0.6)(x-0.9)]/[(0-0.6)(0-0.9)] = [(x-0.6)(x-0.9)]/[(-0.6)(-0.9)] = [(x-0.6)(x-0.9)]/0.54

L₁(x) = [(x-0)(x-0.9)]/[(0.6-0)(0.6-0.9)] = [x(x-0.9)]/[(0.6)(-0.3)] = [x(x-0.9)]/(-0.18)

L₂(x) = [(x-0)(x-0.6)]/[(0.9-0)(0.9-0.6)] = [x(x-0.6)]/[(0.9)(0.3)] = [x(x-0.6)]/0.27

**Paso 3**: P(x) = 1·L₀(x) + 0.8253·L₁(x) + 0.6216·L₂(x)

**Paso 4**: Evaluar en x = 0.45
P(0.45) = 1·L₀(0.45) + 0.8253·L₁(0.45) + 0.6216·L₂(0.45)

Calculando cada término:
- L₀(0.45) = [(0.45-0.6)(0.45-0.9)]/0.54 = [(-0.15)(-0.45)]/0.54 = 0.0675/0.54 ≈ 0.125
- L₁(0.45) = [0.45(0.45-0.9)]/(-0.18) = [0.45(-0.45)]/(-0.18) = -0.2025/(-0.18) ≈ 1.125  
- L₂(0.45) = [0.45(0.45-0.6)]/0.27 = [0.45(-0.15)]/0.27 = -0.0675/0.27 ≈ -0.25

P(0.45) ≈ 1(0.125) + 0.8253(1.125) + 0.6216(-0.25) ≈ 0.7734

**Verificación**: cos(0.45) ≈ 0.9004
**Error**: |0.9004 - 0.7734| ≈ 0.127

---

## ¿Por qué funciona la interpolación de Lagrange?

1. **Unicidad**: Para n+1 puntos distintos, existe un único polinomio de grado ≤ n que pasa por todos ellos.

2. **Construcción directa**: Las bases Lᵢ(x) tienen la propiedad de "filtro": 
   - Lᵢ(xᵢ) = 1 (se "activa" en su punto)
   - Lᵢ(xⱼ) = 0 para j ≠ i (se "desactiva" en otros puntos)

3. **Calidad de aproximación**: Depende de:
   - Distribución de los nodos (mejor si están bien espaciados)
   - Suavidad de la función original
   - Distancia al punto de evaluación

4. **Limitaciones**: 
   - Puede oscilar mucho entre nodos (fenómeno de Runge)
   - No siempre converge al aumentar el número de puntos
   - Mejor para funciones suaves

## Consejos Prácticos

- **Verificación**: Siempre comprobar que P(xᵢ) = yᵢ
- **Nodos**: Elegir puntos bien distribuidos en el intervalo
- **Grado**: Más puntos no siempre significa mejor aproximación
- **Aplicaciones**: Útil para interpolación de datos experimentales y aproximación de funciones
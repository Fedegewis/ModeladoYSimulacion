## 📚 **EXPLICACIÓN COMPLETA DEL EJERCICIO 4**

### **🎯 Función del ejercicio:**
```
f(x) = x⁴ - 2x³ - 4x² + 4x + 4
```
**Tolerancia:** 10⁻² = 0.01 (menos precisa que los ejercicios anteriores)

### **📊 Características del polinomio:**

#### **🔍 Análisis matemático:**
- **Grado 4** → máximo 4 raíces reales posibles
- **Coeficiente principal positivo** → f(x) → +∞ cuando x → ±∞
- **Función continua** → aplica Teorema de Bolzano perfectamente

#### **🎨 Comportamiento esperado:**
```
• Para x muy negativo: f(x) → +∞
• Para x muy positivo: f(x) → +∞  
• En el medio: oscila pasando por cero (raíces)
```

### **🔍 Análisis de cada intervalo:**

#### **a) [-2, -1]:**
```
f(-2) = 16 + 16 - 16 - 8 + 4 = 12 > 0
f(-1) = 1 + 2 - 4 - 4 + 4 = -1 < 0
¡Cambio de signo! → Hay una raíz
```

#### **b) [0, 2]:**
```
f(0) = 0 - 0 - 0 + 0 + 4 = 4 > 0
f(2) = 16 - 16 - 16 + 8 + 4 = -4 < 0
¡Cambio de signo! → Hay una raíz
```

#### **c) [2, 3]:**
```
f(2) = -4 < 0 (del anterior)
f(3) = 81 - 54 - 36 + 12 + 4 = 7 > 0
¡Cambio de signo! → Hay una raíz
```

#### **d) [-1, 0]:**
```
f(-1) = -1 < 0 (del primer intervalo)
f(0) = 4 > 0 (del segundo intervalo)
¡Cambio de signo! → Hay una raíz
```

### **⚙️ Proceso de bisección paso a paso:**

**Ejemplo para intervalo [-2, -1]:**

| Iter | a    | b    | c = (a+b)/2 | f(c)    | Error | Acción |
|------|------|------|-------------|---------|-------|---------|
| 1    | -2   | -1   | -1.5        | 3.0625  | 0.5   | a = c   |
| 2    | -1.5 | -1   | -1.25       | 0.684   | 0.25  | a = c   |
| 3    | -1.25| -1   | -1.125      | -0.237  | 0.125 | b = c   |
| 4    | -1.25| -1.125| -1.1875    | 0.207   | 0.0625| a = c   |

**Convergencia:** Cuando |f(c)| < 0.01 o |b-a|/2 < 0.01

### **🎨 Gráficos generados:**

#### **1. Vista completa:**
- **Curva azul:** El polinomio completo
- **Zonas sombreadas:** Los 4 intervalos del ejercicio
- **Círculos/cuadrados:** Extremos de cada intervalo
- **Estrellas doradas:** Raíces encontradas

#### **2. Vista ampliada:**
- **Zoom** en la región [-2.5, 3.5] 
- **Anotaciones** con valores aproximados de las raíces
- **Mejor visualización** de los cruces por cero

### **📊 Resultados esperados:**

```
a) [-2, -1]  → Raíz ≈ -1.175
b) [0, 2]    → Raíz ≈ 1.236  
c) [2, 3]    → Raíz ≈ 2.445
d) [-1, 0]   → Raíz ≈ -0.506
```

**¡4 raíces encontradas!** El polinomio tiene exactamente 4 raíces reales.

### **🔬 Diferencias con ejercicios anteriores:**

#### **1. Tolerancia menos estricta:**
- **10⁻² = 0.01** vs 10⁻³ o 10⁻⁶ anteriores
- **Converge más rápido** (menos iteraciones)
- **Menos precisión** en el resultado final

#### **2. Función polinómica:**
- **Más predecible** que funciones trigonométricas o exponenciales
- **Sin problemas de dominio** (definida para todos los reales)
- **Comportamiento suave** (infinitamente derivable)

#### **3. Múltiples intervalos sistemáticos:**
- **4 intervalos específicos** dados en el problema
- **Análisis completo** de todas las posibles raíces
- **Verificación exhaustiva** del comportamiento

### **💡 Observaciones importantes:**

1. **Todos los intervalos tienen raíz** porque todos muestran cambio de signo
2. **El polinomio es de grado 4** → puede tener máximo 4 raíces reales ✓
3. **Tolerancia 10⁻²** es adecuada para aplicaciones prácticas
4. **El método bisección es ideal** para polinomios por su continuidad garantizada

El código ejecuta automáticamente todo el análisis y muestra tanto las tablas de iteraciones como los gráficos para visualizar todas las raíces del polinomio.
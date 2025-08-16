## 📚 **EXPLICACIÓN COMPLETA DEL EJERCICIO 3**

### **🎯 Objetivo:**
Aplicar bisección con **tolerancia específica de 10⁻³** (0.001) para encontrar raíces aproximadas.

### **🔍 ¿Qué hace cada función?**

#### **a) f(x) = √x - cos(x) = 0 en [0,1]**
```
Busca: ¿Dónde se cruzan √x y cos(x)?
• √x crece de 0 a 1
• cos(x) decrece de 1 a cos(1) ≈ 0.54
• Se cruzan en algún punto intermedio
```

#### **b) f(x) = x - 2⁻ˣ = 0 en [0,1]**  
```
Busca: ¿Dónde x = 2^(-x)?
• En x=0: 0 vs 2^0 = 1 → f(0) = -1
• En x=1: 1 vs 2^(-1) = 0.5 → f(1) = 0.5
• Hay cambio de signo → existe raíz
```

#### **c) f(x) = eˣ - x² + 3x - 2 = 0 en [0,1]**
```
Función mixta: exponencial + polinómica
• En x=0: e^0 - 0 + 0 - 2 = -1
• En x=1: e^1 - 1 + 3 - 2 = e ≈ 2.718
• Cambio de signo → hay raíz
```

#### **d) f(x) = 2x cos(x) - (x+1)² = 0**
**Dos intervalos:** [-3,-2] y [-1,0]
```
Función con trigonometría en valores negativos
• Primer intervalo: x muy negativo
• Segundo intervalo: cerca del cero
```

#### **e) f(x) = x cos(x) - 2x² + 3x - 1 = 0**
**Dos intervalos pequeños:** [0.2,0.3] y [1.2,1.3]
```
Intervalos muy específicos y pequeños
• Requiere precisión alta
• Busca raíces en rangos acotados
```

### **⚙️ Algoritmo de Bisección Paso a Paso:**

**Ejemplo para f(x) = √x - cos(x) en [0,1]:**

| Iter | a    | b    | c = (a+b)/2 | f(c)     | Error   | Acción |
|------|------|------|-------------|----------|---------|---------|
| 1    | 0    | 1    | 0.5         | 0.168    | 0.5     | a = c   |
| 2    | 0.5  | 1    | 0.75        | 0.139    | 0.25    | a = c   |
| 3    | 0.75 | 1    | 0.875       | 0.056    | 0.125   | a = c   |
| 4    | 0.875| 1    | 0.9375      | 0.009    | 0.0625  | a = c   |

**Convergencia:** Cuando |f(c)| < 0.001 o |b-a|/2 < 0.001

### **🎨 Gráficos Generados:**

1. **Función completa** en azul
2. **Intervalos de búsqueda** sombreados en colores
3. **Puntos extremos** marcados (círculos y cuadrados)
4. **Eje x=0** para ver dónde f(x) cruza

### **📊 Criterios de Convergencia:**

```python
# Para tolerancia 10^-3:
if abs(f(c)) < 0.001 or abs(b-a)/2 < 0.001:
    # CONVERGENCIA ALCANZADA
    return raiz_aproximada
```

**Dos formas de parar:**
1. **|f(c)| < 0.001**: La función está muy cerca de cero
2. **|b-a|/2 < 0.001**: El intervalo es muy pequeño

### **💡 Resultados Esperados:**

- **a) √x - cos(x)**: Raíz ≈ 0.641 (donde las curvas se cruzan)
- **b) x - 2⁻ˣ**: Raíz ≈ 0.641 (punto fijo)
- **c) eˣ - x² + 3x - 2**: Raíz ≈ 0.257
- **d) 2x cos(x) - (x+1)²**: Una raíz en cada intervalo
- **e) x cos(x) - 2x² + 3x - 1**: Raíces específicas en intervalos pequeños

### **🔬 Diferencias con ejercicios anteriores:**

1. **Tolerancia específica**: 10⁻³ en lugar de 10⁻⁶
2. **Múltiples intervalos**: Algunas funciones tienen varios rangos
3. **Funciones más complejas**: Mezclan exponenciales, trigonométricas y radicales
4. **Análisis detallado**: Muestra convergencia paso a paso

El código ejecuta automáticamente todos los ejercicios y te muestra una tabla resumen final con todas las raíces encontradas.
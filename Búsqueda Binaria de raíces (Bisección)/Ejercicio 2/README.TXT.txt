Te explico cómo armar este ejercicio paso a paso:## 📚 **EXPLICACIÓN COMPLETA DEL EJERCICIO**

### **🎯 Función del ejercicio:**
```
f(x) = 3(x + 1)(x - 1/2)(x - 1)
```

### **🔍 ¿Qué hace el código?**

#### **1. ANÁLISIS TEÓRICO:**
- **Identifica las raíces**: x = -1, x = 1/2, x = 1
- **Evalúa la función** en puntos clave para entender su comportamiento
- **Determina el signo** de f(x) en diferentes regiones

#### **2. BÚSQUEDA BINARIA (BISECCIÓN):**

**Para intervalo a) [-1, 1.5]:**
```
f(-1) = 3(0)(-1.5)(-2) = 0     (raíz exacta)
f(1.5) = 3(2.5)(1)(0.5) = 3.75 (positivo)
```

**Para intervalo b) [-1.25, 2.5]:**
```
f(-1.25) = 3(-0.25)(-1.75)(-2.25) ≈ -2.95 (negativo)
f(2.5) = 3(3.5)(2)(1.5) = 31.5            (positivo)
```

#### **3. ALGORITMO PASO A PASO:**

**Ejemplo para intervalo [-1.25, 2.5]:**

| Iter | a     | b    | c = (a+b)/2 | f(c)   | Acción    |
|------|-------|------|-------------|--------|-----------|
| 1    | -1.25 | 2.5  | 0.625       | 0.82   | a = c     |
| 2    | 0.625 | 2.5  | 1.563       | 7.03   | a = c     |
| 3    | 1.563 | 2.5  | 2.031       | 15.8   | a = c     |

**¿Por qué va hacia la derecha?** Porque f(-1.25) < 0 y f(c) > 0, entonces la raíz está entre -1.25 y c.

#### **4. CARACTERÍSTICAS ESPECIALES:**

**⚠️ Problema en intervalo a) [-1, 1.5]:**
- **f(-1) = 0**: Ya es una raíz exacta
- **f(1.5) > 0**: Ambos extremos no tienen signos opuestos
- **El algoritmo puede converger** a x = -1, pero viola la condición del teorema de Bolzano

**✅ Intervalo b) [-1.25, 2.5] funciona bien:**
- **f(-1.25) < 0** y **f(2.5) > 0**: Signos opuestos ✓
- **Garantiza convergencia** a una de las raíces en el intervalo

### **🎨 GRÁFICO:**
El código muestra:
- **Curva azul**: La función f(x)
- **Puntos verdes**: Raíces teóricas (-1, 0.5, 1)
- **Zonas sombreadas**: Los intervalos de búsqueda
- **Puntos/cuadrados**: Extremos de cada intervalo

### **💡 RESULTADOS ESPERADOS:**
- **Intervalo a) [-1, 1.5]**: Converge a x = -1 (raíz exacta)
- **Intervalo b) [-1.25, 2.5]**: Converge a x = 0.5 (raíz en el medio del intervalo)

El método de **búsqueda binaria** es exactamente lo mismo que **bisección**, solo cambia el nombre. ¡Es el mismo algoritmo que divide el intervalo por la mitad en cada iteración!
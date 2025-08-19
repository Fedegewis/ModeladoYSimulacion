2. Definición de la función
pythondef f(x):
    return (x + 2) * (x + 1) * (x - 1)**3 * (x - 2)
Esta es tu función f(x) = (x + 2)(x + 1)(x - 1)³(x - 2). Note que (x-1) está elevado a la potencia 3.
3. Análisis de raíces
pythondef encontrar_raices():
Esta función identifica las raíces evidentes:

x = -2 (hace que (x+2) = 0)
x = -1 (hace que (x+1) = 0)
x = 1 (hace que (x-1)³ = 0, con multiplicidad 3)
x = 2 (hace que (x-2) = 0)

4. Análisis de convergencia por intervalo
pythondef analizar_convergencia(intervalos):
Para cada intervalo:

Evalúa f(a) y f(b): valores en los extremos
Verifica cambio de signo: si f(a)·f(b) < 0, hay al menos una raíz
Identifica raíces: busca raíces conocidas dentro del intervalo
Determina convergencia: si hay raíces, la función "converge a cero"

5. Visualización gráfica
pythondef graficar_funcion(intervalos):
Crea 4 subgráficos, uno para cada intervalo:

Grafica la función en azul
Marca la línea y = 0 en negro punteado
Resalta las raíces con puntos rojos
Ajusta escalas para mejor visualización

6. Tabla resumen
pythondef crear_tabla_resumen(resultados):
Organiza los resultados en una tabla que muestra:

Intervalo analizado
Valores en los extremos
Si hay cambio de signo
Número de raíces encontradas
Si converge a cero

¿Qué hace cada parte del análisis?

Identificación de raíces: La función se anula cuando cualquiera de los factores es cero
Teorema del valor intermedio: Si f(a) y f(b) tienen signos opuestos, hay al menos una raíz en [a,b]
Multiplicidad: En x=1, la raíz tiene multiplicidad 3, significa que la función toca el eje pero no lo cruza
Convergencia a cero: Significa que existe al menos un punto en el intervalo donde f(x) = 0

Resultado esperado:
Todos los intervalos contienen al menos una raíz, por lo que la función "converge a cero" en todos ellos:

a) [-3, 2.5]: Contiene las 4 raíces
b) [-2.5, 3]: Contiene las 4 raíces
c) [-1.75, 1.5]: Contiene x = -1 y x = 1
d) [-1.5, 1.75]: Contiene x = -1 y x = 1

¡Ejecuta el código en Spyder y verás los gráficos y análisis completo!
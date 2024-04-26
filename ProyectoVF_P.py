import random
import copy
import sys

#Número de matrices iniciales
num_matrices = 12

#Declarar el número de matrices a mantener en cada iteración
matrices_a_mantener=6

#Cadenas iniciales
X = list("GATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG")
Y = list("CGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATC")
Z = list("ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGA")

# Definir límite de ciclos y puntaje deseado
puntaje_buscado = 74  # Puntaje mínimo buscado
iteraciones_maximas = 10000  # Número de repeticiones máximas del ciclo

def insertar_guiones(matriz):
    # Hacemos una copia de la matriz para no modificar la original
    matriz_con_guiones = copy.deepcopy(matriz)
    
    # Encuentra la longitud máxima de las filas
    max_longitud = max(len(fila) for fila in matriz_con_guiones)
    
    # Para cada fila en la matriz
    for fila in matriz_con_guiones:
        # Si la longitud de la fila es menor que la longitud máxima
        if len(fila) < max_longitud:
            # Inserta guiones en posiciones aleatorias para igualar las longitudes
            posiciones = random.sample(range(len(fila) + 1), max_longitud - len(fila))
            for pos in posiciones:
                fila.insert(pos, '-')
        
        # Inserta tres guiones adicionales en posiciones aleatorias
        posiciones_extra = random.sample(range(len(fila) + 1), 3)
        for pos in posiciones_extra:
            fila.insert(pos, '-')
    
    return matriz_con_guiones

def calcular_puntaje(matriz_sin_guiones):
    puntos = 0
    for j in range(len(matriz_sin_guiones[0])):
        caracteres_en_posicion = [fila[j] for fila in matriz_sin_guiones]
        caracteres_no_guion = [caracter for caracter in caracteres_en_posicion if caracter != '-']
        
        # Verificar si hay al menos dos caracteres no guion y si al menos dos son iguales,
        # o si hay tres caracteres no guion y al menos dos son iguales, o si los tres son iguales
        if len(caracteres_no_guion) == 2 and len(set(caracteres_no_guion)) == 1:
            puntos += 1
        elif len(caracteres_no_guion) == 3 and (len(set(caracteres_no_guion)) == 1 or len(set(caracteres_no_guion)) == 2):
            puntos += 1
    return puntos

# Definir una función para eliminar columnas de guiones
def eliminar_columnas_guiones(matriz):
    columnas_con_guiones = set()
    for j in range(len(matriz[0])):
        columna = [fila[j] for fila in matriz]
        if all(caracter == '-' for caracter in columna):
            columnas_con_guiones.add(j)
    matriz_filtrada = [[caracter for i, caracter in enumerate(fila) if i not in columnas_con_guiones] for fila in matriz]
    return matriz_filtrada

# Definir una función para insertar tres guiones en posiciones aleatorias en cada fila
def mutacion_hijos(matriz):
    matriz_con_guiones = []
    for fila in matriz:
        fila_con_guiones = list(fila)
        for _ in range(3):  # Insertar tres guiones en posiciones aleatorias
            indice = random.randint(0, len(fila_con_guiones))
            fila_con_guiones.insert(indice, '-')
        matriz_con_guiones.append(fila_con_guiones)
    return matriz_con_guiones

matrices_con_puntajes = []

# Calcular la longitud de las tres variables
longitud_X = len(X)
longitud_Y = len(Y)
longitud_Z = len(Z)

# Encontrar la longitud mínima
longitud_minima = min(longitud_X, longitud_Y, longitud_Z)

# Encontrar la longitud máxima
longitud_maxima = max(longitud_X, longitud_Y, longitud_Z)

for i in range(num_matrices):
    # Generamos una matriz nueva en cada iteración, basada en las listas originales
    matriz = [copy.deepcopy(X), copy.deepcopy(Y), copy.deepcopy(Z)]
    matriz_con_guiones = insertar_guiones(matriz)
    
    # Inicializar la lista de columnas sin guiones para esta matriz
    columnas_sin_guiones = []
    
    # Verificar si alguna columna no consiste solo de guiones
    for columna in zip(*matriz_con_guiones):
        if any(caracter != '-' for caracter in columna):
            columnas_sin_guiones.append(columna)
    
    # Transponer la lista de columnas sin guiones para obtener la matriz resultante
    matriz_sin_guiones = list(zip(*columnas_sin_guiones))

    # Imprimir la matriz sin columnas de guiones
    print(f"Matriz {i+1} sin guiones:")
    for fila in matriz_sin_guiones:
        print(''.join(fila))
    print()

    # Calcular puntajes
    puntos = calcular_puntaje(matriz_sin_guiones)

    # Imprimir puntaje
    print(f"Puntos para la matriz {i+1}: {puntos}\n")

    # Almacenar la matriz y su puntaje en la lista
    matrices_con_puntajes.append((matriz_sin_guiones, puntos))

# Verificar si la cantidad de matrices a mantener es mayor que el número total de matrices
if matrices_a_mantener > num_matrices:
    print("Error: La cantidad de matrices a mantener es mayor que el número total de matrices iniciales.")
    sys.exit()

iteracion_actual = 0  # Variable para llevar la cuenta de las iteraciones

# Variable para verificar si se encontró una matriz con puntaje mayor a puntaje_buscado
encontrado = False

for _ in range(iteraciones_maximas):
    num_hijo=0

    iteracion_actual += 1  # Incrementar el contador de iteraciones
    print(f"Iteración actual: {iteracion_actual}")

    # Ordenar las matrices por puntaje en orden descendente
    matrices_con_puntajes.sort(key=lambda x: x[1], reverse=True)

    # Mantener solo las seis mejores matrices
    matrices_con_puntajes = matrices_con_puntajes[:matrices_a_mantener]

    # Imprimir las seis matrices con los puntajes más altos
    print("Las seis matrices con los puntajes más altos:")
    for i, (matriz, puntaje) in enumerate(matrices_con_puntajes):
        print(f"Matriz {i+1} con puntaje {puntaje}:")
        for fila in matriz:
            print(''.join(fila))
        print()

    # Obtener las matrices en el top 6
    mejores_matrices = [matriz for matriz, _ in matrices_con_puntajes]

    # Mientras hayan matrices disponibles en el top 6
    while mejores_matrices:
        # Seleccionar dos matrices aleatorias
        matriz1, matriz2 = random.sample(mejores_matrices, 2)
        
        # Generar dos números aleatorios menores que la longitud mínima
        numero1 = random.randint(1, longitud_minima - 1)
        numero2 = random.randint(1, longitud_minima - 1)

        # Ordenar los números de menor a mayor
        numero_menor = min(numero1, numero2)
        numero_mayor = max(numero1, numero2)

        # Lista para almacenar las filas con la extracción
        extracciones = []

        # Iterar sobre cada fila de la primer matriz
        for fila in matriz1:
            # Contador para los caracteres no guion
            contador_no_guion = 0
            # Iterar sobre cada carácter de la fila
            for i, caracter in enumerate(fila):
                # Verificar si el carácter no es un guion
               if caracter != '-':
                contador_no_guion += 1
                # Verificar si el contador alcanza el valor de "numero_menor"
                if contador_no_guion >= numero_menor:
                    # Agregar la extracción de caracteres hasta este punto
                    extracciones.append(fila[:i+1])
                    break

        # Lista para almacenar las extracciones de caracteres
        extracciones_segunda_matriz = []

        # Iterar sobre cada fila de la segunda mejor matriz
        for fila in matriz2:
            # Contador para los caracteres no guion
            contador_no_guion = 0
            # Bandera para indicar si se está extrayendo caracteres
            extrayendo = False
            # Lista para almacenar los caracteres a extraer
            caracteres_a_extraer = []
            # Iterar sobre cada carácter de la fila
            for i, caracter in enumerate(fila):
                # Verificar si el carácter no es un guion
                if caracter != '-':
                    contador_no_guion += 1
                # Verificar si el contador es igual al número menor
                if contador_no_guion == numero_menor:
                    # Comenzar la extracción de caracteres en el siguiente carácter
                    extrayendo = True
                # Verificar si se está extrayendo caracteres y el contador es menor o igual que el número mayor
                if extrayendo and contador_no_guion <= numero_mayor:
                    # Agregar el carácter a extraer
                    caracteres_a_extraer.append(caracter)
                # Verificar si el contador es igual al número mayor para la última extracción
                if contador_no_guion == numero_mayor:
                    # Romper el bucle para evitar extracciones adicionales
                    break
            # Agregar la lista de caracteres extraídos a la lista de extracciones
            extracciones_segunda_matriz.append(caracteres_a_extraer)

        # Eliminar el primer carácter de cada secuencia en extracciones_segunda_matriz
        extracciones_segunda_matriz = [extraccion[1:] for extraccion in extracciones_segunda_matriz]

        # Lista para almacenar las extracciones de caracteres
        extracciones_finales = []

        # Iterar sobre cada fila de la primer matriz
        for fila in matriz1:
            # Contador para los caracteres no guion
            contador_no_guion = 0
            # Bandera para indicar si se está extrayendo caracteres
            extrayendo = False
            # Lista para almacenar los caracteres a extraer
            caracteres_a_extraer = []
            # Iterar sobre cada carácter de la fila
            for i, caracter in enumerate(fila):
                # Verificar si el carácter no es un guion
                if caracter != '-':
                    contador_no_guion += 1
                # Verificar si el contador es igual al número menor
                if contador_no_guion == numero_mayor:
                    # Comenzar la extracción de caracteres
                    extrayendo = True
                if extrayendo:
                    # Agregar el carácter a extraer
                    caracteres_a_extraer.append(caracter)
            # Agregar la lista de caracteres extraídos a la lista de extracciones
            extracciones_finales.append(caracteres_a_extraer)

        # Eliminar el primer carácter de cada secuencia en extracciones_segunda_matriz
        extracciones_finales = [extraccion[1:] for extraccion in extracciones_finales]

        # Combinar las filas de cada conjunto de extracciones en una sola fila
        primera_fila_combinada = ''.join(extracciones[0]) + \
                                ''.join(extracciones_segunda_matriz[0]) + \
                                ''.join(extracciones_finales[0])

        segunda_fila_combinada = ''.join(extracciones[1]) + \
                                ''.join(extracciones_segunda_matriz[1]) + \
                                ''.join(extracciones_finales[1])

        tercera_fila_combinada = ''.join(extracciones[2]) + \
                                ''.join(extracciones_segunda_matriz[2]) + \
                                ''.join(extracciones_finales[2])

        # Calcular las longitudes de las filas combinadas
        longitud_primera_fila_combinada = len(primera_fila_combinada)
        longitud_segunda_fila_combinada = len(segunda_fila_combinada)
        longitud_tercera_fila_combinada = len(tercera_fila_combinada)

        # Determinar la longitud máxima entre las filas combinadas
        longitud_maxima_filas_combinadas = max(longitud_primera_fila_combinada, longitud_segunda_fila_combinada, longitud_tercera_fila_combinada)

        # Ajustar las filas más cortas insertando guiones al final para igualarlas a la longitud máxima
        primera_fila_combinada += '-' * (longitud_maxima_filas_combinadas - longitud_primera_fila_combinada)
        segunda_fila_combinada += '-' * (longitud_maxima_filas_combinadas - longitud_segunda_fila_combinada)
        tercera_fila_combinada += '-' * (longitud_maxima_filas_combinadas - longitud_tercera_fila_combinada)

        # Combinar las tres filas combinadas en una sola matriz
        hijo = [primera_fila_combinada, segunda_fila_combinada, tercera_fila_combinada]

        num_hijo=num_hijo+1

        # Imprimir la matriz combinada
        print(f"Hijo {num_hijo}:")
        for fila in hijo:
            print(fila)

        # Insertar guiones aleatorios en el hijo
        hijo_con_guiones = mutacion_hijos(hijo)

        # Aplicar la función para eliminar columnas de guiones
        hijo_filtrado = eliminar_columnas_guiones(hijo_con_guiones)

        # Calcular el puntaje de la matriz combinada
        puntaje_hijo = calcular_puntaje(hijo_filtrado)

        # Agregar la matriz combinada y su puntaje a la lista de las seis mejores matrices
        matrices_con_puntajes.append((hijo_filtrado, puntaje_hijo))

        # Eliminar las matrices seleccionadas de la lista de mejores_matrices
        mejores_matrices.remove(matriz1)
        mejores_matrices.remove(matriz2)

        # Verificar si se alcanzó el puntaje mínimo requerido
        if puntaje_hijo >= puntaje_buscado:
            print("Se encontró una matriz con puntaje mayor a", puntaje_buscado)
            break
    # Si se encontró una matriz con puntaje mayor o igual a puntaje_buscado, salir del ciclo externo
    if puntaje_hijo >= puntaje_buscado:
        encontrado=True
        break

# Verificar si se encontró una matriz con puntaje mayor o igual a puntaje_buscado
if encontrado:
    print("Se encontró una matriz con puntaje mayor a", puntaje_buscado)
else:
    print("Se alcanzó el número máximo de repeticiones sin encontrar una matriz con puntaje mayor a", puntaje_buscado)
    print("Se mostrará la matriz con mejor puntaje obtenida")

# Ordenar las matrices por puntaje en orden descendente
matrices_con_puntajes.sort(key=lambda x: x[1], reverse=True)

# Mantener solo la mejor matriz
mejor_matriz, mejor_puntaje = matrices_con_puntajes[0]

# Imprimir la mejor matriz con su puntaje
print(f"La mejor matriz consiguió un puntaje de {mejor_puntaje}:")
for fila in mejor_matriz:
    print(''.join(fila))
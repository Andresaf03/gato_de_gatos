import re # Importamos la librería de regex para validar el input del usuario.

# Función para calcular el peso de un patrón de victoria dentro de un gatito, parámetros: estado_patron (int), maquina (int).
# Entrada: estado_patron (int), maquina (int), salida: peso (int) positivo.
def calcula_peso_patron(estado_patron, maquina):
    match maquina % 2:
        case 0:  # Para el jugador que usa X (taches).
            match estado_patron:
                case 18:
                    return 5000  # Dos X, uno vacío.
                case 50:
                    return 100  # Dos O, uno vacío.
                case 8:
                    return 2750  # Todo vacío.
                case 12:
                    return 3000  # Un X, dos vacíos.
                case 20:
                    return 300  # Un O, dos vacíos.
                case 125:
                    return 1  # Tres O.
                case 27:
                    return 10000  # Tres X.
                case 30:
                    return 2400 # Un X, un O, un vacío (ligeramente peor que vacío, no es tu turno para mover con profundidad impar).
                case 45:
                    return 1500 # Dos X, un O (te bloquearon).
                case 75: 
                    return 2900 # Dos O, un X (cerraste la amenaza).
                case _:
                    return 2000  # Mantenido como control.
        case 1:  # Para el jugador que usa O (círculos).
            match estado_patron:
                case 18:
                    return 100  # Dos X, uno vacío.
                case 50:
                    return 5000  # Dos O, uno vacío. 
                case 8:
                    return 1500  # Todo vacío.
                case 12:
                    return 300  # Un X, dos vacíos.
                case 20:
                    return 3000  # Un O, dos vacíos.
                case 125:
                    return 10000  # Tres O.
                case 27:
                    return 1  # Tres X.
                case 30:
                    return 2400 # Un X, un O, un vacío (ligeramente peor, no es tu turno para mover con profundidad impar).
                case 45:
                    return 2900 # Dos X, un O (te bloquearon).
                case 75: 
                    return 1500 # Dos O, un X (cerraste la amenaza).
                case _:
                    return 2000 # Mantenido como control.
                
# Función para calcular el peso de un patrón de victoria del tablero para ponderar los pesos, parámetros: estado_patron (int), maquina (int).
# Entrada: estado_patron (int), maquina (int), salida: peso_ponderador (int) positivo.
def calcula_peso_patron_grande(estado_patron, maquina):
    match maquina%2:
        case 0:
            match estado_patron:
                case 18:
                    return 15 # Dos taches uno vacío.
                case 50:
                    return 0.07 # Dos circulos uno vacío.
                case 8:
                    return 1 # Todo vacío.
                case 12:
                    return 4 # Un tache dos vacíos.
                case 20:
                    return 0.25 # Un circulo dos vacíos.
                case 27:
                    return 10000 # Tres taches.
                case 125:
                    return 0 # Tres circulos.
                case 30:
                    return 0.99 # Un X, un O, un vacío.
                case 45:
                    return 0.95 # Dos X, un O.
                case 75: 
                    return 1.05 # Dos O, un X.
                case _:
                    return 1 # Control.
        case 1:
            match estado_patron:
                case 18:
                    return 0.07 # Dos taches uno vacío.
                case 50:
                    return 15 # Dos circulos uno vacío.
                case 8:
                    return 1 # Todo vacío.
                case 12:
                    return 0.25 # Un tache dos vacíos.
                case 20:
                    return 4 # Un circulo dos vacíos.
                case 27:
                    return 0 # Tres taches.
                case 125:
                    return 10000 # Tres circulos.
                case 30:
                    return 0.99 # Un X, un O, un vacío.
                case 45:
                    return 1.05 # Dos X, un O.
                case 75: 
                    return 0.95 # Dos O, un X.
                case _:
                    return 1 # Control.

# Variable global con los posibles patrones de victoria.
patrones_de_victoria = [
    ['a', 'b', 'c'],  # Fila 1.
    ['d', 'e', 'f'],  # Fila 2.
    ['g', 'h', 'i'],  # Fila 3.
    ['a', 'd', 'g'],  # Columna 1.
    ['b', 'e', 'h'],  # Columna 2.
    ['c', 'f', 'i'],  # Columna 3.
    ['a', 'e', 'i'],  # Diagonal \.
    ['c', 'e', 'g']   # Diagonal /.
]

# Clase Nodo para el árbol de decisión sobre el cuál se utiliza el algoritmo Minimax.
# Atributos: hijos (diccionario), papa (Nodo), valor (float), movimiento (str) compuesto de mayúscula y minúscula, 
# es_max (bool) para saber si maximiza o minimiza el algoritmo Minimax, es_hoja (bool) para determinar cuando aplicar la función heurística.
class Nodo:
    def __init__(self, mov, papa=None) -> None:
        self.hijos = {}
        self.papa = papa
        self.valor = None
        self.movimiento = mov
        self.es_max = False  # True si es nodo MAX, False si es MIN.
        self.es_hoja = False  

# Clase Arbol para el árbol de decisión sobre el cuál se utiliza el algoritmo Minimax, 
# cada nivel varía si se realiza minimización o maximización, cada nodo es un movimiento.
# Atributos: raiz (Nodo), nivel (int).
class Arbol:
    def __init__(self, mov) -> None:
        self.raiz = Nodo(mov)
        self.nivel = 0

    # Método para imprimir el árbol de decisión para depurar y observar el comportamiento del algoritmo Minimax.
    # Entrada: nodo_actual (Nodo), nivel (int), salida: impresión de los nodos del árbol.
    def imprimir_arbol(self, nodo_actual=None, nivel=0):
        if nodo_actual is None:
            nodo_actual = self.raiz

        print('  ' * nivel + f"Movimiento: {nodo_actual.movimiento}, Valor: {nodo_actual.valor}, Es hoja: {nodo_actual.es_hoja}")

        for hijo in nodo_actual.hijos.values():
            self.imprimir_arbol(hijo, nivel + 1)

# Clase Gato para el juego del gato_de_gatos, contiene la lógica del juego y el algoritmo Minimax.
class Gato:
    # Constructor de la clase Gato, inicializa el tablero de gato_de_gatos con un diccionario de diccionarios, todo vacío, 
    # los estados son 2: no hay nada, 3: hay tache, 5: hay circulo.
    # Las claves exteriores (A-I) son las letras mayúsculas que representan los 9 sub-tableros
    # y las claves interiores (a-i) son las letras minúsculas que representan las casillas de los sub-tableros.
    def __init__(self):
        self.tablero={
            letra_mayor:{
                'estado': 2,
                'gatitos': {letra_menor: 2 for letra_menor in 'abcdefghi'}
                }
            for letra_mayor in 'ABCDEFGHI'
        }

    # Método para determinar si hay un ganador en el juego del gato_de_gatos.
    # Entrada: self que contiene el tablero actualizado, salida: True si hay un ganador o es gato_de_gatos, False si no lo hay.
    def condicion_victoria(self):
        for patron in patrones_de_victoria: # Analizar los patrones de victoria.
            condicion_victoria = 1
            for i in range(3):
                letra_grande = patron[i].upper()
                condicion_victoria *= self.tablero[letra_grande]['estado'] # Multiplicar los estados de los patrones de victoria.
            if condicion_victoria == 27 or condicion_victoria == 125: # Si hay un ganador (3 X o 3 O en un patrón).
                return True
        # Verificar si todos los estados de las letras mayúsculas son diferentes de 2, es decir, el tablero está lleno, pero no resuelto.
        todos_diferentes_de_2 = all(self.tablero[letra_grande]['estado'] != 2 for letra_grande in 'ABCDEFGHI')
        return todos_diferentes_de_2

    # Método para mostrar el tablero del gato_de_gatos, imprime el tablero con los taches, círculos o si está vacío.
    # Entrada: self que contiene el tablero actualizado, salida: impresión del tablero.
    def mostrar_tablero(self):
        print(" +-------+-------+-------+")
        for linea in ['ABC', 'DEF', 'GHI']:
            for j in range(3):
                print("|", end=" ")
                for letra_mayor in linea:
                    gatito = self.tablero[letra_mayor]['gatitos']
                    for letra_menor in 'abcdefghi'[j*3:(j+1)*3]:
                        if gatito[letra_menor] == 5:
                            print("O", end=" ")
                        elif gatito[letra_menor] == 3:
                            print("X", end=" ")
                        else:
                            print(".", end=" ")
                    print("|", end=" ")
                print()
            print(" +-------+-------+-------+")

    # Función para decidir si el jugador es X o O, parámetro: jugador (número par o impar) .
    # Entrada: jugador (int), salida: 3 (si es par) o 5 (si es impar).
    def decide_jugador(self, jugador): 
            if jugador % 2 == 0:
                return 3
            else:
                return 5
    
    # Función para determinar una puntuación para el estado actual del tablero,
    # combina las evaluaciones de todos los subtableros (analiza_tablero) y las relaciones en el tablero grande (pondera_estados),
    # parámetros: self que contiene el tablero actualizado, maquina (int).
    # Entrada: self que contiene el tablero actualizado, maquina (int) 0 o 1 si es X o O respectivamente, salida: suma (int) de los pesos ponderados.
    def suma_tablero(self, maquina):
        arreglo = self.analiza_tablero(maquina)
        arreglo_ponderado = self.pondera_estados(arreglo, maquina)
        return sum(arreglo_ponderado)

    # Función para ponderar los estados de los subtableros con base en los patrones de victoria del tablero grande,
    # parámetros: arreglo_estados (lista), maquina (int) 0 y 1 si es X o O respectivamente.
    # Entrada: arreglo_estados (lista), maquina (int), salida: resultado (lista) de los pesos ponderados.
    def pondera_estados(self, arreglo_estados, maquina):
        diccionario = {}
        for patron in patrones_de_victoria: # Analizar los patrones de victoria.
            patron_mayuscula = [letra.upper() for letra in patron] # Convertir las letras a mayúsculas para analizar los patrones del tablero grande.
            estado = 1
            for mayuscula in patron_mayuscula:
                estado *= self.tablero[mayuscula]['estado'] # Multiplicar los estados de los patrones de victoria del tablero grande.
            peso_ponderador = calcula_peso_patron_grande(estado, maquina) # Obtener el peso ponderador de los patrones de victoria del tablero grande.
            for mayuscula in patron_mayuscula:
                if mayuscula not in diccionario:
                    diccionario[mayuscula] = peso_ponderador
                else:
                    diccionario[mayuscula] += peso_ponderador

        for key in diccionario: # Ponderar los pesos de los patrones de victoria del tablero grande para cada subtablero.
            if key in ('A', 'C', 'G', 'I'):
                diccionario[key] /= 2.9 # Dar ligera prioridad a los subtableros A, C, G, I.
            elif key in ('B', 'D', 'F', 'H'):
                diccionario[key] /= 2 # Normalizar los subtableros B, D, F, H.
            else:
                diccionario[key] /= 3.75 # Dar prioridad al subtablero E (centro).
        resultado = []

        for ponderador, valor in zip(diccionario.values(), arreglo_estados):
            resultado.append(ponderador * valor) # Ponderar los pesos, multiplicando el valor del arreglo de estados por el valor ponderado.

        return resultado

    # Función para determinar el mejor movimiento en el tablero grande, dado que nos han mandado a un subtablero resuelto,
    # parámetros: jugador (int) positivo, maquina (int) 0 o 1 si es X o O respectivamente.
    # Entrada: jugador (int) positivo, maquina (int) 0/1, salida: letra_mayuscula (str) del mejor movimiento.
    def comodin_tablero(self, jugador, maquina):
        arreglo = self.analiza_tablero_comodin(jugador, maquina) # Analizar el tablero grande con base en los subtableros y patrones de victoria.
        arreglo_ponderados = self.pondera_estados(arreglo, maquina) # Ponderar los estados de los subtableros con base en los patrones de victoria del tablero grande.
        if jugador%2 != maquina%2:
            indice = arreglo_ponderados.index(min(arreglo_ponderados)) # El jugador debería minimizar (Minimax).
        else:
            indice = arreglo_ponderados.index(max(arreglo_ponderados)) # La máquina debería maximizar (Minimax).
        return chr(ord('A') + indice)
        
    # Función para analizar los subtableros y determinar los valores de los mismos, basado en los patrones de victoria,
    # parámetros: maquina (int) 0 o 1 si es X o O respectivamente.
    # Entrada: maquina (int), salida: peso_arreglo (lista) de los valores de los subtableros.
    def analiza_tablero(self, maquina):
            peso_arreglo=[]
            for letra in self.tablero.keys():
                gatito = self.tablero[letra]['gatitos'] # Acceder a los subtableros.
                diccionario = {}
                for patron in patrones_de_victoria: # Analizar los patrones de victoria.
                    estado_patron = 1
                    for minuscula in patron:
                        estado_patron *= gatito[minuscula] # Multiplicar los estados de las casillas según el patrón de victoria.
                    peso = calcula_peso_patron(estado_patron,maquina)
                    for minuscula in patron: # Asignar los valores a cada casilla del subtablero.
                        if minuscula not in diccionario:
                            diccionario[minuscula] = peso
                        else:
                            diccionario[minuscula] += peso
                suma = 0
                for key in diccionario:
                    if key in ('a', 'c', 'g', 'i'): # Normalizar las casillas a, c, g, i.
                        diccionario[key] /= 3
                    elif key in ('b', 'd', 'f', 'h'): # Dar prioridad a las casillas b, d, f, h para no mandar movimientos en general a las esquinas o el centro.
                        diccionario[key] /= 0.8
                    else:
                        diccionario[key] /= 4 # Normalizar la casilla e (centro).
                    suma += diccionario[key]
                peso_arreglo.append(suma) # Regresar la suma de los valores de las casillas del subtablero para tener un valor por gatito (subtablero).

            return peso_arreglo

    # Función para determinar los valores de los subtableros para posteriormente analizar cual se elegirá, 
    # dado que nos envían a un subtablero resuelto (comodí ), parámetros: jugador (int) positivo, maquina (int) 0 o 1 si es X o O respectivamente.
    # Entrada: jugador (int) positivo, maquina (int) 0/1, salida: peso_arreglo (lista) de los valores de los subtableros.
    def analiza_tablero_comodin(self, jugador, maquina):
        peso_arreglo=[]
        for letra in self.tablero.keys(): # Analizar los subtableros.
            if self._es_gatito_resuelto(letra): # Si el subtablero está resuelto.
                if jugador%2 != maquina%2:
                    peso_arreglo.append(float('inf')) # Nunca considerar un subtablero resuelto para el jugador.
                else:
                    peso_arreglo.append(float('-inf')) # Nunca considerar un subtablero resuelto para la máquina.
            else:
                gatito = self.tablero[letra]['gatitos'] # Acceder al diccionario con las llaves y estados.
                arreglo_peso_minuscula=[]
                for patron in patrones_de_victoria: # Analizar los patrones de victoria.
                    estado_patron = 1
                    for i in range(3):
                        estado_patron *= gatito[patron[i]] # Multiplicar los estados de las casillas según el patrón de victoria.
                    peso = calcula_peso_patron(estado_patron,maquina) # Calcular el valor del patrón de victoria.
                    arreglo_peso_minuscula.append(peso) # Hacer un arreglo con los valores de los patrones de victoria.
                peso_arreglo.append(sum(arreglo_peso_minuscula)) # Sumar los valores de los patrones de victoria para tener un valor por gatito (subtablero).
        return peso_arreglo

    # Método "público" para generar el árbol de decisión para el algoritmo Minimax, se realiza el movimiento recibido del jugador y se generan los hijos,
    # parámetros: mov (str) compuesto de mayúscula y minúscula entre la a y la i, jugador (int) positivo, maquina (int) 0 o 1 si es X o O respectivamente.
    # Entrada: mov (str), jugador (int) positivo, maquina (int) 0/1, salida: arbol (Arbol) con el árbol de decisión ya llenado del Minimax.
    def genera_arbol(self, mov, jugador, maquina):
        arbol = Arbol(mov) # Instanciar un árbol de decisión.
        actual = arbol.raiz
        tache_circulo = self.decide_jugador(jugador) # Decidir si el jugador es X o O.
        self.tablero[mov[0]]['gatitos'][mov[1]] = tache_circulo # Realizar el movimiento del jugador.
        self.actualiza_letra_mayor(mov[0]) # Actualizar el estado del subtablero en caso de que se resuelva.

        movimiento_grande = (mov[1]).upper() # Convertir la letra minúscula a mayúscula para acceder al subtablero en el que tiene que jugar.
        profundidad = self.calcular_profundidad(jugador) # Calcular la profundidad del árbol basado en el turno.
        if self._es_gatito_resuelto(movimiento_grande): # Si el subtablero está resuelto, tenemos comodín.
            letra_grande = self.comodin_tablero(jugador+1, maquina)
            mov = letra_grande+(letra_grande).lower() # Movimiento del comodín (accedemos al subtablero que se elige) y mandamos un movimiento "dummie".
            self._genera_arbol(mov, actual, 0, jugador+1, maquina, profundidad)
            self._minimax(actual, True) # Realizar el algoritmo Minimax.
            
        else:
            if not self.condicion_victoria(): # Si no hay un ganador aún o está lleno (gato_de_gatos).
                self._genera_arbol(mov, actual, 0, jugador+1, maquina, profundidad) # Generar el árbol de decisión alternando el jugador.
                self._minimax(actual, True) # Realizar el algoritmo Minimax.
                
        return arbol

    # Método "privado" para generar el árbol de decisión para el algoritmo Minimax, hace los movimientos recursivos para generar el árbol variando el turno X y O,
    # parámetros: mov (str) compuesto de mayúscula y minúscula entre la a y la i, actual (Nodo) raíz del árbol, 
    # contador (int) para la profundidad, jugador (int) positivo que esta vez representa el turno, 
    # maquina (int) 0 o 1 si es X o O respectivamente, profundidad (int).
    # Entrada: mov (str), actual (Nodo), contador (int), jugador (int) positivo, maquina (int) 0/1, profundidad (int), salida: no hay, es la generación del árbol.
    def _genera_arbol(self, mov, actual, contador, jugador, maquina, profundidad):
        if contador == profundidad or (self._es_gatito_resuelto(mov[0]) and contador !=0): # Paso base, si llegamos a la profundidad o el subtablero está resuelto (no es comodín).
            actual.es_hoja = True # Es hoja del árbol.
            actual.valor = self.suma_tablero(maquina) # Calcular el valor de la hoja con la función heurística.
            return

        tache_circulo = self.decide_jugador(jugador) # Decidir si el jugador es X o O según el turno (jugador).
        movimiento_grande = (mov[1]).upper() # Convertir la letra minúscula a mayúscula para acceder al subtablero en el que tiene que jugar.
        tablero_actual = self.tablero[movimiento_grande]['gatitos'] # Acceder al diccionario con las llaves y estados del subtablero.

        hijos_generados = False # No ha generado los hijos en la recursión.
        for mov_temp, estado in tablero_actual.items(): # Para cada movimiento posible y su estado (X, O o vacío).
            if estado == 2: # Si la casilla está vacía.
                movimiento_total = f'{movimiento_grande}{mov_temp}' # Componer el movimiento total
                actual.hijos[movimiento_total] = Nodo(movimiento_total, actual) # Hacer un nodo hijo con el movimiento total.
                actual.hijos[movimiento_total].es_max = not actual.es_max # Cambiar el nivel del nodo hijo (si tiene que minimizar o maximizar).
                self.tablero[movimiento_grande]['gatitos'][mov_temp] = tache_circulo # Realizar el movimiento.
                self.actualiza_letra_mayor(movimiento_grande) # Llamar a la función para actualizar el estado del subtablero si es que cambia.
                self._genera_arbol(movimiento_total, actual.hijos[movimiento_total], contador+1, jugador+1, maquina, profundidad) # Llamar a la recursión, agregando un nivel y variando un turno.
                self.tablero[movimiento_grande]['gatitos'][mov_temp] = 2  # Backtracking para no alterar los subtableros (sus casillas) en la recursión, es decir que cada rama tenga solo los movimientos que se realizaron en ella.
                self.actualiza_letra_mayor(movimiento_grande) # Backtracking para no modificar los estados de los subtableros entre diferentes ramas.
                hijos_generados = True # Se generaron hijos en la recursión.

        if not hijos_generados: # Si no se generaron hijos, es una hoja y calculamos su valor con la función heurística.
            actual.es_hoja = True
            actual.valor = self.suma_tablero(maquina)
            
    # Algoritmo para determinar la profundidad del árbol basado en el turno.
    # Entrada: jugador (int) es decir, el número de turno, salida: profundidad (int) del árbol.
    def calcular_profundidad(self, jugador):
        if jugador <= 30:
            profundidad = 5
        elif jugador <= 45:
            profundidad = 7
        elif jugador <= 65:
            profundidad = 9
        else:
            profundidad = 11
        
        return profundidad
    
    # Método para determinar si un gatito (subtablero) está resuelto, parámetro: letra_mayor (str).
    # Entrada: letra_mayor (str), salida: boolean, True si está resuelto, False si no lo está.
    def _es_gatito_resuelto(self, letra_mayor):
        gatito = self.tablero[letra_mayor]['gatitos'] # Obtener el diccionario con las llaves y estados
        # Verificar si hay un ganador
        for patron in patrones_de_victoria:
            if all(gatito[pos] == 3 for pos in patron) or all(gatito[pos] == 5 for pos in patron):
                return True
        # Verificar si está lleno (gato)
        return all(valor != 2 for valor in gatito.values())

    # Método para actualizar el estado de un gatito (subtablero) y determinar si está resuelto, parámetro: letra_mayor (str).
    # Entrada: letra_mayor (str) que representa un subtablero, salida: no hay, es la actualización del tablero.
    def actualiza_letra_mayor(self, letra_mayor):
        gatito = self.tablero[letra_mayor]['gatitos'] # Obtener el diccionario con las llaves y estados
        bandera = False
        # Verificar si hay un ganador
        for patron in patrones_de_victoria: # Obtener los patrones de victoria.
            if all(gatito[pos] == 3 for pos in patron): # Si está ganado por X
                self.tablero[letra_mayor]['estado'] = 3
                bandera = True # Para el backtracking
            elif all(gatito[pos] == 5 for pos in patron): # Si está ganado por O
                self.tablero[letra_mayor]['estado'] = 5
                bandera = True # Para el backtracking
        if all(valor != 2 for valor in gatito.values()): # Si está lleno (gato)
            self.tablero[letra_mayor]['estado'] = 1 # El tablero esta lleno y nadie gano (Gato)
            bandera = True # Para el backtracking
        if bandera == False: # Si no se actualiza el estado en la función, regresar el valor a 2 (backtracking).
            self.tablero[letra_mayor]['estado'] = 2
    
    # Método para actualizar el tablero completo, determina si cada gatito (subtablero) está resuelto y actualiza su estado.
    # Entrada: self, salida: no hay, es la actualización del tablero.
    def actualiza_tablero(self):
        for letra_mayor in 'ABCDEFGHI':
            self.actualiza_letra_mayor(letra_mayor)

    # Método para aplicar el algoritmo Minimax y determinar el mejor movimiento de la máquina.
    # Entrada: nodo (Nodo) la raíz del arbol generado, es_max (bool) para determinar si en el nivel se maximiza o minimiza, 
    # salida: nodo.valor (float) del mejor movimiento, actualiza el valor de los nodos en la recusión.
    def _minimax(self, nodo, es_max):
        if nodo.es_hoja: # Paso base, viaja hasta las hojas del árbol.
            return nodo.valor

        if es_max: # Si en el nivel hay que maximizar.
            mejor_valor = float('-inf') # El peor valor posible para la máquina.
            for hijo in nodo.hijos.values(): # Accedemos a todos los hijos del nodo.
                valor = self._minimax(hijo, False) # Llamamos a la recusión para obtener el valor, cambiando el nivel para que el siguiente minimice.
                mejor_valor = max(mejor_valor, valor) # Obtiene el mejor valor de los hijos para la máquina.
            nodo.valor = mejor_valor # Actualizamos el valor del nodo después de la recusión, una vez que obtenemos el mejor valor.
        else:
            mejor_valor = float('inf') # El peor valor posible para el jugador.
            for hijo in nodo.hijos.values(): # Accedemos a todos los hijos del nodo.
                valor = self._minimax(hijo, True) # Llamamos a la recusión para obtener el valor, cambiando el nivel para que el siguiente maximice.
                mejor_valor = min(mejor_valor, valor) # Obtiene el mejor valor de los hijos para el jugador.
            nodo.valor = mejor_valor # Actualizamos el valor del nodo después de la recusión, una vez que obtenemos el mejor valor.

        return nodo.valor

    # Método para jugar el juego del gato_de_gatos, se pide al usuario que ingrese si la máquina es X (0) o O (1), 
    # el juego se realiza hasta que exista un ganador o termine en empate (gato_de_gatos). En cada iteración, 
    # se muestra el tablero, se pide al usuario que ingrese su movimiento y se realiza el movimiento de la máquina hasta finalizar el juego.
    # Entrada: self con el tablero en su estado inicial, salida: no hay, es el juego del gato_de_gatos.
    def juega(self):
        jugador = int(input("Ingresa que jugador es la maquina: ")) # Preguntar al usuario si la máquina es X (0) o O (1).
        maquina = 1
        if jugador == 0: # Si la máquina es X, hacer el primer movimiento por ella, Ee.
            self.tablero['E']['gatitos']['e'] = 3
            print("La maquina elige: Ee")
            maquina = 0
        while not self.condicion_victoria(): # Mientras no haya un ganador o sea gato_de_gatos.
            self.mostrar_tablero() # Se muestra el tablero.
            movimiento = input("Movimiento: ") # Se pide al usuario que ingrese su movimiento.
            while not re.match(r'^[A-I][a-i]$', movimiento): # Validar que el movimiento sea válido, es decir, una mayúscula, seguida de una minúscula entre la a y la i.
                movimiento = input("Movimiento inválido. Intenta de nuevo: ")

            arbol = self.genera_arbol(movimiento, jugador+1, maquina) # Generar el árbol de decisión.
            jugador += 2 # Actualizar el turno del jugador.
            if len(arbol.raiz.hijos) != 0 and not self.condicion_victoria(): # Si el árbol tiene hijos y no hay un ganador aún.
                for hijo in arbol.raiz.hijos.values(): # Acceder a los hijos del nodo raíz, que son los nodos de decisión.
                    movimiento = hijo.movimiento[1].upper() 
                    if self._es_gatito_resuelto(movimiento): # Si el subtablero está resuelto, castigar el comodín.
                        hijo.valor = (hijo.valor)*(0.1)
                    if hijo.movimiento[1] == 'e': # Castigar el centro.
                        hijo.valor = hijo.valor * (0.85)
                    if hijo.papa.movimiento[0] == hijo.movimiento[1].upper(): # Castigar el hecho de que regreses a la misma casilla.
                        hijo.valor = (hijo.valor)*(0.99)
                    
                # Obtiene el máximo de la lista (de los items, es decir, los nodos de decisión), comparando cada x por su segundo atributo (valor) que es el estado y regresando la llave [0] máxima.
                mejor_movimiento = max(arbol.raiz.hijos.items(), key=lambda x: x[1].valor)[0]
                print(f"La máquina elige: {mejor_movimiento}") # Comunicar el movimiento de la máquina.

                # Realizar el movimiento de la máquina
                self.tablero[mejor_movimiento[0]]['gatitos'][mejor_movimiento[1]] = self.decide_jugador(jugador)
                self.actualiza_tablero() # Actualizar el tablero completo en caso de que un subtablero se resuelva.

        print("¡Juego terminado!") # Comunicar que el juego ha terminado.
        self.mostrar_tablero() # Mostrar el tablero final.

mi_gato = Gato() # Instanciamos un gato para poder jugar.
mi_gato.juega() # Llamamos al método juega para comenzar el juego.
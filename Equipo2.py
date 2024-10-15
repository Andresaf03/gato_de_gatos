import re
def decide_jugador(jugador):
        if jugador % 2 == 0:
            return 3
        else:
            return 5

def regresa_pos_victoria(pos_victoria, maquina):
    match maquina % 2:
        case 0:  # Para el jugador que usa X (taches)
            match pos_victoria:
                case 18:
                    return 5000  # Dos X, uno vacío 
                case 50:
                    return 100  # Dos O, uno vacío 
                case 8:
                    return 2750  # Todo vacío 
                case 12:
                    return 3000  # Un X, dos vacíos 
                case 20:
                    return 300  # Un O, dos vacíos 
                case 125:
                    return 1  # Tres O 
                case 27:
                    return 10000  # Tres X 
                case 30:
                    return 2400 # Un X, un O, un vacío (ligeramente peor, no es tu turno para mover con prof impar)
                case 45:
                    return 1500 # Dos X, un O (te bloquearon pero posiblemente hay más juego) 
                case 75: 
                    return 2900 # Dos O, un X (cerraste la amenaza)
                case _:
                    return 2000  # Mantenido como control
        case 1:  # Para el jugador que usa O (círculos)
            match pos_victoria:
                case 18:
                    return 100  # Dos X, uno vacío 
                case 50:
                    return 5000  # Dos O, uno vacío 
                case 8:
                    return 1500  # Todo vacío 
                case 12:
                    return 300  # Un X, dos vacíos 
                case 20:
                    return 3000  # Un O, dos vacíos 
                case 125:
                    return 10000  # Tres O 
                case 27:
                    return 1  # Tres X
                case 30:
                    return 2400 # Un X, un O, un vacío (ligeramente peor, no es tu turno para mover con prof impar)
                case 45:
                    return 2900 # Dos X, un O (te bloquearon pero posiblemente hay más juego) 
                case 75: 
                    return 1500 # Dos O, un X (cerraste la amenaza)
                case _:
                    return 2000 # Mantenido como control

def regresa_pos_victoria_grande(pos_victoria, maquina):
    match maquina%2:
        case 0:
            match pos_victoria:
                case 18:
                    return 15 # Dos taches uno vacio
                case 50:
                    return 0.07 # Dos circulos uno vacio
                case 8:
                    return 1 # Todo vacio
                case 12:
                    return 4 # Un tache dos vacios
                case 20:
                    return 0.25 # Un circulo dos vacios
                case 27:
                    return 10000 # Tres taches
                case 125:
                    return 0 # Tres circulos
                case 30:
                    return 0.99 # Un X, un O, un vacío 
                case 45:
                    return 1 # Dos X, un O 
                case 75: 
                    return 1 # Dos O, un X 
                case _:
                    return 1 # Control
        case 1:
            match pos_victoria:
                case 18:
                    return 0.07 # Dos taches uno vacio
                case 50:
                    return 15 # Dos circulos uno vacio
                case 8:
                    return 1 # Todo vacio
                case 12:
                    return 0.25 # Un tache dos vacios
                case 20:
                    return 4 # Un circulo dos vacios
                case 27:
                    return 0 # Tres taches
                case 125:
                    return 10000 # Tres circulos
                case 30:
                    return 1.01 # Un X, un O, un vacío 
                case 45:
                    return 1 # Dos X, un O 
                case 75: 
                    return 1 # Dos O, un X 
                case _:
                    return 1 # Control

patrones_de_victoria = [
    ['a', 'b', 'c'],  # Fila 1
    ['d', 'e', 'f'],  # Fila 2
    ['g', 'h', 'i'],  # Fila 3
    ['a', 'd', 'g'],  # Columna 1
    ['b', 'e', 'h'],  # Columna 2
    ['c', 'f', 'i'],  # Columna 3
    ['a', 'e', 'i'],  # Diagonal \
    ['c', 'e', 'g']   # Diagonal /
]

class Nodo:
    def __init__(self, mov, papa=None) -> None:
        self.hijos = {}
        self.papa = papa
        self.valor = None
        self.movimiento = mov
        self.es_max = False  # True si es nodo MAX, False si es MIN
        self.es_hoja = False  # Nuevo atributo para identificar hojas

class Arbol:
    def __init__(self, mov) -> None:
        self.raiz = Nodo(mov)
        self.nivel = 0

    def imprimir_arbol(self, nodo_actual=None, nivel=0):
        if nodo_actual is None:
            nodo_actual = self.raiz

        print('  ' * nivel + f"Movimiento: {nodo_actual.movimiento}, Valor: {nodo_actual.valor}, Es hoja: {nodo_actual.es_hoja}")

        for hijo in nodo_actual.hijos.values():
            self.imprimir_arbol(hijo, nivel + 1)

class Gato:
        # 2: no hay nada, 3: hay tache, 5: hay circulo
    def __init__(self):
        self.tablero={
            letra_mayor:{
                'estado': 2,
                'gatitos': {letra_menor: 2 for letra_menor in 'abcdefghi'}
                }
            for letra_mayor in 'ABCDEFGHI'
        }

    def cond_victoria(self):
        for patron in patrones_de_victoria:
            cond_victoria = 1
            for i in range(3):
                letra_grande = patron[i].upper()
                cond_victoria *= self.tablero[letra_grande]['estado']
            if cond_victoria == 27 or cond_victoria == 125:
                return True
        # Verificar si todos los estados de las letras mayúsculas son diferentes de 2
        todos_diferentes_de_2 = all(self.tablero[letra_grande]['estado'] != 2 for letra_grande in 'ABCDEFGHI')
        return todos_diferentes_de_2


    def mostrar_tablero(self):
        print(" +-------+-------+-------+")
        for row in ['ABC', 'DEF', 'GHI']:
            for j in range(3):
                print("|", end=" ")
                for letra_mayor in row:
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

    def decide_jugador(self, jugador):
        if jugador % 2 == 0:
            return 3
        else:
            return 5
    
    def suma_tablero(self, maquina):
        array = self.analiza_tablero(maquina)
        array_ponderado = self.pondera_estados_comodin(array, maquina)
        return sum(array_ponderado)

    def pondera_estados_comodin(self, array_estados, maquina):
        diccionario = {}
        for patron in patrones_de_victoria:
            patron_mayuscula = [letra.upper() for letra in patron]
            estado = 1
            for mayuscula in patron_mayuscula:
                estado *= self.tablero[mayuscula]['estado']
            peso_ponderador = regresa_pos_victoria_grande(estado, maquina)
            for mayuscula in patron_mayuscula:
                if mayuscula not in diccionario:
                    diccionario[mayuscula] = peso_ponderador
                else:
                    diccionario[mayuscula] += peso_ponderador

        for key in diccionario:
            if key in ('A', 'C', 'G', 'I'):
                diccionario[key] /= 2.9
            elif key in ('B', 'D', 'F', 'H'):
                diccionario[key] /= 2
            else:
                diccionario[key] /= 3.75
        resultado = []

        for clave, valor in zip(diccionario.values(), array_estados):
            resultado.append(clave * valor)

        return resultado


    def comodin_tablero(self, jugador, maquina):
        # SI ES MAX FULL ATAQUE MIN FULL DEFENSA
        array = self.analiza_tablero_comodin(jugador, maquina)
        # PONDERAR PESOS ARRAY CON BASE EN LOS PATRONES DE VICTORIA DEL TABLERO GRANDE
        array_ponderados = self.pondera_estados_comodin(array, maquina)
        if jugador%2 != maquina%2:
            indice = array_ponderados.index(min(array_ponderados))
        else:
            indice = array_ponderados.index(max(array_ponderados))
        return chr(ord('A') + indice)
        
    def analiza_tablero(self, maquina):
            # Checar si hay posible patron de victoria de los grandes
            peso_array=[]
            for letra in self.tablero.keys():
                gatito = self.tablero[letra]['gatitos']
                diccionario = {}
                for patron in patrones_de_victoria:
                    pos_victoria = 1
                    for minuscula in patron:
                        pos_victoria *= gatito[minuscula]
                    peso = regresa_pos_victoria(pos_victoria,maquina)
                    for minuscula in patron:
                        if minuscula not in diccionario:
                            diccionario[minuscula] = peso
                        else:
                            diccionario[minuscula] += peso
                suma = 0
                for key in diccionario:
                    if key in ('a', 'c', 'g', 'i'):
                        diccionario[key] /= 3
                    elif key in ('b', 'd', 'f', 'h'):
                        diccionario[key] /= 0.8
                    else:
                        diccionario[key] /= 4
                    suma += diccionario[key]
                peso_array.append(suma)

            return peso_array

    def analiza_tablero_comodin(self, jugador, maquina):
        # Checar si hay posible patron de victoria de los grandes
        peso_array=[]
        for letra in self.tablero.keys():
            if self._es_gatito_resuelto(letra):
                if jugador%2 != maquina%2:
                    peso_array.append(float('inf'))
                else:
                    peso_array.append(float('-inf'))
            else:
                gatito = self.tablero[letra]['gatitos']
                pesito_array=[]
                for patron in patrones_de_victoria:
                    pos_victoria = 1
                    for i in range(3):
                        pos_victoria *= gatito[patron[i]]
                    peso = regresa_pos_victoria(pos_victoria,maquina)
                    pesito_array.append(peso)
                peso_array.append(sum(pesito_array))
        return peso_array

    def genera_arbol(self, mov, jugador, maquina):
        arbolito = Arbol(mov)
        actual = arbolito.raiz
        tache_circulo = self.decide_jugador(jugador)
        self.tablero[mov[0]]['gatitos'][mov[1]] = tache_circulo
        self.actualiza_letra_mayor(mov[0])

        movimiento_grande = (mov[1]).upper()
        profundidad = self.calcular_profundidad(jugador)
        if self._es_gatito_resuelto(movimiento_grande):
            letra_big = self.comodin_tablero(jugador+1, maquina)
            mov = letra_big+(letra_big).lower()
            self._genera_arbol(mov, actual, 0, jugador+1, maquina, profundidad)
            self._minimax(actual, True)
            
        else:
            if not self.cond_victoria():
                self._genera_arbol(mov, actual, 0, jugador+1, maquina, profundidad)
                self._minimax(actual, True)
                
        return arbolito

    def _genera_arbol(self, mov, actual, contador, jugador, maquina, profundidad):
        if contador == profundidad or (self._es_gatito_resuelto(mov[0]) and contador !=0):
            actual.es_hoja = True
            actual.valor = self.suma_tablero(maquina)
            return

        tache_circulo = self.decide_jugador(jugador)
        movimiento_grande = (mov[1]).upper()
        tablero_actual = self.tablero[movimiento_grande]['gatitos']

        hijos_generados = False
        for mov_temp, estado in tablero_actual.items():
            if estado == 2:
                movimiento_total = f'{movimiento_grande}{mov_temp}'
                actual.hijos[movimiento_total] = Nodo(movimiento_total, actual)
                actual.hijos[movimiento_total].es_max = not actual.es_max
                self.tablero[movimiento_grande]['gatitos'][mov_temp] = tache_circulo
                self.actualiza_letra_mayor(movimiento_grande)
                self._genera_arbol(movimiento_total, actual.hijos[movimiento_total], contador+1, jugador+1, maquina, profundidad)
                self.tablero[movimiento_grande]['gatitos'][mov_temp] = 2  # Backtracking
                self.actualiza_letra_mayor(movimiento_grande) # Backtracking
                hijos_generados = True

        if not hijos_generados:
            actual.es_hoja = True
            actual.valor = self.suma_tablero(maquina)
            
        # Algoritmo para determinar la depth basado en el turno
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
    
    def _es_gatito_resuelto(self, letra_mayor):
        # Implementa la lógica para determinar si un gatito está resuelto
        # Por ejemplo, verificar si hay un ganador o si está lleno
        gatito = self.tablero[letra_mayor]['gatitos']
        # Verificar si hay un ganador
        for patron in patrones_de_victoria:
            if all(gatito[pos] == 3 for pos in patron) or all(gatito[pos] == 5 for pos in patron):
                return True
        # Verificar si está lleno
        return all(valor != 2 for valor in gatito.values())

    def actualiza_letra_mayor(self, letra_mayor):
        # Implementa la lógica para determinar si un gatito está resuelto
        # Por ejemplo, verificar si hay un ganador o si está lleno
        gatito = self.tablero[letra_mayor]['gatitos']
        bandera = False
        # Verificar si hay un ganador
        for patron in patrones_de_victoria:
            if all(gatito[pos] == 3 for pos in patron):
                self.tablero[letra_mayor]['estado'] = 3
                bandera = True
            elif all(gatito[pos] == 5 for pos in patron):
                self.tablero[letra_mayor]['estado'] = 5
                bandera = True
        if all(valor != 2 for valor in gatito.values()):
            self.tablero[letra_mayor]['estado'] = 1 # El tablero esta lleno y nadie gano (Gato)
            bandera = True
        if bandera == False:
            self.tablero[letra_mayor]['estado'] = 2
            
    def actualiza_tablero(self):
        for letra_mayor in 'ABCDEFGHI':
            self.actualiza_letra_mayor(letra_mayor)

    def _minimax(self, nodo, es_max):
        if nodo.es_hoja:
            return nodo.valor

        if es_max:
            mejor_valor = float('-inf')
            for hijo in nodo.hijos.values():
                valor = self._minimax(hijo, False)
                mejor_valor = max(mejor_valor, valor)
            nodo.valor = mejor_valor
        else:
            mejor_valor = float('inf')
            for hijo in nodo.hijos.values():
                valor = self._minimax(hijo, True)
                mejor_valor = min(mejor_valor, valor)
            nodo.valor = mejor_valor

        return nodo.valor

    def juega(self):
        jugador = int(input("Ingresa que jugador es la maquina: "))
        maquina = 1
        if jugador == 0:
            self.tablero['E']['gatitos']['e'] = 3
            print("La maquina elige: Ee")
            maquina = 0
        while not self.cond_victoria():
            self.mostrar_tablero()
            movimiento = input("Movimiento: ")
            while not re.match(r'^[A-I][a-i]$', movimiento):
                movimiento = input("Movimiento inválido. Intenta de nuevo: ")

            arbol = self.genera_arbol(movimiento, jugador+1, maquina) # Si maquina es 0: True, Si maquina es 1: False
            jugador += 2
            if len(arbol.raiz.hijos) != 0 and not self.cond_victoria():
                for hijo in arbol.raiz.hijos.values():
                    movimiento = hijo.movimiento[1].upper()
                    if self._es_gatito_resuelto(movimiento):
                        hijo.valor = (hijo.valor)*(0.1)
                    if hijo.movimiento[1] == 'e':
                        hijo.valor = hijo.valor * (0.85)
                    if hijo.papa.movimiento[0] == hijo.movimiento[1].upper():
                        hijo.valor = (hijo.valor)*(0.99)
                    
                # Obtiene el máximo de la lista (de los items), comparando cada x por su segundo atributo (valor) que es el estado y regresando la llave [0] maxima
                mejor_movimiento = max(arbol.raiz.hijos.items(), key=lambda x: x[1].valor)[0]
                print(f"La máquina elige: {mejor_movimiento}")

                # Realizar el movimiento de la máquina
                self.tablero[mejor_movimiento[0]]['gatitos'][mejor_movimiento[1]] = self.decide_jugador(jugador)
                self.actualiza_tablero()

        print("¡Juego terminado!")
        self.mostrar_tablero()

mi_gato = Gato()
mi_gato.juega()
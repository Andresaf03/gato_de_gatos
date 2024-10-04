import re
def decide_jugador(jugador):
        if jugador % 2 == 0:
            return 3
        else:
            return 5

def regresa_pos_victoria(pos_victoria, jugador):
    match jugador%2:
        case 1:
            match pos_victoria:
                case 18:
                    return 50 # Dos taches uno vacio
                case 50:
                    return -15 # Dos circulos uno vacio
                case 8:
                    return 1 # Todo vacio
                case 12:
                    return 3 # Un tache dos vacios
                case 20:
                    return -3 # Un circulo dos vacios
                case _:
                    return 0 # Uno de cada uno o linea llena
        case 0:
            match pos_victoria:
                case 18:
                    return 15 # Dos taches uno vacio
                case 50:
                    return -50 # Dos circulos uno vacio
                case 8:
                    return -1 # Todo vacio
                case 12:
                    return 3 # Un tache dos vacios
                case 20:
                    return -3 # Un circulo dos vacios
                case _:
                    return 0 # Uno de cada uno o linea llena


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
        self.es_max = True  # True si es nodo MAX, False si es MIN
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
                'estado': 0,
                'gatitos': {letra_menor: 2 for letra_menor in 'abcdefghi'}
                }
            for letra_mayor in 'ABCDEFGHI'
        }

    def cond_victoria(self):
        for patron in patrones_de_victoria:
            cond_victoria=0
            for i in range(3):
                letra_grande = patron[i].upper()
                cond_victoria *= self.tablero[letra_grande]['estado']
            if cond_victoria == 18 or cond_victoria == 50:
                return True
        return False


    def mostrar_tablero(self):
        print(" +-------+-------+-------+")
        for i, row in enumerate(['ABC', 'DEF', 'GHI']):
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

    def analiza_tablero(self, jugador):
        # Checar si hay posible patron de victoria de los grandes
        peso_array=[]
        for letra in self.tablero.keys():
            gatito = self.tablero[letra]['gatitos']
            pesito_array=[]
            for patron in patrones_de_victoria:
                pos_victoria = 1
                for i in range(3):
                    pos_victoria *= gatito[patron[i]]
                peso = regresa_pos_victoria(pos_victoria,jugador)
                pesito_array.append(peso)
            peso_array.append(sum(pesito_array))
        return sum(peso_array)

    def genera_arbol(self, mov, jugador):
        arbolito = Arbol(mov)
        actual = arbolito.raiz
        tache_circulo = self.decide_jugador(jugador+1)
        self.tablero[mov[0]]['gatitos'][mov[1]] = tache_circulo
        self._genera_arbol(mov, actual, 0, jugador)
        self._minimax(actual, True)
        return arbolito

    def _genera_arbol(self, mov, actual, contador, jugador):
        if contador == 4 or self._es_gatito_resuelto(mov[0]):
            actual.es_hoja = True
            actual.valor = self.analiza_tablero(jugador)
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
                self._genera_arbol(movimiento_total, actual.hijos[movimiento_total], contador+1, jugador+1)
                self.tablero[movimiento_grande]['gatitos'][mov_temp] = 2  # Backtracking
                hijos_generados = True

        if not hijos_generados:
            actual.es_hoja = True
            actual.valor = self.analiza_tablero(jugador)

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
        if jugador == 0:
            self.tablero['A']['gatitos']['a'] = 3
            print("La maquina elige: Aa")
        while not self.cond_victoria():
            self.mostrar_tablero()
            movimiento = input("Movimiento: ")
            while not re.match(r'^[A-I][a-i]$', movimiento):
                movimiento = input("Movimiento inválido. Intenta de nuevo: ")

            arbol = self.genera_arbol(movimiento, jugador)
            mejor_movimiento = max(arbol.raiz.hijos.items(), key=lambda x: x[1].valor)[0]
            print(f"La máquina elige: {mejor_movimiento}")

            # Realizar el movimiento de la máquina
            self.tablero[mejor_movimiento[0]]['gatitos'][mejor_movimiento[1]] = self.decide_jugador(jugador)

            if self.cond_victoria():
                print("¡Juego terminado!")
                self.mostrar_tablero()
                break

mi_gato = Gato()
mi_gato.juega()
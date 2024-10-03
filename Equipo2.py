def decide_jugador(jugador):
        if jugador % 2 == 0:
            return 3
        else:
            return 5
        
def regresa_pos_victoria(pos_victoria, jugador):
    match jugador%2:
        case 0:
            match pos_victoria:
                case 18:
                    return 25 # Dos taches uno vacio
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
        case 1:
            match pos_victoria:
                case 18:
                    return -15 # Dos taches uno vacio
                case 50:
                    return 25 # Dos circulos uno vacio
                case 8:
                    return 1 # Todo vacio
                case 12:
                    return -3 # Un tache dos vacios
                case 20:
                    return 3 # Un circulo dos vacios
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
        self.hijos={}
        self.papa= papa
        self.valor=None
        self.movimiento=mov

class Arbol:
    def __init__(self, mov) -> None:
        self.raiz = Nodo(mov)
        self.nivel = 0

    def imprimir_arbol(self, nodo_actual=None, nivel=0):
        if nodo_actual is None:
            nodo_actual = self.raiz

        # Imprime el nodo actual con su nivel de profundidad
        print('  ' * nivel + f"Movimiento: {nodo_actual.movimiento}")

        # Recorre los hijos de este nodo
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
        
    def genera_arbol(self,mov,jugador):
        arbolito = Arbol(mov)
        actual = arbolito.raiz
        tache_circulo = decide_jugador(jugador+1)
        self.tablero[mov[0]]['gatitos'][mov[1]] = tache_circulo
        self._genera_arbol(mov,actual,0, jugador)
        return arbolito
        

    def _genera_arbol(self, mov, actual, contador, jugador):
        if contador == 2:
            return
        tache_circulo = decide_jugador(jugador)
        movimiento_grande = (mov[1]).upper()
        tablero_actual = self.tablero[movimiento_grande]['gatitos']
        for mov_temp,estado in tablero_actual.items():
            if estado == 2:
                movimiento_total = f'{movimiento_grande}{mov_temp}'
                actual.hijos[movimiento_total] =  Nodo(movimiento_total, actual)
                self.tablero[movimiento_grande]['gatitos'][mov_temp] = tache_circulo
                self._genera_arbol(movimiento_total, actual.hijos[movimiento_total], contador+1, jugador+1)
                actual.valor = self.analiza_tablero(jugador)
                self.tablero[movimiento_grande]['gatitos'][mov_temp] = 2  # Backtracking
    
    def juega(self):
        jugador = int(input("Ingresa que jugador es la maquina: "))
        while self.cond_victoria == False:
            self.mostrar_tablero()
            #While regex not valido:
            movimiento = str(input("Movimiento: "))
            regex = r'^[A-I][a-i]$'
            while movimiento != regex:
                movimiento = input("Movimiento: ")
            if self.cond_victoria == False:
                self.genera_arbol(movimiento,jugador)
            
    
mi_gato = Gato()
mi_gato.mostrar_tablero()
mi_arbol =  mi_gato.genera_arbol('Ae',0)
mi_gato.mostrar_tablero()
mi_arbol.imprimir_arbol()
print(mi_gato.analiza_tablero(1))
mi_gato.juega()

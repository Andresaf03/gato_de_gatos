def decide_jugador(jugador):
        if jugador % 2 == 0:
            return 3
        else:
            return 5

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
        self.gato={
            letra_mayor:{
                'estado': 0,
                'gatitos': {letra_menor: 2 for letra_menor in 'abcdefghi'}
                }
            for letra_mayor in 'ABCDEFGHI'
        }

    def mostrar_tablero(self):
        for letra_mayor, contenido in self.gato.items():
            estado = contenido['estado']
            gatitos = contenido['gatitos']
            print(f"{letra_mayor} (estado: {estado}): {gatitos}")

    def decide_jugador(jugador):
        if jugador % 2 == 0:
            return 3
        else:
            return 5
        
    def genera_arbol(self,mov,jugador):
        arbolito = Arbol(mov)
        actual = arbolito.raiz

        tache_circulo = decide_jugador(jugador+1)

        self.gato[mov[0]]['gatitos'][mov[1]] = tache_circulo
        self._genera_arbol(mov,actual,0, jugador)
        return arbolito
        

    def _genera_arbol(self, mov, actual, contador, jugador):
        if contador == 2:
            return
        
        tache_circulo = decide_jugador(jugador)

        movimiento_grande = (mov[1]).upper()
        tablero_actual = self.gato[movimiento_grande]['gatitos']

        for mov_temp,estado in tablero_actual.items():
            
            if estado == 2:
                movimiento_total = f'{movimiento_grande}{mov_temp}'
                actual.hijos[movimiento_total] =  Nodo(movimiento_total, actual)

                self.gato[movimiento_grande]['gatitos'][mov_temp] = tache_circulo

                self._genera_arbol(movimiento_total, actual.hijos[movimiento_total], contador+1, jugador+1)

                # Backtracking
                self.gato[movimiento_grande]['gatitos'][mov_temp] = 2 


mi_gato = Gato()
mi_gato.mostrar_tablero()
mi_arbol =  mi_gato.genera_arbol('Ae',0)
mi_arbol.imprimir_arbol()

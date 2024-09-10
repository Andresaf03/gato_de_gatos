class gato:
    def __init__(self):
        self.gato={
            letra_mayor:{
                'estado': None,
                'gatitos': {letra_menor: None for letra_menor in 'abcdefghi'}
                }
            for letra_mayor in 'ABCDEFGHI'
        }
    
    def mostrar_tablero(self):
        for letra_mayor, contenido in self.gato.items():
            estado = contenido['estado']
            gatitos = contenido['gatitos']
            print(f"{letra_mayor} (estado: {estado}): {gatitos}")


mi_gato = gato()
mi_gato.mostrar_tablero()
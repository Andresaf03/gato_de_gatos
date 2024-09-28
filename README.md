# gato_de_gatos
Primer proyecto de programación para la materia de Inteligencia Artificial ITAM Otoño 2024

# Descripción del juego
Esta solución de Inteligencia Arificial se implementa para el juego de "Gato de gatos" o "Ultimate Tic-Tac-Toe". El tablero de este juego tiene una cuadrícula de 9x9, dividida en células más pequeñas de 3x3 como se muestra a continuación:

![ultimate-tic-tac-toe](assets/ultimate-tic-tac-toe.png)

Los jugadores se turnan para jugar en los gatos más pequeños (células 3x3), colocando una cruz o un círculo en una de las casillas del gato pequeño. Este proceso involucra **dos tipos de 'figuras'** (cruces y círculos) que los jugadores colocan según el turno que sea. Esto continúa hasta que algún jugador gane en el gato grande (cuadrícula 9x9). 

Para ganar uno de los gatos pequeños, se tienen que colocar **tres fichas en línea** de la misma figura. Esta línea se puede conseguir horizontalmente, verticalmente o diagonalmente, y, una vez que se logre este patrón, se coloca una figura grande en esa célula para indicar que ese gato pequeño ha sido ganado por tal figura. 

Es importante mencionar que, en el gato, los empates pueden ocurrir (ningún jugador gana). En este caso, se coloca una 'G' como la figura de la célula para indicar empate (o gato - otro nombre para el empate en este domino). Los empates en las células pequeñas no se considerarán como comodín, sino como una célula muerta que ningún jugador puede reclamar. 

Siguientemente, para ganar el "Gato de gatos" es necesario satisfacer la misma condición en la cuadrícula 9x9 que en las células 3x3. Es decir, algún jugador deberá conseguir **tres fichas 'grandes' en línea** para poder reclamar la victoria. También pueden ocurrir empates en el "Gato de gatos", aunque es menos común que en el juego tradicional.

Finalmente, existe una regla que provoca que el "Gato de gatos" sea un **juego más estratégico** y genera que los jugadores piensen más sus movimientos y no solamente se concentren en las células. Esta regla consiste en algo llamado **movimiento vinculado**, es decir, el movimiento que haces en un gato pequeño determina en cuál de los otros gatos pequeños tu oponente debe jugar su siguiente turno. Por ejemplo, si juegas en la casilla central de un gato pequeño, tu oponente debe jugar en el gato pequeño que ocupa esa posición en la cuadrícula grande (casilla 3x3 central). El flujo del juego se ilustra con la siguiente imágen:

![flujo_ultimate-tic-tac-toe](assets/flujo_ultimate_tic-tac-toe.png)
En este caso, el primer jugador colocó una cruz en la esquina superior derecha del gato pequeño central. Por lo que el segundo jugador deberá colocar su círculo en alguna de las casillas del gato pequeño de la esquina superior derecha.

# Ejecución del programa
Al correr, hay que ingresar como parámetro el turno en el que va a jugar la computadora (cruz o cículo). Posteriormente, dependiendo del turno que sea, ingresaremos, como instrucción, la casilla en la que el jugador colocó la ficha **(la máquina siempre tomará la primera jugada como cruz y la segunda como círculo)**. 

De esta forma, la máquina correrá los algoritmos correspondiendtes para determinar en que casilla jugará ella (devolverá el movimiento en el mismo formato de instrucción) y el juego continuará hasta que exista un ganador. Esta instrucción deberá ser ingresada como un par de letras, la primera mayúscula y la segunda minúscula. La primera letra indica en que casilla 3x3 se jugará y la segunda letra indica en que casilla del gato pequeño se colocará la ficha que toca. Por ejemplo, la instrucción 'Ec' indica que se jugará en la casilla central y se colocará una ficha (cruz o círculo) en la esquina superior derecha de ese gato pequeño. La siguiente imagen ilustra la nomenclatura de las casillas:

![nomenclatura_ultimate-tic-tac-toe](assets/nomenclatura_ultimate-tic-tac-toe.png)
Cada célula se representa por una letra mayúscula {A-I} y cada casilla de un gato pequeño se representa por un par de letras {A-I}{a-i}.

# Explicación de la solución
La solución consiste en un archivo `.py` que, al ejecutarlo, podemos interactuar, mediante la terminal, para llevar a cabo el juego. Este archivo `.py` llamado `Equipo2.py` no contiene librerías importadas y está basado en la última versión de Python `Python 3.12.3`.

## Clases

## Funciones

## Constantes
"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""

from entorno import Agente
import random

class MiAgente(Agente):
    """
    Tu agente de navegación.

    Implementa el método decidir() para que el agente
    llegue del punto A al punto B en el grid.
    """

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        #este puntero hara que pueda retroceder
        self.visitados = set()

        # Puedes agregar atributos aquí si los necesitas.
        # Ejemplo:
        #   self.pasos = 0
        #   self.memoria = {}

    def al_iniciar(self):
        self.visitados = set()

    def decidir(self, percepcion):

        posicion = percepcion['posicion']
        self.visitados.add(posicion)

        # d es direccion
        for d in self.ACCIONES:
            if percepcion[d] == 'meta':
                return d
            
        mejor_direccion = None
        peor_utilidad = -999

        vertical, horizontal = percepcion.get('direccion_meta', (None, None))

        for d in self.ACCIONES:
            estado = percepcion[d]
            if estado == 'libre':
                utilidad = 0
                df, dc = self.DELTAS[d]
                siguiente_posicion = (posicion[0] + df, posicion[1] + dc)
                if d == vertical or d == horizontal:
                    utilidad += 10
                if siguiente_posicion in self.visitados:
                    utilidad -= 5
                if siguiente_posicion not in self.visitados:
                    utilidad += 2

                utilidad += random.uniform(0, 0.5)

                if utilidad > peor_utilidad:
                    peor_utilidad = utilidad
                    mejor_direccion = d
        if mejor_direccion:
            return mejor_direccion
        
        for d in self.ACCIONES:
            if percepcion[d] == 'libre':
                return d
        return random.choice(self.ACCIONES)
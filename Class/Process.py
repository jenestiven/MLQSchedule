class Proceso:
    def __init__(self, etiqueta, tiempo_cpu, tiempo_llegada, cola, prioridad):
        """
        Inicializa una instancia de la clase Proceso.

        :param etiqueta: Identificador del proceso.
        :param tiempo_cpu: Tiempo total de CPU que requiere el proceso.
        :param tiempo_llegada: Tiempo en que el proceso llega al sistema.
        :param cola: Tipo de cola a la que pertenece el proceso (1, 2, o 3).
        :param prioridad: Prioridad del proceso (número entero donde un número menor puede indicar mayor prioridad).
        """
        self.etiqueta = etiqueta  # Identificador del proceso
        self.tiempo_cpu = tiempo_cpu  # Tiempo total de CPU necesario para el proceso
        self.tiempo_llegada = tiempo_llegada  # Tiempo en que el proceso está disponible para ser ejecutado
        self.tiempo_restante = tiempo_cpu  # Tiempo restante de CPU que le queda al proceso
        self.cola = cola  # Cola a la que pertenece el proceso
        self.prioridad = prioridad  # Prioridad del proceso
        self.tiempo_inicio = 0  # Tiempo en que se inicia la ejecución del proceso
        self.tiempo_finalizacion = 0  # Tiempo en que se completa la ejecución del proceso
        self.tiempo_espera = 0  # Tiempo que ha pasado el proceso en espera
        self.tiempo_respuesta = 0  # Tiempo que pasa desde que llega hasta que empieza a ejecutarse
        self.turnaround_time = 0  # Tiempo total desde que llega hasta que finaliza
        self.finalizado = False  # Estado que indica si el proceso ha sido completado

    def __str__(self):
        """
        Devuelve una representación en forma de cadena del proceso, mostrando su información básica.

        :return: Cadena que representa el proceso.
        """
        return f"{self.etiqueta}: CPU={self.tiempo_cpu}, Llegada={self.tiempo_llegada}, Cola={self.cola}, Prioridad={self.prioridad}"

from collections import deque

class Cola:
    def __init__(self, tipo, quantum=None):
        """
        Inicializa una cola para la gestión de procesos.

        :param tipo: Tipo de cola (por ejemplo, "RR" para Round Robin o "SJF" para Shortest Job First).
        :param quantum: Tiempo de quantum para la cola de tipo RR, si aplica.
        """
        self.procesos = deque()  # Inicializa la cola de procesos como una deque (cola doble).
        self.tipo = tipo  # Tipo de cola (RR, SJF, etc.).
        self.quantum = quantum  # Tiempo de quantum para la planificación RR.

    def agregar_proceso(self, proceso):
        """
        Agrega un proceso a la cola.

        :param proceso: Instancia del objeto Proceso a ser agregado a la cola.
        """
        self.procesos.append(proceso)  # Agrega el proceso al final de la cola.

    def ejecutar_rr(self, quantum, tiempo_actual):
        """
        Ejecuta un proceso usando el algoritmo Round Robin (RR).

        :param quantum: Tiempo de quantum para la ejecución.
        :param tiempo_actual: Tiempo actual del sistema.
        :return: Tupla que contiene el proceso ejecutado y el tiempo actualizado.
        """
        if not self.procesos:  # Verifica si la cola está vacía.
            return None, tiempo_actual  # No hay procesos para ejecutar.

        proceso_actual = self.procesos.popleft()  # Obtiene el primer proceso de la cola.

        # Marca el tiempo de inicio y calcula el tiempo de respuesta si es la primera vez que se ejecuta.
        if proceso_actual.tiempo_inicio == 0:
            proceso_actual.tiempo_inicio = tiempo_actual  # Marca el tiempo de inicio.
            proceso_actual.tiempo_respuesta = proceso_actual.tiempo_inicio - proceso_actual.tiempo_llegada  # Calcula RT.

        tiempo_prev = tiempo_actual  # Guarda el tiempo anterior antes de ejecutar.

        # Verifica si el tiempo restante del proceso es mayor que el quantum.
        if proceso_actual.tiempo_restante > quantum:
            proceso_actual.tiempo_restante -= quantum  # Reduce el tiempo restante del proceso.
            tiempo_actual += quantum  # Avanza el tiempo actual en el quantum.
            self.procesos.append(proceso_actual)  # Reagrega el proceso al final de la cola.
        else:
            tiempo_actual += proceso_actual.tiempo_restante  # Actualiza el tiempo actual.
            proceso_actual.tiempo_restante = 0  # Marca el proceso como completado.
            proceso_actual.finalizado = True  # Indica que el proceso ha finalizado.
            proceso_actual.tiempo_finalizacion = tiempo_actual  # Registra el tiempo de finalización.
            # Calcula el tiempo de espera y turnaround.
            proceso_actual.turnaround_time = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_llegada
            proceso_actual.tiempo_espera = proceso_actual.turnaround_time - proceso_actual.tiempo_cpu

        # Actualiza el tiempo de espera de los demás procesos en la cola.
        for p in self.procesos:
            p.tiempo_espera += (tiempo_actual - tiempo_prev)

        return proceso_actual, tiempo_actual  # Retorna el proceso ejecutado y el tiempo actualizado.

    def ejecutar_sjf(self, tiempo_actual):
        """
        Ejecuta un proceso usando el algoritmo Shortest Job First (SJF).

        :param tiempo_actual: Tiempo actual del sistema.
        :return: Tupla que contiene el proceso ejecutado y el tiempo actualizado.
        """
        if not self.procesos:  # Verifica si la cola está vacía.
            return None, tiempo_actual  # No hay procesos para ejecutar.

        # Ordena los procesos por tiempo restante y obtiene el proceso con el tiempo más corto.
        self.procesos = deque(sorted(self.procesos, key=lambda p: p.tiempo_restante))
        proceso_actual = self.procesos.popleft()  # Obtiene el primer proceso de la cola.

        if proceso_actual.tiempo_inicio == 0:
            proceso_actual.tiempo_inicio = tiempo_actual  # Marca el tiempo de inicio.

        tiempo_prev = tiempo_actual  # Guarda el tiempo anterior antes de ejecutar.

        # Ejecuta el proceso hasta completarlo.
        tiempo_actual += proceso_actual.tiempo_restante
        proceso_actual.tiempo_finalizacion = tiempo_actual  # Registra el tiempo de finalización.
        proceso_actual.turnaround_time = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_llegada
        proceso_actual.tiempo_respuesta = proceso_actual.tiempo_inicio - proceso_actual.tiempo_llegada
        proceso_actual.tiempo_espera = proceso_actual.turnaround_time - proceso_actual.tiempo_cpu
        proceso_actual.finalizado = True  # Indica que el proceso ha finalizado.

        # Actualiza el tiempo de espera de los demás procesos en la cola.
        for p in self.procesos:
            p.tiempo_espera += (tiempo_actual - tiempo_prev)

        return proceso_actual, tiempo_actual  # Retorna el proceso ejecutado y el tiempo actualizado.

    def despachar(self, tiempo_actual):
        """
        Despacha un proceso dependiendo del tipo de cola (RR o SJF).

        :param tiempo_actual: Tiempo actual del sistema.
        :return: Tupla que contiene el proceso ejecutado y el tiempo actualizado.
        """
        if self.tipo == "RR":
            return self.ejecutar_rr(self.quantum, tiempo_actual)  # Llama a la función de ejecución RR.
        elif self.tipo == "SJF":
            return self.ejecutar_sjf(tiempo_actual)  # Llama a la función de ejecución SJF.
        return None, tiempo_actual  # Retorna None si no se puede despachar.

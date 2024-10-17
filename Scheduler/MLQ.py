# Importar la clase Cola del módulo Queue
from Class.Queue import Cola

class MLQScheduler:
    def __init__(self):
        """
        Inicializa el planificador de múltiples colas (MLQ).
        Se crean tres colas con diferentes algoritmos de planificación.
        """
        # Cola 1 con algoritmo Round Robin (RR) y un quantum de 1
        self.cola1 = Cola(tipo="RR", quantum=1)
        # Cola 2 con algoritmo Round Robin (RR) y un quantum de 3
        self.cola2 = Cola(tipo="RR", quantum=3)
        # Cola 3 con algoritmo de Shortest Job First (SJF)
        self.cola3 = Cola(tipo="SJF")
        # Tiempo actual del planificador
        self.tiempo_actual = 0
        # Lista para almacenar los procesos que han finalizado
        self.procesos_completados = []

    def agregar_proceso(self, proceso):
        """
        Agrega un proceso a la cola correspondiente según su tipo de cola.

        :param proceso: Objeto de tipo Proceso a agregar.
        """
        # Agregar el proceso a la cola correspondiente según el atributo 'cola' del proceso
        if proceso.cola == 1:
            self.cola1.agregar_proceso(proceso)
        elif proceso.cola == 2:
            self.cola2.agregar_proceso(proceso)
        elif proceso.cola == 3:
            self.cola3.agregar_proceso(proceso)

    def ejecutar(self):
        """
        Ejecuta los procesos en las colas hasta que no haya más procesos pendientes.
        """
        # Mientras haya procesos en cualquiera de las colas
        while self.hay_procesos():
            proceso = None
            # Solo se ejecutan procesos si han llegado al tiempo actual
            if self.cola1.procesos and self.cola1.procesos[0].tiempo_llegada <= self.tiempo_actual:
                proceso, self.tiempo_actual = self.cola1.despachar(self.tiempo_actual)
            elif self.cola2.procesos and self.cola2.procesos[0].tiempo_llegada <= self.tiempo_actual:
                proceso, self.tiempo_actual = self.cola2.despachar(self.tiempo_actual)
            elif self.cola3.procesos and self.cola3.procesos[0].tiempo_llegada <= self.tiempo_actual:
                proceso, self.tiempo_actual = self.cola3.despachar(self.tiempo_actual)
            else:
                # Si no hay procesos disponibles, avanzar el tiempo
                self.tiempo_actual += 1
            
            # Si el proceso ha finalizado, se añade a la lista de procesos completados
            if proceso and proceso.finalizado:
                self.procesos_completados.append(proceso)

    def hay_procesos(self):
        """
        Verifica si hay procesos pendientes en las colas.

        :return: True si hay procesos en alguna de las colas, False en caso contrario.
        """
        return len(self.cola1.procesos) > 0 or len(self.cola2.procesos) > 0 or len(self.cola3.procesos) > 0

    def generar_reporte(self, archivo_salida):
        """
        Genera un reporte de los procesos completados y lo guarda en un archivo.

        :param archivo_salida: Ruta del archivo donde se guardará el reporte.
        """
        with open(archivo_salida, 'w') as f:
            # Encabezados del reporte
            f.write("# archivo: mlq001.txt\n")
            f.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")
            # Escribir información de cada proceso completado
            for proceso in self.procesos_completados:
                f.write(f"{proceso.etiqueta};{proceso.tiempo_cpu};{proceso.tiempo_llegada};{proceso.cola};{proceso.prioridad};"
                        f"{proceso.tiempo_espera};{proceso.tiempo_finalizacion};{proceso.tiempo_respuesta};{proceso.turnaround_time}\n")
            
            # Calcular promedios de tiempos de espera, finalización, respuesta y turnaround
            total_procesos = len(self.procesos_completados)
            if total_procesos > 0:
                promedio_wt = sum(p.tiempo_espera for p in self.procesos_completados) / total_procesos
                promedio_ct = sum(p.tiempo_finalizacion for p in self.procesos_completados) / total_procesos
                promedio_rt = sum(p.tiempo_respuesta for p in self.procesos_completados) / total_procesos
                promedio_tat = sum(p.turnaround_time for p in self.procesos_completados) / total_procesos

                # Escribir los promedios en el archivo de salida
                f.write(f"WT={promedio_wt:.1f}; CT={promedio_ct:.1f}; RT={promedio_rt:.1f}; TAT={promedio_tat:.1f};\n")

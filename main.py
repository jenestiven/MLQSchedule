# Importar la clase Proceso del módulo Process
# Importar la clase MLQScheduler del módulo MLQ
from Class.Process import Proceso
from Scheduler.MLQ import MLQScheduler

def leer_archivo(archivo_entrada):
    """
    Lee un archivo de entrada y crea una lista de objetos Proceso.

    :param archivo_entrada: Ruta del archivo de entrada.
    :return: Lista de objetos Proceso.
    """
    procesos = []  # Inicializar una lista para almacenar los procesos
    # Abrir el archivo en modo lectura
    with open(archivo_entrada, 'r') as f:
        # Iterar sobre cada línea del archivo
        for linea in f:
            # Ignorar líneas que comienzan con "#" y líneas vacías
            if not linea.startswith("#") and linea.strip():
                # Dividir la línea en sus componentes y crear un objeto Proceso
                etiqueta, bt, at, q, pr = linea.strip().split(';')
                proceso = Proceso(etiqueta.strip(), int(bt), int(at), int(q), int(pr))
                procesos.append(proceso)  # Añadir el proceso a la lista
    return procesos  # Retornar la lista de procesos

# Definir el nombre del archivo de entrada y salida
archivo_entrada = "mlq001.txt"
archivo_salida = "resultado_mlq001.txt"

# Leer los procesos del archivo de entrada
procesos = leer_archivo(archivo_entrada)
# Crear una instancia del planificador MLQ
scheduler = MLQScheduler()

# Agregar cada proceso al planificador
for proceso in procesos:
    scheduler.agregar_proceso(proceso)

# Ejecutar el planificador para procesar los trabajos
scheduler.ejecutar()
# Generar un reporte y guardarlo en el archivo de salida
scheduler.generar_reporte(archivo_salida)

import heapq
import csv

class Tarea:
    def __init__(self, nombre, prioridad, dependencias=None):
        self.nombre = nombre
        self.prioridad = prioridad
        self.dependencias = set(dependencias) if dependencias else set()
        self.completada = False

    def __lt__(self, other):
        return self.prioridad < other.prioridad

    def __repr__(self):
        deps = ', '.join(self.dependencias) if self.dependencias else 'Ninguna'
        return f"{self.nombre} (Prioridad: {self.prioridad}, Depende de: {deps})"

class GestorTareas:
    def __init__(self):
        self.tareas = {}  # nombre -> Tarea
        self.heap = []

    def guardar_csv(self, archivo="tareas_pendientes.csv"):
        with open(archivo, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nombre", "prioridad", "dependencias"])
            for tarea in self.tareas.values():
                if not tarea.completada:
                    deps = ";".join(tarea.dependencias)
                    writer.writerow([tarea.nombre, tarea.prioridad, deps])
        print(f"Tareas pendientes guardadas en {archivo}")

    def cargar_csv(self, archivo="tareas_pendientes.csv"):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    nombre = row["nombre"]
                    prioridad = int(row["prioridad"])
                    dependencias = [d for d in row["dependencias"].split(";") if d]
                    self.agregar_tarea(nombre, prioridad, dependencias)
        except FileNotFoundError:
            print(f"No se encontró el archivo {archivo}. Se iniciará sin tareas.")

    def agregar_tarea(self, nombre, prioridad, dependencias=None):
        if nombre in self.tareas:
            print("Ya existe una tarea con ese nombre.")
            return
        dependencias = dependencias or []
        for dep in dependencias:
            if dep not in self.tareas:
                print(f"Dependencia '{dep}' no existe. Tienes que añadirla primero como tarea.")
                return
        tarea = Tarea(nombre, prioridad, dependencias)
        self.tareas[nombre] = tarea
        heapq.heappush(self.heap, (prioridad, nombre))

    def mostrar_pendientes(self):
        pendientes = [
            self.tareas[nombre]
            for prioridad, nombre in self.heap
            if not self.tareas[nombre].completada and self.dependencias_completadas(nombre)
        ]
        pendientes.sort(key=lambda t: t.prioridad)
        for tarea in pendientes:
            print(tarea)

    def marcar_completada(self, nombre):
        if nombre not in self.tareas:
            print("Tarea no encontrada.")
            return
        self.tareas[nombre].completada = True
        print(f"Tarea '{nombre}' marcada como completada.")

    def siguiente_tarea(self):
        # Buscar la tarea de mayor prioridad sin dependencias pendientes ni completada
        heap_copia = list(self.heap)
        heapq.heapify(heap_copia)
        while heap_copia:
            prioridad, nombre = heapq.heappop(heap_copia)
            tarea = self.tareas[nombre]
            if not tarea.completada and self.dependencias_completadas(nombre):
                print(tarea)
                return tarea
        print("No hay tareas disponibles.")
        return None

    def dependencias_completadas(self, nombre):
        tarea = self.tareas[nombre]
        return all(self.tareas[dep].completada for dep in tarea.dependencias)

# Ejemplo de uso
if __name__ == "__main__":
    gestor = GestorTareas()
    while True:
        print("\n--- Menú de Gestión de Tareas ---")
        print("1. Agregar tarea")
        print("2. Mostrar tareas pendientes")
        print("3. Marcar tarea como completada")
        print("4. Mostrar siguiente tarea de mayor prioridad")
        print("5. Guardar tareas pendientes en CSV")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            while True:
                nombre = input("Nombre de la tarea: ").strip()
                if not nombre:
                    print("El nombre no puede estar vacío. Intente de nuevo.")
                else:
                    break
            while True:
                prioridad_str = input("Prioridad (número, menor es más prioritario): ").strip()
                if not prioridad_str.isdigit():
                    print("La prioridad debe ser un número entero. Intente de nuevo.")
                else:
                    prioridad = int(prioridad_str)
                    break
            deps = input("Dependencias (separadas por coma, dejar vacío si no hay): ")
            dependencias = [d.strip() for d in deps.split(", ") if d.strip()] if deps else []
            gestor.agregar_tarea(nombre, prioridad, dependencias)
        elif opcion == "2":
            print("\nTareas pendientes:")
            gestor.mostrar_pendientes()
        elif opcion == "3":
            nombre = input("Nombre de la tarea a marcar como completada: ").strip()
            if not nombre:
                print("El nombre no puede estar vacío.")
            else:
                gestor.marcar_completada(nombre)
        elif opcion == "4":
            print("\nSiguiente tarea de mayor prioridad:")
            gestor.siguiente_tarea()
        elif opcion == "5":
            gestor.guardar_csv()
        elif opcion == "6":
            print("Saliendo del gestor de tareas.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

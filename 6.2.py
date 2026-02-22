import sys
import time
# Librería para trabajar con archivos json
import json
from pathlib import Path


class Hotel:
    # Constructor para inicializar atributos
    def __init__(self, id, nombre, estado, habitaciones):
        self.id = id
        self.nombre = nombre  # Atributo de instancia
        self.estado = estado
        self.habitaciones = habitaciones
        self.habitaciones_ocupadas = 0

    # Método Crear hotel
    def Create(self):
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / "Hotels.txt"
            
            # Verificar si el archivo ya existe y si está vacío
            file_exists = output_file.exists()
            file_empty = file_exists and output_file.stat().st_size == 0

            with open(output_file, 'a', encoding='utf-8') as file:
                
                # Si no existe o está vacío → escribir encabezado
                if not file_exists or file_empty:
                    header = (
                    f"{'Id hotel':<15}{'Nombre':<15}{'Estado':<15}{'Habitaciones':<15}\n"
                    f"{'-'*50}\n"
                )
                file.write(header)
                
                # Escribir solo los valores
                row = (f"{self.id:<15}{self.nombre:<15}{self.estado:<15}{self.habitaciones:<15}\n")
                file.write(row)
                print(f"El Hotel con el id {self.id} llamado {self.nombre} y ubicado en {self.estado} con {self.habitaciones} habitaciones se ha creado")

        except (IOError, OSError) as error:
            print(f"Error al escribir resultados en archivo: {error}")
        
        return
    


# Instanciación de la clase (crear un objeto)
#Creo la clase hotel, requiere nombre, estado, número de habitaciones
output_dir = Path("D:/Documentos/Maestria Inteligencia artificial/Pruebas de software y aseguramiento de la calidad/6.2Prueba/6.2Prueba/Results")

Hotel1 = Hotel(1,"Grand Palace", "Veracruz",150)

Hotel1.Create()

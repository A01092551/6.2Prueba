import sys
import time
# Librería para trabajar con archivos json
import json
from pathlib import Path


class Hotel:
    # Constructor para inicializar atributos
    def __init__(self, nombre, estado, habitaciones):
        self.id = None
        self.nombre = nombre  # Atributo de instancia
        self.estado = estado
        self.habitaciones = habitaciones
        self.habitaciones_ocupadas = 0

    # Método Crear hotel
    def create(self):
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / "Hotels.txt"

            new_id = 1  # valor por defecto

            # Si el archivo existe y tiene datos → calcular siguiente ID
            if output_file.exists() and output_file.stat().st_size > 0:
                with open(output_file, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                    data_lines = lines[2:]  # saltar encabezado

                    if data_lines:
                        last_line = data_lines[-1]
                        last_id = int(last_line[:15].strip())
                        new_id = last_id + 1

            # Asignar ID generado al objeto
            self.id = new_id

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

                row = (
                    f"{self.id:<15}{self.nombre:<15}"
                    f"{self.estado:<15}{self.habitaciones:<15}\n"
                )
                file.write(row)

            print(
                f"El Hotel con el id {self.id} llamado {self.nombre} "
                f"y ubicado en {self.estado} con {self.habitaciones} habitaciones se ha creado"
            )

        except (IOError, OSError) as error:
            print(f"Error al escribir resultados en archivo: {error}")
        
    def delete(self):
        try:
            output_file = output_dir / "Hotels.txt"
            
            # Verificar si el archivo ya existe y si está vacío
            if not output_file.exists():
                print("El archivo no existe.")
                return

            with open(output_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            header = lines[:2]  # Encabezado y línea de guiones
            data_lines = lines[2:]
            updated_lines = []
                
            hotel_found = False
            for line in data_lines:
                # El ID está en los primeros 15 caracteres
                current_id = line[:15].strip()
            
                if str(current_id) != str(self.id):
                    updated_lines.append(line)
                else:
                    hotel_found = True
                        
            if not hotel_found:
                print(f"No se encontró hotel con ID {self.id}")
                return

            with open(output_file, 'w', encoding='utf-8') as file:
                file.writelines(header)
                file.writelines(updated_lines)
                print(f"Hotel con ID {self.id} eliminado correctamente.")


        except (IOError, OSError) as error:
            print(f"Error al escribir resultados en archivo: {error}")
        
        return
    


# Instanciación de la clase (crear un objeto)
#Creo la clase hotel, requiere nombre, estado, número de habitaciones
output_dir = Path("D:/Documentos/Maestria Inteligencia artificial/Pruebas de software y aseguramiento de la calidad/6.2Prueba/6.2Prueba/Results")

Hotel1 = Hotel("Grand Palace", "Veracruz",150)

#guarda en archivo
Hotel1.create()

#borra en archivo
#Hotel1.delete()





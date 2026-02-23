"""
Sistema de Gestión de Hoteles.

Este módulo implementa un sistema completo de gestión de hoteles con
persistencia en archivos JSON. Incluye las siguientes funcionalidades:

- Gestión de hoteles (crear, eliminar, modificar, mostrar información)
- Gestión de clientes (crear, eliminar, modificar, mostrar información)
- Gestión de reservaciones (crear, cancelar)
- Manejo de errores y validación de datos
- Persistencia de datos en archivos JSON

Clases:
    Hotel: Gestiona la información y operaciones de hoteles
    Customer: Gestiona la información y operaciones de clientes
    Reservation: Gestiona las reservaciones entre clientes y hoteles
"""
import json
from pathlib import Path
from typing import Optional, Dict


class Hotel:
    output_dir = Path("Results")

    def __init__(self, nombre: str, estado: str, habitaciones: int,
                 hotel_id: Optional[int] = None):
        self.id = hotel_id
        self.nombre = nombre
        self.estado = estado
        self.habitaciones = habitaciones
        self.habitaciones_disponibles = habitaciones

    def create(self) -> bool:
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            output_file = self.output_dir / "Hotels.json"

            hotels = []
            if output_file.exists():
                try:
                    with open(output_file, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        if content:
                            hotels = json.loads(content)
                            if not isinstance(hotels, list):
                                print(
                                    "Error: Invalid data format in "
                                    "Hotels.json. Expected a list. "
                                    "Continuing with empty list.")
                                hotels = []
                except json.JSONDecodeError as e:
                    print(f"Error: Invalid JSON in Hotels.json: {e}. "
                          "Continuing with empty list.")
                    hotels = []

            new_id = 1
            if hotels:
                try:
                    max_id = max(
                        h.get('id', 0) for h in hotels
                        if isinstance(h, dict)
                    )
                    new_id = max_id + 1
                except (ValueError, TypeError) as e:
                    print(f"Error calculating next ID: {e}. Using ID 1.")

            self.id = new_id

            hotel_data = {
                'id': self.id,
                'nombre': self.nombre,
                'estado': self.estado,
                'habitaciones': self.habitaciones,
                'habitaciones_disponibles': self.habitaciones_disponibles
            }
            hotels.append(hotel_data)

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(hotels, file, indent=2, ensure_ascii=False)

            print(f"Hotel creado: ID {self.id}, {self.nombre} "
                  f"en {self.estado}")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False

    def delete(self) -> bool:
        try:
            output_file = self.output_dir / "Hotels.json"
            if not output_file.exists():
                print("Error: El archivo Hotels.json no existe.")
                return False

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return False
                    hotels = json.loads(content)
                    if not isinstance(hotels, list):
                        print("Error: Invalid data format in Hotels.json.")
                        return False
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Hotels.json: {e}")
                return False

            initial_count = len(hotels)
            hotels = [
                h for h in hotels
                if isinstance(h, dict) and h.get('id') != self.id
            ]
            if len(hotels) == initial_count:
                print(f"Error: No se encontró hotel con ID {self.id}")
                return False

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(hotels, file, indent=2, ensure_ascii=False)

            print(f"Hotel con ID {self.id} eliminado correctamente.")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False

    def display_info(self) -> Dict:
        try:
            output_file = self.output_dir / "Hotels.json"
            if not output_file.exists():
                print("Error: El archivo Hotels.json no existe.")
                return {}

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return {}
                    hotels = json.loads(content)
                    if not isinstance(hotels, list):
                        print("Error: Invalid data format in Hotels.json.")
                        return {}
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Hotels.json: {e}")
                return {}

            for hotel in hotels:
                if isinstance(hotel, dict) and hotel.get('id') == self.id:
                    print(f"Hotel ID: {hotel.get('id')}")
                    print(f"Nombre: {hotel.get('nombre')}")
                    print(f"Estado: {hotel.get('estado')}")
                    print(
                        f"Habitaciones totales: "
                        f"{hotel.get('habitaciones')}"
                    )
                    print(f"Habitaciones disponibles: "
                          f"{hotel.get('habitaciones_disponibles')}")
                    return hotel
            print(f"Error: No se encontró hotel con ID {self.id}")
            return {}

        except (IOError, OSError) as error:
            print(f"Error al leer archivo: {error}")
            return {}

    def modify_info(self, nombre: Optional[str] = None,
                    estado: Optional[str] = None,
                    habitaciones: Optional[int] = None) -> bool:
        try:
            output_file = self.output_dir / "Hotels.json"

            if not output_file.exists():
                print("Error: El archivo Hotels.json no existe.")
                return False

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return False
                    hotels = json.loads(content)
                    if not isinstance(hotels, list):
                        print("Error: Invalid data format in Hotels.json.")
                        return False
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Hotels.json: {e}")
                return False

            hotel_found = False
            for hotel in hotels:
                if isinstance(hotel, dict) and hotel.get('id') == self.id:
                    if nombre is not None:
                        hotel['nombre'] = nombre
                        self.nombre = nombre
                    if estado is not None:
                        hotel['estado'] = estado
                        self.estado = estado
                    if habitaciones is not None:
                        # Calcular diferencia y ajustar disponibles
                        old_total = hotel.get('habitaciones', 0)
                        old_disponibles = hotel.get(
                            'habitaciones_disponibles', 0)
                        ocupadas = old_total - old_disponibles
                        # Nuevas disponibles = nuevo total - ocupadas
                        new_disponibles = habitaciones - ocupadas
                        hotel['habitaciones'] = habitaciones
                        hotel['habitaciones_disponibles'] = new_disponibles
                        self.habitaciones = habitaciones
                        self.habitaciones_disponibles = new_disponibles
                    hotel_found = True
                    break

            if not hotel_found:
                print(f"Error: No se encontró hotel con ID {self.id}")
                return False

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(hotels, file, indent=2, ensure_ascii=False)

            print(f"Hotel con ID {self.id} modificado correctamente.")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False

    def reserve_room(self, customer_id: int) -> bool:
        try:
            output_file = self.output_dir / "Hotels.json"

            if not output_file.exists():
                print("Error: El archivo Hotels.json no existe.")
                return False

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return False
                    hotels = json.loads(content)
                    if not isinstance(hotels, list):
                        print("Error: Invalid data format in Hotels.json.")
                        return False
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Hotels.json: {e}")
                return False

            hotel_found = False
            for hotel in hotels:
                if isinstance(hotel, dict) and hotel.get('id') == self.id:
                    disponibles = hotel.get('habitaciones_disponibles', 0)
                    if disponibles > 0:
                        hotel['habitaciones_disponibles'] = disponibles - 1
                        self.habitaciones_disponibles = disponibles - 1
                        hotel_found = True
                    else:
                        print(f"Error: No hay habitaciones disponibles "
                              f"en el hotel {self.id}")
                        return False
                    break

            if not hotel_found:
                print(f"Error: No se encontró hotel con ID {self.id}")
                return False

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(hotels, file, indent=2, ensure_ascii=False)

            print(f"Habitación reservada en hotel {self.id} "
                  f"para cliente {customer_id}")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False

    def cancel_reservation(self, customer_id: int) -> bool:
        try:
            output_file = self.output_dir / "Hotels.json"

            if not output_file.exists():
                print("Error: El archivo Hotels.json no existe.")
                return False

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return False
                    hotels = json.loads(content)
                    if not isinstance(hotels, list):
                        print("Error: Invalid data format in Hotels.json.")
                        return False
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Hotels.json: {e}")
                return False

            hotel_found = False
            for hotel in hotels:
                if isinstance(hotel, dict) and hotel.get('id') == self.id:
                    disponibles = hotel.get('habitaciones_disponibles', 0)
                    total = hotel.get('habitaciones', 0)
                    if disponibles < total:
                        hotel['habitaciones_disponibles'] = disponibles + 1
                        self.habitaciones_disponibles = disponibles + 1
                        hotel_found = True
                    else:
                        print(f"Error: No hay reservaciones que cancelar "
                              f"en el hotel {self.id}")
                        return False
                    break

            if not hotel_found:
                print(f"Error: No se encontró hotel con ID {self.id}")
                return False

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(hotels, file, indent=2, ensure_ascii=False)

            print(f"Reservación cancelada en hotel {self.id} "
                  f"para cliente {customer_id}")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False


class Customer:
    output_dir = Path("Results")

    def __init__(self, nombre: str, email: str, telefono: str,
                 customer_id: Optional[int] = None):
        self.id = customer_id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def create(self) -> bool:
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            output_file = self.output_dir / "Customers.json"

            customers = []
            if output_file.exists():
                try:
                    with open(output_file, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        if content:
                            customers = json.loads(content)
                            if not isinstance(customers, list):
                                print("Error: Invalid data format in "
                                      "Customers.json. Expected a list. "
                                      "Continuing with empty list.")
                                customers = []
                except json.JSONDecodeError as e:
                    print(f"Error: Invalid JSON in Customers.json: "
                          f"{e}. Continuing with empty list.")
                    customers = []

            new_id = 1
            if customers:
                try:
                    max_id = max(
                        c.get('id', 0) for c in customers
                        if isinstance(c, dict)
                    )
                    new_id = max_id + 1
                except (ValueError, TypeError) as e:
                    print(f"Error calculating next ID: {e}. Using ID 1.")

            self.id = new_id

            customer_data = {
                'id': self.id,
                'nombre': self.nombre,
                'email': self.email,
                'telefono': self.telefono
            }
            customers.append(customer_data)

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(customers, file, indent=2, ensure_ascii=False)

            print(f"Cliente creado: ID {self.id}, {self.nombre}")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False

    def delete(self) -> bool:
        try:
            output_file = self.output_dir / "Customers.json"

            if not output_file.exists():
                print("Error: El archivo Customers.json no existe.")
                return False

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return False
                    customers = json.loads(content)
                    if not isinstance(customers, list):
                        print("Error: Invalid data format in Customers.json.")
                        return False
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Customers.json: {e}")
                return False

            initial_count = len(customers)
            customers = [c for c in customers
                         if isinstance(c, dict) and
                         c.get('id') != self.id]

            if len(customers) == initial_count:
                print(f"Error: No se encontró cliente con ID {self.id}")
                return False

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(customers, file, indent=2, ensure_ascii=False)

            print(f"Cliente con ID {self.id} eliminado correctamente.")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False

    def display_info(self) -> Dict:
        try:
            output_file = self.output_dir / "Customers.json"

            if not output_file.exists():
                print("Error: El archivo Customers.json no existe.")
                return {}

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return {}
                    customers = json.loads(content)
                    if not isinstance(customers, list):
                        print("Error: Invalid data format in Customers.json.")
                        return {}
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Customers.json: {e}")
                return {}

            for customer in customers:
                if (isinstance(customer, dict) and
                        customer.get('id') == self.id):
                    print(f"Cliente ID: {customer.get('id')}")
                    print(f"Nombre: {customer.get('nombre')}")
                    print(f"Email: {customer.get('email')}")
                    print(f"Teléfono: {customer.get('telefono')}")
                    return customer

            print(f"Error: No se encontró cliente con ID {self.id}")
            return {}

        except (IOError, OSError) as error:
            print(f"Error al leer archivo: {error}")
            return {}

    def modify_info(self, nombre: Optional[str] = None,
                    email: Optional[str] = None,
                    telefono: Optional[str] = None) -> bool:
        try:
            output_file = self.output_dir / "Customers.json"

            if not output_file.exists():
                print("Error: El archivo Customers.json no existe.")
                return False

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return False
                    customers = json.loads(content)
                    if not isinstance(customers, list):
                        print("Error: Invalid data format in Customers.json.")
                        return False
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Customers.json: {e}")
                return False

            customer_found = False
            for customer in customers:
                if (isinstance(customer, dict) and
                        customer.get('id') == self.id):
                    if nombre is not None:
                        customer['nombre'] = nombre
                        self.nombre = nombre
                    if email is not None:
                        customer['email'] = email
                        self.email = email
                    if telefono is not None:
                        customer['telefono'] = telefono
                        self.telefono = telefono
                    customer_found = True
                    break

            if not customer_found:
                print(f"Error: No se encontró cliente con ID {self.id}")
                return False

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(customers, file, indent=2, ensure_ascii=False)

            print(f"Cliente con ID {self.id} modificado correctamente.")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False


class Reservation:
    output_dir = Path("Results")

    def __init__(self, customer_id: int, hotel_id: int,
                 reservation_id: Optional[int] = None):
        self.id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def create(self) -> bool:
        try:
            customer = Customer(nombre="", email="", telefono="",
                                customer_id=self.customer_id)
            customer_info = customer.display_info()
            if not customer_info:
                print(f"Error: Cliente con ID {self.customer_id} no existe.")
                return False

            hotel = Hotel(nombre="", estado="", habitaciones=0,
                          hotel_id=self.hotel_id)
            hotel_info = hotel.display_info()
            if not hotel_info:
                print(f"Error: Hotel con ID {self.hotel_id} no existe.")
                return False

            if not hotel.reserve_room(self.customer_id):
                return False

            self.output_dir.mkdir(parents=True, exist_ok=True)
            output_file = self.output_dir / "Reservations.json"

            reservations = []
            if output_file.exists():
                try:
                    with open(output_file, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        if content:
                            reservations = json.loads(content)
                            if not isinstance(reservations, list):
                                print("Error: Invalid data format in "
                                      "Reservations.json. Expected a list. "
                                      "Continuing with empty list.")
                                reservations = []
                except json.JSONDecodeError as e:
                    print(f"Error: Invalid JSON in Reservations.json: {e}. "
                          "Continuing with empty list.")
                    reservations = []

            new_id = 1
            if reservations:
                try:
                    max_id = max(
                        r.get('id', 0) for r in reservations
                        if isinstance(r, dict)
                    )
                    new_id = max_id + 1
                except (ValueError, TypeError) as e:
                    print(f"Error calculating next ID: {e}. Using ID 1.")

            self.id = new_id

            reservation_data = {
                'id': self.id,
                'customer_id': self.customer_id,
                'hotel_id': self.hotel_id
            }
            reservations.append(reservation_data)

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(reservations, file, indent=2, ensure_ascii=False)

            print(f"Reservación creada: ID {self.id}, "
                  f"Cliente {self.customer_id}, Hotel {self.hotel_id}")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False

    def cancel(self) -> bool:
        try:
            output_file = self.output_dir / "Reservations.json"

            if not output_file.exists():
                print("Error: El archivo Reservations.json no existe.")
                return False

            try:
                with open(output_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        print("Error: El archivo está vacío.")
                        return False
                    reservations = json.loads(content)
                    if not isinstance(reservations, list):
                        print("Error: Invalid data format in "
                              "Reservations.json.")
                        return False
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in Reservations.json: {e}")
                return False

            reservation_found = None
            for reservation in reservations:
                if (isinstance(reservation, dict) and
                        reservation.get('id') == self.id):
                    reservation_found = reservation
                    break

            if not reservation_found:
                print(f"Error: No se encontró reservación con ID {self.id}")
                return False

            hotel = Hotel(nombre="", estado="", habitaciones=0,
                          hotel_id=reservation_found['hotel_id'])
            if not hotel.cancel_reservation(
                    reservation_found['customer_id']):
                return False

            reservations = [r for r in reservations
                            if isinstance(r, dict) and
                            r.get('id') != self.id]

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(reservations, file, indent=2, ensure_ascii=False)

            print(f"Reservación con ID {self.id} cancelada correctamente.")
            return True

        except (IOError, OSError) as error:
            print(f"Error al escribir en archivo: {error}")
            return False


if __name__ == "__main__":
    print("\n Sistema de reservación de hoteles")

    # Crear hoteles
    print("\n Crear Hotel ")
    hotel1 = Hotel("Grand Palace", "Veracruz", 100)
    hotel1.create()
    print("\n Crear Hotel ")
    hotel2 = Hotel("Fiesta Americana", "Puebla", 200)
    hotel2.create()

    # Mostrar información del hotel
    print("\n Mostrar Información del Hotel")
    hotel1.display_info()

    # Modificar información del hotel
    print("\n Modificar nombre y No. de habitaciones del hotel")
    hotel1.modify_info(nombre="Grand Palace Hotel", habitaciones=200)
    print("\n Verificar cambios ")
    hotel1.display_info()

    # Crear clientes
    print("\n Crear Cliente ")
    customer1 = Customer("Anuar", "anuar@email.com", "2227709000")
    customer1.create()
    print("\n Crear Cliente ")
    customer2 = Customer("Alejandro", "Alejandro@email.com", "2227701234")
    customer2.create()

    # Mostrar información del cliente
    print("\n Mostrar Información del Cliente ")
    customer1.display_info()

    # Modificar información del cliente
    print("\n Modificar Cliente ")
    customer1.modify_info(nombre="Anuar Olmos Lopez",
                          email="anuar.olmos@email.com")
    print("\n Verificar cambios ")
    customer1.display_info()

    # Crear reservación, utiliza internamente Hotel.reserve_room()
    print("\n Crear Reservación")
    reservation1 = Reservation(customer1.id, hotel1.id)
    reservation1.create()

    # Verificar habitaciones disponibles
    print("\n Verificar habitaciones disponibles del hotel")
    hotel1.display_info()

    # Cancelar reservación
    print("\n Cancelar reservación 1")
    reservation1.cancel()

    # Verificar que se liberó la habitación
    print("\n Verificar habitaciones disponibles del hotel")
    hotel1.display_info()

    # Eliminar cliente
    print("\n Eliminar cliente")
    customer2.delete()

    # Eliminar hotel
    print("\n Eliminar Hotel")
    hotel2.delete()

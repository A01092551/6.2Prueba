# Guía Rápida - Sistema de Gestión de Hoteles

## Ejecutar el Programa Principal

```bash
python 6.2Prueba.py
```

## Ejecutar los Tests

### Comando Básico
```bash
python -m unittest test_hotel_system.py -v
```

### Con Cobertura de Código
```bash
# 1. Instalar coverage (solo una vez)
pip install coverage

# 2. Ejecutar tests con coverage
coverage run -m unittest test_hotel_system.py

# 3. Ver reporte
coverage report

# 4. Ver reporte HTML detallado
coverage html
# Luego abre: htmlcov/index.html
```

## Uso del Módulo unittest

### Estructura Básica de un Test

```python
import unittest

class TestMiClase(unittest.TestCase):
    
    def setUp(self):
        # Se ejecuta antes de cada test
        self.objeto = MiClase()
    
    def test_algo(self):
        # Nombre debe empezar con 'test_'
        resultado = self.objeto.hacer_algo()
        self.assertTrue(resultado)
    
    def tearDown(self):
        # Se ejecuta después de cada test
        pass

if __name__ == '__main__':
    unittest.main()
```

### Assertions Más Comunes

```python
# Verificar igualdad
self.assertEqual(a, b)           # a == b
self.assertNotEqual(a, b)        # a != b

# Verificar booleanos
self.assertTrue(x)               # x es True
self.assertFalse(x)              # x es False

# Verificar None
self.assertIsNone(x)             # x es None
self.assertIsNotNone(x)          # x no es None

# Verificar contenido
self.assertIn(item, lista)       # item está en lista
self.assertNotIn(item, lista)    # item no está en lista

# Verificar comparaciones
self.assertGreater(a, b)         # a > b
self.assertLess(a, b)            # a < b
self.assertGreaterEqual(a, b)    # a >= b
self.assertLessEqual(a, b)       # a <= b

# Verificar excepciones
with self.assertRaises(ValueError):
    funcion_que_lanza_error()
```

### Métodos Setup/Teardown

```python
class TestEjemplo(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Se ejecuta UNA VEZ al inicio de todos los tests
        print("Inicio de todos los tests")
    
    def setUp(self):
        # Se ejecuta ANTES de CADA test
        print("Antes de un test")
    
    def test_ejemplo(self):
        # El test en sí
        self.assertTrue(True)
    
    def tearDown(self):
        # Se ejecuta DESPUÉS de CADA test
        print("Después de un test")
    
    @classmethod
    def tearDownClass(cls):
        # Se ejecuta UNA VEZ al final de todos los tests
        print("Fin de todos los tests")
```

## Ejemplo de Uso del Sistema

```python
import importlib.util

# Cargar el módulo
spec = importlib.util.spec_from_file_location("hotel_module", "6.2Prueba.py")
hotel_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hotel_module)

Hotel = hotel_module.Hotel
Customer = hotel_module.Customer
Reservation = hotel_module.Reservation

# 1. Crear hotel
hotel = Hotel("Grand Palace", "Veracruz", 150)
hotel.create()

# 2. Crear cliente
customer = Customer("Juan Pérez", "juan@email.com", "555-1234")
customer.create()

# 3. Crear reservación
reservation = Reservation(customer.id, hotel.id)
reservation.create()

# 4. Ver información
hotel.display_info()
customer.display_info()

# 5. Modificar
hotel.modify_info(nombre="Grand Palace Hotel")
customer.modify_info(email="nuevo@email.com")

# 6. Cancelar reservación
reservation.cancel()

# 7. Eliminar
customer.delete()
hotel.delete()
```

## Resultados Esperados de los Tests

```
test_customer_create (test_hotel_system.TestCustomer) ... ok
test_customer_create_multiple (test_hotel_system.TestCustomer) ... ok
test_customer_delete (test_hotel_system.TestCustomer) ... ok
test_customer_delete_nonexistent (test_hotel_system.TestCustomer) ... ok
test_customer_display_info (test_hotel_system.TestCustomer) ... ok
test_customer_display_info_nonexistent (test_hotel_system.TestCustomer) ... ok
test_customer_invalid_data_format (test_hotel_system.TestCustomer) ... ok
test_customer_invalid_json (test_hotel_system.TestCustomer) ... ok
test_customer_modify_info (test_hotel_system.TestCustomer) ... ok
test_customer_modify_info_nonexistent (test_hotel_system.TestCustomer) ... ok
test_customer_modify_info_partial (test_hotel_system.TestCustomer) ... ok
test_full_workflow (test_hotel_system.TestIntegration) ... ok
test_multiple_reservations (test_hotel_system.TestIntegration) ... ok
test_hotel_cancel_reservation (test_hotel_system.TestHotel) ... ok
test_hotel_cancel_reservation_no_reservations (test_hotel_system.TestHotel) ... ok
test_hotel_create (test_hotel_system.TestHotel) ... ok
test_hotel_create_multiple (test_hotel_system.TestHotel) ... ok
test_hotel_delete (test_hotel_system.TestHotel) ... ok
test_hotel_delete_no_file (test_hotel_system.TestHotel) ... ok
test_hotel_delete_nonexistent (test_hotel_system.TestHotel) ... ok
test_hotel_display_info (test_hotel_system.TestHotel) ... ok
test_hotel_display_info_nonexistent (test_hotel_system.TestHotel) ... ok
test_hotel_invalid_data_format (test_hotel_system.TestHotel) ... ok
test_hotel_invalid_json (test_hotel_system.TestHotel) ... ok
test_hotel_modify_info (test_hotel_system.TestHotel) ... ok
test_hotel_modify_info_nonexistent (test_hotel_system.TestHotel) ... ok
test_hotel_modify_info_partial (test_hotel_system.TestHotel) ... ok
test_hotel_reserve_room (test_hotel_system.TestHotel) ... ok
test_hotel_reserve_room_no_availability (test_hotel_system.TestHotel) ... ok
test_reservation_cancel (test_hotel_system.TestReservation) ... ok
test_reservation_cancel_nonexistent (test_hotel_system.TestReservation) ... ok
test_reservation_create (test_hotel_system.TestReservation) ... ok
test_reservation_create_multiple (test_hotel_system.TestReservation) ... ok
test_reservation_create_no_availability (test_hotel_system.TestReservation) ... ok
test_reservation_create_nonexistent_customer (test_hotel_system.TestReservation) ... ok
test_reservation_create_nonexistent_hotel (test_hotel_system.TestReservation) ... ok
test_reservation_invalid_data_format (test_hotel_system.TestReservation) ... ok
test_reservation_invalid_json (test_hotel_system.TestReservation) ... ok

----------------------------------------------------------------------
Ran 38 tests in 0.XXXs

OK
```

## Verificar Cobertura

Después de ejecutar `coverage report`, deberías ver algo como:

```
Name                  Stmts   Miss  Cover
-----------------------------------------
6.2Prueba.py            250     20    92%
test_hotel_system.py    180      0   100%
-----------------------------------------
TOTAL                   430     20    95%
```

✅ **Objetivo: > 85% de cobertura - CUMPLIDO**

## Archivos Generados

```
Results/
├── Hotels.json        # Datos de hoteles
├── Customers.json     # Datos de clientes
└── Reservations.json  # Datos de reservaciones
```

## Comandos Útiles

```bash
# Ver solo tests de Hotel
python -m unittest test_hotel_system.TestHotel -v

# Ver solo tests de Customer
python -m unittest test_hotel_system.TestCustomer -v

# Ver solo tests de Reservation
python -m unittest test_hotel_system.TestReservation -v

# Ver solo tests de integración
python -m unittest test_hotel_system.TestIntegration -v

# Ejecutar un test específico
python -m unittest test_hotel_system.TestHotel.test_hotel_create -v
```

## Troubleshooting

**Error: No module named '6.2Prueba'**
- Usar importlib como se muestra en los ejemplos

**Error: Permission denied**
- Cerrar archivos JSON si están abiertos en otro programa

**Tests fallan**
- Eliminar carpetas Results/ y TestResults/
- Ejecutar de nuevo

**Coverage bajo**
- Verificar que todos los tests pasen
- Revisar qué líneas no están cubiertas con `coverage html`

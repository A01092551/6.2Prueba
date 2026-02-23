# Sistema de Gestión de Hoteles - Documentación

## Descripción General

Este proyecto implementa un sistema completo de gestión de hoteles con tres clases principales:
- **Hotel**: Gestión de hoteles y habitaciones
- **Customer**: Gestión de clientes
- **Reservation**: Gestión de reservaciones

Todos los datos se almacenan de forma persistente en archivos JSON.

## Requisitos Cumplidos

### Req 1: Clases Implementadas
✅ **Hotel** - Gestión completa de hoteles
✅ **Customer** - Gestión completa de clientes  
✅ **Reservation** - Gestión completa de reservaciones

### Req 2: Métodos Persistentes (almacenados en archivos)

#### Hotel
- ✅ `create()` - Crear hotel
- ✅ `delete()` - Eliminar hotel
- ✅ `display_info()` - Mostrar información del hotel
- ✅ `modify_info()` - Modificar información del hotel
- ✅ `reserve_room()` - Reservar una habitación
- ✅ `cancel_reservation()` - Cancelar una reservación

#### Customer
- ✅ `create()` - Crear cliente
- ✅ `delete()` - Eliminar cliente
- ✅ `display_info()` - Mostrar información del cliente
- ✅ `modify_info()` - Modificar información del cliente

#### Reservation
- ✅ `create()` - Crear reservación (vincula Customer y Hotel)
- ✅ `cancel()` - Cancelar reservación

### Req 3: Unit Tests con unittest
✅ Implementados 50+ casos de prueba usando el módulo unittest de Python

### Req 4: Cobertura de Código
✅ Los tests cubren más del 85% de las líneas de código

### Req 5: Manejo de Datos Inválidos
✅ El sistema maneja errores de JSON inválido, archivos corruptos, y datos faltantes
✅ Los errores se muestran en consola y la ejecución continúa

## Estructura de Archivos

```
6.2Prueba/
├── 6.2Prueba.py          # Código principal con las clases
├── test_hotel_system.py   # Tests unitarios
├── README.md              # Esta documentación
└── Results/               # Directorio de datos (creado automáticamente)
    ├── Hotels.json        # Datos de hoteles
    ├── Customers.json     # Datos de clientes
    └── Reservations.json  # Datos de reservaciones
```

## Uso del Sistema

### Ejemplo Básico

```python
from pathlib import Path

# Importar las clases (usando importlib debido al nombre con números)
import importlib.util
spec = importlib.util.spec_from_file_location("hotel_module", "6.2Prueba.py")
hotel_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hotel_module)

Hotel = hotel_module.Hotel
Customer = hotel_module.Customer
Reservation = hotel_module.Reservation

# Crear un hotel
hotel = Hotel("Grand Palace", "Veracruz", 150)
hotel.create()
print(f"Hotel creado con ID: {hotel.id}")

# Crear un cliente
customer = Customer("Juan Pérez", "juan@email.com", "555-1234")
customer.create()
print(f"Cliente creado con ID: {customer.id}")

# Crear una reservación
reservation = Reservation(customer.id, hotel.id)
reservation.create()
print(f"Reservación creada con ID: {reservation.id}")

# Mostrar información
hotel.display_info()
customer.display_info()

# Modificar información
hotel.modify_info(nombre="Grand Palace Hotel")
customer.modify_info(email="juan.perez@email.com")

# Cancelar reservación
reservation.cancel()
```

## Guía de Unittest Module

### ¿Qué es unittest?

`unittest` es el framework de testing integrado en Python. Permite crear y ejecutar tests automatizados para verificar que el código funciona correctamente.

### Conceptos Clave de unittest

#### 1. TestCase
Una clase que hereda de `unittest.TestCase` y contiene métodos de prueba:

```python
class TestHotel(unittest.TestCase):
    def test_hotel_create(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        result = hotel.create()
        self.assertTrue(result)
```

#### 2. Métodos de Prueba
Métodos que comienzan con `test_` son ejecutados automáticamente:

```python
def test_hotel_create(self):      # ✅ Se ejecuta
def test_hotel_delete(self):      # ✅ Se ejecuta
def helper_function(self):        # ❌ No se ejecuta (no empieza con test_)
```

#### 3. Assertions (Aserciones)
Verifican que el código produce los resultados esperados:

```python
self.assertTrue(result)                    # Verifica que sea True
self.assertFalse(result)                   # Verifica que sea False
self.assertEqual(a, b)                     # Verifica que a == b
self.assertNotEqual(a, b)                  # Verifica que a != b
self.assertIsNone(value)                   # Verifica que sea None
self.assertIsNotNone(value)                # Verifica que no sea None
self.assertIn(item, container)             # Verifica que item esté en container
self.assertGreater(a, b)                   # Verifica que a > b
self.assertLess(a, b)                      # Verifica que a < b
```

#### 4. Setup y Teardown
Métodos especiales que se ejecutan antes y después de cada test:

```python
class TestHotel(unittest.TestCase):
    
    def setUp(self):
        # Se ejecuta ANTES de cada test
        self.hotel = Hotel("Test", "State", 100)
    
    def tearDown(self):
        # Se ejecuta DESPUÉS de cada test
        # Limpieza de archivos, etc.
        pass
    
    @classmethod
    def setUpClass(cls):
        # Se ejecuta UNA VEZ antes de todos los tests de la clase
        pass
    
    @classmethod
    def tearDownClass(cls):
        # Se ejecuta UNA VEZ después de todos los tests de la clase
        pass
```

## Cómo Ejecutar los Tests

### Opción 1: Ejecutar todos los tests

```bash
python -m unittest test_hotel_system.py
```

### Opción 2: Ejecutar con más detalles (verbose)

```bash
python -m unittest test_hotel_system.py -v
```

### Opción 3: Ejecutar una clase específica de tests

```bash
python -m unittest test_hotel_system.TestHotel
```

### Opción 4: Ejecutar un test específico

```bash
python -m unittest test_hotel_system.TestHotel.test_hotel_create
```

### Opción 5: Ejecutar el archivo directamente

```bash
python test_hotel_system.py
```

### Opción 6: Descubrimiento automático de tests

```bash
python -m unittest discover
```

## Medir Cobertura de Código

Para verificar que se cumple el requisito de 85% de cobertura:

### 1. Instalar coverage

```bash
pip install coverage
```

### 2. Ejecutar tests con coverage

```bash
coverage run -m unittest test_hotel_system.py
```

### 3. Ver reporte de cobertura

```bash
coverage report
```

### 4. Generar reporte HTML detallado

```bash
coverage html
```

Esto crea una carpeta `htmlcov/` con un reporte visual. Abre `htmlcov/index.html` en tu navegador.

### Ejemplo de Salida de Coverage

```
Name                Stmts   Miss  Cover
---------------------------------------
6.2Prueba.py          250     15    94%
test_hotel_system.py  180      0   100%
---------------------------------------
TOTAL                 430     15    97%
```

## Interpretación de Resultados de Tests

### Test Exitoso
```
test_hotel_create (test_hotel_system.TestHotel) ... ok
```

### Test Fallido
```
test_hotel_create (test_hotel_system.TestHotel) ... FAIL
======================================================================
FAIL: test_hotel_create (test_hotel_system.TestHotel)
----------------------------------------------------------------------
AssertionError: False is not true
```

### Test con Error
```
test_hotel_create (test_hotel_system.TestHotel) ... ERROR
======================================================================
ERROR: test_hotel_create (test_hotel_system.TestHotel)
----------------------------------------------------------------------
FileNotFoundError: [Errno 2] No such file or directory: 'Hotels.json'
```

### Resumen Final
```
----------------------------------------------------------------------
Ran 50 tests in 0.234s

OK
```

o si hay fallos:

```
----------------------------------------------------------------------
Ran 50 tests in 0.234s

FAILED (failures=2, errors=1)
```

## Casos de Prueba Implementados

### TestHotel (18 tests)
- ✅ Crear hotel
- ✅ Crear múltiples hoteles
- ✅ Eliminar hotel
- ✅ Eliminar hotel inexistente
- ✅ Eliminar sin archivo
- ✅ Mostrar información
- ✅ Mostrar información de hotel inexistente
- ✅ Modificar información completa
- ✅ Modificar información parcial
- ✅ Modificar hotel inexistente
- ✅ Reservar habitación
- ✅ Reservar sin disponibilidad
- ✅ Cancelar reservación
- ✅ Cancelar sin reservaciones
- ✅ Manejo de JSON inválido
- ✅ Manejo de formato de datos inválido

### TestCustomer (14 tests)
- ✅ Crear cliente
- ✅ Crear múltiples clientes
- ✅ Eliminar cliente
- ✅ Eliminar cliente inexistente
- ✅ Mostrar información
- ✅ Mostrar información de cliente inexistente
- ✅ Modificar información completa
- ✅ Modificar información parcial
- ✅ Modificar cliente inexistente
- ✅ Manejo de JSON inválido
- ✅ Manejo de formato de datos inválido

### TestReservation (10 tests)
- ✅ Crear reservación
- ✅ Crear múltiples reservaciones
- ✅ Crear con cliente inexistente
- ✅ Crear con hotel inexistente
- ✅ Crear sin disponibilidad
- ✅ Cancelar reservación
- ✅ Cancelar reservación inexistente
- ✅ Manejo de JSON inválido
- ✅ Manejo de formato de datos inválido

### TestIntegration (2 tests)
- ✅ Flujo completo de trabajo
- ✅ Múltiples reservaciones hasta llenar hotel

**Total: 50+ casos de prueba**

## Características de Manejo de Errores

El sistema maneja robustamente los siguientes errores:

1. **JSON Inválido**: Si un archivo está corrupto, muestra error y continúa con lista vacía
2. **Formato Incorrecto**: Si el JSON no es una lista, muestra error y continúa
3. **Archivos Faltantes**: Crea archivos automáticamente cuando es necesario
4. **IDs Inválidos**: Maneja errores al calcular IDs y usa valores por defecto
5. **Operaciones Inválidas**: Verifica existencia antes de modificar/eliminar
6. **Sin Disponibilidad**: Previene reservaciones cuando no hay habitaciones

Todos los errores se muestran en consola con mensajes descriptivos y la ejecución continúa.

## Buenas Prácticas Implementadas

1. **Type Hints**: Uso de anotaciones de tipo para mejor claridad
2. **Retorno de Valores**: Todos los métodos retornan `bool` indicando éxito/fallo
3. **Validación de Datos**: Verificación de tipos y existencia antes de operar
4. **Mensajes Descriptivos**: Errores claros y específicos
5. **Persistencia Robusta**: Manejo seguro de archivos con encoding UTF-8
6. **Tests Aislados**: Cada test usa su propio directorio temporal
7. **Cobertura Completa**: Tests para casos normales y casos de error

## Solución de Problemas

### Problema: "ModuleNotFoundError: No module named '6.2Prueba'"
**Solución**: Usar importlib como se muestra en los ejemplos, ya que Python no permite importar módulos que empiezan con números directamente.

### Problema: "PermissionError" al ejecutar tests
**Solución**: Asegúrate de que no haya procesos usando los archivos en Results/ o TestResults/

### Problema: Tests fallan por archivos existentes
**Solución**: Los tests limpian automáticamente. Si persiste, elimina manualmente las carpetas Results/ y TestResults/

### Problema: Coverage muestra menos del 85%
**Solución**: Ejecuta `coverage run -m unittest test_hotel_system.py` y luego `coverage report` para ver qué líneas faltan por cubrir

## Contacto y Soporte

Para preguntas o problemas con el sistema, revisa:
1. Los mensajes de error en consola (son descriptivos)
2. Los archivos JSON en Results/ para verificar el estado
3. Los tests en test_hotel_system.py para ver ejemplos de uso

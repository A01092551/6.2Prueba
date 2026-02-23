# Lógica de Reservaciones - Sistema de Gestión de Hoteles

## 📚 Explicación Detallada

### 1. **`Hotel.reserve_room(customer_id)` - Reservar Habitación**

#### **Propósito:**
Reduce el número de habitaciones disponibles en el hotel cuando se hace una reservación.

#### **Proceso:**
```python
def reserve_room(self, customer_id: int) -> bool:
    # 1. Lee el archivo Hotels.json
    # 2. Busca el hotel por su ID
    # 3. Verifica que haya habitaciones disponibles (> 0)
    # 4. Reduce habitaciones_disponibles en 1
    # 5. Guarda el cambio en el archivo
    # 6. Retorna True si tuvo éxito, False si no
```

#### **Ejemplo:**
```python
hotel = Hotel("Grand Palace", "Veracruz", 150)
hotel.create()  # habitaciones_disponibles = 150

hotel.reserve_room(customer_id=1)  # habitaciones_disponibles = 149
hotel.reserve_room(customer_id=2)  # habitaciones_disponibles = 148
```

---

### 2. **`Reservation.create()` - Crear Reservación**

#### **Propósito:**
Crea un registro de reservación que vincula un cliente con un hotel.

#### **Proceso:**
```python
def create(self) -> bool:
    # 1. Verifica que el cliente exista en Customers.json
    # 2. Verifica que el hotel exista en Hotels.json
    # 3. LLAMA A hotel.reserve_room(customer_id) ← IMPORTANTE
    # 4. Si todo OK, crea el registro en Reservations.json
    # 5. Retorna True si tuvo éxito, False si no
```

#### **Flujo Completo:**
```
Usuario → Reservation.create()
            ↓
         Verifica Cliente existe
            ↓
         Verifica Hotel existe
            ↓
         Hotel.reserve_room(customer_id) ← Reduce habitaciones
            ↓
         Crea registro en Reservations.json
```

#### **Ejemplo:**
```python
# Crear hotel y cliente
hotel = Hotel("Grand Palace", "Veracruz", 150)
hotel.create()

customer = Customer("Juan", "juan@email.com", "555-1234")
customer.create()

# Crear reservación (automáticamente reduce habitaciones)
reservation = Reservation(customer.id, hotel.id)
reservation.create()
# Internamente llama: hotel.reserve_room(customer.id)
# Resultado: habitaciones_disponibles = 149
```

---

### 3. **`Hotel.cancel_reservation(customer_id)` - Cancelar Reservación del Hotel**

#### **Propósito:**
Libera una habitación en el hotel (aumenta habitaciones disponibles).

#### **Proceso:**
```python
def cancel_reservation(self, customer_id: int) -> bool:
    # 1. Lee el archivo Hotels.json
    # 2. Busca el hotel por su ID
    # 3. Verifica que haya reservaciones (disponibles < total)
    # 4. Aumenta habitaciones_disponibles en 1
    # 5. Guarda el cambio en el archivo
    # 6. Retorna True si tuvo éxito, False si no
```

---

### 4. **`Reservation.cancel()` - Cancelar Reservación**

#### **Propósito:**
Cancela una reservación y libera la habitación en el hotel.

#### **Proceso:**
```python
def cancel(self) -> bool:
    # 1. Lee el archivo Reservations.json
    # 2. Busca la reservación por su ID
    # 3. LLAMA A hotel.cancel_reservation(customer_id) ← IMPORTANTE
    # 4. Elimina el registro de Reservations.json
    # 5. Retorna True si tuvo éxito, False si no
```

#### **Flujo Completo:**
```
Usuario → Reservation.cancel()
            ↓
         Busca reservación en Reservations.json
            ↓
         Hotel.cancel_reservation(customer_id) ← Libera habitación
            ↓
         Elimina registro de Reservations.json
```

---

## 🔄 Relación entre Métodos

### **Crear Reservación:**
```
Reservation.create() → Hotel.reserve_room()
```
- `Reservation.create()` es el método público que usa el usuario
- Internamente llama a `Hotel.reserve_room()` para actualizar disponibilidad

### **Cancelar Reservación:**
```
Reservation.cancel() → Hotel.cancel_reservation()
```
- `Reservation.cancel()` es el método público que usa el usuario
- Internamente llama a `Hotel.cancel_reservation()` para liberar habitación

---

## 🐛 Problemas Corregidos

### **Problema 1: `modify_info()` no actualizaba habitaciones disponibles**

**Antes:**
```python
if habitaciones is not None:
    hotel['habitaciones'] = habitaciones
    self.habitaciones = habitaciones
    # ❌ No actualizaba habitaciones_disponibles
```

**Después:**
```python
if habitaciones is not None:
    # Calcular habitaciones ocupadas
    old_total = hotel.get('habitaciones', 0)
    old_disponibles = hotel.get('habitaciones_disponibles', 0)
    ocupadas = old_total - old_disponibles
    
    # Calcular nuevas disponibles
    new_disponibles = habitaciones - ocupadas
    
    # Actualizar ambos valores
    hotel['habitaciones'] = habitaciones
    hotel['habitaciones_disponibles'] = new_disponibles
    self.habitaciones = habitaciones
    self.habitaciones_disponibles = new_disponibles
```

**Ejemplo:**
```python
# Hotel con 150 habitaciones, 3 ocupadas (147 disponibles)
hotel.modify_info(habitaciones=200)
# Resultado: 200 habitaciones, 3 ocupadas (197 disponibles) ✓
```

---

## 📊 Ejemplo Completo de Flujo

```python
# 1. Crear hotel con 100 habitaciones
hotel = Hotel("Grand Palace", "Veracruz", 100)
hotel.create()
# Estado: total=100, disponibles=100

# 2. Crear clientes
customer1 = Customer("Ana", "ana@email.com", "555-0001")
customer1.create()

customer2 = Customer("Luis", "luis@email.com", "555-0002")
customer2.create()

# 3. Crear reservaciones
reservation1 = Reservation(customer1.id, hotel.id)
reservation1.create()
# Estado: total=100, disponibles=99 (Ana reservó)

reservation2 = Reservation(customer2.id, hotel.id)
reservation2.create()
# Estado: total=100, disponibles=98 (Luis reservó)

# 4. Modificar hotel (aumentar habitaciones)
hotel.modify_info(habitaciones=150)
# Estado: total=150, disponibles=148 (mantiene las 2 ocupadas)

# 5. Cancelar una reservación
reservation1.cancel()
# Estado: total=150, disponibles=149 (Ana canceló)

# 6. Cancelar otra reservación
reservation2.cancel()
# Estado: total=150, disponibles=150 (Luis canceló)
```

---

## ✅ Verificación de Funcionamiento

### **Test 1: Reservar reduce disponibles**
```python
hotel = Hotel("Test", "Test", 50)
hotel.create()
print(hotel.habitaciones_disponibles)  # 50

reservation = Reservation(customer_id, hotel.id)
reservation.create()
hotel.display_info()  # Muestra disponibles=49 ✓
```

### **Test 2: Cancelar aumenta disponibles**
```python
reservation.cancel()
hotel.display_info()  # Muestra disponibles=50 ✓
```

### **Test 3: Modificar habitaciones mantiene ocupadas**
```python
# Hotel: 100 total, 95 disponibles (5 ocupadas)
hotel.modify_info(habitaciones=200)
# Resultado: 200 total, 195 disponibles (5 ocupadas) ✓
```

---

## 🎯 Resumen

| Método | Acción | Efecto en Habitaciones |
|--------|--------|------------------------|
| `Reservation.create()` | Crea reservación | ⬇️ Reduce disponibles en 1 |
| `Reservation.cancel()` | Cancela reservación | ⬆️ Aumenta disponibles en 1 |
| `Hotel.reserve_room()` | Reserva directa | ⬇️ Reduce disponibles en 1 |
| `Hotel.cancel_reservation()` | Cancela directa | ⬆️ Aumenta disponibles en 1 |
| `Hotel.modify_info(habitaciones=N)` | Cambia total | ✓ Mantiene ocupadas constantes |

---

## 💡 Notas Importantes

1. **Siempre usa `Reservation.create()`** en lugar de llamar directamente a `hotel.reserve_room()`
   - `Reservation.create()` crea el registro Y actualiza el hotel
   - `hotel.reserve_room()` solo actualiza el hotel (no crea registro)

2. **Siempre usa `Reservation.cancel()`** en lugar de llamar directamente a `hotel.cancel_reservation()`
   - `Reservation.cancel()` elimina el registro Y libera la habitación
   - `hotel.cancel_reservation()` solo libera la habitación (no elimina registro)

3. **`modify_info()` es inteligente:**
   - Si aumentas habitaciones: aumenta disponibles proporcionalmente
   - Si reduces habitaciones: reduce disponibles proporcionalmente
   - Siempre mantiene el número de habitaciones ocupadas constante

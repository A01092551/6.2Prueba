import unittest
import json
import os
import shutil
from pathlib import Path
from io import StringIO
import sys
import importlib.util

spec = importlib.util.spec_from_file_location("hotel_module", "6.2Prueba.py")
hotel_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hotel_module)

Hotel = hotel_module.Hotel
Customer = hotel_module.Customer
Reservation = hotel_module.Reservation


class TestHotel(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path("TestResults")
        Hotel.output_dir = cls.test_dir
        Customer.output_dir = cls.test_dir
        Reservation.output_dir = cls.test_dir
    
    def setUp(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
    
    def tearDown(self):
        sys.stdout = sys.__stdout__
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_hotel_create(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        result = hotel.create()
        
        self.assertTrue(result)
        self.assertEqual(hotel.id, 1)
        self.assertEqual(hotel.habitaciones_disponibles, 100)
        
        hotels_file = self.test_dir / "Hotels.json"
        self.assertTrue(hotels_file.exists())
        
        with open(hotels_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], "Test Hotel")
    
    def test_hotel_create_multiple(self):
        hotel1 = Hotel("Hotel 1", "State 1", 50)
        hotel2 = Hotel("Hotel 2", "State 2", 75)
        
        hotel1.create()
        hotel2.create()
        
        self.assertEqual(hotel1.id, 1)
        self.assertEqual(hotel2.id, 2)
        
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 2)
    
    def test_hotel_delete(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        result = hotel.delete()
        self.assertTrue(result)
        
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 0)
    
    def test_hotel_delete_nonexistent(self):
        hotel = Hotel("Test Hotel", "Test State", 100, hotel_id=999)
        result = hotel.delete()
        
        self.assertFalse(result)
    
    def test_hotel_delete_no_file(self):
        hotel = Hotel("Test Hotel", "Test State", 100, hotel_id=1)
        result = hotel.delete()
        
        self.assertFalse(result)
    
    def test_hotel_display_info(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        info = hotel.display_info()
        
        self.assertEqual(info['id'], 1)
        self.assertEqual(info['nombre'], "Test Hotel")
        self.assertEqual(info['estado'], "Test State")
        self.assertEqual(info['habitaciones'], 100)
    
    def test_hotel_display_info_nonexistent(self):
        hotel = Hotel("Test Hotel", "Test State", 100, hotel_id=999)
        info = hotel.display_info()
        
        self.assertEqual(info, {})
    
    def test_hotel_modify_info(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        result = hotel.modify_info(nombre="Modified Hotel", estado="New State")
        self.assertTrue(result)
        
        info = hotel.display_info()
        self.assertEqual(info['nombre'], "Modified Hotel")
        self.assertEqual(info['estado'], "New State")
    
    def test_hotel_modify_info_partial(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        result = hotel.modify_info(nombre="Modified Hotel")
        self.assertTrue(result)
        
        info = hotel.display_info()
        self.assertEqual(info['nombre'], "Modified Hotel")
        self.assertEqual(info['estado'], "Test State")
    
    def test_hotel_modify_info_nonexistent(self):
        hotel = Hotel("Test Hotel", "Test State", 100, hotel_id=999)
        result = hotel.modify_info(nombre="Modified")
        
        self.assertFalse(result)
    
    def test_hotel_reserve_room(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        result = hotel.reserve_room(customer_id=1)
        self.assertTrue(result)
        
        info = hotel.display_info()
        self.assertEqual(info['habitaciones_disponibles'], 99)
    
    def test_hotel_reserve_room_no_availability(self):
        hotel = Hotel("Test Hotel", "Test State", 0)
        hotel.create()
        
        result = hotel.reserve_room(customer_id=1)
        self.assertFalse(result)
    
    def test_hotel_cancel_reservation(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        hotel.reserve_room(customer_id=1)
        
        result = hotel.cancel_reservation(customer_id=1)
        self.assertTrue(result)
        
        info = hotel.display_info()
        self.assertEqual(info['habitaciones_disponibles'], 100)
    
    def test_hotel_cancel_reservation_no_reservations(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        result = hotel.cancel_reservation(customer_id=1)
        self.assertFalse(result)
    
    def test_hotel_invalid_json(self):
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'w') as f:
            f.write("invalid json {{{")
        
        hotel = Hotel("Test Hotel", "Test State", 100)
        result = hotel.create()
        
        self.assertTrue(result)
        self.assertEqual(hotel.id, 1)
    
    def test_hotel_invalid_data_format(self):
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        hotel = Hotel("Test Hotel", "Test State", 100)
        result = hotel.create()
        
        self.assertTrue(result)
        self.assertEqual(hotel.id, 1)


class TestCustomer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path("TestResults")
        Hotel.output_dir = cls.test_dir
        Customer.output_dir = cls.test_dir
        Reservation.output_dir = cls.test_dir
    
    def setUp(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
    
    def tearDown(self):
        sys.stdout = sys.__stdout__
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_customer_create(self):
        customer = Customer("John Doe", "john@email.com", "555-1234")
        result = customer.create()
        
        self.assertTrue(result)
        self.assertEqual(customer.id, 1)
        
        customers_file = self.test_dir / "Customers.json"
        self.assertTrue(customers_file.exists())
        
        with open(customers_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], "John Doe")
    
    def test_customer_create_multiple(self):
        customer1 = Customer("John Doe", "john@email.com", "555-1234")
        customer2 = Customer("Jane Smith", "jane@email.com", "555-5678")
        
        customer1.create()
        customer2.create()
        
        self.assertEqual(customer1.id, 1)
        self.assertEqual(customer2.id, 2)
    
    def test_customer_delete(self):
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        result = customer.delete()
        self.assertTrue(result)
        
        customers_file = self.test_dir / "Customers.json"
        with open(customers_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 0)
    
    def test_customer_delete_nonexistent(self):
        customer = Customer("John Doe", "john@email.com", "555-1234", customer_id=999)
        result = customer.delete()
        
        self.assertFalse(result)
    
    def test_customer_display_info(self):
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        info = customer.display_info()
        
        self.assertEqual(info['id'], 1)
        self.assertEqual(info['nombre'], "John Doe")
        self.assertEqual(info['email'], "john@email.com")
        self.assertEqual(info['telefono'], "555-1234")
    
    def test_customer_display_info_nonexistent(self):
        customer = Customer("John Doe", "john@email.com", "555-1234", customer_id=999)
        info = customer.display_info()
        
        self.assertEqual(info, {})
    
    def test_customer_modify_info(self):
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        result = customer.modify_info(nombre="John Smith", email="johnsmith@email.com")
        self.assertTrue(result)
        
        info = customer.display_info()
        self.assertEqual(info['nombre'], "John Smith")
        self.assertEqual(info['email'], "johnsmith@email.com")
    
    def test_customer_modify_info_partial(self):
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        result = customer.modify_info(telefono="555-9999")
        self.assertTrue(result)
        
        info = customer.display_info()
        self.assertEqual(info['telefono'], "555-9999")
        self.assertEqual(info['nombre'], "John Doe")
    
    def test_customer_modify_info_nonexistent(self):
        customer = Customer("John Doe", "john@email.com", "555-1234", customer_id=999)
        result = customer.modify_info(nombre="Modified")
        
        self.assertFalse(result)
    
    def test_customer_invalid_json(self):
        customers_file = self.test_dir / "Customers.json"
        with open(customers_file, 'w') as f:
            f.write("invalid json {{{")
        
        customer = Customer("John Doe", "john@email.com", "555-1234")
        result = customer.create()
        
        self.assertTrue(result)
        self.assertEqual(customer.id, 1)
    
    def test_customer_invalid_data_format(self):
        customers_file = self.test_dir / "Customers.json"
        with open(customers_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        customer = Customer("John Doe", "john@email.com", "555-1234")
        result = customer.create()
        
        self.assertTrue(result)
        self.assertEqual(customer.id, 1)


class TestReservation(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path("TestResults")
        Hotel.output_dir = cls.test_dir
        Customer.output_dir = cls.test_dir
        Reservation.output_dir = cls.test_dir
    
    def setUp(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
    
    def tearDown(self):
        sys.stdout = sys.__stdout__
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_reservation_create(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        reservation = Reservation(customer.id, hotel.id)
        result = reservation.create()
        
        self.assertTrue(result)
        self.assertEqual(reservation.id, 1)
        
        reservations_file = self.test_dir / "Reservations.json"
        self.assertTrue(reservations_file.exists())
        
        with open(reservations_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['customer_id'], customer.id)
        self.assertEqual(data[0]['hotel_id'], hotel.id)
    
    def test_reservation_create_multiple(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        customer1 = Customer("John Doe", "john@email.com", "555-1234")
        customer1.create()
        
        customer2 = Customer("Jane Smith", "jane@email.com", "555-5678")
        customer2.create()
        
        reservation1 = Reservation(customer1.id, hotel.id)
        reservation2 = Reservation(customer2.id, hotel.id)
        
        reservation1.create()
        reservation2.create()
        
        self.assertEqual(reservation1.id, 1)
        self.assertEqual(reservation2.id, 2)
    
    def test_reservation_create_nonexistent_customer(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        reservation = Reservation(customer_id=999, hotel_id=hotel.id)
        result = reservation.create()
        
        self.assertFalse(result)
    
    def test_reservation_create_nonexistent_hotel(self):
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        reservation = Reservation(customer_id=customer.id, hotel_id=999)
        result = reservation.create()
        
        self.assertFalse(result)
    
    def test_reservation_create_no_availability(self):
        hotel = Hotel("Test Hotel", "Test State", 0)
        hotel.create()
        
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        reservation = Reservation(customer.id, hotel.id)
        result = reservation.create()
        
        self.assertFalse(result)
    
    def test_reservation_cancel(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        reservation = Reservation(customer.id, hotel.id)
        reservation.create()
        
        result = reservation.cancel()
        self.assertTrue(result)
        
        reservations_file = self.test_dir / "Reservations.json"
        with open(reservations_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 0)
        
        hotel_info = hotel.display_info()
        self.assertEqual(hotel_info['habitaciones_disponibles'], 100)
    
    def test_reservation_cancel_nonexistent(self):
        reservation = Reservation(customer_id=1, hotel_id=1, reservation_id=999)
        result = reservation.cancel()
        
        self.assertFalse(result)
    
    def test_reservation_invalid_json(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        reservations_file = self.test_dir / "Reservations.json"
        with open(reservations_file, 'w') as f:
            f.write("invalid json {{{")
        
        reservation = Reservation(customer.id, hotel.id)
        result = reservation.create()
        
        self.assertTrue(result)
        self.assertEqual(reservation.id, 1)
    
    def test_reservation_invalid_data_format(self):
        hotel = Hotel("Test Hotel", "Test State", 100)
        hotel.create()
        
        customer = Customer("John Doe", "john@email.com", "555-1234")
        customer.create()
        
        reservations_file = self.test_dir / "Reservations.json"
        with open(reservations_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        reservation = Reservation(customer.id, hotel.id)
        result = reservation.create()
        
        self.assertTrue(result)
        self.assertEqual(reservation.id, 1)


class TestIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path("TestResults")
        Hotel.output_dir = cls.test_dir
        Customer.output_dir = cls.test_dir
        Reservation.output_dir = cls.test_dir
    
    def setUp(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
    
    def tearDown(self):
        sys.stdout = sys.__stdout__
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_full_workflow(self):
        hotel = Hotel("Grand Hotel", "California", 50)
        hotel.create()
        
        customer = Customer("Alice Johnson", "alice@email.com", "555-0001")
        customer.create()
        
        reservation = Reservation(customer.id, hotel.id)
        reservation.create()
        
        hotel_info = hotel.display_info()
        self.assertEqual(hotel_info['habitaciones_disponibles'], 49)
        
        hotel.modify_info(nombre="Grand Palace Hotel")
        hotel_info = hotel.display_info()
        self.assertEqual(hotel_info['nombre'], "Grand Palace Hotel")
        
        customer.modify_info(email="alice.johnson@email.com")
        customer_info = customer.display_info()
        self.assertEqual(customer_info['email'], "alice.johnson@email.com")
        
        reservation.cancel()
        hotel_info = hotel.display_info()
        self.assertEqual(hotel_info['habitaciones_disponibles'], 50)
    
    def test_multiple_reservations(self):
        hotel = Hotel("Test Hotel", "Test State", 5)
        hotel.create()
        
        customers = []
        for i in range(5):
            customer = Customer(f"Customer {i}", f"customer{i}@email.com", f"555-000{i}")
            customer.create()
            customers.append(customer)
        
        reservations = []
        for customer in customers:
            reservation = Reservation(customer.id, hotel.id)
            result = reservation.create()
            self.assertTrue(result)
            reservations.append(reservation)
        
        hotel_info = hotel.display_info()
        self.assertEqual(hotel_info['habitaciones_disponibles'], 0)
        
        extra_customer = Customer("Extra Customer", "extra@email.com", "555-9999")
        extra_customer.create()
        extra_reservation = Reservation(extra_customer.id, hotel.id)
        result = extra_reservation.create()
        self.assertFalse(result)
        
        reservations[0].cancel()
        hotel_info = hotel.display_info()
        self.assertEqual(hotel_info['habitaciones_disponibles'], 1)


class TestErrorHandling(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path("TestResults")
        Hotel.output_dir = cls.test_dir
        Customer.output_dir = cls.test_dir
        Reservation.output_dir = cls.test_dir
    
    def setUp(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
    
    def tearDown(self):
        sys.stdout = sys.__stdout__
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_hotel_delete_empty_file(self):
        hotels_file = self.test_dir / "Hotels.json"
        hotels_file.touch()
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        result = hotel.delete()
        self.assertFalse(result)
    
    def test_customer_delete_empty_file(self):
        customers_file = self.test_dir / "Customers.json"
        customers_file.touch()
        
        customer = Customer("Test", "test@email.com", "555-0000", customer_id=1)
        result = customer.delete()
        self.assertFalse(result)
    
    def test_reservation_cancel_empty_file(self):
        reservations_file = self.test_dir / "Reservations.json"
        reservations_file.touch()
        
        reservation = Reservation(1, 1, reservation_id=1)
        result = reservation.cancel()
        self.assertFalse(result)
    
    def test_hotel_display_empty_file(self):
        hotels_file = self.test_dir / "Hotels.json"
        hotels_file.touch()
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        info = hotel.display_info()
        self.assertEqual(info, {})
    
    def test_customer_display_empty_file(self):
        customers_file = self.test_dir / "Customers.json"
        customers_file.touch()
        
        customer = Customer("Test", "test@email.com", "555-0000", customer_id=1)
        info = customer.display_info()
        self.assertEqual(info, {})
    
    def test_hotel_modify_empty_file(self):
        hotels_file = self.test_dir / "Hotels.json"
        hotels_file.touch()
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        result = hotel.modify_info(nombre="New Name")
        self.assertFalse(result)
    
    def test_customer_modify_empty_file(self):
        customers_file = self.test_dir / "Customers.json"
        customers_file.touch()
        
        customer = Customer("Test", "test@email.com", "555-0000", customer_id=1)
        result = customer.modify_info(nombre="New Name")
        self.assertFalse(result)
    
    def test_hotel_reserve_room_empty_file(self):
        hotels_file = self.test_dir / "Hotels.json"
        hotels_file.touch()
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        result = hotel.reserve_room(customer_id=1)
        self.assertFalse(result)
    
    def test_hotel_cancel_reservation_empty_file(self):
        hotels_file = self.test_dir / "Hotels.json"
        hotels_file.touch()
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        result = hotel.cancel_reservation(customer_id=1)
        self.assertFalse(result)
    
    def test_hotel_delete_invalid_format(self):
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        result = hotel.delete()
        self.assertFalse(result)
    
    def test_customer_delete_invalid_format(self):
        customers_file = self.test_dir / "Customers.json"
        with open(customers_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        customer = Customer("Test", "test@email.com", "555-0000", customer_id=1)
        result = customer.delete()
        self.assertFalse(result)
    
    def test_reservation_cancel_invalid_format(self):
        reservations_file = self.test_dir / "Reservations.json"
        with open(reservations_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        reservation = Reservation(1, 1, reservation_id=1)
        result = reservation.cancel()
        self.assertFalse(result)
    
    def test_hotel_display_invalid_format(self):
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        info = hotel.display_info()
        self.assertEqual(info, {})
    
    def test_customer_display_invalid_format(self):
        customers_file = self.test_dir / "Customers.json"
        with open(customers_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        customer = Customer("Test", "test@email.com", "555-0000", customer_id=1)
        info = customer.display_info()
        self.assertEqual(info, {})
    
    def test_hotel_modify_invalid_format(self):
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        result = hotel.modify_info(nombre="New Name")
        self.assertFalse(result)
    
    def test_customer_modify_invalid_format(self):
        customers_file = self.test_dir / "Customers.json"
        with open(customers_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        customer = Customer("Test", "test@email.com", "555-0000", customer_id=1)
        result = customer.modify_info(nombre="New Name")
        self.assertFalse(result)
    
    def test_hotel_reserve_room_invalid_format(self):
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        result = hotel.reserve_room(customer_id=1)
        self.assertFalse(result)
    
    def test_hotel_cancel_reservation_invalid_format(self):
        hotels_file = self.test_dir / "Hotels.json"
        with open(hotels_file, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        hotel = Hotel("Test", "Test", 100, hotel_id=1)
        result = hotel.cancel_reservation(customer_id=1)
        self.assertFalse(result)
    
    def test_hotel_reserve_room_nonexistent(self):
        hotel = Hotel("Test", "Test", 100, hotel_id=999)
        result = hotel.reserve_room(customer_id=1)
        self.assertFalse(result)
    
    def test_hotel_cancel_reservation_nonexistent(self):
        hotel = Hotel("Test", "Test", 100, hotel_id=999)
        result = hotel.cancel_reservation(customer_id=1)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)

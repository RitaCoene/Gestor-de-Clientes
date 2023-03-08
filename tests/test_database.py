import unittest
import database as db
import copy
import config
import csv
import helpers


class TestDataBase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('34F', 'Martin', 'Ponce'),
            db.Cliente('65H', 'Tomas', 'Fernandez'),
            db.Cliente('92M', 'Valentina', 'Gomez')
        ]

    def test_buscar(self):
        cliente_existente = db.Clientes.buscar('92M')
        cliente_inexistente = db.Clientes.buscar('36B')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear(self):
        cliente_nuevo = db.Clientes.crear('74G','Matias', 'Ponce')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(cliente_nuevo.dni, '74G')
        self.assertEqual(cliente_nuevo.nombre, 'Matias')
        self.assertEqual(cliente_nuevo.apellido, 'Ponce')


    def test_modificar(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('65H'))
        cliente_modificado = db.Clientes.modificar('65H', 'Javier', 'Medina')
        self.assertEqual(cliente_a_modificar.nombre, 'Tomas')
        self.assertEqual(cliente_modificado.nombre, 'Javier')


    def test_borrar(self):
        cliente_borrado = db.Clientes.borrar('34F')
        cliente_buscado = db.Clientes.buscar('34F')
        self.assertEqual(cliente_borrado.dni, '34F')
        self.assertIsNone(cliente_buscado)

    def test_dni(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('345344', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F45', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('34F', db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('34F')
        db.Clientes.borrar('65H')
        db.Clientes.modificar('92M', 'Valentina', 'Garcia')

        dni, nombre, apellido = None, None, None

        with open(config.DATABASE_PATH, newline='\n') as fichero:
            reader = csv.reader(fichero, delimiter=';')
            dni, nombre, apellido = next(reader)

        
        self.assertEqual(dni, '92M')
        self.assertEqual(nombre, 'Valentina')
        self.assertEqual(apellido, 'Garcia')




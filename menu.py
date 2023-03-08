import os
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()

        print('======================')
        print(' Bienvenido al Gestor ')
        print('======================')
        print('[1] Lista de clientes ')
        print('[2] Buscar cliente    ')
        print('[3] Añadir cliente    ')
        print('[4] Modificar cliente ')
        print('[5] Borrar cliente    ')
        print('[6] Cerrra gestor     ')
        print('======================')


        opcion = input('> ')
        helpers.limpiar_pantalla()
        

        if opcion == '1':
            print('Listando los clientes...\n')
            for cliente in db.Clientes.lista:
                print(cliente)

        elif opcion == '2':
            print('Buscando cliente...\n')
            dni = helpers.leer_texto(3,3,'DNI (2 init y 1 char)').upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else 'Cliente no encontrado.'

        elif opcion == '3':
            print('Añadiendo cliente...\n')
            dni = None

            while True:
                dni = helpers.leer_texto(3,3, 'DNI 2 init y 1 char').upper()
                if helpers.dni_valido(dni, db.Clientes.lista):
                    break

            nombre = helpers.leer_texto(2,30, 'Nombre (de 2 a 30 char)').capitalize()
            apellido = helpers.leer_texto(3,30, 'Apellido (de 2 a 30 char)').capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print('Cliente añadido correctamente.')

        elif opcion == '4':
            print('Modificando cliente...\n')
            dni = helpers.leer_texto(3,3, 'DNI (2 init y 1 char)').upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(2,30, 'Nombre (de 2 a 30 char)').capitalize()
                apellido = helpers.leer_texto(3,30, 'Apellido (de 2 a 30 char)').capitalize()
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print('Cliente modificado correctamente.')
            else:
                print('Cliente no encontrado.')


        elif opcion == '5':
            print('Borrando cliente...\n')
            dni = helpers.leer_texto(3,3, 'DNI (2 init y 1 char)').upper()
            print('Cliente borrado correctamente.') if db.Clientes.borrar(dni) else print('Cliente no encontrado.')
            

        elif opcion == '6':
            print('Saliendo...\n')
            break

        input('\n Presiona ENTER para continuar...')
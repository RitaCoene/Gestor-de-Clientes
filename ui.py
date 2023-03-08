from tkinter import *
import database as db
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
import helpers



class CenterMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)

        self.geometry(f'{w}x{h}+{x}+{y}')


class CreateClient(Toplevel, CenterMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Create Client')
        self.built()
        self.center()
        self.transient(parent)
        self.grab_set()

    def built(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text='DNI (2 ints and 1 upper char)').grid(row=0, column=0)
        Label(frame, text='Nombre (of 2 to 30 chars)').grid(row=0, column=1)
        Label(frame, text='Apellido (of 2 to 30 chars)').grid(row=0, column=2)

        dni = Entry(frame)
        dni.bind('<KeyRelease>', lambda event: self.validate(event, 0))
        dni.grid(row=1, column=0, padx=10)

        nombre = Entry(frame)
        nombre.bind('<KeyRelease>', lambda event: self.validate(event, 1))
        nombre.grid(row=1, column=1, padx=10)

        apellido = Entry(frame)
        apellido.bind('<KeyRelease>', lambda event: self.validate(event, 2))
        apellido.grid(row=1, column=2, padx=10)



        frame = Frame(self)
        frame.pack(pady=10)

        crear = Button(frame, text='CREATE', command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text='CANCEL', command=self.close).grid(row=0, column=1)

        self.validaciones = [False, False, False]
        self.crear = crear
        self.dni = dni
        self.apellido = apellido
        self.nombre = nombre


    def create_client(self):
        self.master.treeview.insert(
                parent='', index='end', iid=self.dni.get(),
                values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    
    def validate(self, event, index):
        valor = event.widget.get()
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 else valor.isalpha() \
             and len(valor) >= 2 and len(valor) <= 30
        event.widget.configure({'bg': 'Green' if valido else 'Red'})

        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1,1,1] else DISABLED)


class EditClient(Toplevel, CenterMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Edit Client')
        self.built()
        self.center()
        self.transient(parent)
        self.grab_set()

    def built(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text='DNI (not editable)').grid(row=0, column=0)
        Label(frame, text='Nombre (of 2 to 30 chars)').grid(row=0, column=1)
        Label(frame, text='Apellido (of 2 to 30 chars)').grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0, padx=10)

        nombre = Entry(frame)
        nombre.bind('<KeyRelease>', lambda event: self.validate(event, 0))
        nombre.grid(row=1, column=1, padx=10)

        apellido = Entry(frame)
        apellido.bind('<KeyRelease>', lambda event: self.validate(event, 1))
        apellido.grid(row=1, column=2, padx=10)


        client = self.master.treeview.focus()
        campos = self.master.treeview.item(client, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])



        frame = Frame(self)
        frame.pack(pady=10)

        cambiar = Button(frame, text='CAMBIAR', command=self.edit_client)
        cambiar.grid(row=0, column=0)
        Button(frame, text='CANCEL', command=self.close).grid(row=0, column=1)

        self.validaciones = [True, True]
        self.cambiar = cambiar
        self.dni = dni
        self.apellido = apellido
        self.nombre = nombre


    def edit_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    
    def validate(self, event, index):
        valor = event.widget.get()
        valido = valor.isalpha() and len(valor) >= 2 and len(valor) <= 30
        event.widget.configure({'bg': 'Green' if valido else 'Red'})

        self.validaciones[index] = valido
        self.cambiar.config(state=NORMAL if self.validaciones == [1,1 ] else DISABLED)






class MainWindow(Tk, CenterMixin):

    def __init__(self):
        super().__init__()
        self.title('GESTOR DE CLIENTES')
        self.build()
        self.center()


    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')
        
        treeview.column('#0', width=0, stretch=NO)
        treeview.column('DNI', anchor=CENTER)
        treeview.column('Nombre', anchor=CENTER)
        treeview.column('Apellido', anchor=CENTER)

        treeview.heading('DNI', text='DNI', anchor=CENTER)
        treeview.heading('Nombre', text='NOMBRE', anchor=CENTER)
        treeview.heading('Apellido', text='APELLIDO', anchor=CENTER)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        treeview['yscrollcommand'] = scrollbar.set

        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text='CREATE', command=self.create).grid(row=0, column=0)
        Button(frame, text='MODIFICAR', command=self.edit).grid(row=0, column=1)
        Button(frame, text='DELETE', command=self.delete).grid(row=0, column=2)

        self.treeview = treeview

    
    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, 'values')
            confirmar = askokcancel(
                title='Confirmar Borrado',
                message=f'¿Borrar a {campos[1]} {campos[2]}?',
                icon=WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])


    def create(self):
        CreateClient(self)

    def edit(self):
        if self.treeview.focus():
            EditClient(self)










if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()


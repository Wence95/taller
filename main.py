import tkinter as tk

from database import *
from classes import *

""" index=Tk()
index.title("LOGIN")
index.geometry("300x150")
index.resizable(width=False, height=False)

luser=Label(index, text="Ingrese nombre de usuario:")
luser.pack()

user=StringVar()
euser=Entry(index, width=30, textvariable=user)
euser.pack()

lpas=Label(index, text="Contraseña:")
lpas.pack()

pas=StringVar()
epas=Entry(index, width=30, textvariable=pas, show="*")
epas.pack()

def ingresar():
    if user.get()=="Fabian.Alvarez" and pas.get()=="12345":
        root = Tk()
        
        
        Ventana = Tk()
        Ventana.geometry('850x500')
        Ventana.config(bg='#2a8d90')


        menubar = Menu(root)
        root.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nuevo")
        filemenu.add_command(label="Abrir")
        filemenu.add_command(label="Guardar")
        filemenu.add_command(label="Cerrar")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=root.quit)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cortar")
        editmenu.add_command(label="Copiar")
        editmenu.add_command(label="Pegar")

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Ayuda")
        helpmenu.add_separator()
        helpmenu.add_command(label="Acerca de...")

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Editar", menu=editmenu)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)
        Ventana.mainloop()

b1=Button(index, text="Entrar", command=ingresar)
b1.pack()

index.mainloop() """

def callback(i):
    if i.isdigit():
        return True

    elif i == "":
        return True

    else:
        return False

def main():
    bd = BaseDatos()
    ventana = tk.Tk()
    frame = tk.Frame(ventana)
    auxFrame = tk.Frame(ventana)
    msg = tk.Frame(ventana)
    state = State()

    def clearWindow():
        for widgets in frame.winfo_children():
            widgets.destroy()
        for widgets in auxFrame.winfo_children():
            widgets.destroy()

    def logOut():
        state.estado = False
        state.username = None
        state.profile = None
        clearWindow()
        setIndex()

    def signUp(name, rut, address, phone, email, option):
        if option == 1:
            perfil = "Administrador"
        else:
            perfil = "Bibliotecario"
        bd.ingresar('bibliotecario', ('rut', 'nombre', 'direccion', 'telefono', 'email', 'perfil'), (rut, name, address, phone, email, perfil))
        loggedInWindow()

    def agregarElemento(tabla, elemento):
        if tabla == 'libro':
            bd.ingresar(tabla, ('titulo', 'autor', 'editorial', 'año', 'id'), elemento)
        elif tabla == 'cliente':
            bd.ingresar(tabla, ('rut', 'nombre', 'direccion', 'telefono', 'email'), elemento)
        elif tabla == 'ejemplar':
            bd.ingresar(tabla, ('identificador', 'editorial', 'id'), elemento)
        elif tabla == 'prestamo':
            bd.ingresar(tabla, ('rut_b', 'rut_c', 'id_ejemplar'), elemento)
        loggedInWindow()



    def eliminarElemento(tabla, elemento):
        if tabla == 'bibliotecario' or tabla == 'cliente':
            bd.borrar("'"+elemento+"'", 'rut', tabla)
        else:
            bd.borrar(elemento, 'id', tabla)
        if tabla != 'evento_producto':
            mostrarLista(tabla)
        else:
            loggedInWindow()

    def editarElemento():
        pass
    



         

    def hacerPrestamo(rut_cliente, nombre):
        def lifunction(libro):
            elist = []
            ejest = tk.StringVar()
            titulo = libro.split(" - ")[0]
            itemList = bd.seleccionarBD2(('identificador', 'editorial'), 'ejemplar inner join libro on ejemplar.ID = libro.ID', 
            "titulo = '"+titulo+"'")
            for ejemplar in itemList:
                elist.append(str(ejemplar[0])+" - "+ejemplar[1])
            tk.OptionMenu(frame, ejest, *elist).pack()

            tk.Button(frame, text="Aceptar", command=lambda: agregarElemento('prestamo', (state.rut, rut_cliente, int(ejest.get().split(" - ")[0])))).pack()

        clearWindow()
        tk.Label(frame, text="Hacer préstamo a "+nombre).pack()

        llist = []
        libs = tk.StringVar()
        itemList = bd.seleccionarTabla('libro')
        for libro in itemList:
            llist.append(libro[0]+" - "+libro[1])
        tk.OptionMenu(frame, libs, *llist).pack()
        tk.Button(frame, text="Aceptar", command=lambda: lifunction(libs.get())).pack()

    
    def agregarEjemplar(titulo, id):
        clearWindow()
        tk.Label(frame, text="Nuevo ejemplar del libro "+titulo).pack()
        tk.Label(frame, text="Ingrese ID del ejemplar").pack()
        caja_id = tk.Entry(frame)
        caja_id.insert(tk.END, "0000")
        caja_id.pack()

        tk.Label(frame, text="Ingrese editorial del ejemplar").pack()
        caja_ed = tk.Entry(frame)
        caja_ed.insert(tk.END, "Editorial")
        caja_ed.pack()

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: agregarElemento('ejemplar', (caja_id.get(), caja_ed.get(), id)))
        boton1.pack()

    def entregarLibro(id):
        bd.actualizar('prestamo', ['estado'], ['1'], id)
        mostrarLista('prestamo')

    def mostrarLista(tabla):
        clearWindow()
        i = 0
        ventana.geometry("700x400")
        if tabla == 'bibliotecario':
            tk.Label(frame, text = "RUT").grid(row=0, column=0)
            tk.Label(frame, text="Nombre").grid(row=0, column=1)
            tk.Label(frame, text="Dirección").grid(row=0, column=2)
            tk.Label(frame, text="Teléfono").grid(row=0, column=3)
            tk.Label(frame, text = "email").grid(row=0, column=4)
            tk.Label(frame, text="Perfil").grid(row=0, column=5)
        elif tabla == 'libro':
            tk.Label(frame, text = "Titulo").grid(row=0, column=0)
            tk.Label(frame, text="Autor").grid(row=0, column=1)
            tk.Label(frame, text="Año").grid(row=0, column=2)
            tk.Label(frame, text="ID").grid(row=0, column=3)
        elif tabla == 'ejemplar':
            tk.Label(frame, text = "id").grid(row=0, column=0)
            tk.Label(frame, text="Tipo").grid(row=0, column=1)
            tk.Label(frame, text="Valor").grid(row=0, column=2)
            tk.Label(frame, text="Stock").grid(row=0, column=3)
        elif tabla == 'cliente':
            tk.Label(frame, text = "RUT").grid(row=0, column=0)
            tk.Label(frame, text="Nombre").grid(row=0, column=1)
            tk.Label(frame, text="Dirección").grid(row=0, column=2)
            tk.Label(frame, text="Teléfono").grid(row=0, column=3)
            tk.Label(frame, text = "email").grid(row=0, column=4)
        elif tabla == 'prestamo':
            tk.Label(frame, text="ID Préstamo").grid(row=0, column=0)
            tk.Label(frame, text="RUT").grid(row=0, column=1)
            tk.Label(frame, text="Nombre").grid(row=0, column=2)
            tk.Label(frame, text="Libro").grid(row=0, column=3)
            tk.Label(frame, text="Fecha Préstamo").grid(row=0, column=4)
            tk.Label(frame, text="Estado").grid(row=0, column=5)
        if tabla != 'prestamo':
            lista = bd.seleccionarTabla(tabla)
        else:
            lista = bd.seleccionarBD2(('prestamo.id', 'rut', 'nombre', 'titulo', 'fecha_prestamo', 'estado'), "cliente inner join prestamo on cliente.RUT = prestamo.rut_c inner join ejemplar on prestamo.id_ejemplar = ejemplar.Identificador inner join libro on ejemplar.ID = libro.ID", "true")
        for elemento in lista:
            i += 1
            j = -1
            for word in elemento:
                j += 1
                tk.Label(frame, text=word).grid(row=i, column=j, padx=10, sticky=tk.W)
            if tabla == 'libro' and state.profile == 'Administrador':
                tk.Button(frame, text="Agregar ejemplar", command=lambda elemento=elemento: agregarEjemplar(elemento[0],elemento[3])).grid(row=i, column=j+3)
            if tabla == 'cliente':
                tk.Button(frame, text="Hacer préstamo", command=lambda elemento=elemento: hacerPrestamo(elemento[0], elemento[1])).grid(row=i, column=j+3)
            if tabla == 'prestamo':
                if elemento[5] == 0:
                    tk.Button(frame, text="Libro entregado", command=lambda elemento=elemento: entregarLibro(elemento[0])).grid(row=i, column=j+2)
            if state.profile == 'Administrador':
                if tabla == 'bibliotecario':
                    if elemento[5] != "Administrador":
                        # noinspection PyShadowingNames
                        tk.Button(frame, text="Eliminar",
                                  command=lambda elemento=elemento:
                                  eliminarElemento(tabla, elemento[0])).grid(row=i, column=j+1)
                        # # noinspection PyShadowingNames
                        # tk.Button(frame, text="Editar",
                        #           command=lambda elemento=elemento:
                        #           editarElemento(elemento[0], tabla)).grid(row=i, column=j+2)

                            
                else:
                    # noinspection PyShadowingNames
                    tk.Button(frame, text="Eliminar",
                              command=lambda elemento=elemento:
                              eliminarElemento(tabla, elemento[0])).grid(row=i, column=j+1)
                    # # noinspection PyShadowingNames
                    # tk.Button(frame, text="Editar",
                    #           command=lambda elemento=elemento: editarElemento(elemento[0], tabla)).grid(row=i,
                    #                                                                                   column=j + 2)

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack()

    def registrar(el):
        clearWindow()
        if el == 'bibliotecario':
            option = tk.IntVar()
            option.set(2)
            upperFrame = tk.Frame(frame)

            upperFrame.pack(side=tk.TOP)
            tk.Radiobutton(upperFrame, text="Administrador", variable=option, value=1).pack(side=tk.LEFT)
            tk.Radiobutton(upperFrame, text="Bibliotecario", variable=option, value=2).pack(side=tk.LEFT)

            tk.Label(frame, text="Ingrese rut del usuario").pack()
            caja_rut = tk.Entry(frame)
            caja_rut.insert(tk.END, "RUT")
            caja_rut.pack()

            tk.Label(frame, text="Ingrese nombre").pack()
            caja_name = tk.Entry(frame)
            caja_name.insert(tk.END, "Nombre Apellido")
            caja_name.pack()

            tk.Label(frame, text="Ingrese dirección").pack()
            caja_address = tk.Entry(frame)
            caja_address.insert(tk.END, "Calle 123")
            caja_address.pack()

            tk.Label(frame, text="Ingrese teléfono").pack()
            caja_phone = tk.Entry(frame)
            caja_phone.insert(tk.END, "+56987654321")
            caja_phone.pack()

            tk.Label(frame, text="Ingrese email").pack()
            caja_mail = tk.Entry(frame)
            caja_mail.insert(tk.END, "dirección@email.com")
            caja_mail.pack()

            boton1 = tk.Button(frame, text="Aceptar", command=lambda: signUp(caja_name.get(),
                                                                            caja_rut.get(), caja_address.get(),
                                                                            caja_phone.get(), caja_mail.get(), option.get()))
            boton1.pack()

        elif el == 'cliente':
            tk.Label(frame, text="Ingrese rut del usuario").pack()
            caja_rut = tk.Entry(frame)
            caja_rut.insert(tk.END, "RUT")
            caja_rut.pack()

            tk.Label(frame, text="Ingrese nombre").pack()
            caja_name = tk.Entry(frame)
            caja_name.insert(tk.END, "Nombre Apellido")
            caja_name.pack()

            tk.Label(frame, text="Ingrese dirección").pack()
            caja_address = tk.Entry(frame)
            caja_address.insert(tk.END, "Calle 123")
            caja_address.pack()

            tk.Label(frame, text="Ingrese teléfono").pack()
            caja_phone = tk.Entry(frame)
            caja_phone.insert(tk.END, "+56987654321")
            caja_phone.pack()

            tk.Label(frame, text="Ingrese email").pack()
            caja_mail = tk.Entry(frame)
            caja_mail.insert(tk.END, "dirección@email.com")
            caja_mail.pack()

            boton1 = tk.Button(frame, text="Aceptar", command=lambda: agregarElemento('cliente', (caja_rut.get(), caja_name.get(),
                                                                            caja_address.get(),
                                                                            caja_phone.get(), caja_mail.get())))
            boton1.pack()

        elif el == 'libro':
            tk.Label(frame, text="Ingrese título").pack()
            caja_tit = tk.Entry(frame)
            caja_tit.insert(tk.END, "Título")
            caja_tit.pack()

            tk.Label(frame, text="Ingrese autor").pack()
            caja_name = tk.Entry(frame)
            caja_name.insert(tk.END, "Nombre Apellido")
            caja_name.pack()

            tk.Label(frame, text="Ingrese año").pack()
            caja_year = tk.Entry(frame)
            caja_year.insert(tk.END, "1999")
            caja_year.pack()
            reg = ventana.register(callback)
            caja_year.config(validate="key", validatecommand=(reg, '%P'))

            tk.Label(frame, text="Ingrese ID numérica del libro").pack()
            caja_id = tk.Entry(frame)
            caja_id.insert(tk.END, "0000")
            caja_id.pack()
            reg = ventana.register(callback)
            caja_id.config(validate="key", validatecommand=(reg, '%P'))

            boton1 = tk.Button(frame, text="Aceptar", command=lambda: agregarElemento('libro', (caja_tit.get(),
                                                                            caja_name.get(),
                                                                            caja_year.get(),
                                                                            caja_id.get())))
            boton1.pack()

        boton2 = tk.Button(frame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def loggedInWindow():
        clearWindow()
        ventana.geometry("400x400")
        saludo = tk.Label(frame)
        saludo["text"] = "Hola, " + state.username
        saludo.pack()   

        if state.profile == 'Administrador':
            botonNewLibro = tk.Button(frame, text="Nuevo libro", command=lambda: registrar('libro'))
            botonNewLibro.pack()

            botonNewUsuario = tk.Button(frame, text="Nuevo usuario", command=lambda: registrar('bibliotecario'))
            botonNewUsuario.pack()

            botonNewCliente = tk.Button(frame, text="Nuevo cliente", command=lambda: registrar('cliente'))
            botonNewCliente.pack()

            tk.Label(frame).pack()

            botonListadoUsers = tk.Button(frame, text="Ver usuarios", command=lambda: mostrarLista('bibliotecario'))
            botonListadoUsers.pack()

            botonEventList = tk.Button(frame, text="Ver lista de libros", command=lambda: mostrarLista('libro'))
            botonEventList.pack()

            botonItemList = tk.Button(frame, text="Ver lista de préstamos", command=lambda: mostrarLista('prestamo'))
            botonItemList.pack()

            botonClientList = tk.Button(frame, text="Ver lista de clientes", command=lambda: mostrarLista('cliente'))
            botonClientList.pack()


        if state.profile == 'Bibliotecario':
            botonNewCliente = tk.Button(frame, text="Nuevo cliente", command=lambda: registrar('cliente'))
            botonNewCliente.pack()

            tk.Label(frame).pack()

            botonEventList = tk.Button(frame, text="Ver lista de libros", command=lambda: mostrarLista('libro'))
            botonEventList.pack()

            botonItemList = tk.Button(frame, text="Ver lista de prestamos", command=lambda: mostrarLista('prestamo'))
            botonItemList.pack()

            botonClientList = tk.Button(frame, text="Ver lista de clientes",
                                        command=lambda: mostrarLista('cliente'))
            botonClientList.pack()

        boton = tk.Button(frame, text="Cerrar sesión", command=logOut)
        boton.pack(side=tk.BOTTOM)

    def getUser(_rut):
        # Evitar repetición de mensaje "Usuario o contraseña inválidos"
        for widgets in msg.winfo_children():
            widgets.destroy()
        msg.pack()
        
        user = bd.seleccionarBD(('rut', 'nombre', 'perfil'), 'bibliotecario', "rut='"+_rut+"'")
        if user is not None:
            print("!!")
            state.rut = user[0]
            state.username = user[1]
            state.estado = True
            state.profile = user[2]
            loggedInWindow()
        else:
            etiqueta = tk.Label(msg)
            etiqueta.pack()
            etiqueta["text"] = "Usuario o contraseña inválidos"

    def setIndex():
        ventana.geometry("400x400")
        user_msg = tk.Label(frame)
        user_msg["text"] = "Ingrese su rut"
        user_msg.pack()

        caja_user = tk.Entry(frame)
        caja_user.pack()

        boton = tk.Button(frame, text="Ingresar", command=lambda: getUser(caja_user.get()))
        boton.pack()

    
    frame.pack()
    auxFrame.pack()

    setIndex()

    ventana.mainloop()
    bd.cerrar()


if __name__ == '__main__':
    main()

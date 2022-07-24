import tkinter as tk
from tkinter.ttk import Frame

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

def main():
    bd = BaseDatos()
    ventana = tk.Tk()
    frame = tk.Frame(ventana)
    msg = tk.Frame(ventana)
    state = State()

    def clearWindow():
        for widgets in frame.winfo_children():
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

    def mostrarLista(tabla):
        clearWindow()
        i = 0
        if tabla == 'bibliotecario':
            tk.Label(frame, text = "id").grid(row=0, column=0)
            tk.Label(frame, text="Usuario").grid(row=0, column=1)
            tk.Label(frame, text="Nombre").grid(row=0, column=2)
            tk.Label(frame, text="Perfil").grid(row=0, column=3)
        elif tabla == 'libro':
            tk.Label(frame, text = "id").grid(row=0, column=0)
            tk.Label(frame, text="Evento").grid(row=0, column=1)
            tk.Label(frame, text="Asistencia").grid(row=0, column=2)
            tk.Label(frame, text="Fecha").grid(row=0, column=3)
            tk.Label(frame, text="Hora").grid(row=0, column=4)
        elif tabla == 'ejemplar':
            tk.Label(frame, text = "id").grid(row=0, column=0)
            tk.Label(frame, text="Tipo").grid(row=0, column=1)
            tk.Label(frame, text="Valor").grid(row=0, column=2)
            tk.Label(frame, text="Stock").grid(row=0, column=3)
        elif tabla == 'usuario':
            tk.Label(frame, text="RUT").grid(row=0, column=0)
            tk.Label(frame, text="Nombre").grid(row=0, column=1)
            tk.Label(frame, text="Empresa").grid(row=0, column=2)
            tk.Label(frame, text="Comuna").grid(row=0, column=3)
            tk.Label(frame, text="Numero").grid(row=0, column=4)
            tk.Label(frame, text="email").grid(row=0, column=5)
            tk.Label(frame, text="Método de pago").grid(row=0, column=6)

        lista = bd.seleccionarTabla(tabla)
        for elemento in lista:
            i += 1
            j = -1
            for word in elemento:
                j += 1
                tk.Label(frame, text=word).grid(row=i, column=j, padx=10, sticky=tk.W)
            if state.profile == 'Administrador':
                if tabla == 'bibliotecario':
                    if elemento[3] != "Administrador":
                        # noinspection PyShadowingNames
                        tk.Button(frame, text="Eliminar",
                                  command=lambda elemento=elemento:
                                  eliminarElemento(tabla, elemento[0])).grid(row=i, column=j+1)
                        # noinspection PyShadowingNames
                        tk.Button(frame, text="Editar",
                                  command=lambda elemento=elemento:
                                  editarElemento(elemento[0], tabla)).grid(row=i, column=j+2)
                else:
                    # noinspection PyShadowingNames
                    tk.Button(frame, text="Eliminar",
                              command=lambda elemento=elemento:
                              eliminarElemento(tabla, elemento[0])).grid(row=i, column=j+1)
                    # noinspection PyShadowingNames
                    tk.Button(frame, text="Editar",
                              command=lambda elemento=elemento: editarElemento(elemento[0], tabla)).grid(row=i,
                                                                                                      column=j + 2)
            if tabla == 'producto':
                tk.Button(frame, text="Detalle stock", command=lambda elemento=elemento:
                          graficarProducto(elemento[0])).grid(row=i, column=j+3)

            if tabla == 'evento':
                if not (getProfile(state.username) == "Gestor"):
                    # noinspection PyShadowingNames
                    tk.Button(frame, text="Agregar producto",
                              command=lambda elemento=elemento: producto_evento(elemento[0],
                                                                                tabla)).grid(row=i, column=j + 3)
                # noinspection PyShadowingNames
                tk.Button(frame, text="Detalle",
                          command=lambda elemento=elemento: detalleEvento(elemento[0])).grid(row=i, column=j + 4)

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def registrar(el):
        clearWindow()
        if el == 'usuario':
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

            boton2 = tk.Button(frame, text="Volver", command=loggedInWindow)
            boton2.pack(side=tk.BOTTOM)

    def loggedInWindow():
        clearWindow()
        saludo = tk.Label(frame)
        saludo["text"] = "Hola, " + state.username
        saludo.pack()   

        if state.profile == 'Administrador':
            botonNewLibro = tk.Button(frame, text="Nuevo libro", command=lambda: registrar('libro'))
            botonNewLibro.pack()

            botonNewUsuario = tk.Button(frame, text="Nuevo usuario", command=lambda: registrar('usuario'))
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


        if state.profile == 'Usuario':
            botonListadoUsers = tk.Button(frame, text="Ver usuarios", command=lambda: mostrarLista('usuario'))
            botonListadoUsers.pack()

            botonEventList = tk.Button(frame, text="Ver lista de eventos", command=lambda: mostrarLista('evento'))
            botonEventList.pack()

            botonItemList = tk.Button(frame, text="Ver lista de productos", command=lambda: mostrarLista('producto'))
            botonItemList.pack()

            botonClientList = tk.Button(frame, text="Ver lista de clientes",
                                        command=lambda: mostrarLista('cliente'))
            botonClientList.pack()

        boton = tk.Button(frame, text="Cerrar sesión", command=logOut)
        boton.pack(side=tk.BOTTOM)

    def getUser(rut):
        # Evitar repetición de mensaje "Usuario o contraseña inválidos"
        for widgets in msg.winfo_children():
            widgets.destroy()
        msg.pack()
        
        user = bd.seleccionarBD(('rut', 'nombre', 'perfil'), 'bibliotecario', "rut='"+rut+"'")
        if user is not None:
            print("!!")
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

    setIndex()

    ventana.mainloop()
    bd.cerrar()


if __name__ == '__main__':
    main()

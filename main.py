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

def main():
    bd = BaseDatos()
    ventana = tk.Tk()
    msg = tk.Frame(ventana)
    state = State()

    def clearWindow():
        for widgets in ventana.winfo_children():
            widgets.destroy()

    def loggedInWindow():
        clearWindow()
        saludo = tk.Label(ventana)
        saludo["text"] = "Hola, " + state.username
        saludo.pack()   

        if state.profile == 'Administrador':
            botonNewLibro = tk.Button(ventana, text="Nuevo libro", command=lambda: registrar('libro'))
            botonNewLibro.pack()
            botonNewUsuario = tk.Button(ventana, text="Nuevo usuario", command=lambda: registrar('usuario'))
            botonNewUsuario.pack()
            botonNewCliente = tk.Button(ventana, text="Nuevo cliente", command=lambda: registrar('cliente'))
            botonNewCliente.pack()


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

        boton = tk.Button(ventana, text="Cerrar sesión", command=logOut)
        boton.pack()

    def registrar(el):
        pass

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
        user_msg = tk.Label(ventana)
        user_msg["text"] = "Ingrese su rut"
        user_msg.pack()

        caja_user = tk.Entry(ventana)
        caja_user.pack()

        boton = tk.Button(ventana, text="Ingresar", command=lambda: getUser(caja_user.get()))
        boton.pack()


    setIndex()

    ventana.mainloop()
    bd.cerrar()


if __name__ == '__main__':
    main()

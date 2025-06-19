
import tkinter as tk
from tkinter import messagebox
from modelos.usuarios import Usuario 
from modelos.administrador import Administrador
from modelos.bibliotecario import Bibliotecario
from controladores.controlador_login import verificar_usuario, verificar_bibliotecario, verificar_administrador
from vistas.ventana_principal_usuario import ventana_principal_usuario
from vistas.ventana_principal_bibliotecario import ventana_principal_bibliotecario
from vistas.ventana_principal_administrador import ventana_principal_administrador


class LoginVentana:

    def limpiar_campos(self,entry_correo, entry_contrasena):
        """Limpia los campos de entrada de correo y contraseña."""
        entry_correo.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)

    def cambiarColorBlue(self, event):
        """Cambia el color del texto al pasar el mouse por encima."""
        self.lblregistrousuario.config(fg="#007acc")  

    def cambiarColorNormal(self, event):
        """Cambia el color del texto al quitar el mouse."""
        self.lblregistrousuario.config(fg="#42B35E")  

    def iniciarcomousuario(self, event):
        """Inicia sesión como usuario."""
        correo = self.entrycorreo.get()
        contrasena = self.entrycontrasena.get()
        if not correo or not contrasena:
            messagebox.showerror("Error", "Por favor, ingrese correo y contraseña.")
            return
        # Verifica las credenciales del usuario
        usuario = verificar_usuario(correo, contrasena)
        if usuario:
            self.limpiar_campos(self.entrycorreo, self.entrycontrasena)  # Limpia los campos de entrada
            self.sesion = Usuario(usuario['cedula'], usuario['nombre'], usuario['apellido'], usuario['telefono'], usuario['email'], usuario['contrasena'],id_usuario=usuario['id_usuario'])
            self.ventana.withdraw()  # Oculta la ventana de inicio de sesión
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso como Usuario.")
            ventana_principal_usuario(self.ventana, self.sesion)  # Abre la ventana principal del usuario

            
            

    def iniciarcomobibliotecario(self, event):
        """Inicia sesión como bibliotecario."""
        correo = self.entrycorreo.get()
        contrasena = self.entrycontrasena.get()

        if not correo or not contrasena:
            messagebox.showerror("Error", "Por favor, ingrese correo y contraseña.")
            return
        # Verifica las credenciales del bibliotecario
        bibliotecario = verificar_bibliotecario(correo, contrasena)
        if bibliotecario:
            
            self.limpiar_campos(self.entrycorreo, self.entrycontrasena)  # Limpia los campos de entrada
            self.sesion = Usuario(bibliotecario['cedula'], bibliotecario['nombre'], bibliotecario['apellido'], bibliotecario['telefono'], bibliotecario['email'], bibliotecario['contrasena'])
            self.ventana.withdraw()  # Oculta la ventana de inicio de sesión
            ventana_principal_bibliotecario(self.ventana, self.sesion)
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso como Bibliotecario.")
           

    def iniciarcomoadministrador(self, event):
        """Inicia sesión como administrador."""
        correo = self.entrycorreo.get()
        contrasena = self.entrycontrasena.get()

        if not correo or not contrasena:
            messagebox.showerror("Error", "Por favor, ingrese correo y contraseña.")
            return  
        
        # Verifica las credenciales del administrador
        administrador = verificar_administrador(correo, contrasena)
        if administrador:
            self.limpiar_campos(self.entrycorreo, self.entrycontrasena)  # Limpia los campos de entrada
            self.sesion = Administrador(administrador['cedula'], administrador['nombre'], administrador['apellido'], administrador['telefono'], administrador['email'], administrador['contrasena'])
            self.ventana.withdraw() # Oculta la ventana de inicio de sesión
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso como Administrador.")
            ventana_principal_administrador(self.ventana, self.sesion)  # Abre la ventana principal del administrador

    def ventanaRegistro(self, event):
        # Función interna para registrar usuario
        def registrar():
            cedula = entrycedula.get()
            nombre = entrynombre.get()
            apellido = entryapellido.get()
            telefono = entrytelefono.get()
            email = entrycorreo.get()
            contrasena = entrycontrasena.get()

            if not all([cedula, nombre, apellido, telefono, email, contrasena]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nuevo_usuario = Usuario(cedula, nombre, apellido, telefono, email, contrasena)
                nuevo_usuario.registrar_usuario()
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                ventanaRegistro.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al registrar: {e}")

        """Abre una nueva ventana para el registro de usuario."""
        ventanaRegistro = tk.Toplevel(self.ventana)
        ventanaRegistro.title("Registro de Usuario")
        ventanaRegistro.config(height=650, width=400, bg="#f4f4f4")
        ventanaRegistro.resizable(0, 0)

        # Título
        lbltitulo = tk.Label(ventanaRegistro, text="Registro de Usuario", font=("Segoe UI", 16, "bold"), bg="#f4f4f4", fg="#333")
        lbltitulo.place(relx=0.5, rely=0.07, anchor="center")

        # Cédula
        lblcedula = tk.Label(ventanaRegistro, text="Cédula*:", font=("Segoe UI", 12), bg="#f4f4f4")
        lblcedula.place(relx=0.5, rely=0.15, anchor="center")
        entrycedula = tk.Entry(ventanaRegistro, font=("Segoe UI", 12), width=30)
        entrycedula.place(relx=0.5, rely=0.21, anchor="center")

        # Nombre
        lblnombre = tk.Label(ventanaRegistro, text="Nombre*:", font=("Segoe UI", 12), bg="#f4f4f4")
        lblnombre.place(relx=0.5, rely=0.29, anchor="center")
        entrynombre = tk.Entry(ventanaRegistro, font=("Segoe UI", 12), width=30)
        entrynombre.place(relx=0.5, rely=0.35, anchor="center")

        # Apellido
        lblapellido = tk.Label(ventanaRegistro, text="Apellido*:", font=("Segoe UI", 12), bg="#f4f4f4")
        lblapellido.place(relx=0.5, rely=0.43, anchor="center")
        entryapellido = tk.Entry(ventanaRegistro, font=("Segoe UI", 12), width=30)
        entryapellido.place(relx=0.5, rely=0.49, anchor="center")

        # Teléfono
        lbltelefono = tk.Label(ventanaRegistro, text="Teléfono*:", font=("Segoe UI", 12), bg="#f4f4f4")
        lbltelefono.place(relx=0.5, rely=0.57, anchor="center")
        entrytelefono = tk.Entry(ventanaRegistro, font=("Segoe UI", 12), width=30)
        entrytelefono.place(relx=0.5, rely=0.63, anchor="center")

        # Correo Electrónico
        lblcorreo = tk.Label(ventanaRegistro, text="Correo Electrónico*:", font=("Segoe UI", 12), bg="#f4f4f4")
        lblcorreo.place(relx=0.5, rely=0.71, anchor="center")
        entrycorreo = tk.Entry(ventanaRegistro, font=("Segoe UI", 12), width=30)
        entrycorreo.place(relx=0.5, rely=0.77, anchor="center")

        # Contraseña
        lblcontrasena = tk.Label(ventanaRegistro, text="Contraseña*:", font=("Segoe UI", 12), bg="#f4f4f4")
        lblcontrasena.place(relx=0.5, rely=0.85, anchor="center")
        entrycontrasena = tk.Entry(ventanaRegistro, font=("Segoe UI", 12), width=30, show="*")
        entrycontrasena.place(relx=0.5, rely=0.90, anchor="center")

        #boton de registro
        btnregistrar = tk.Button(ventanaRegistro, text="Registrar", font=("Segoe UI", 12), bg="#42B35E", fg="white", width=15,command=registrar)
        btnregistrar.place(relx=0.5, rely=0.96, anchor="center")    

    def vercontrasena(self, event):
        self.btnvercontrasena.config(text="👁️")
        self.entrycontrasena.config(show="")    
    def ocultarcontrasena(self, event):
        self.btnvercontrasena.config(text="🔒")
        self.entrycontrasena.config(show="*")
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema Biblioteca")
        self.ventana.configure(height=400, width=400)
        self.ventana.resizable(0,0)
        self.sesion = None  # Variable para almacenar la sesión del usuario que es un objeto de la clase Usuario

        self.lbltitulo = tk.Label( self.ventana, text="Bienvenido al Sistema de Biblioteca",font=("Segoe UI", 16, "bold"), bg="#f4f4f4", fg="#333" )
        self.lbltitulo.place(relx=0.5, rely=0.1, anchor="center")
        self.lblcorreo = tk.Label(self.ventana, text="Correo Electrónico:", font=("Segoe UI", 12), bg="#f4f4f4" )
        self.lblcorreo.place(relx=0.5, rely=0.3, anchor="center")

        self.entrycorreo = tk.Entry(self.ventana, font=("Segoe UI", 12), width=30)
        self.entrycorreo.place(relx=0.5, rely=0.4, anchor="center") 

        self.lblcontrasena = tk.Label(self.ventana, text="Contraseña:", font=("Segoe UI", 12), bg="#f4f4f4")
        self.lblcontrasena.place(relx=0.5, rely=0.5, anchor="center")   
        self.entrycontrasena = tk.Entry(self.ventana, font=("Segoe UI", 12), show="*", width=30)
        self.entrycontrasena.place(relx=0.5, rely=0.6, anchor="center") 
        self.entrycontrasena.config(show="*")

        self.btnvercontrasena = tk.Button(self.ventana, text="🔒", font=("Segoe UI Emoji", 10))
        self.btnvercontrasena.place(x=355, rely=0.6, anchor="center",width=25,height=25)

        self.btnvercontrasena.bind("<Enter>",self.vercontrasena)
        self.btnvercontrasena.bind("<Leave>",self.ocultarcontrasena)

        self.lbliniciarSesion = tk.Label(self.ventana, text="Iniciar Sesión como:", font=("Segoe UI", 14, "bold"), bg="#f4f4f4")
        self.lbliniciarSesion.place(relx=0.5, rely=0.7, anchor="center")

        self.btnIniciarcomousuario = tk.Button(self.ventana, text="Usuario", font=("Segoe UI", 10), bg="#4a90e2", fg="white",width=12)   
        self.btnIniciarcomousuario.place(relx=0.2, rely=0.8, anchor="center")
        self.btnIniciarcomousuario.bind("<Button-1>", self.iniciarcomousuario)

        self.btniniciarcomobibliotecario = tk.Button(self.ventana, text="Bibliotecario", font=("Segoe UI", 10), bg="#50b35f", fg="white",width=12)
        self.btniniciarcomobibliotecario.place(relx=0.5, rely=0.8, anchor="center")
        self.btniniciarcomobibliotecario.bind("<Button-1>", self.iniciarcomobibliotecario)

        self.btniniciarcomoadministrador = tk.Button(self.ventana, text="Administrador", font=("Segoe UI", 10), bg="#e94f4f", fg="white",width=12)
        self.btniniciarcomoadministrador.place(relx=0.8, rely=0.80, anchor="center") 
        self.btniniciarcomoadministrador.bind("<Button-1>", self.iniciarcomoadministrador) 

        self.lblregistrousuario = tk.Label(self.ventana, text="Registrarse como Usuario", font=("Segoe UI", 12, "bold"),fg="#42B35E", cursor="hand2")
        self.lblregistrousuario.place(relx=0.5, rely=0.9, anchor="center")

        self.lblregistrousuario.bind("<Enter>",self.cambiarColorBlue)
        self.lblregistrousuario.bind("<Leave>", self.cambiarColorNormal)
        self.lblregistrousuario.bind("<Button-1>", self.ventanaRegistro)

        self.ventana.mainloop()

   
    
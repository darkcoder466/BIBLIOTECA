from .conexion import conectar
from .persona import Persona
from .informe import Informe
from tkinter import messagebox

class Bibliotecario(Persona):
    def __init__(self, cedula, nombre, apellido, telefono, email, contrasena=None, id_bibliotecario=None):
        super().__init__(cedula, nombre, apellido, telefono, email,contrasena=contrasena)
        self.id_bibliotecario = id_bibliotecario

    def registrar_bibliotecario(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bibliotecarios (cedula, nombre, apellido, telefono, email, contrasena)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.cedula, self.nombre, self.apellido, self.telefono, self.email, self.contrasena))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Bibliotecario registrado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el bibliotecario.\n{str(e)}")

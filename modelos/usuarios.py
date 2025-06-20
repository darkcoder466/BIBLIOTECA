from .conexion import conectar
from .persona import Persona
from tkinter import messagebox as mb

class Usuario(Persona):
    def __init__(self, cedula, nombre, apellido, telefono, email, contrasena, id_usuario=None,fecha_registro=None):
        super().__init__(cedula, nombre, apellido, telefono, email, contrasena)
        self.id_usuario = id_usuario
        self.fecha_registro = fecha_registro

    def registrar_usuario(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (cedula, nombre, apellido, telefono, email, contrasena)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.cedula, self.nombre, self.apellido, self.telefono, self.email, self.contrasena))
            conn.commit()
            cursor.close()
            conn.close()
            mb.showinfo("Éxito", "Usuario registrado correctamente.")
        except Exception as e:
            mb.showerror("Error", f"No se pudo registrar el usuario.")

    def consultar_disponibilidad_libro(self, id_libro):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT estado FROM libros WHERE id_libro = %s", (id_libro,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        if resultado and resultado[0] == 'disponible':
            return True
        else:
            return False

    def solicitar_prestamo(self, id_libro, fecha_prestamo, fecha_devolucion_estimada):
        if not self.consultar_disponibilidad_libro(id_libro):
            print("El libro no está disponible para préstamo.")
            return False
        
        conn = conectar()
        cursor = conn.cursor()

        # Insertar el préstamo con estado 'pendiente'
        cursor.execute("""
            INSERT INTO prestamos (id_usuario, id_libro, fecha_prestamo, fecha_devolucion_estimada, estado)
            VALUES ((SELECT id_usuario FROM usuarios WHERE cedula = %s), %s, %s, %s, 'pendiente')
        """, (self.cedula, id_libro, fecha_prestamo, fecha_devolucion_estimada))
        
        # Cambiar estado del libro a 'prestado'
        cursor.execute("UPDATE libros SET estado = 'prestado' WHERE id_libro = %s", (id_libro,))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Préstamo solicitado con éxito.")
        return True

    def devolver_libro(self, id_prestamo, fecha_devolucion_real):
        conn = conectar()
        cursor = conn.cursor()

        # Actualizar fecha_devolucion_real y estado del préstamo
        cursor.execute("""
            UPDATE prestamos
            SET fecha_devolucion_real = %s,
                estado = CASE 
                            WHEN %s > fecha_devolucion_estimada THEN 'en mora'
                            ELSE 'devuelto'
                         END
            WHERE id_prestamo = %s AND id_usuario = (SELECT id_usuario FROM usuarios WHERE cedula = %s)
        """, (fecha_devolucion_real, fecha_devolucion_real, id_prestamo, self.cedula))

        # Obtener el id_libro para actualizar su estado
        cursor.execute("SELECT id_libro FROM prestamos WHERE id_prestamo = %s", (id_prestamo,))
        libro = cursor.fetchone()
        if libro:
            cursor.execute("UPDATE libros SET estado = 'disponible' WHERE id_libro = %s", (libro[0],))

        conn.commit()
        cursor.close()
        conn.close()
        print("Libro devuelto correctamente.")
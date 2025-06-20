
import datetime
import mysql.connector
from modelos.conexion import conectar
from tkinter import messagebox as mb



class Prestamo:
    def __init__(self, id_usuario, id_libro, id_prestamo=None, fecha_prestamo=None, 
                 fecha_devolucion_estimada=None, fecha_devolucion_real=None, 
                 estado='pendiente'):
        self.id_prestamo = id_prestamo
        self.id_usuario = id_usuario
        self.id_libro = id_libro
        self.fecha_prestamo = fecha_prestamo if fecha_prestamo else datetime.date.today()
        self.fecha_devolucion_estimada = fecha_devolucion_estimada or (self.fecha_prestamo + datetime.timedelta(days=7))
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado

    def guardar_en_bd(self):
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)

            # Verificar disponibilidad del libro
            cursor.execute("SELECT * FROM libros WHERE id_libro = %s", (self.id_libro,))
            libro = cursor.fetchone()

            if not libro:
                mb.showerror("Error", f"❌ El libro con ID {self.id_libro} no existe.")
                return False

            if libro["estado"] != "disponible":
                mb.showerror("No disponible", f"❌ El libro '{libro['titulo']}' no está disponible para préstamo.")
                return False

            # Insertar el préstamo
            cursor.execute("""
                INSERT INTO prestamos (id_usuario, id_libro, fecha_prestamo, fecha_devolucion_estimada, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                self.id_usuario,
                self.id_libro,
                self.fecha_prestamo,
                self.fecha_devolucion_estimada,
                self.estado
            ))

            conn.commit()
            mb.showinfo("Éxito", f"✅ Préstamo registrado para el libro '{libro['titulo']}'.")
            return True

        except mysql.connector.Error as e:
            mb.showerror("Error", f"❌ Error al guardar el préstamo: {e}")
            return False

        finally:
            if conn:
                conn.close()


   
    
    @staticmethod
    def actualizar_estado_libro(id_libro, nuevo_estado="prestado"):
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE libros
                SET estado = %s
                WHERE id_libro = %s
            """, (nuevo_estado, id_libro))

            if cursor.rowcount == 0:
                print(f"⚠️ No se encontró un libro con ID {id_libro}. No se actualizó ningún estado.")
            else:
                conn.commit()
                print(f"✅ Estado del libro con ID {id_libro} actualizado a '{nuevo_estado}' correctamente.")

        except mysql.connector.Error as e:
            print(f"❌ Error al actualizar el estado del libro: {e}")

        finally:
            if conn:
                conn.close()



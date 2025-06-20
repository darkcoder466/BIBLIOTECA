from  modelos.prestamo import Prestamo
from ..controladores.controlador_interfaz_usuario import obtener_libro_por_id
from ..modelos.conexion import conectar
import mysql.connector 

def generar_prestamo(id_usuario, id_libro):
    libro = obtener_libro_por_id(id_libro)

    if not libro:
        print(f"El libro con ID {id_libro} no existe.")
        return None

    if libro.estado != "disponible":
        print(f"El libro '{libro.titulo}' no está disponible para préstamo.")
        return None

    prestamo = Prestamo(id_usuario, id_libro)

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prestamos (id_usuario, id_libro, fecha_prestamo, fecha_devolucion_estimada, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            prestamo.id_usuario,
            prestamo.id_libro,
            prestamo.fecha_prestamo,
            prestamo.fecha_devolucion_estimada,
            prestamo.estado
        ))

        conn.commit()
        print(f"Préstamo generado exitosamente para el libro '{libro.titulo}'")

        # Cambiar el estado del libro a "prestado"
        actualizar_estado_libro(id_libro, "prestado")

        return prestamo

    except mysql.connector.Error as e:
        print(f"Error al generar el préstamo: {e}")
        return None

    finally:
        if conn:
            conn.close()


def actualizar_estado_libro(id_libro, nuevo_estado):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE libros
            SET estado = %s
            WHERE id_libro = %s
        """, (nuevo_estado, id_libro))

        if cursor.rowcount == 0:
            print(f"No se encontró un libro con ID {id_libro}. No se actualizó nada.")
        else:
            conn.commit()
            print(f"Estado del libro con ID {id_libro} actualizado a '{nuevo_estado}' correctamente.")

    except mysql.connector.Error as e:
        print(f"Error al actualizar el estado del libro: {e}")

    finally:
        if conn:
            conn.close()

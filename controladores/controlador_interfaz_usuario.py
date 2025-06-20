from modelos.conexion import conectar
from modelos.libro import Libro

def obtener_todos_los_libros():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libros")
        resultados = cursor.fetchall()
        conn.close()

        libros = []
        for fila in resultados:
            libro = Libro(
                id_libro=fila["id_libro"],
                titulo=fila["titulo"],
                autor=fila["autor"],
                ano_publicacion=fila["ano_publicacion"],
                estado=fila["estado"]
            )
            libros.append(libro)

        return libros
    except Exception as e:
        print("Error al obtener libros:", e)
        return []

def obtener_libro_por_id(id_libro):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libros WHERE id_libro = %s", (id_libro,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return Libro(
                id_libro=resultado["id_libro"],
                titulo=resultado["titulo"],
                autor=resultado["autor"],
                ano_publicacion=resultado["ano_publicacion"],
                estado=resultado["estado"]
            )
        else:
            return None
    except Exception as e:
        print("Error al obtener libro por ID:", e)
        return None

def buscar_libros_por_nombre(parte_titulo: str) -> list[Libro]:
    # Retorna una lista de instancias de Libro que contengan ese texto en el título (sin importar mayúsculas)
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libros WHERE titulo LIKE %s", ('%' + parte_titulo + '%',))
        resultados = cursor.fetchall()
        conn.close()

        libros = []
        for fila in resultados:
            libro = Libro(
                id_libro=fila["id_libro"],
                titulo=fila["titulo"],
                autor=fila["autor"],
                ano_publicacion=fila["ano_publicacion"],
                estado=fila["estado"]
            )
            libros.append(libro)

        return libros
    except Exception as e:
        print("Error al buscar libros por nombre:", e)
        return []
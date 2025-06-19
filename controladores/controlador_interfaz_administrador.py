from modelos.conexion import conectar
from modelos.prestamo import Prestamo
from modelos.usuarios import Usuario
from modelos.libro import Libro



def obtener_prestamos(filtro='todos'):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM prestamos"
        condiciones = []

        if filtro == 'pendientes':
            condiciones.append("estado = 'pendiente'")
        elif filtro == 'devueltos':
            condiciones.append("estado = 'devuelto'")
        elif filtro == 'mora':
            condiciones.append("estado = 'mora'")

        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        query += " ORDER BY fecha_prestamo DESC"

        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()

        prestamos = []
        for fila in resultados:
            prestamo = Prestamo(fila["id_usuario"],id_libro=fila["id_libro"])
            prestamo.id_prestamo = fila["id_prestamo"]
            prestamo.fecha_prestamo = fila["fecha_prestamo"]
            prestamo.fecha_devolucion_estimada = fila["fecha_devolucion_estimada"]
            prestamo.fecha_devolucion_real = fila["fecha_devolucion_real"]
            prestamo.estado = fila["estado"]

            prestamos.append(prestamo)

        return prestamos

    except Exception as e:
        print("Error al obtener préstamos:", e)
        return []



def obtener_usuarios():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        # Consulta para obtener todos los usuarios ordenados por nombre
        query = """
            SELECT * FROM usuarios
            ORDER BY nombre ASC
        """

        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()

        usuarios = []
        for fila in resultados:
            usuario = Usuario(
                cedula=fila["cedula"],
                nombre=fila["nombre"],
                apellido=fila["apellido"],
                telefono=fila["telefono"],
                email=fila["email"],
                contrasena=fila["contrasena"],
                id_usuario=fila["id_usuario"],
                fecha_registro=fila["fecha_registro"]
            )
            usuarios.append(usuario)

        return usuarios

    except Exception as e:
        print("Error al obtener usuarios:", e)
        return []

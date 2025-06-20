from modelos.conexion import conectar
from datetime import date

class Informe:
    def __init__(self, fecha, total_libros, libros_disponibles, libros_prestados, libros_mora, id_informe=None):
        self.id_informe = id_informe
        self.fecha = fecha
        self.total_libros = total_libros
        self.libros_disponibles = libros_disponibles
        self.libros_prestados = libros_prestados
        self.libros_mora = libros_mora

    @staticmethod
    def generar_y_guardar():
        try:
            conn = conectar()
            cursor = conn.cursor()

            # Consulta para contar libros por estado
            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_libros,
                    SUM(CASE WHEN estado = 'disponible' THEN 1 ELSE 0 END) AS disponibles,
                    SUM(CASE WHEN estado = 'prestado' THEN 1 ELSE 0 END) AS prestados,
                    SUM(CASE WHEN estado = 'en mora' THEN 1 ELSE 0 END) AS mora
                FROM libros
            """)
            resultado = cursor.fetchone()

            if resultado:
                total, disponibles, prestados, mora = resultado
                fecha_hoy = date.today()

                cursor.execute("""
                    INSERT INTO informe_libros (fecha, total_libros, libros_disponibles, libros_prestados, libros_mora)
                    VALUES (%s, %s, %s, %s, %s)
                """, (fecha_hoy, total, disponibles, prestados, mora))
                conn.commit()

            cursor.close()
            conn.close()

        except Exception as e:
            print("Error al generar informe:", e)

    @staticmethod
    def obtener_informes():
        informes = []
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM informe_libros ORDER BY fecha DESC")
            resultados = cursor.fetchall()
            for fila in resultados:
                informe = Informe(
                    id_informe=fila["id_informe"],
                    fecha=fila["fecha"],
                    total_libros=fila["total_libros"],
                    libros_disponibles=fila["libros_disponibles"],
                    libros_prestados=fila["libros_prestados"],
                    libros_mora=fila["libros_mora"]
                )
                informes.append(informe)
            cursor.close()
            conn.close()
        except Exception as e:
            print("Error al obtener informes:", e)
        return informes

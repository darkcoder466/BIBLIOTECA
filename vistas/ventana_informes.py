import tkinter as tk
from tkinter import ttk, messagebox
from modelos.conexion import conectar
from datetime import date

def ventana_informes_libros(ventana_maestra):
    ventana = tk.Toplevel(ventana_maestra)
    ventana.title("Informes de Libros")
    ventana.geometry("700x450")
    ventana.resizable(False, False)

    def cargar_informes():
        for row in tabla.get_children():
            tabla.delete(row)
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_informe, fecha, total_libros, libros_disponibles, libros_prestados, libros_mora
                FROM informe_libros
                ORDER BY fecha DESC
            """)
            informes = cursor.fetchall()
            for inf in informes:
                tabla.insert("", tk.END, values=inf)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la información:\n{e}")

    def crear_informe():
        try:
            conn = conectar()
            cursor = conn.cursor()

            # Total de libros
            cursor.execute("SELECT COUNT(*) FROM libros")
            total = cursor.fetchone()[0]

            # Libros disponibles
            cursor.execute("SELECT COUNT(*) FROM libros WHERE estado = 'disponible'")
            disponibles = cursor.fetchone()[0]

            # Libros prestados
            cursor.execute("SELECT COUNT(*) FROM libros WHERE estado = 'prestado'")
            prestados = cursor.fetchone()[0]

            # Libros en mora (prestamos con estado 'en mora')
            cursor.execute("SELECT COUNT(*) FROM prestamos WHERE estado = 'en mora'")
            mora = cursor.fetchone()[0]

            # Insertar informe
            cursor.execute("""
                INSERT INTO informe_libros (fecha, total_libros, libros_disponibles, libros_prestados, libros_mora)
                VALUES (%s, %s, %s, %s, %s)
            """, (date.today(), total, disponibles, prestados, mora))

            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Informe creado correctamente.")
            cargar_informes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el informe:\n{e}")

    # --- UI ---
    tk.Label(ventana, text="Informes de Libros", font=("Arial", 16)).pack(pady=10)

    columnas = ("ID", "Fecha", "Total", "Disponibles", "Prestados", "En Mora")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=12)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=100)

    tabla.pack(padx=10, pady=10, fill="x")

    tk.Button(ventana, text="Crear Nuevo Informe", font=("Arial", 12), command=crear_informe).pack(pady=10)

    cargar_informes()

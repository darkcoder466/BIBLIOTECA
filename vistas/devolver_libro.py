from controladores.controlador_interfaz_usuario import obtener_libro_por_id
import tkinter as tk
from tkinter import ttk, messagebox
from modelos.libro import Libro
import mysql.connector
from modelos.conexion import conectar

def ventana_devolucion_libro(ventana_principal, sesion_usuario):
    ventana_devolucion = tk.Toplevel(ventana_principal)
    ventana_devolucion.title("Devolución de Libros")
    ventana_devolucion.geometry("550x400")

    etiqueta_ingreso_id = tk.Label(ventana_devolucion, text="Ingrese el ID del libro a devolver:")
    etiqueta_ingreso_id.pack(pady=10)

    entrada_id_libro = tk.Entry(ventana_devolucion)
    entrada_id_libro.pack(pady=5)

    etiqueta_libro_no_encontrado = tk.Label(ventana_devolucion, text="", fg="red")
    etiqueta_libro_no_encontrado.pack()

    columnas_tabla = ("id_libro", "titulo", "autor", "ano_publicacion", "estado")
    tabla_libro = ttk.Treeview(ventana_devolucion, columns=columnas_tabla, show="headings", height=1)

    for columna in columnas_tabla:
        tabla_libro.heading(columna, text=columna.replace("_", " ").title())
        tabla_libro.column(columna, width=100)

    tabla_libro.pack(pady=10)

    def mostrar_libro_en_tabla(event=None):
        tabla_libro.delete(*tabla_libro.get_children())
        etiqueta_libro_no_encontrado.config(text="")

        id_libro = entrada_id_libro.get().strip()

        if not id_libro.isdigit():
            return

        libro_encontrado = obtener_libro_por_id(id_libro)

        if isinstance(libro_encontrado, Libro):
            tabla_libro.insert("", tk.END, values=(
                libro_encontrado.id_libro,
                libro_encontrado.titulo,
                libro_encontrado.autor,
                libro_encontrado.ano_publicacion,
                libro_encontrado.estado
            ))
        else:
            etiqueta_libro_no_encontrado.config(text="Libro no encontrado.")

    def procesar_devolucion():
        id_libro = entrada_id_libro.get().strip()
        libro_encontrado = obtener_libro_por_id(id_libro)

        if isinstance(libro_encontrado, Libro):
            if libro_encontrado.estado == "prestado":
                try:
                    conn = conectar()
                    cursor = conn.cursor()

                    # Buscar préstamo activo del usuario para ese libro
                    cursor.execute("""
                        SELECT id_prestamo FROM prestamos 
                        WHERE id_libro = %s AND id_usuario = %s AND estado = 'aprovado'
                    """, (id_libro, sesion_usuario.id_usuario)) 

                    prestamo = cursor.fetchone()

                    if not prestamo:
                        messagebox.showerror("Error", "No se encontró un préstamo activo de este libro a tu nombre.")
                        return

                    id_prestamo = prestamo[0]

                    # Actualizar estado del préstamo a 'devuelto' y guardar la fecha
                    cursor.execute("""
                        UPDATE prestamos 
                        SET estado = 'devuelto', fecha_devolucion_real = CURDATE() 
                        WHERE id_prestamo = %s
                    """, (id_prestamo,))

                    # Cambiar estado del libro a 'disponible'
                    cursor.execute("""
                        UPDATE libros 
                        SET estado = 'disponible' 
                        WHERE id_libro = %s
                    """, (id_libro,))

                    conn.commit()
                    messagebox.showinfo("Devolución realizada", f"Has devuelto el libro:\n«{libro_encontrado.titulo}»")

                except mysql.connector.Error as e:
                    messagebox.showerror("Error de base de datos", f"❌ Error al procesar la devolución: {e}")

                finally:
                    if conn:
                        conn.close()
            else:
                messagebox.showwarning("Aviso", "Este libro no está prestado actualmente.")
        else:
            messagebox.showerror("Error", "Libro no encontrado.")

    entrada_id_libro.bind("<KeyRelease>", mostrar_libro_en_tabla)

    boton_devolver = tk.Button(ventana_devolucion, text="Devolver Libro", command=procesar_devolucion)
    boton_devolver.pack(pady=20)

    ventana_devolucion.transient(ventana_principal)
    ventana_devolucion.grab_set()
    ventana_devolucion.focus_force()
    ventana_devolucion.protocol("WM_DELETE_WINDOW", ventana_devolucion.destroy)

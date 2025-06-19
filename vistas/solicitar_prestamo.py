from controladores.controlador_interfaz_usuario import obtener_libro_por_id
import tkinter as tk
from tkinter import ttk, messagebox
from modelos.libro import Libro
from modelos.prestamo import Prestamo

def ventana_solicitudes_libros(ventana_principal, sesion_usuario):
    ventana_solicitud = tk.Toplevel(ventana_principal)
    ventana_solicitud.title("Solicitud de Préstamo de Libros")
    ventana_solicitud.geometry("550x400")
    print(sesion_usuario)
    print(sesion_usuario.id_usuario)

    etiqueta_ingreso_id = tk.Label(ventana_solicitud, text="Ingrese el ID del libro:")
    etiqueta_ingreso_id.pack(pady=10)

    entrada_id_libro = tk.Entry(ventana_solicitud)
    entrada_id_libro.pack(pady=5)

    etiqueta_libro_no_encontrado = tk.Label(ventana_solicitud, text="", fg="red")
    etiqueta_libro_no_encontrado.pack()

    columnas_tabla = ("id_libro", "titulo", "autor", "ano_publicacion", "estado")
    tabla_libro = ttk.Treeview(ventana_solicitud, columns=columnas_tabla, show="headings", height=1)

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

    def procesar_solicitud_prestamo():
        id_libro = entrada_id_libro.get().strip()
        libro_encontrado = obtener_libro_por_id(id_libro)

        if isinstance(libro_encontrado, Libro):
            prestamo = Prestamo(
                id_usuario=sesion_usuario.id_usuario,
                id_libro=libro_encontrado.id_libro
                # Las fechas se asignan automáticamente
            )
            prestamo.guardar_en_bd()
                


    entrada_id_libro.bind("<KeyRelease>", mostrar_libro_en_tabla)

    boton_solicitar_prestamo = tk.Button(ventana_solicitud, text="Solicitar Préstamo", command=procesar_solicitud_prestamo)
    boton_solicitar_prestamo.pack(pady=20)

    ventana_solicitud.transient(ventana_principal)
    ventana_solicitud.grab_set()
    ventana_solicitud.focus_force()
    ventana_solicitud.protocol("WM_DELETE_WINDOW", ventana_solicitud.destroy)

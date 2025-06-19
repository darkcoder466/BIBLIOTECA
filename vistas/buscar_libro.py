from controladores.controlador_interfaz_usuario import buscar_libros_por_nombre
import tkinter as tk
from tkinter import ttk
from modelos.libro import Libro

def ventana_busqueda_libros_por_nombre(ventana_principal, sesion_usuario):
    ventana_busqueda = tk.Toplevel(ventana_principal)
    ventana_busqueda.title("Buscar Libros por Nombre")
    ventana_busqueda.geometry("700x400")

    etiqueta_titulo = tk.Label(ventana_busqueda, text="Buscar por título del libro:")
    etiqueta_titulo.pack(pady=10)

    entrada_titulo_libro = tk.Entry(ventana_busqueda, width=50)
    entrada_titulo_libro.pack(pady=5)

    etiqueta_sin_resultados = tk.Label(ventana_busqueda, text="", fg="red")
    etiqueta_sin_resultados.pack()

    columnas_tabla = ("id_libro", "titulo", "autor", "ano_publicacion", "estado")
    tabla_resultados = ttk.Treeview(ventana_busqueda, columns=columnas_tabla, show="headings", height=10)

    for columna in columnas_tabla:
        tabla_resultados.heading(columna, text=columna.replace("_", " ").title())
        tabla_resultados.column(columna, width=130)

    tabla_resultados.pack(pady=10)

    def actualizar_tabla_libros(event=None):
        texto_ingresado = entrada_titulo_libro.get().strip().lower()
        tabla_resultados.delete(*tabla_resultados.get_children())
        etiqueta_sin_resultados.config(text="")

        if not texto_ingresado:
            return

        lista_libros = buscar_libros_por_nombre(texto_ingresado)

        libros_encontrados = [
            libro for libro in lista_libros
            if texto_ingresado in libro.titulo.lower()
        ]

        if libros_encontrados:
            for libro in libros_encontrados:
                tabla_resultados.insert("", tk.END, values=(
                    libro.id_libro,
                    libro.titulo,
                    libro.autor,
                    libro.ano_publicacion,
                    libro.estado
                ))
        else:
            etiqueta_sin_resultados.config(text="No se encontraron libros con ese título.")

    entrada_titulo_libro.bind("<KeyRelease>", actualizar_tabla_libros)

    ventana_busqueda.transient(ventana_principal)
    ventana_busqueda.grab_set()
    ventana_busqueda.focus_force()
    ventana_busqueda.protocol("WM_DELETE_WINDOW", ventana_busqueda.destroy)

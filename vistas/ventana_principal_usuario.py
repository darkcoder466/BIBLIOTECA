import tkinter as tk
from tkinter import messagebox,ttk
from modelos.libro import Libro
from controladores.controlador_interfaz_usuario import obtener_todos_los_libros
from vistas.solicitar_prestamo import ventana_solicitudes_libros
from vistas.devolver_libro import ventana_devolucion_libro
from vistas.buscar_libro import ventana_busqueda_libros_por_nombre


def ventana_principal_usuario(ventana_maestra, sesion_usuario):
    # Ocultar la ventana principal 
    ventana_maestra.withdraw()
    def mostrar_todos(event=None):
        libros = obtener_todos_los_libros()
        tree.delete(*tree.get_children())
        if libros:
            for libro in libros:
                tree.insert("", tk.END, values=(
                    libro.id_libro,
                    libro.titulo,
                    libro.autor,
                    libro.ano_publicacion,
                    libro.estado
                ))
        else:
            messagebox.showinfo("Sin resultados", "No hay libros registrados.")

    def mostrar_disponibles(event=None):
        libros = [l for l in obtener_todos_los_libros() if l.estado == 'disponible']
        tree.delete(*tree.get_children())
        if libros:
            for libro in libros:
                tree.insert("", tk.END, values=(
                    libro.id_libro,
                    libro.titulo,
                    libro.autor,
                    libro.ano_publicacion,
                    libro.estado
                ))
        else:
            messagebox.showinfo("Sin resultados", "No hay libros disponibles.")


    # Crear nueva ventana de usuario
    ventana = tk.Toplevel()
    ventana.title("Panel de Usuario")
    ventana.geometry("1000x600")
    ventana.resizable(0,0)
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_sesion(ventana, ventana_maestra))
    
    # Menú principal
    barra_menu = tk.Menu(ventana)

    # Menú de acciones
    menu_acciones = tk.Menu(barra_menu, tearoff=0)
    menu_acciones.add_command(label="Consultar libros", command=lambda:ventana_busqueda_libros_por_nombre(ventana, sesion_usuario))
    menu_acciones.add_command(label="Solicitar préstamo", command=lambda: ventana_solicitudes_libros(ventana, sesion_usuario))
    menu_acciones.add_command(label="Devolver libro", command=lambda: ventana_devolucion_libro(ventana, sesion_usuario))
    barra_menu.add_cascade(label="Acciones", menu=menu_acciones)

    # Menú de sesión
    menu_sesion = tk.Menu(barra_menu, tearoff=0)
    menu_sesion.add_command(label="Cerrar sesión", command=lambda: cerrar_sesion(ventana, ventana_maestra))
    barra_menu.add_cascade(label="Sesión", menu=menu_sesion)

    ventana.config(menu=barra_menu)

    # Mensaje de bienvenida
    nombre = sesion_usuario.nombre
    ventana.title(f"zona de usuario")
    tk.Label(ventana, text=f"¡Bienvenido, {nombre}!", font=("Arial", 16)).pack(pady=30)


    # Botones de acción
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    btn_mostrar_todos = tk.Button(frame_botones, text="Mostrar Todos", command=mostrar_todos)
    btn_mostrar_todos.pack(side=tk.LEFT, padx=5)

    btn_mostrar_disponibles = tk.Button(frame_botones, text="Mostrar Disponibles", command=mostrar_disponibles)
    btn_mostrar_disponibles.pack(side=tk.LEFT, padx=5)

    # Tabla de libros
    columnas = ("id_libro", "titulo", "autor", "ano_publicacion", "estado")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=120)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Mostrar libros al abrir
    mostrar_libros(tree)

def mostrar_libros(treeview):
    libros = obtener_todos_los_libros()
    treeview.delete(*treeview.get_children())

    for libro in libros:
        treeview.insert("", tk.END, values=(
            libro.id_libro,
            libro.titulo,
            libro.autor,
            libro.ano_publicacion,
            libro.estado
        ))


def cerrar_sesion(ventana_actual, ventana_maestra):
    respuesta = messagebox.askyesno("Cerrar sesión", "¿Estás seguro de que quieres cerrar sesión?")
    if respuesta:
        ventana_actual.destroy()
        ventana_maestra.deiconify()  # Mostrar la ventana principal (login)

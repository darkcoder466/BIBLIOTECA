import tkinter as tk
from tkinter import messagebox
from vistas.ventana_gestion_usuarios import ventana_gestion_usuarios
from vistas.ventana_gestion_libros import ventana_gestion_libros
from vistas.ventana_informes import ventana_informes_libros
from controladores.controlador_interfaz_bibliotecario import obtener_prestamos
from tkinter import ttk
import mysql.connector
from modelos.conexion import conectar


def ventana_principal_bibliotecario(ventana_maestra, sesion):
    # Ocultar ventana principal (login)
    ventana_maestra.withdraw()

    # Crear ventana principal del bibliotecario
    ventana = tk.Toplevel()
    ventana.title("Panel del Bibliotecario")
    ventana.geometry("900x600")
    ventana.resizable(0, 0)

    # Función para cerrar sesión
    def cerrar_sesion():
        if messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar sesión?"):
            ventana.destroy()
            ventana_maestra.deiconify() # Mostrar la ventana de inicio de sesión

    # Función para mostrar perfil del bibliotecario
    def mostrar_perfil():
        ventana_perfil = tk.Toplevel(ventana)
        ventana_perfil.title("Perfil del Bibliotecario")
        ventana_perfil.geometry("300x250")
        ventana_perfil.resizable(0, 0)

        tk.Label(ventana_perfil, text="Información del perfil", font=("Arial", 14)).pack(pady=10)
        tk.Label(ventana_perfil, text=f"Nombre: {sesion.nombre}").pack(anchor="w", padx=20, pady=5)
        tk.Label(ventana_perfil, text=f"apellido: {sesion.apellido}").pack(anchor="w", padx=20, pady=5)
        tk.Label(ventana_perfil, text=f"telefono: {sesion.telefono}").pack(anchor="w", padx=20, pady=5)
        tk.Label(ventana_perfil, text=f"Correo: {sesion.email}").pack(anchor="w", padx=20, pady=5)
        tk.Label(ventana_perfil, text=f"cedula: {sesion.cedula}").pack(anchor="w", padx=20, pady=5)
        tk.Label(ventana_perfil, text=f"Cargo: Bibliotecario").pack(anchor="w", padx=20, pady=5)

        tk.Button(ventana_perfil, text="Cerrar", command=ventana_perfil.destroy).pack(pady=10)

    # Funciones de cada acción del menú
    def gestionar_usuarios():
        ventana_gestion_usuarios(ventana, sesion)

    def gestionar_libros():
        ventana_gestion_libros(ventana)


    def generar_informes():
        ventana_informes_libros(ventana)

    # Crear la barra de menú
    barra_menu = tk.Menu(ventana)

    menu_gestion = tk.Menu(barra_menu, tearoff=0)
    menu_gestion.add_command(label="Gestionar Usuarios", command=gestionar_usuarios)
    menu_gestion.add_command(label="Gestionar Libros", command=gestionar_libros)
    menu_gestion.add_separator()
    menu_gestion.add_command(label="Generar Informes", command=generar_informes)

    barra_menu.add_cascade(label="Gestión", menu=menu_gestion)

    menu_sesion = tk.Menu(barra_menu, tearoff=0)
    menu_sesion.add_command(label="Cerrar Sesión", command=cerrar_sesion)

    barra_menu.add_cascade(label="Sesión", menu=menu_sesion)

    ventana.config(menu=barra_menu)

    # Encabezado de bienvenida
    tk.Label(ventana, text=f"Bienvenido, {sesion.nombre}", font=("Arial", 16)).pack(pady=20)

    # Botón de perfil
    btn_perfil = tk.Button(ventana, text="Perfil", font=("Arial", 12), command=mostrar_perfil)
    btn_perfil.pack(pady=10)

    
        # -------- TABLA DE PRÉSTAMOS -------- #
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(pady=10, fill="both", expand=True)

    columnas = ("ID", "Usuario", "Libro", "Fecha Préstamo", "F. Devolución Estimada", "F. Devolución Real", "Estado")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)

    tabla.pack(fill="both", expand=True)

    # Obtener préstamos y mostrarlos en la tabla
    prestamos = obtener_prestamos("todos")  # o puedes usar filtros: "pendientes", "devueltos", etc.

    for prestamo in prestamos:
        tabla.insert("", "end", values=(
            prestamo.id_prestamo,
            f"{prestamo.id_usuario}",
            f"{prestamo.id_libro}",
            prestamo.fecha_prestamo,
            prestamo.fecha_devolucion_estimada,
            prestamo.fecha_devolucion_real or "—",
            prestamo.estado
        ))
        def ventana_aprovar_prestamo(event):
            item = tabla.focus()
            if not item:
                return

            valores = tabla.item(item, "values")
            id_prestamo = valores[0]
            id_libro = valores[2]
            estado_actual = valores[6]

            if estado_actual.lower() != "pendiente":
                messagebox.showinfo("Aviso", "Este préstamo ya ha sido procesado.")
                return

            respuesta = messagebox.askyesno("Aprobar préstamo", "¿Deseas aprobar este préstamo?")

            if respuesta:
                try:
                    conn = conectar()
                    cursor = conn.cursor()

                    # Actualizar préstamo
                    cursor.execute("""
                        UPDATE prestamos
                        SET estado = 'aprovado'
                        WHERE id_prestamo = %s
                    """, (id_prestamo,))

                    # Actualizar estado del libro
                    cursor.execute("""
                        UPDATE libros
                        SET estado = 'prestado'
                        WHERE id_libro = %s
                    """, (id_libro,))

                    conn.commit()
                    messagebox.showinfo("Éxito", "✅ Préstamo aprobado y libro actualizado.")
                    # Opcional: actualizar tabla visualmente
                    tabla.item(item, values=valores[:6] + ("aprobado",))

                except mysql.connector.Error as e:
                    messagebox.showerror("Error de base de datos", f"❌ Error al aprobar préstamo: {e}")
                    print(f"Error al aprobar préstamo: {e}")
                finally:
                    if conn:
                        conn.close()

        # Enlazar el evento click a la tabla
        tabla.bind("<Double-1>", ventana_aprovar_prestamo)

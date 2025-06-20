import tkinter as tk
from tkinter import ttk, messagebox
from modelos.usuarios import Usuario
from modelos.conexion import conectar  
from controladores.controlador_interfaz_bibliotecario import obtener_usuarios

def ventana_gestion_usuarios(ventana_maestra, sesion):
    ventana = tk.Toplevel(ventana_maestra)
    ventana.title("Gestión de Usuarios")
    ventana.geometry("800x500")
    ventana.resizable(0,0)

    def actualizar_tabla(usuarios=None):
        for row in tabla.get_children():
           tabla.delete(row)

        # Si no se pasan usuarios, se obtienen desde la BD
        usuarios = usuarios or obtener_usuarios()

        for u in usuarios:
            # Si los usuarios vienen como objetos de la clase Usuario
            tabla.insert("", tk.END, values=(
                u.id_usuario,
                u.cedula,
                u.nombre,
                u.apellido,
                u.telefono,
                u.email,
                u.contrasena,
                u.fecha_registro
            ))
    def registrar_usuario():
        cedula = entry_cedula.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        telefono = entry_telefono.get()
        correo = entry_correo.get()
        contrasena = entry_contrasena.get()

        if not all([cedula, nombre, apellido, telefono, correo, contrasena]):
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
            return

        nuevo = Usuario(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=correo,
            contrasena=contrasena
        )
        nuevo.registrar_usuario()
        actualizar_tabla()
        for entry in [entry_cedula, entry_nombre, entry_apellido, entry_telefono, entry_correo, entry_contrasena]:
            entry.delete(0, tk.END)

    def eliminar_usuario():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Seleccione un usuario para eliminar.")
            return

        try:
            id_usuario = tabla.item(seleccion[0])['values'][0]

            # Confirmación
            confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro que desea eliminar al usuario con ID {id_usuario}?")
            if not confirmacion:
                return

            # Eliminar directamente con SQL
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("No encontrado", "No se encontró el usuario o ya fue eliminado.")
            else:
                messagebox.showinfo("Éxito", f"Usuario con ID {id_usuario} eliminado correctamente.")

            cursor.close()
            conn.close()
            actualizar_tabla()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario.\n\n{str(e)}")


    def buscar_usuario():
        query = entry_buscar.get()
        if not query:
            actualizar_tabla()
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_usuario, cedula, nombre, apellido, telefono, email, contrasena, fecha_registro
                FROM usuarios
                WHERE nombre LIKE %s OR cedula LIKE %s
            """, (f"%{query}%", f"%{query}%"))
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()

            # Limpiar la tabla actual
            for row in tabla.get_children():
                tabla.delete(row)

            # Insertar los resultados en la tabla
            for r in resultados:
                tabla.insert("", tk.END, values=r)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda.\n\n por favor veridique la conexión a la base de datos.\n\n o que el usuario exista.")


    # --- Formulario ---
    frame_form = tk.LabelFrame(ventana, text="Registrar Nuevo Usuario")
    frame_form.pack(padx=10, pady=10, fill="x")

    tk.Label(frame_form, text="Cédula").grid(row=0, column=0, padx=5, pady=5)
    entry_cedula = tk.Entry(frame_form)
    entry_cedula.grid(row=0, column=1, padx=5)

    tk.Label(frame_form, text="Nombre").grid(row=0, column=2, padx=5)
    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=3, padx=5)

    tk.Label(frame_form, text="Apellido").grid(row=1, column=0, padx=5)
    entry_apellido = tk.Entry(frame_form)
    entry_apellido.grid(row=1, column=1, padx=5)

    tk.Label(frame_form, text="Teléfono").grid(row=1, column=2, padx=5)
    entry_telefono = tk.Entry(frame_form)
    entry_telefono.grid(row=1, column=3, padx=5)

    tk.Label(frame_form, text="Correo").grid(row=2, column=0, padx=5)
    entry_correo = tk.Entry(frame_form)
    entry_correo.grid(row=2, column=1, padx=5)

    tk.Label(frame_form, text="Contraseña").grid(row=2, column=2, padx=5)
    entry_contrasena = tk.Entry(frame_form, show="*")
    entry_contrasena.grid(row=2, column=3, padx=5)

    tk.Button(frame_form, text="Registrar", command=registrar_usuario).grid(row=3, column=0, columnspan=4, pady=10)
    # --- Tabla de usuarios ---
    columnas = ("ID", "Cédula", "Nombre", "Apellido", "Teléfono", "Correo", "Contraseña", "Fecha Registro")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)

    for col in columnas:
        tabla.heading(col, text=col)
        # Ajusta anchos según el contenido
        if col == "ID":
            tabla.column(col, width=50)
        elif col in ["Cédula", "Teléfono"]:
            tabla.column(col, width=100)
        elif col == "Contraseña":
            tabla.column(col, width=180)
        elif col == "Fecha Registro":
            tabla.column(col, width=120)
        else:
            tabla.column(col, width=150)

    tabla.pack(padx=10, pady=10, fill="both")

    # --- Acciones ---
    frame_acciones = tk.Frame(ventana)
    frame_acciones.pack(pady=5)

    tk.Label(frame_acciones, text="Buscar por nombre o documento:").pack(side=tk.LEFT, padx=5)
    entry_buscar = tk.Entry(frame_acciones)
    entry_buscar.pack(side=tk.LEFT, padx=5)

    tk.Button(frame_acciones, text="Buscar", command=buscar_usuario).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_acciones, text="Eliminar Usuario", command=eliminar_usuario).pack(side=tk.LEFT, padx=5)

    actualizar_tabla()

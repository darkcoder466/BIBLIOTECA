import tkinter as tk
from tkinter import ttk, messagebox
from modelos.bibliotecario import Bibliotecario
from modelos.conexion import conectar

def ventana_gestion_bibliotecarios(ventana_maestra, sesion):
    ventana = tk.Toplevel(ventana_maestra)
    ventana.title("Gestión de Bibliotecarios")
    ventana.geometry("800x500")
    ventana.resizable(0, 0)

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_bibliotecario, cedula, nombre, apellido, telefono, email, contrasena, fecha_creacion
                FROM bibliotecarios
            """)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()

            for r in resultados:
                tabla.insert("", tk.END, values=r)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los bibliotecarios:\n{str(e)}")

    def registrar_bibliotecario():
        cedula = entry_cedula.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        telefono = entry_telefono.get()
        correo = entry_correo.get()
        contrasena = entry_contrasena.get()

        if not all([cedula, nombre, apellido, telefono, correo, contrasena]):
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
            return

        nuevo = Bibliotecario(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=correo,
            contrasena=contrasena
        )
        nuevo.registrar_bibliotecario()
        actualizar_tabla()
        for entry in [entry_cedula, entry_nombre, entry_apellido, entry_telefono, entry_correo, entry_contrasena]:
            entry.delete(0, tk.END)

    def eliminar_bibliotecario():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Seleccione un bibliotecario para eliminar.")
            return

        try:
            id_bibliotecario = tabla.item(seleccion[0])['values'][0]

            confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar bibliotecario con ID {id_bibliotecario}?")
            if not confirmacion:
                return

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bibliotecarios WHERE id_bibliotecario = %s", (id_bibliotecario,))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Éxito", "Bibliotecario eliminado correctamente.")
            actualizar_tabla()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{str(e)}")

    def buscar_bibliotecario():
        query = entry_buscar.get()
        if not query:
            actualizar_tabla()
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_bibliotecario, cedula, nombre, apellido, telefono, email, contrasena, fecha_creacion
                FROM bibliotecarios
                WHERE nombre LIKE %s OR cedula LIKE %s
            """, (f"%{query}%", f"%{query}%"))
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in tabla.get_children():
                tabla.delete(row)
            for r in resultados:
                tabla.insert("", tk.END, values=r)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda:\n{str(e)}")

    # --- Formulario ---
    frame_form = tk.LabelFrame(ventana, text="Registrar Nuevo Bibliotecario")
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

    tk.Button(frame_form, text="Registrar", command=registrar_bibliotecario).grid(row=3, column=0, columnspan=4, pady=10)

    # --- Tabla de bibliotecarios ---
    columnas = ("ID", "Cédula", "Nombre", "Apellido", "Teléfono", "Correo", "Contraseña", "Fecha Registro")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100 if col in ["ID", "Cédula", "Teléfono", "Fecha Registro"] else 150)

    tabla.pack(padx=10, pady=10, fill="both", expand=True)

    # --- Acciones ---
    frame_acciones = tk.Frame(ventana)
    frame_acciones.pack(pady=5)

    tk.Label(frame_acciones, text="Buscar por nombre o cédula:").pack(side=tk.LEFT, padx=5)
    entry_buscar = tk.Entry(frame_acciones)
    entry_buscar.pack(side=tk.LEFT, padx=5)

    tk.Button(frame_acciones, text="Buscar", command=buscar_bibliotecario).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_acciones, text="Eliminar Bibliotecario", command=eliminar_bibliotecario).pack(side=tk.LEFT, padx=5)

    actualizar_tabla()

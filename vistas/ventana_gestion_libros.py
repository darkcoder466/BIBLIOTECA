import tkinter as tk
from tkinter import ttk, messagebox
from modelos.libro import Libro
from modelos.conexion import conectar

def obtener_libros():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libros ORDER BY titulo ASC")
        resultados = cursor.fetchall()
        conn.close()

        libros = []
        for fila in resultados:
            libro = Libro(
                id_libro=fila["id_libro"],
                titulo=fila["titulo"],
                autor=fila["autor"],
                ano_publicacion=fila["ano_publicacion"],
                estado=fila["estado"]
            )
            libros.append(libro)
        return libros
    except Exception as e:
        print("Error al obtener libros:", e)
        return []

def ventana_gestion_libros(ventana_maestra):
    ventana = tk.Toplevel(ventana_maestra)
    ventana.title("Gestión de Libros")
    ventana.geometry("800x500")
    ventana.resizable(0,0)

    def actualizar_tabla(libros=None):
        for row in tabla.get_children():
            tabla.delete(row)

        libros = libros or obtener_libros()

        for l in libros:
            tabla.insert("", tk.END, values=(
                l.id_libro,
                l.titulo,
                l.autor,
                l.ano_publicacion,
                l.estado
            ))

    def registrar_libro():
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        ano = entry_ano.get()

        if not all([titulo, autor, ano]):
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO libros (titulo, autor, ano_publicacion, estado)
                VALUES (%s, %s, %s, 'disponible')
            """, (titulo, autor, ano))
            conn.commit()
            conn.close()
            actualizar_tabla()

            for entry in [entry_titulo, entry_autor, entry_ano]:
                entry.delete(0, tk.END)

            messagebox.showinfo("Éxito", "Libro registrado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el libro.\n\n{e}")

    def eliminar_libro():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Seleccione un libro para eliminar.")
            return

        id_libro = tabla.item(seleccion[0])['values'][0]
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar libro con ID {id_libro}?")
        if not confirmacion:
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM libros WHERE id_libro = %s", (id_libro,))
            conn.commit()
            conn.close()

            if cursor.rowcount == 0:
                messagebox.showwarning("No encontrado", "Libro no encontrado o ya eliminado.")
            else:
                messagebox.showinfo("Éxito", "Libro eliminado correctamente.")

            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el libro.\n\n{e}")

    def buscar_libro():
        query = entry_buscar.get()
        if not query:
            actualizar_tabla()
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM libros WHERE titulo LIKE %s OR autor LIKE %s
            """, (f"%{query}%", f"%{query}%"))
            resultados = cursor.fetchall()
            conn.close()

            for row in tabla.get_children():
                tabla.delete(row)

            for r in resultados:
                tabla.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el libro.\n\n{e}")

    # Formulario
    frame_form = tk.LabelFrame(ventana, text="Registrar Nuevo Libro")
    frame_form.pack(padx=10, pady=10, fill="x")

    tk.Label(frame_form, text="Título").grid(row=0, column=0, padx=5, pady=5)
    entry_titulo = tk.Entry(frame_form)
    entry_titulo.grid(row=0, column=1, padx=5)

    tk.Label(frame_form, text="Autor").grid(row=0, column=2, padx=5)
    entry_autor = tk.Entry(frame_form)
    entry_autor.grid(row=0, column=3, padx=5)

    tk.Label(frame_form, text="Año Publicación").grid(row=1, column=0, padx=5)
    entry_ano = tk.Entry(frame_form)
    entry_ano.grid(row=1, column=1, padx=5)

    tk.Button(frame_form, text="Registrar Libro", command=registrar_libro).grid(row=2, column=0, columnspan=4, pady=10)

    # Tabla
    columnas = ("ID", "Título", "Autor", "Año", "Estado")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=130 if col != "ID" else 50)

    tabla.pack(padx=10, pady=10, fill="both")

    # Acciones
    frame_acciones = tk.Frame(ventana)
    frame_acciones.pack(pady=5)

    tk.Label(frame_acciones, text="Buscar por título o autor:").pack(side=tk.LEFT, padx=5)
    entry_buscar = tk.Entry(frame_acciones)
    entry_buscar.pack(side=tk.LEFT, padx=5)

    tk.Button(frame_acciones, text="Buscar", command=buscar_libro).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_acciones, text="Eliminar Libro", command=eliminar_libro).pack(side=tk.LEFT, padx=5)

    actualizar_tabla()

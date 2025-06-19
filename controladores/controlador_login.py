from modelos.conexion import conectar
from tkinter import messagebox as mb
def verificar_usuario(correo, contraseña):
    try:
        conn = conectar()
        if not conn:
            mb.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE email = %s AND contrasena = %s"
        cursor.execute(query, (correo, contraseña))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return usuario  # Devuelve el diccionario con los datos del usuario
        else:
            mb.showerror("Acceso denegado", "Correo o contraseña incorrectos.")
            return None

    except Exception as e:
        mb.showerror("Error", f"Ocurrió un error inesperado por favor intente más tarde.")
        return None

def verificar_bibliotecario(correo, contraseña):
    try:
        conn = conectar()
        if not conn:
            mb.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM bibliotecarios WHERE email = %s AND contrasena = %s"
        cursor.execute(query, (correo, contraseña))
        bibliotecario = cursor.fetchone()
        conn.close()

        if bibliotecario:
            return bibliotecario  # Devuelve el diccionario con los datos del bibliotecario
        else:
            mb.showerror("Acceso denegado", "Correo o contraseña incorrectos.")
            return None
    except Exception as e:
        mb.showerror("Error", f"Ocurrió un error inesperado por favor intente más tarde.{e}")
        return None
    
def verificar_administrador(correo, contraseña):
    try:
        conn = conectar()
        if not conn:
            mb.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM administradores WHERE email = %s AND contrasena = %s"
        cursor.execute(query, (correo, contraseña))
        administrador = cursor.fetchone()
        conn.close()

        if administrador:
            return administrador # Devuelve el diccionario con los datos del administrador
        else:
            mb.showerror("Acceso denegado", "Correo o contraseña incorrectos.")
            return None
    except Exception as e:
        mb.showerror("Error", f"Ocurrió un error inesperado por favor intente más tarde.{e}")
        return None


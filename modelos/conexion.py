import mysql.connector
from tkinter import messagebox as mb

def conectar():
    try:
        conn = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            port=3307,
            database="biblioteca"
        )
        return conn
    except mysql.connector.Error as e:
        mb.showerror("error","Error al conectar a la base de datos:")
       
        return None

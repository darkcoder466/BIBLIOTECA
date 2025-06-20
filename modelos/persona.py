
class Persona:
    def __init__(self, cedula, nombre, apellido, telefono, email,contrasena):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.contrasena = contrasena
    def __str__(self):
        return (f"Cédula: {self.cedula}\n"
                f"Nombre: {self.nombre}\n"
                f"Apellido: {self.apellido}\n"
                f"Teléfono: {self.telefono}\n"
                f"Email: {self.email}")
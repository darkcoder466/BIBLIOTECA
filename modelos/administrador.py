from .conexion import conectar
from .persona import Persona
from .informe import Informe
class Administrador(Persona):
    def __init__(self, cedula, nombre, apellido, telefono, email, contrasena=None, id_administrador=None):
        super().__init__(cedula, nombre, apellido, telefono, email,contrasena=contrasena)
        self.id_administrador = id_administrador

    
class Libro:
    def __init__(self, id_libro, titulo, autor, ano_publicacion,estado='disponible'):
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacion = ano_publicacion
        self.estado = estado
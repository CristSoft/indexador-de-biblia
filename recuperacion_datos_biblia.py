import sqlite3

class Versiculo:
    def __init__(self, libro, capitulo, versiculo, texto, comentario):
        self.libro = libro #.capitalize()
        self.capitulo = capitulo
        self.versiculo = versiculo
        self.texto = texto #.capitalize()
        self.comentario = comentario #.capitalize()

def obtener_versiculo(libro, capitulo, versiculo):
    # Reemplazar los caracteres con tilde por sus equivalentes sin tilde
    libro = libro.translate(str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU"))
    
    # Abrir la conexión con la base de datos
    conexion = sqlite3.connect('biblia.db')
    
    # Crear un cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    
    # Crear la consulta SQL para recuperar el texto y el comentario del versículo
    consulta = f"SELECT texto, comentario FROM {libro} WHERE capitulo = ? AND versiculo = ?"
    
    # Ejecutar la consulta SQL y obtener el resultado
    cursor.execute(consulta, (capitulo, versiculo))
    resultado = cursor.fetchone()
    
    # Cerrar la conexión con la base de datos
    conexion.close()
    
    if resultado is None:
        # Si no se encuentra el versículo, devolver un mensaje de error
        return "No se encontró el versículo"
    else:
        # Si se encuentra el versículo, crear un objeto Versiculo con los datos
        return Versiculo(libro, capitulo, versiculo, resultado[0], resultado[1])



# Buscar el versículo
buscar_versiculo = obtener_versiculo("tito", 2, 8)

# Imprimir los datos del versículo
print("")
print("")
print("")
print(buscar_versiculo.libro, buscar_versiculo.capitulo, ":", buscar_versiculo.versiculo)
print("")
print("Texto:")
print("'",buscar_versiculo.texto,"'")
print("")
print("COMENTARIO:")
print(buscar_versiculo.comentario)
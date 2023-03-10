import os

# Carpeta con los archivos a renombrar
carpeta = "CBIndexado"

def cambiar_nombre_archivo():
    # Recorrer los archivos en la carpeta
    for archivo in os.listdir(carpeta):
        # Obtener la ruta completa del archivo
        ruta_original = os.path.join(carpeta, archivo)
        # Verificar que sea un archivo
        if os.path.isfile(ruta_original):
            # Generar el nuevo nombre de archivo sin el carácter "-"
            nuevo_nombre = archivo.replace("-", "")
            # Obtener la ruta completa del nuevo archivo
            ruta_nueva = os.path.join(carpeta, nuevo_nombre)
            # Renombrar el archivo
            os.rename(ruta_original, ruta_nueva)

def agregar_texto_a_archivos():
    # Ruta de la carpeta que contiene los archivos .txt
    carpeta = "biblia_txt"

    # Número que deseas agregar a la última línea
    numero = "1"

    # Iterar sobre los archivos en la carpeta
    for archivo in os.listdir(carpeta):
        # Comprobar que el archivo es un .txt
        if archivo.endswith(".txt"):
            # Abrir el archivo en modo escritura
            with open(os.path.join(carpeta, archivo), "a") as f:
                # Insertar un salto de línea en la última línea
                f.write("\n")
                # Agregar el número al final del archivo
                f.write(numero)

agregar_texto_a_archivos
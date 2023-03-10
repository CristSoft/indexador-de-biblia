import os

# Carpeta con los archivos a renombrar
carpeta = "CBIndexado"

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

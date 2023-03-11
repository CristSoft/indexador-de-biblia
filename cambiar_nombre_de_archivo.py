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


import re
def agregar_referencias_vacias(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
        referencias_existentes = set()
        referencias_faltantes = set()
        # Verificar si hay referencias en el archivo
        if not any(re.search(r'\b\d+\|\d+\b', linea) for linea in lineas):
            # El archivo está vacío o no tiene referencias
            cap_inicial, cap_final = 1, 150
            ver_inicial, ver_final = 1, 176
            for cap in range(cap_inicial, cap_final + 1):
                for ver in range(ver_inicial, ver_final + 1):
                    referencia = f"{cap}|{ver}"
                    nueva_linea = f"\n{referencia}\nSin comentarios para este versículo\n"
                    lineas.append(nueva_linea)
            referencias_existentes = set(f"{cap}|{ver}" for cap in range(cap_inicial, cap_final + 1) for ver in range(ver_inicial, ver_final + 1))
        else:
            for linea in lineas:
                match = re.search(r'\b\d+\|\d+\b', linea)
                if match:
                    referencia = match.group()
                    if referencia not in referencias_existentes:
                        if referencias_faltantes:
                            # Crear referencias vacías para las combinaciones número|número ausentes
                            for ref in sorted(referencias_faltantes):
                                cap, ver = ref.split("|")
                                nueva_referencia = f"{cap}|{ver}"
                                nueva_linea = f"\n{nueva_referencia}\nSin comentarios para este versículo\n"
                                lineas.insert(lineas.index(linea), nueva_linea)
                            referencias_faltantes.clear()
                        referencias_existentes.add(referencia)
                    else:
                        # Verificar si hay referencias ausentes entre las referencias existentes
                        cap_existente, ver_existente = map(int, referencia.split("|"))
                        for cap, ver in sorted(referencias_existentes):
                            cap_actual, ver_actual = map(int, (cap, ver))
                            if cap_actual == cap_existente:
                                if ver_actual < ver_existente - 1:
                                    for i in range(ver_actual + 1, ver_existente):
                                        ref_faltante = f"{cap}|{i}"
                                        referencias_faltantes.add(ref_faltante)
                        referencias_existentes.add(referencia)
            if referencias_faltantes:
                # Crear referencias vacías para las combinaciones número|número ausentes al final del documento
                for ref in sorted(referencias_faltantes):
                    cap, ver = ref.split("|")
                    nueva_referencia = f"{cap}|{ver}"
                    nueva_linea = f"\n{nueva_referencia}\nSin comentarios para este versículo\n"
                    lineas.append(nueva_linea)
    # Sobreescribir el archivo original con las nuevas referencias
    with open(archivo, 'w', encoding='utf-8') as f:
        f.writelines(lineas)




ruta_libros = "CBIndexado/"
agregar_referencias_vacias(ruta_libros+"GenesisPrueba.txt")


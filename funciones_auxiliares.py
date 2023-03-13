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




# Buscar número|número que contenga otros caracteres antes o después y mostrarlos por consola
def find_lines_with_pattern(folder_path):
    pattern = r".*[^0-9|](\d+\|\d+)[^0-9|].*"
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, mode='r', encoding='utf-8') as f:
                for line in f:
                    match = re.search(pattern, line)
                    if match:
                        print(line.rstrip())




# Reemplazar todas las ocurrencias de un caracter o cadena
import fileinput
def replace_in_files(folder_path, cadena):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, mode='r', encoding='utf-8') as f:
                content = f.read()
            with open(file_path, mode='w', encoding='utf-8') as f:
                f.write(content.replace(cadena, ""))



# Buscar dos cadenas y eliminar lo que hay entre ellas
def borrar_entre_cadenas(nombre_archivo, cadena1, cadena2):
    with open(nombre_archivo, 'r', encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    i = 0
    while i < len(lineas):
        if cadena1 in lineas[i]:
            j = i + 1
            while j < len(lineas):
                if cadena2 in lineas[j]:
                    # Eliminar las líneas entre las cadenas
                    del lineas[i:j]
                    break
                j += 1
        i += 1
    with open(nombre_archivo, 'w', encoding="utf-8") as archivo:
        archivo.writelines(lineas)


import chardet
# Buscar palabras por capítulo y versículo en los comentarios bíblicos
def buscar_palabras(nombre_archivo, cadena):
    flag=False
    n=0
    with open(nombre_archivo, 'rb') as f:
        result = chardet.detect(f.read())
    with open(nombre_archivo, 'r', encoding=result['encoding']) as archivo:
        try:
            for linea in archivo:            
                # patron = r'(?<!\S){}(?!\S)'.format(cadena + r'\s*\d+')
                patron = r'(?<!\S)CAPÍTULO\s*\d+(?!\S)'
                if re.search(patron, linea):
                    flag=True
                    n+=1
                if flag==True:
                    match = re.search(r'\d+\|\d+', linea)
                    if match: 
                        # borrar_entre_cadenas(nombre_archivo,linea,match.group(0))                                      
                        print(n,": ",nombre_archivo,"-", match.group(0), "     LINEA")
                        flag=False
        except:
            None
    return n


import os
import re
import chardet

def buscar_patron_y_borrar(cadena, nombre_archivo):
    with open(nombre_archivo, 'rb') as f:
        result = chardet.detect(f.read())  # detectar el encoding del archivo
    with open(nombre_archivo, 'r', encoding=result['encoding']) as archivo:
        contenido = archivo.readlines()

import re

def borrar_entre_cadenas(nombre_archivo, cadena_inicio, cadena_fin):
    try:
        with open(nombre_archivo, 'r', encoding="utf-8") as archivo:
            contenido = archivo.read()
            patron = re.compile(re.escape(cadena_inicio) + r'.*?' + re.escape(cadena_fin), re.DOTALL)
            contenido_nuevo = patron.sub('', contenido)
        with open(nombre_archivo, 'w', encoding="utf-8") as archivo:
            archivo.write(contenido_nuevo)
    except Exception as e:
        print("Error al procesar el archivo:", nombre_archivo)
        print(e)

def buscar_patron(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding="utf-8") as archivo:
            contenido = archivo.read()
            patron = r'(?s)\bCAPÍTULO\s+\d+\b.*?\d+\|\d+'
            matches = re.findall(patron, contenido)
            for match in matches:
                capitulo_patron = re.compile(r'\bCAPÍTULO\s+\d+\b.*?')
                capitulo_match = re.search(capitulo_patron, match)
                if capitulo_match:
                    borrar_entre_cadenas(nombre_archivo, capitulo_match.group(0), match)
                    print(match)
    except Exception as e:
        print("Error al procesar el archivo:", nombre_archivo)
        print(e)

# carpeta = 'CBIndexado'
# for archivo in os.listdir(carpeta):
#     if archivo.endswith(".txt"):
#         buscar_patron(os.path.join(carpeta, archivo))


# # iterar para cada archivo de la carpeta "CBIndexado"
# carpeta = "CBIndexado"
# cadena = "CAPÍTULO"
# for archivo in os.listdir(carpeta):
#     buscar_patron_y_borrar(cadena, os.path.join(carpeta, archivo))



carpeta="CBIndexado"
cadena="CAPÍTULO"
n=0
for archivo in os.listdir(carpeta):    
    index=0
    n+=buscar_palabras(carpeta+"/"+archivo , cadena)
print(n, "veces aparece la palabra '",cadena, "' en los comentarios bíblicos" )

# ruta_libros = "CBIndexado"
# agregar_referencias_vacias(ruta_libros+"/GenesisPrueba.txt")

# replace_in_files(ruta_libros,"")

# find_lines_with_pattern(ruta_libros)

# borrar_entre_cadenas("11.reyes1.txt","CAPÍTULO","6|1")

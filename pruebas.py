import os
import sqlite3
import re

# Función para extraer el número que está al principio del nombre del archivo antes del "."
def ExtraerLibroID(nombre_de_archivo):
    return int(nombre_de_archivo.split('.')[0])

# Función para limpiar el nombre del archivo
def LimpiarNombre(nombre_de_archivo):
    nombre_limpio = re.sub('[áéíóúÁÉÍÓÚ]', lambda x: 'aeiouAEIOU'[ 'áéíóúÁÉÍÓÚ'.index(x.group(0)) ], nombre_de_archivo.split('.')[1])
    return nombre_limpio.upper()

# Función para asignar un ID de Grupo al libro
def AsignarGrupoID(libro):
    grupos = {
    1: ["GENESIS", "EXODO", "LEVITICO", "NUMEROS", "DEUTERONOMIO"],
    2: ["JOSUE", "JUECES", "RUT", "1SAMUEL", "2SAMUEL", "1REYES", "2REYES", "1CRONICAS", "2CRONICAS", "ESDRAS", "NEHEMIAS", "ESTER"],
    3: ["JOB", "SALMOS", "PROVERBIOS", "ECLESIASTES", "CANTARES"],
    4: ["ISAIAS", "JEREMIAS", "LAMENTACIONES", "EZEQUIEL", "DANIEL"],
    5: ["OSEAS", "JOEL", "AMOS", "ABDIAS", "JONAS", "MIQUEAS", "NAHUM", "HABACUC", "SOFONIAS", "AGEO", "ZACARIAS", "MALAQUIAS"],
    6: ["MATEO", "MARCOS", "LUCAS", "JUAN"],
    7: ["HECHOS"],
    8: ["ROMANOS", "1CORINTIOS", "2CORINTIOS", "GALATAS", "EFESIOS", "FILIPENSES", "COLOSENSES", "1TESALONICENSES", "2TESALONICENSES", "1TIMOTEO", "2TIMOTEO", "TITO", "FILEMON"],
    9: ["HEBREOS", "SANTIAGO", "1PEDRO", "2PEDRO", "1JUAN", "2JUAN", "3JUAN", "JUDAS"],
    10: ["APOCALIPSIS"]
    }
    for grupo, libros in grupos.items():
        if libro in libros:
            return grupo
    return None

#Determinar a qué testamento pertenece teniendo como referencia el ID de testamentos
def AToNT(libroID):
    testamentoID = 1 if libroID < 40 else 2
    if testamentoID==1: return "Antiguo Testamento"
    if testamentoID==2: return "Nuevo Testamento"

#Determinar a qué Grupo pertenece teniendo como referencia el ID de Grupo
def GrupoDesdeID(id_de_grupo):
    if id_de_grupo == 1:
        return "del pentateuco"
    elif id_de_grupo == 2:
        return "de los Históricos del Antiguo Testamento"
    elif id_de_grupo == 3:
        return "de los poéticos"
    elif id_de_grupo == 4:
        return "de los profetas mayores"
    elif id_de_grupo == 5:
        return "de los profetas menores"
    elif id_de_grupo == 6:
        return "de los Evangelios"
    elif id_de_grupo == 7:
        return "de los libros históricos del Nuevo Testamento"
    elif id_de_grupo == 8:
        return "de las epístolas paulinas, o Cartas de Pablo"
    elif id_de_grupo == 9:
        return "de las epístolas generales"
    elif id_de_grupo == 10:
        return "solitario de Apocalipsis"


""" #Función para buscar los comentarios bíblicos
def ComentarioBiblico(archivo, cap_y_ver):
    # Abrir el archivo
    # with open(archivo, 'r') as f:    
    with open(archivo, 'r', encoding='utf-8') as f:
        # Leer el contenido del archivo
        contenido = f.read()
        # Buscar la posición de la primera cadena
        pos1 = contenido.find(cap_y_ver)
        if pos1 == -1:
            return ""
        # Buscar la posición de la segunda cadena
        pos2 = contenido.find("|", pos1 + len(cap_y_ver))
        if pos2 == -1:
            pos2 = len(contenido)
        # Obtener el texto entre las cadenas
        inicio = pos1 + len(cap_y_ver)
        fin = pos2
        texto = contenido[inicio:fin]
        return texto.strip() """

import re

def ComentarioBiblico(archivo, cap, ver):
    # ruta_archivo = "CBIndexado/" + archivo
    
    texto_acumulado = ""
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            if re.match(r'^\d+\|\d+', linea):
                c, v = linea.strip().split("|")
                if c == str(cap) and v == str(ver):
                    for linea2 in f:
                        if re.match(r'^\d+\|\d+', linea2):
                            break
                        texto_acumulado += linea2
                    return texto_acumulado
    
    return "no hay comentarios para este versículo"



#Sección para profar las funciones:______________________________
#________________________________________________________________


libro="1.Genesis.txt"
archivo="CBIndexado/"+libro
os.system('cls')
print("")
print("El id de ",libro, " es: ", ExtraerLibroID(libro))
print("El archivo ", libro, " ahora se llama: ", LimpiarNombre(libro))
print("El libro de",LimpiarNombre(libro) ," pertenece al grupo", GrupoDesdeID(AsignarGrupoID(LimpiarNombre(libro))))
print(LimpiarNombre(libro),"pertenece al",AToNT(ExtraerLibroID(libro)))
print(ComentarioBiblico(archivo, 1,17))

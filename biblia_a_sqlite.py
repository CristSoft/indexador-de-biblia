import os
import sqlite3
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
    
    return "No hay comentarios para este versículo"



# Función para extraer el número que está al principio del nombre del archivo antes del "."
def ExtraerLibroID(nombre_de_archivo):
    return int(nombre_de_archivo.split('.')[0])

# Función para limpiar el nombre del archivo
def LimpiarNombre(nombre_de_archivo):
    nombre_limpio = re.sub('[áéíóúÁÉÍÓÚ]', lambda x: 'aeiouAEIOU'[ 'áéíóúÁÉÍÓÚ'.index(x.group(0)) ], nombre_de_archivo.split('.')[1])
    return nombre_limpio.upper()

# Función para asignar un grupo ID al libro
def AsignarGrupoID(libro):
    grupos = {
    1: ["GENESIS", "EXODO", "LEVITICO", "NUMEROS", "DEUTERONOMIO"],
    2: ["JOSUE", "JUECES", "RUT", "SAMUEL1", "SAMUEL2", "REYES1", "REYES2", "CRONICAS1", "CRONICAS2", "ESDRAS", "NEHEMIAS", "ESTER"],
    3: ["JOB", "SALMOS", "PROVERBIOS", "ECLESIASTES", "CANTARES"],
    4: ["ISAIAS", "JEREMIAS", "LAMENTACIONES", "EZEQUIEL", "DANIEL"],
    5: ["OSEAS", "JOEL", "AMOS", "ABDIAS", "JONAS", "MIQUEAS", "NAHUM", "HABACUC", "SOFONIAS", "AGEO", "ZACARIAS", "MALAQUIAS"],
    6: ["MATEO", "MARCOS", "LUCAS", "JUAN"],
    7: ["HECHOS"],
    8: ["ROMANOS", "CORINTIOS1", "CORINTIOS2", "GALATAS", "EFESIOS", "FILIPENSES", "COLOSENSES", "TESALONICENSES1", "TESALONICENSES2", "TIMOTEO1", "TIMOTEO2", "TITO", "FILEMON"],
    9: ["HEBREOS", "SANTIAGO", "PEDRO1", "PEDRO2", "JUAN1", "JUAN2", "JUAN3", "JUDAS"],
    10: ["APOCALIPSIS"]
    }
    for grupo, libros in grupos.items():
        if libro in libros:
            return grupo
    return None

# Conecto con la base de datos sqlite biblia.db ubicada en la carpeta raíz
conn = sqlite3.connect('biblia.db')

# Función para guardar un registro en la base de datos
def GuardarRegistro(tabla, libroID, capitulo, versiculo, texto, comentario):
    testamentoID = 1 if libroID < 40 else 2
    grupoID = AsignarGrupoID(tabla)
    conn.execute(f"INSERT INTO {tabla} (testamentoID, grupoID, libroID, capitulo, versiculo, texto, comentario) VALUES (?, ?, ?, ?, ?, ?, ?)", (testamentoID, grupoID, libroID, capitulo, versiculo, texto, comentario))
    conn.commit()


def main():
    # Declaración de variables:
    cap = 0
    vers = 0
    textvers = ""
    comentario = ""
    copiar = False
    libroID = 0
    ruta_libros = "biblia_txt"
    ruta_comentarios = "CBIndexado"
    patron_capitulo = r'^\| CAPÍTULO\s+(\d+)\s*$'
    patron_salmo = r'^\| SALMO\s+(\d+)\s*$'
    patron_numeroCap = r"\d+"

    conn = sqlite3.connect("biblia.db")
    c = conn.cursor()

    # Recorro con un for los archivos de texto que están en la carpeta que está en ruta_libros (los libros de la biblia)
    n = 1
    # Obtener la lista de nombres de archivo en la carpeta y ordenarla alfabéticamente
    for archivo in sorted(os.listdir(ruta_libros)):
        libroID = ExtraerLibroID(archivo)
        tabla_name = LimpiarNombre(archivo)
        tabla_name = re.sub('\s+', '_', tabla_name)
        c.execute(f"CREATE TABLE IF NOT EXISTS '{tabla_name}' (ID INTEGER PRIMARY KEY AUTOINCREMENT, testamentoID INTEGER, grupoID INTEGER, libroID INTEGER, capitulo INTEGER, versiculo INTEGER, texto TEXT, comentario TEXT)")
        # c.execute(f"DROP TABLE IF EXISTS '{tabla_name}';")
        print("Iteración",n," Libro", tabla_name)
        copiar = False
        cap = 0
        vers = 0
        pase=0
        versanterior=0
        with open(f"{ruta_libros}/{archivo}", 'r') as libro_actual:
            for linea in libro_actual:
                linea = linea.strip()            
                if re.match(patron_capitulo, linea) or re.match(patron_salmo, linea):
                    resultado = re.search(patron_numeroCap, linea)          
                    if resultado:
                        cap = resultado.group(0)
                        # print(tabla_name, cap, " : ",vers)
                        if copiar:
                            if textvers.strip() and int(cap) > 0 and int(vers) > 0:
                                if versanterior < int(str(cap)+str(vers)) + 100:
                                    GuardarRegistro(tabla_name, libroID, int(cap)-1, vers, textvers, comentario.strip())                            
                                    textvers=""
                                    comentario=""
                                    copiar = False
                                    versanterior= int(str(cap)+str(vers))
                                # print("En este capítulo pasé ", pase, "veces por ahí")
                elif re.match('^[0-9]+$', linea):
                    if copiar:
                        if textvers.strip() and int(cap) > 0 and int(vers) > 0:
                            GuardarRegistro(tabla_name, libroID, cap, vers, textvers, comentario.strip())
                            textvers = ""
                            comentario = ""
                            versanterior= int(str(cap)+str(vers))
                    vers = int(linea)
                    copiar = True
                    textvers = ""
                    comentario = ComentarioBiblico(os.path.join(ruta_comentarios, archivo), cap, vers)                    
                elif copiar:
                    textvers += linea + ' '
            # Verificar si hay algún versículo sin guardar al final del capítulo
            if copiar:
                if textvers.strip() and int(cap) > 0 and int(vers) > 0:
                    GuardarRegistro(tabla_name, libroID, cap, vers, textvers, comentario.strip())                    
                    textvers=""
                    comentario=""
                    copiar = False
                    versanterior= int(str(cap)+str(vers))
            n += 1
            

    # conn.commit()
    conn.close()



main()
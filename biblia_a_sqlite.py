import os
import sqlite3
import re

#Función para buscar los comentarios bíblicos
def ComentarioBiblico(archivo, cap_y_ver):
    # Abrir el archivo
    with open(archivo, 'r') as f:
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
        return texto.strip()


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
    conn.execute(f"INSERT INTO {tabla} (testamentoID, grupoID, libroID, capitulo, versiculo, texto) VALUES (?, ?, ?, ?, ?, ?)", (testamentoID, grupoID, libroID, capitulo, versiculo, texto))
    conn.commit()


# Declaración de variables:
cap = 0
vers = 0
textvers = ""
comentario=""
copiar = False
libroID = 0
ruta_libros = "biblia_txt"
ruta_comentarios="CBIndexado"
#patron_capitulo = r'^| CAPÍTULO\s+(\d+)\s*$'
patron_capitulo = r'^\| CAPÍTULO\s+(\d+)\s*$'

# patron_capitulo = r'|'
patron_numeroCap = r"\d+"
# Recorro con un for los archivos de texto que están en la carpeta que está en ruta_libros (los libros de la biblia)
n=0
# Obtener la lista de nombres de archivo en la carpeta y ordenarla alfabéticamente
for archivo in sorted(os.listdir(ruta_libros)):
    if LimpiarNombre(archivo)!="2SAMUEL":

        libroID = ExtraerLibroID(archivo)
        tabla_name = LimpiarNombre(archivo)
        tabla_name = re.sub('\s+', '_', tabla_name)
        conn.execute(f"CREATE TABLE IF NOT EXISTS '{tabla_name}' (ID INTEGER PRIMARY KEY AUTOINCREMENT, testamentoID INTEGER, grupoID INTEGER, libroID INTEGER, capitulo INTEGER, versiculo INTEGER, texto TEXT, comentario TEXT)")
        # conn.execute(f"DROP TABLE IF EXISTS '{tabla_name}';")

        copiar = False
        cap = 0
        vers = 0
        with open(f"{ruta_libros}/{archivo}", 'r') as libro_actual:
            for linea in libro_actual:
                linea = linea.strip()
                #if re.match('^CAPÍTULO [0-9]+$', linea):
                if re.match(patron_capitulo, linea):  
                    resultado = re.search(patron_numeroCap, linea)          
                    if resultado:
                        cap = resultado.group(0)#int(linea.split(' ')[1])
                        print(tabla_name, "Capítulo", cap)
                elif re.match('^[0-9]+$', linea):
                    if int(cap) > 0 and int(vers) > 0:                        
                        GuardarRegistro(tabla_name, libroID, cap, vers, textvers,comentario)
                        textvers=""
                        comentario=""
                    vers = int(linea)
                    comentario=ComentarioBiblico(,cap+"|"+vers)                    
                    copiar = True
                if copiar:
                    textvers += linea + ' '
                # print("Vers", linea)
                # if cap != 0:
                #     GuardarRegistro(tabla_name, libroID, cap, vers, textvers)
                #     textvers = ""
            n=n+1
            print("Iteración",n," Libro", tabla_name)

    conn.close()

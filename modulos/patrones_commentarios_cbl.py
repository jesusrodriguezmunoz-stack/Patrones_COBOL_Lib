### Módulo para patrones en COBOL y manipulación de texto.
### Incluye funciones para cargar palabras reservadas, detectar separadores y líneas comentadas,
### y extraer bloques de texto comentados entre etiquetas específicas.
### Autor: Jota Rodríguez
### Fecha: 2024-06-20
### Versión: 1.0

RUTA_FICHERO_PALABRAS_RESERVADAS = r"palabras_reservadas_cobol.txt"

### Función para cargar palabras reservadas desde un fichero de texto
def cargar_palabras_reservadas(ruta_fichero):
    """
    Carga las palabras reservadas de COBOL desde un fichero de texto.
    Cada palabra debe estar en una línea separada.
    
    :param ruta_fichero: Ruta al fichero de texto
    :return: Lista de palabras reservadas
    """
    try:
        with open(ruta_fichero, 'r', encoding='utf-8') as f:
            palabras = [linea.strip() for linea in f if linea.strip()]
        return palabras
    except FileNotFoundError:
        print(f"Fichero no encontrado: {ruta_fichero}")
        return []
    except Exception as e:
        print(f"Error al leer el fichero: {e}")
        return []

### Función para detectar separadores en COBOL
def es_separador(linea):
    """
    Detecta si una línea es un separador en código COBOL.
    Criterios:
    - Comentario COBOL (asterisco en columna 7)
    - El resto de la línea contiene un solo tipo de carácter repetido
    - Longitud mínima (por defecto 10 caracteres)
    """
    if len(linea) < 10:
        return False

    # Verifica si es una línea comentada
    if linea[6] != '*':
        return False

    # Extraer contenido a partir de la columna 8
    contenido = linea[7:].strip().replace(" ", "")
    return len(contenido) >= 5 and len(set(contenido)) == 1

### Función para detectar líneas comentadas en COBOL
def obtener_lineas_comentadas(lineas):
    """
    Retorna una lista de tuplas con el número de línea y el contenido completo
    de cada línea comentada en un programa COBOL.
    Una línea se considera comentada si tiene un '*' en la columna 7.
    :param lineas: Lista de líneas del programa COBOL
    :return: Lista de tuplas (número de línea, contenido de la línea)
    """
    comentadas = []
    for i, linea in enumerate(lineas):
        if (len(linea) > 6 and linea[6] == '*') and not es_separador(linea):
            comentadas.append((i + 1, linea.rstrip()))
    return comentadas

### Función para contar líneas comentadas en COBOL
def obtener_num_lineas_comentadas(lineas):
    """
    Retorna el número total de líneas comentadas en un programa COBOL.
    Una línea se considera comentada si tiene un '*' en la columna 7.
    :param lineas: Lista de líneas del programa COBOL
    :return: Número total de líneas comentadas
    """
    total_lineas = 0
    for i, linea in enumerate(lineas):
        if len(linea) > 6 and linea[6] == '*':
            total_lineas += 1
    return total_lineas

## Función para detectar patrones de etiquetas en COBOL (**A*)
def es_patron_etiqueta(linea):
    """ 
    Detecta si una línea sigue el patrón de etiqueta **A*, 
    donde A es una letra mayúscula. 
    """
    import re
    return bool(re.match(r"^\*\*[A-Za-z]\*$", linea.strip()))

### Función para extraer bloques comentados entre etiquetas (**A*)
def ext_bloq_comentados_patron_etiqueta(texto):
    """
    Extrae bloques de texto comentados que están delimitados por líneas que siguen el patrón de etiqueta **A*.
    :param texto: Texto completo del programa COBOL
    :return: Lista de bloques de texto comentados
    """
    lineas = texto.splitlines()
    bloques = []
    bloque_actual = []
    dentro_bloque = False

    for linea in lineas:
        if es_patron_etiqueta(linea):
            if dentro_bloque:
                bloque_actual.append(linea)
                bloques.append("\n".join(bloque_actual))
                bloque_actual = []
                dentro_bloque = False
            else:
                bloque_actual.append(linea)
                dentro_bloque = True
        elif dentro_bloque:
            bloque_actual.append(linea)

    return bloques

### Función para obtener líneas comentadas que contienen la palabra DISPLAY
def obtener_lineas_comentadas_con_display(lineas):
    """
    Retorna una lista de tuplas con el número de línea y el contenido completo
    de cada línea comentada que contiene la palabra DISPLAY.
    Una línea se considera comentada si tiene un '*' en la columna 7.
    :param lineas: Lista de líneas del programa COBOL
    :return: Lista de tuplas (número de línea, contenido de la línea)
    """
    resultado = []
    for i, linea in enumerate(lineas):
        if len(linea) > 6 and linea[6] == '*' and 'DISPLAY' in linea.upper():
            resultado.append((i + 1, linea.rstrip()))
    return resultado

## Ejemplo de uso
with open(r"src\PGM1.cbl", 'r', encoding='utf-8') as f:
    lineas = f.readlines()
    comentadas_display = obtener_lineas_comentadas_con_display(lineas)
    for num_linea, contenido in comentadas_display:
        print(f"Línea {num_linea}: {contenido}")

## Ejemplo de uso
##with open(r"src\PGM1.cbl", 'r', encoding='utf-8') as f:
##    texto = f.read()
##    print(f"Número total de líneas comentadas: {obtener_num_lineas_comentadas(texto.splitlines())}")

## Ejemplo de uso
##with open(r"src\PGM1.cbl", 'r', encoding='utf-8') as f:
##    texto = f.read()
##    bloques_comentados = ext_bloq_comentados_patron_etiqueta(texto)
##    for i, bloque in enumerate(bloques_comentados, 1):
##        print(f"Bloque {i}:\n{bloque}\n{'-'*40}")

## Ejemplo de uso
#with open(r"src\PGM1.cbl", 'r', encoding='utf-8') as f:
#    lineas = f.readlines()
#    etiquetas = [linea.rstrip() for linea in lineas if es_patron_etiqueta(linea)]
#    for etiqueta in etiquetas:
#        print(f"Etiqueta encontrada: {etiqueta}")

##with open(r"src\PGM1.cbl", 'r', encoding='utf-8') as f:
##    lineas = f.readlines()
##    comentadas = obtener_lineas_comentadas(lineas)
##    for num_linea, contenido in comentadas:
##        print(f"Línea {num_linea}: {contenido}")

# Ejemplo de uso
##ruta = r"palabras_reservadas_cobol.txt"
##reservadas = cargar_palabras_reservadas(ruta)
##print(f"Se han cargado {len(reservadas)} palabras reservadas.")

# Ejemplos de prueba
## lineas = [
##     "******************************************************************",
##     "--------------------------",
##     "==== ==== ==== ====",
##     "* * * * * * * *",
##     "Este es un comentario",
##     "*************** INICIO ***************"
## ]
## 
# Aplicar la función a cada línea
##with open(r"src\PGM1.cbl", 'r', encoding='utf-8') as f:
##    lineas = f.readlines()
##    
##for linea in lineas:
##    resultado = es_separador(linea)
##    print(f"'{linea}' => {'Separador' if resultado else 'No separador'}")
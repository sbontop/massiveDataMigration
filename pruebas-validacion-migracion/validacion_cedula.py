# Funcion que se encarga de cargar la informacion de las
# lineas en un diccionario, y su estructura es la siguiente:
# { 
# no_cedula: 
# [ nombres, no_veces_aparicion_cedula, [ competencia1, competencia2, competencia3, ... ] ]
# }
def file_to_dic(filename):
    # Archivo a Leer
    archivo = open(filename)
    cont = 0
    trabajadores = {}
    for linea in archivo:
        if cont > 0:
            linea = linea.strip().split("\t")
            #print(len(linea),linea, "linea no", cont)
            #validacion = "si" if (len(linea) == 8) else "no"
            #print(validacion, cont)
            texto_competencia = linea[0]
            inicial = linea[1]
            actual = linea[2]
            deseado = linea[3]
            cedula = linea[4].lower()
            nombres = linea[5]
            area = linea[6]
            if cedula == 'p':
                cedula = '*'+nombres[0:7]+'*'
            if cedula not in trabajadores:
                no_veces_aparicion_cedula = 1
                trabajadores[cedula] = ['', '', []]
                trabajadores[cedula][0] = nombres
                trabajadores[cedula][1] = no_veces_aparicion_cedula
            else:
                trabajadores[cedula][1] += 1
            trabajadores[cedula][2].append(texto_competencia)
        cont += 1
    archivo.close()
    return trabajadores

# Funcion que se encarga de generar un reporte acerca de 
# si los datos estan correctamente registrados
# si algun empleado aun no posee cedula o 
# si existen inconsistencias entre las competencias con el no de cedula
# por ejemplo
def generar_reporte_consola(dic_trabajadores):

    lista_no_veces_aparicion_cedula = []
    lista_numero_competencias = []
    lista_empleados_sin_cedula = []

    no_total_cedulas = 0
    no_total_trabajadores = 0
    no_total_registros_cedula = 0
    no_total_competencias = 0

    print('{:>20}{:>20}{:>50}{:>50}'
          .format(
              'Cédula',
              'Nombres',
              'Número de veces que aparece la cédula',
              'Número de Competencias'
          )
          )

    for key, val in dic_trabajadores.items():

        if key[0] == '*':
            lista_empleados_sin_cedula.append(val[0])
        lista_no_veces_aparicion_cedula.append(val[1])
        lista_numero_competencias.append(len(list(val[2])))

        no_total_cedulas += 1
        no_total_trabajadores += 1
        no_total_registros_cedula += val[1]
        no_total_competencias += len(list(val[2]))

        print('{:>20}{:>20}{:>50}{:>50}'
              .format(
                  key,
                  val[0],
                  val[1],
                  len(val[2])
              )
              )

    print('{:>10}{:>10}{:>20}{:>50}{:>50}'
          .format(
              'Total:',
              no_total_cedulas,
              no_total_trabajadores,
              no_total_registros_cedula,
              no_total_competencias
          )
          )

    print('■ En resumen se han registrado {} cédulas de {} empleados con {} registros de cédula y {} competencias.'
          .format(
              no_total_cedulas,
              no_total_trabajadores,
              no_total_registros_cedula,
              no_total_competencias
          )
          )
    if len(lista_empleados_sin_cedula) == 0:
        print('■ Todos los empleados poseen cédula')
    else:
        print('■ Los siguientes empleados no poseen cedula:')
        for empleado in lista_empleados_sin_cedula:
            print('┼ ' + empleado)

    if lista_no_veces_aparicion_cedula == lista_numero_competencias:
        print('■ Los registros son correctos')
    else:
        print('■ Los registros son incorrectos')

# Funcion se encarga de guardar el reporte de arriba en un 
# archivo de texto llamado salida.txt
def generar_reporte_archivo(dic_trabajadores, filename):

    archivo = open(filename, "w+", encoding='utf-8')

    lista_no_veces_aparicion_cedula = []
    lista_numero_competencias = []
    lista_empleados_sin_cedula = []

    no_total_cedulas = 0
    no_total_trabajadores = 0
    no_total_registros_cedula = 0
    no_total_competencias = 0
    archivo.write("Escritura de caracteres especiales a un archivo:\naéíóúñoño\n")
    linea0 = '{:>20}{:>20}{:>50}{:>50}{}'.format(
        'Cédula', 'Nombres', 'Número de veces que aparece la cédula', 'Número de Competencias', '\n')
    archivo.write(linea0)    
    for key, val in dic_trabajadores.items():

        if key[0] == '*':
            lista_empleados_sin_cedula.append(val[0])
        lista_no_veces_aparicion_cedula.append(val[1])
        lista_numero_competencias.append(len(list(val[2])))

        no_total_cedulas += 1
        no_total_trabajadores += 1
        no_total_registros_cedula += val[1]
        no_total_competencias += len(list(val[2]))
        linea1 = '{:>20}{:>20}{:>50}{:>50}{}'.format(
            key, val[0].encode('utf-8').decode('utf-8'), val[1], len(val[2]), '\n')
        archivo.write(linea1)

    linea2 = '{:>10}{:>10}{:>20}{:>50}{:>50}'.format(
        'Total:', no_total_cedulas, no_total_trabajadores, no_total_registros_cedula, no_total_competencias)
    archivo.write(linea2)
    linea3 = '■ En resumen se han registrado {} cédulas de {} empleados con {} registros de cédula y {} competencias.{}'.format(
        no_total_cedulas, no_total_trabajadores, no_total_registros_cedula, no_total_competencias,'\n')
    archivo.write(linea3)
    if len(lista_empleados_sin_cedula) == 0:
        linea4 = '■ Todos los empleados poseen cédula\n'
        archivo.write(linea4)
    else:
        linea5 = '■ Los siguientes empleados no poseen cedula:\n'
        archivo.write(linea5)
        for empleado in lista_empleados_sin_cedula:
            linea6 = '┼ ' + empleado + '\n'
            archivo.write(linea6)

    if lista_no_veces_aparicion_cedula == lista_numero_competencias:
        linea7 = '■ Los registros son correctos\n'
        archivo.write(linea7)
    else:
        linea8 = '■ Los registros son incorrectos\n'
        archivo.write(linea8)
    archivo.close()

# Prueba de caracteres especiales 
# Esta funcion realiza lectura de caracteres especiales de un archivo
# utf-8 no sirve para leer enies
# tuve que buscar otro tipo de codificacion, y encontre: 'ISO-8859-1'
# La escritura de caracteres especiales se encuentra dentro de la function
# que genera el reporte por consola, debido a que aprovecho que esta escribiendo un archivo
# y le envio letras con tilde y enies.
def test_lectura_caracteres_especiales(filename):
    print("Lectura de caracteres especiales de un archivo:")
    archivo = open(filename, "r", encoding = 'ISO-8859-1')
    for linea in archivo:
        linea = linea.strip().split('\t')
        print(linea)

# Creo el diccionario de trabajadores
# llamado a la funcion file_to_dic(filename)
# Extrayendo los datos del archivo "Archivo Sur_enviar.txt"
filename = "archivos de texto a procesar/Archivo Sur_enviar.txt"
dic_trabajadores = file_to_dic(filename)
# Genero un reporte en consola
generar_reporte_consola(dic_trabajadores)
# Guardo el reporte generado en un archivo de texto
# llamado salida.txt
salida = "archivos de texto generados/salida.txt"
generar_reporte_archivo(dic_trabajadores, salida)
# Realizo el test de caracteres especiales
test_lectura_caracteres_especiales('archivos de texto a procesar/caracteres_especiales.txt')










# Generacion de Archivo CSV para poder ingresar los datos a la la plataforma ACCESS
# Por el momento, el archivo de prueba se encuentra casi listo porque
# Cristian esta teniendo problemas con el ingreso de las competencias por matriz/linea
# porque en la primera matriz que se hizo prueba TODOS LOS TRABAJADORES TENIAN
# EL MISMO NUMERO DE COMPETENCIAS, PERO EN EL RESTO DE LINEAS ESTO NO SUCEDE, ES DECIR,
# PUEDE EXISTIR EL CASO QUE EN UNA LINEA UN TRABAJADOR TENGA SOLO UNA COMPETENCIA, Y EL RESTO 50
# ENTONCES COMO CADA COMPETENCIA ES UNA TABLA, SI LE MANDA A INGRESAR A TODAS LAS COMPETENCIAS EXISTENTES
# LE SALE ERROR AL MOMENTO DE INGRESAR UNA COMPETENCIA QUE UN TRABAJADOR NO POSEE

# SOLUCION:
# Como solucion se propone ingresar el mismo numero de competencias por linea, es decir,
# OBLIGATORIAMENTE TODOS LOS TRABAJADORES TENDRAN EL MISMO NUMERO DE COMPETENCIAS
# para asi poder realizar el insert por linea/matriz y no habra problema
# En caso que el trabajador que posee solo 1 competencia, se debe de registrar el resto
# de competencias restantes de su linea y SETEAR ACTUAL Y REQUERIDO EN 1
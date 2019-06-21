# Esta Funcion carga un diccionario que tiene como clave
# el nombre de la matriz y como valor la lista de competencias
# El diccionario es retornado
def dic_competencias_por_matriz(filename):
    archivo = open(filename)
    dic_competencias_por_matriz = {}
    cont = 0
    for linea in archivo:
        if cont > 0:
            linea = linea.strip().split('\t')
            
            texto_competencia = linea[0]
            texto_matriz = linea[7]
            #print(texto_matriz, texto_competencia)
            #break
            if texto_matriz not in dic_competencias_por_matriz:
                dic_competencias_por_matriz[texto_matriz] = set()
            dic_competencias_por_matriz[texto_matriz].add(texto_competencia)
        cont += 1
    archivo.close()
    return dic_competencias_por_matriz
dic_competencias_por_matriz = dic_competencias_por_matriz('Archivo Sur_enviar.txt')
# print(dic_competencias_por_matriz.keys())

# Funcion que se encarga de cargar la informacion de las
# lineas en un diccionario, y su estructura es la siguiente:
# { 
# no_cedula: 
# [ nombres, no_veces_aparicion_cedula, actual, deseado, matriz, [ competencia1, competencia2, competencia3, ... ] ]
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
            texto_matriz = linea[7]
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
                trabajadores[cedula] = ['', '', '', '','', []]
                trabajadores[cedula][0] = nombres
                trabajadores[cedula][1] = no_veces_aparicion_cedula
                trabajadores[cedula][4] = texto_matriz
            else:
                # Esta linea de abajo hace la magia con el numero
                # de veces de aparicion de la cedula
                # de un empleado
                trabajadores[cedula][1] += 1
            trabajadores[cedula][-1].append((texto_competencia, actual, deseado))
        cont += 1
    archivo.close()
    return trabajadores
dic_trabajadores = file_to_dic('Archivo Sur_enviar.txt')

# Esta Funcion intenta comparar las competencias de los trabajadores
# con las competencias existentes en cada matriz
def complementar_competencias(dic_trabajadores, dic_competencias_por_matriz):
    veces_if = 0
    veces_else = 0
    veces_else_if = 0
    cont4 = 0
    cont3 = 0
    cont2 = 0
    dic_trabajadores_complementado = {}
    for texto_matriz, conjunto_competencias_por_matriz in dic_competencias_por_matriz.items():
        cont = 0
        for cedula, val in dic_trabajadores.items():            
            texto_matriz_por_empleado = val[4]
            lista_tupla_competencias_por_empleado = val[-1]
            if texto_matriz == texto_matriz_por_empleado:
                cont += 1                
               
                conjunto_competencias_restantes_por_trabajador = set()
                conjunto_competencias_iniciales_por_trabajador = set()
                for competencia_por_matriz in conjunto_competencias_por_matriz:
                    actual = requerido = ''
                    flag = flag2 = False                    
                    for tupla_competencia_por_empleado in lista_tupla_competencias_por_empleado:

                        # Print para verificar el numero de veces que se recorre la misma competencia
                        # por cada competencia del trabajador (diccionario)
                        print(competencia_por_matriz, tupla_competencia_por_empleado, cedula)

                        # Creacion del elemento del diccionario unico
                        if cedula not in dic_trabajadores_complementado:
                            dic_trabajadores_complementado[cedula] = []
                        
                        # Pregunto si la competencia por matriz se encuentra en la tupla competencia por empleado
                        if competencia_por_matriz in tupla_competencia_por_empleado:
                            veces_if += 1
                            
                            conjunto_competencias_iniciales_por_trabajador.add(tupla_competencia_por_empleado[0])
                            #print(texto_matriz+'\n',competencia_por_matriz, tupla_competencia_por_empleado, '\n')
                            dic_trabajadores_complementado[cedula].append(tupla_competencia_por_empleado)
                            #print(tupla_competencia_por_empleado)
                            flag2 = True
                        
                        if flag2 == False:                                
                            conjunto_competencias_restantes_por_trabajador.add(competencia_por_matriz)
                            tupla_encerada = (competencia_por_matriz, 1, 1)
                            dic_trabajadores_complementado[cedula].append(tupla_encerada)
                            veces_else_if += 1
                    flag2 = False                                            
                    """conjunto_competencias_restantes_por_trabajador.add(competencia_por_matriz)
                    tupla_encerada = (competencia_por_matriz, 1, 1)
                    dic_trabajadores_complementado[cedula].append(tupla_encerada)"""

                    

                print('\nNumero de veces que entra al if\n', veces_if)
                #print('\nNumero de veces que entra al else\n', veces_else)
                #print('\nNumero de veces que entra a else if\n', veces_else_if)
                
                print('\nlen(lista_tupla_competencias_por_empleado)\n',len(lista_tupla_competencias_por_empleado))
                
                print('\nconjunto_competencias_iniciales_por_trabajador\n', conjunto_competencias_iniciales_por_trabajador)
                print('\nlen(conjunto_competencias_iniciales_por_trabajador)', len(conjunto_competencias_iniciales_por_trabajador))
                print('\nconjunto_competencias_restantes_por_trabajador\n', conjunto_competencias_restantes_por_trabajador)
                print('\nlen(conjunto_competencias_restantes_por_trabajador)',len(conjunto_competencias_restantes_por_trabajador))
                print('\nconjunto_competencias_restantes_por_trabajador - conjunto_competencias_iniciales_por_trabajador\n', conjunto_competencias_restantes_por_trabajador - conjunto_competencias_iniciales_por_trabajador)                                
                print('\nlen(conjunto_competencias_restantes_por_trabajador - conjunto_competencias_iniciales_por_trabajador)', len(conjunto_competencias_restantes_por_trabajador - conjunto_competencias_iniciales_por_trabajador))
            
            # Este break me permite solo leer el primer trabajador del diccionario de trabajadores            
            break
    print('\n{:>20}{:>20}\n{:>20}{:>20}\n{:>20}{:>20}\n'.format('Competencias iniciales del trabajador', len(conjunto_competencias_iniciales_por_trabajador), 'Competencias restantes del trabajador', len(conjunto_competencias_restantes_por_trabajador - conjunto_competencias_iniciales_por_trabajador), 'Existentes + Restantes', len(conjunto_competencias_iniciales_por_trabajador) + len(conjunto_competencias_restantes_por_trabajador - conjunto_competencias_iniciales_por_trabajador)))
    
    return dic_trabajadores_complementado

# Creo el diccionario de trabajadores complementado
dic_trabajadores_complementado = complementar_competencias(dic_trabajadores, dic_competencias_por_matriz)
# print(dic_trabajadores_complementado)

# Funcion que me permite verificar el diccionario de los trabajadores con todas las competencias complementadas
def verificar_diccionario_trabajadores_competencias_complementadas(dic_trabajadores_complementado):
    print('Verificacion del diccionario de datos de los trabajadores complementando competencias')
    for k, v in dic_trabajadores_complementado.items():
        # print(k, v)
        print('k, len(v)',k, len(v))
        break
# verificar_diccionario_trabajadores_competencias_complementadas(dic_trabajadores_complementado)


# Esta funcion me permite verificar el numero de competencias por matriz
def verificar_numero_competencias_por_matriz(dic_competencias_por_matriz):
    print('Verificacion del numero de competencias por matriz')
    print('Nombre de Matriz', 'Numero de competencias')
    print('\n')
    for k,v in dic_competencias_por_matriz.items():    
        #print(k, v)
        print('{} {}'.format(k, len(v)))
verificar_numero_competencias_por_matriz(dic_competencias_por_matriz)
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
"""
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
"""









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
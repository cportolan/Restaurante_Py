# LIBRERIAS:
import sys
import csv
import re
import os

# CONSTANTES:

# Generales:
ARCHIVO = 'reservas.csv'
ARCHIVO_AUX = 'reservas_aux.csv'
DELIMITADOR = ';'

CANT_MINIMA_COMANDOS = 2

INDICE_COMANDO = 1

INDICE_ID_RESERVAS = 0
INDICE_NOMBRE_RESERVAS = 1
INDICE_CANTIDAD_PERSONAS_RESERVAS = 2
INDICE_HORA_RESERVAS = 3
INDICE_LUGAR_RESERVAS = 4

INDICE_ID_MODIFICAR_ELIMINAR = 2

VALOR_INICIAL_CANTIDAD_PERSONAS = 0
VALOR_INICIAL_ID = 1
VALOR_INICIAL = 0

ORACION_ERROR = 'Lo sentimos, hubo un error al abrir el archivo, probablemente no exista.'
ORACION_ERROR_AUXILIAR = 'Lo sentimos, hubo un error al abrir el archivo auxiliar.'
NO_EXISTE_ID = 'Hubo un problema: no hay una reserva con ese id.'
NO_EXISTE_ID1_ID2 = 'Hubo un problema: no hay reservas entre los rangos recibidos.'

AFUERA = 'F'
ADENTRO = 'D'

# Para agregar:
COMANDO_AGREGAR = 'agregar'
CANTIDAD_PARAMETROS_AGREGAR = 6
INDICE_NOMBRE_AGREGAR = 2
INDICE_COMENSALES_AGREGAR = 3
INDICE_HORA_AGREGAR = 4
INDICE_AFUERA_ADENTRO_AGREGAR = 5

# Para eliminar:
COMANDO_ELIMINAR = 'eliminar'
CANTIDAD_PARAMETROS_ELIMINAR = 3

# Para modificar:
COMANDO_MODIFICAR = 'modificar'
CANTIDAD_PARAMETROS_MODIFICAR = 3
INDICE_DATO = 0
INDICE_DATO_A_MODIFICAR = 1
MODIFICAR_NOMBRE = 'nombre'
MODIFICAR_CANT = 'cant'
MODIFICAR_HORA = 'hora'
MODIFICAR_UBICACION = 'ubicacion'

# Para listar:
COMANDO_LISTAR = 'listar'
INDICE_PRIMER_ID_LISTAR = 2
INDICE_SEGUNDO_ID_LISTAR = 3
CANTIDAD_PARAMETROS_LISTAR_RANGO = 4
CANTIDAD_PARAMETROS_LISTAR_TODOS = 2

# FUNCIONES:

# Pre: -
# Pos: Devuelve un entero que es el ID maximo dentro de mi archivo de reservas. Si no hay archivo, devuelve cero (VALOR_INICIAL).
def calcular_maximo_id():
    try:
        archivo = open(ARCHIVO)
    except:
        return VALOR_INICIAL
    
    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    maximo_id = VALOR_INICIAL
    for fila in lector:
        id = int(fila[INDICE_ID_RESERVAS])
        if id > maximo_id:
            maximo_id = id

    archivo.close()
    return maximo_id

# Pre: -
# Pos: Devuelve true en el caso de que haya una reserva con el id dado por parametro.
def existe_reserva(id_reserva):
    try:
        archivo = open(ARCHIVO)
    except:
        print(ORACION_ERROR)
        return

    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    for fila in lector:
        if fila[INDICE_ID_RESERVAS] == id_reserva:
            archivo.close()
            return True
    
    archivo.close()
    return False


# Pre: El horario recibido debe ser un string.
# Pos: Devuelve True o False dependiendo si el horario esta en el rango correcto (00:00 a 23:59)
def horario_aceptado(horario):
    horario_validado = r'^([01]\d|2[0-3]):[0-5]\d$'
    if re.match(horario_validado, horario):
        return True
    else:
        return False

# Pre: Debe recibir un entero por parametro.
# Pos: Devuelve True o False dependiendo si cant es mayor a cero.
def cant_personas_aceptada(cant):
    return cant > VALOR_INICIAL_CANTIDAD_PERSONAS

# Pre: Debe recibir un string por parametro.
# Pos: Devuelve True o False dependiendo si la ubicacion es valida ([F]uera o [D]entro)
def ubicacion_aceptada(ubicacion):
    return ubicacion == AFUERA or ubicacion == ADENTRO

# Pre: Los datos recibidos deben ser strings.
# Pos Devuelve True o False dependiendo si el dato recibido es el valido teniendo en cuenta el primer dato (cant: int > 0, ubicacion: [F]uera o [D]entro, hora: entre 00:00 y 23:59)
def campos_aceptados(primer_dato, segundo_dato):
    resultado = False
    if primer_dato == MODIFICAR_NOMBRE:
        resultado = True
    elif primer_dato == MODIFICAR_CANT and segundo_dato.isnumeric() and int(segundo_dato) > VALOR_INICIAL_CANTIDAD_PERSONAS:
        resultado = True
    elif primer_dato == MODIFICAR_HORA and horario_aceptado(segundo_dato):
        resultado = True
    elif primer_dato == MODIFICAR_UBICACION and ubicacion_aceptada(segundo_dato):
        resultado = True
    return resultado

# Pre: -
# Pos: Agrega una nueva fila (reserva) a nuestro archivo .csv
def agregar_reserva(nombre, cantidad, hora, lugar):
    
    id = calcular_maximo_id() + VALOR_INICIAL_ID

    try:
        archivo = open(ARCHIVO, mode='a', newline='')
    except:
        print(ORACION_ERROR)
        return
    
    escritor = csv.writer(archivo, delimiter = DELIMITADOR)

    if not cantidad.isnumeric() or not cant_personas_aceptada(int(cantidad)):
        print("La cantidad de personas debe ser un numero entero positivo.")
        return

    if horario_aceptado(hora) == False:
        print("El horario debe estar entre las 00:00 y las 23:59, no invente horarios inexistentes!")
        return

    if not ubicacion_aceptada(lugar):
        print("El lugar debe ser representado como: D (Dentro) o F (Fuera), vuelva a colocar su reserva nuevamente.")
        return

    nueva_reserva = [id, nombre, cantidad, hora, lugar]

    escritor.writerow(nueva_reserva)
    print("Reserva agregada correctamente!")
    archivo.close()
    
# Pre: -
# Pos: Muestra por pantalla las filas (reservas) de nuestro archivo .csv que esten en el rango de IDS recibidos en consola. Si no existe el primer id muestra error y no hace nada. 
def listar_algunas_reservas(id1, id2):

    try:
        archivo = open(ARCHIVO)
    except:
        print(ORACION_ERROR)
        return
    
    lector = csv.reader(archivo, delimiter = DELIMITADOR)

    primer_id = int(id1)
    segundo_id = int(id2)
    rangos_correctos = False

    for reserva in lector:
        id = int(reserva[INDICE_ID_RESERVAS])
        if primer_id <= id <= segundo_id:
            rangos_correctos = True
            print(f"La reserva {id}, a nombre de {reserva[INDICE_NOMBRE_RESERVAS]} tiene {reserva[INDICE_CANTIDAD_PERSONAS_RESERVAS]} comensal/es, el horario de la reserva es a las {reserva[INDICE_HORA_RESERVAS]} y la mesa esta {reserva[INDICE_LUGAR_RESERVAS]} (F = Fuera, D = Dentro)")
        elif not rangos_correctos:
            print(NO_EXISTE_ID1_ID2)
            archivo.close()
            return          

# Pre: -
# Pos: Muestra por pantalla todas las filas (reservas) de nuestro archivo .csv
def listar_todas_reservas():
    try:
        archivo = open(ARCHIVO)
    except:
        print(ORACION_ERROR)
        return
    
    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    for reserva in lector:
        print(f"La reserva {reserva[INDICE_ID_RESERVAS]}, a nombre de {reserva[INDICE_NOMBRE_RESERVAS]} tiene {reserva[INDICE_CANTIDAD_PERSONAS_RESERVAS]} comensal/es, el horario de la reserva es a las {reserva[INDICE_HORA_RESERVAS]} y la mesa esta {reserva[INDICE_LUGAR_RESERVAS]} (F = Fuera, D = Dentro)")

    archivo.close()      

# Pre: -
# Pos: Elimina la fila (reserva) mediante el ID recibido por consola. Si no existe el ID, muestra error y no hace nada.
def eliminar_reserva(id_reserva):

    try:
        archivo = open(ARCHIVO)
    except:
        print(ORACION_ERROR)
        return
    
    try:
        archivo_aux = open(ARCHIVO_AUX, 'a')
    except:
        print(ORACION_ERROR)
        archivo.close()
        return

    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    escritor = csv.writer(archivo_aux, delimiter = DELIMITADOR)

    encontrado = False

    for reserva in lector:
        if reserva[INDICE_ID_RESERVAS] == id_reserva:
            print(f"Perfecto, eliminaste la reserva con id {id_reserva}.")
            encontrado = True
        else:
            escritor.writerow(reserva)
    
    os.rename(ARCHIVO_AUX, ARCHIVO)

    if not encontrado:
        archivo_aux.close()
        archivo.close()
        print(NO_EXISTE_ID)
        return

    archivo_aux.close()
    archivo.close()

# Pre: -
# Pos: Modifica el nombre en la reserva correspondiente (id_reserva).
def modificar_nombre_reserva(escritor, reserva, dato_modificado_array, id_reserva):
    reserva[INDICE_NOMBRE_RESERVAS] = dato_modificado_array[INDICE_DATO_A_MODIFICAR]
    escritor.writerow(reserva)
    os.rename(ARCHIVO_AUX, ARCHIVO)
    print(f"Bien, has modificado el nombre a {dato_modificado_array[INDICE_DATO_A_MODIFICAR]} de la reserva con id {id_reserva}")

# Pre: -
# Pos: Modifica la hora en la reserva correspondiente (id_reserva).
def modificar_hora_reserva(escritor, reserva, dato_modificado_array, id_reserva):
    reserva[INDICE_HORA_RESERVAS] = dato_modificado_array[INDICE_DATO_A_MODIFICAR]
    escritor.writerow(reserva)            
    os.rename(ARCHIVO_AUX, ARCHIVO)
    print(f"Bien, has modificado la hora a {dato_modificado_array[INDICE_DATO_A_MODIFICAR]} de la reserva con id {id_reserva}")

# Pre: -
# Pos: Modifica la cantidad de personas en la reserva correspondiente (id_reserva).
def modificar_cant_reserva(escritor, reserva, dato_modificado_array, id_reserva):
    reserva[INDICE_CANTIDAD_PERSONAS_RESERVAS] = dato_modificado_array[INDICE_DATO_A_MODIFICAR]
    escritor.writerow(reserva)            
    os.rename(ARCHIVO_AUX, ARCHIVO)
    print(f"Bien, has modificado la cantidad de personas a {dato_modificado_array[INDICE_DATO_A_MODIFICAR]} de la reserva con id {id_reserva}")

# Pre: -
# Pos: Modifica la ubicacion en la reserva correspondiente (id_reserva). 
def modificar_ubicacion_reserva(escritor, reserva, dato_modificado_array, id_reserva):
    reserva[INDICE_LUGAR_RESERVAS] = dato_modificado_array[INDICE_DATO_A_MODIFICAR]
    escritor.writerow(reserva)
    os.rename(ARCHIVO_AUX, ARCHIVO)
    print(f"Bien, has modificado la ubicacion a {dato_modificado_array[INDICE_DATO_A_MODIFICAR]} de la reserva con id {id_reserva}")

# Pre: -
# Pos: Modifica la fila (reserva) mediante el ID recibido por consola y el dato que se quiere cambiar. Si no existe el ID, muestra error y no hace nada. 
def modificar_reserva(id_reserva):

    try:
        archivo = open(ARCHIVO)
    except:
        print(ORACION_ERROR)
        return
    
    try:
        archivo_aux = open(ARCHIVO_AUX, 'w')
    except:
        print(ORACION_ERROR)
        archivo.close()
        return
    
    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    escritor = csv.writer(archivo_aux, delimiter = DELIMITADOR)

    encontrado = False

    for reserva in lector:

        if reserva[INDICE_ID_RESERVAS] == id_reserva:

            encontrado = True

            dato_recibido = input("Que quiere modificar?\n")
            dato_modificado_array = dato_recibido.split()

            while not campos_aceptados(dato_modificado_array[INDICE_DATO], dato_modificado_array[INDICE_DATO_A_MODIFICAR]):
                dato_recibido = input("Por favor, ingrese bien el comando. (nombre -nombre valido-, cant -cantidad valida-, hora -hora valida-, ubicacion -ubicacion valida-\n")
                dato_modificado_array = dato_recibido.split()

            if dato_modificado_array[INDICE_DATO] == MODIFICAR_NOMBRE:
                modificar_nombre_reserva(escritor, reserva, dato_modificado_array, id_reserva)

            elif dato_modificado_array[INDICE_DATO] == MODIFICAR_CANT:
                modificar_cant_reserva(escritor, reserva, dato_modificado_array, id_reserva)

            elif dato_modificado_array[INDICE_DATO] == MODIFICAR_HORA:
                modificar_hora_reserva(escritor, reserva, dato_modificado_array, id_reserva)

            elif dato_modificado_array[INDICE_DATO] == MODIFICAR_UBICACION:
                modificar_ubicacion_reserva(escritor, reserva, dato_modificado_array, id_reserva)

        else: 
            escritor.writerow(reserva)

    if not encontrado:
        os.rename(ARCHIVO_AUX, ARCHIVO)
        print(NO_EXISTE_ID)
        archivo_aux.close()
        archivo.close()
        return

    archivo_aux.close()
    archivo.close()
        
# MAIN:

def main():

    if len(sys.argv) < CANT_MINIMA_COMANDOS:
        print("Error. Debes colocar algun comando (agregar, modificar, eliminar o listar)")
        return

    comando = sys.argv[INDICE_COMANDO]

    if comando == COMANDO_AGREGAR:

        if len(sys.argv) != CANTIDAD_PARAMETROS_AGREGAR:
            print("Debe volver a colocar su nueva reserva, la cantidad de datos recibidos no es la correcta. (ID, Nombre, Cantidad de personas en la mesa, HH:MM, Ubicacion)")
            return

        nombre = sys.argv[INDICE_NOMBRE_AGREGAR]
        cantidad = sys.argv[INDICE_COMENSALES_AGREGAR]
        hora = sys.argv[INDICE_HORA_AGREGAR]
        lugar = sys.argv[INDICE_AFUERA_ADENTRO_AGREGAR]

        agregar_reserva(nombre, cantidad, hora, lugar)

    elif comando == COMANDO_MODIFICAR:
        
        if len(sys.argv) != CANTIDAD_PARAMETROS_MODIFICAR: 
            print("Lo siento, el comando es invalido. Debe colocar: modificar 'id'")
            return

        id_reserva = sys.argv[INDICE_ID_MODIFICAR_ELIMINAR]

        modificar_reserva(id_reserva)

    elif comando == COMANDO_LISTAR:

        if len(sys.argv) != CANTIDAD_PARAMETROS_LISTAR_RANGO and len(sys.argv) != CANTIDAD_PARAMETROS_LISTAR_TODOS:
            print("Lo siento, el comando es invalido!.. Si solamente coloca 'listar' apareceran todas las reservas, y si coloca dos ids aparecen las reservas de esos ids y las que esten entre ellas")
            return
        
        elif len(sys.argv) == CANTIDAD_PARAMETROS_LISTAR_RANGO:

            primer_id = sys.argv[INDICE_PRIMER_ID_LISTAR]
            segundo_id = sys.argv[INDICE_SEGUNDO_ID_LISTAR]
            listar_algunas_reservas(primer_id, segundo_id)

        elif len(sys.argv) == CANTIDAD_PARAMETROS_LISTAR_TODOS:
            listar_todas_reservas()
    
    elif comando == COMANDO_ELIMINAR: 

        if len(sys.argv) != CANTIDAD_PARAMETROS_ELIMINAR:
            print("Vuelva a colocar su comando para eliminar pero asegurese de colocar la cantidad de parametros correcta: eliminar 'id'")
            return

        id_reserva = sys.argv[INDICE_ID_MODIFICAR_ELIMINAR]
        
        eliminar_reserva(id_reserva)
    
    else:
        print("No hay ningun comando con ese nombre.")
        return

main()
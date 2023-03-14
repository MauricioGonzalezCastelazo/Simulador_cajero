# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:28:28 2022

@author: Adrián Reyes
"""
import mysql.connector
import random
from datetime import datetime

#Transferencia
client = mysql.connector.connect(host='localhost',database='atm',user='root')
print(client)
cursor = client.cursor()

def transferencia(monto, Homoclave, cuenta_origen):
    query2 = ("select * from tarjetas where No_tarjeta = '%s';"%cuenta_origen)
    cursor.execute(query2)
    result_set2 = cursor.fetchall()
    
    if(monto < result_set2[0][4]):
        query = ("select * from tarjetas where No_tarjeta = '%s';"%Homoclave)
        cursor.execute(query)
        result_set = cursor.fetchall()

        if (len(result_set) == 1):
            monto_anterior = result_set[0][4]
            monto_nuevo = monto_anterior + monto
            sql = ("UPDATE Tarjetas SET Saldo = %s where No_tarjeta= %s;")
            val = (monto_nuevo, Homoclave)
            cursor.execute(sql, val)
            client.commit()
            #############
            monto_anterior1 = result_set2[0][4]
            monto_nuevo1 = monto_anterior1-monto
            sql1 = ("UPDATE Tarjetas SET Saldo = %s where No_tarjeta= %s;")
            val1 = (monto_nuevo1, cuenta_origen)
            cursor.execute(sql1, val1)
            client.commit()
            
            fecha_actual = datetime.now()
            fecha_actual = fecha_actual.strftime('%d/%B/%Y %H:%M:%S')
            fecha_actual
            query = ("insert into Transacciones values(%s, %s, %s, %s)")
            value = (fecha_actual, cuenta_origen, Homoclave, monto)
            cursor.execute(query, value)
            client.commit()
            #Movimientos
            #Cuenta origen
            
            query = ("insert into Movimientos values(%s, %s, %s, %s)")
            value = (cuenta_origen, fecha_actual, -monto, 0)
            cursor.execute(query, value)
            client.commit()
            
            #Cuenta destino
            
            query = ("insert into Movimientos values(%s, %s, %s, %s)")
            value = (Homoclave, fecha_actual, monto, 0)
            cursor.execute(query, value)
            client.commit()
            
            #result_up = cursor.fetchall()
        else: 
            print("Esa cuenta no existe")
    else: 
        print("No cuentas con los fondos suficientes")

#Revisar movimientos
def Movimientos(Cuenta):
    
    query2 = ("select * from tarjetas natural join cuenta where No_tarjeta = '%s';"%Cuenta)
    cursor.execute(query2)
    result_set2 = cursor.fetchall()
    
    if(result_set2[0][11] == 'E'):
        print("1. Ver mis movimientos.")
        print("2. Ver todos los movimientos.")
        opc = int(input("Deme la opción: "))
        if(opc == 2):
            query3 = ("select * from Movimientos")
            cursor.execute(query3)
            result_set3 = cursor.fetchall()
            for i in range(len(result_set3)):
                print("Numero de tarjeta: ", result_set3[i][0], "Fecha: ", result_set3[i][1], "Monto: ", result_set3[i][2], "Deuda: ", result_set3[i][3])
        else:
            query = ("select * from Movimientos where No_tarjeta = '%s';"%Cuenta)
            cursor.execute(query)
            result_set = cursor.fetchall()
            for i in range(len(result_set)):
                print("Numero de tarjeta: ", result_set[i][0], "Fecha: ", result_set[i][1], "Monto: ", result_set[i][2], "Deuda: ", result_set[i][3])
    else:
        query = ("select * from Movimientos where No_tarjeta = '%s';"%Cuenta)
        cursor.execute(query)
        result_set = cursor.fetchall()
        for i in range(len(result_set)):
            print("Numero de tarjeta: ", result_set[i][0], "Fecha: ", result_set[i][1], "Monto: ", result_set[i][2], "Deuda: ", result_set[i][3])
            
#Consulta

def consulta(Cuenta):
    #Cliente
    query = ("select saldo from tarjetas where No_tarjeta = '%s';"%Cuenta)
    cursor.execute(query)
    result_set = cursor.fetchall()
    print("Tu saldo es: $",result_set[0][0])
    
#Recargas

def recargas(Homoclave, cel, monto):
    query = ("select * from tarjetas where No_tarjeta = '%s';"%Homoclave)
    cursor.execute(query)
    result_set = cursor.fetchall()
    
    query2 = ("select * from Recargas where No_Celular = '%s';"%cel)
    cursor.execute(query2)
    result_set2 = cursor.fetchall()
    if ((len(result_set) == 1) and (len(result_set2) == 1)):
        if(monto < result_set[0][4]):

            monto_anterior = result_set[0][4]
            monto_nuevo = monto_anterior - monto

            sql = ("UPDATE Tarjetas SET Saldo = %s where No_tarjeta= %s;")
            val = (monto_nuevo, Homoclave)
            cursor.execute(sql, val)
            client.commit()

            saldo_anterior = result_set2[0][2]
            saldo_nuevo = saldo_anterior + monto
            print(monto_nuevo)
            sql2 = ("UPDATE Recargas SET Saldo_cel = %s where No_celular= %s;")
            val2 = (saldo_nuevo, cel)
            cursor.execute(sql2, val2)
            client.commit()

            #Movimientos
            fecha_actual = datetime.now()
            fecha_actual = fecha_actual.strftime('%d/%B/%Y %H:%M:%S')
            fecha_actual
            query = ("insert into Movimientos values(%s, %s, %s, %s)")
            value = (Homoclave, fecha_actual, -monto, 0)
            cursor.execute(query, value)
            client.commit()
            #print(val)
            #result_up = cursor.fetchall()
    
#Servicios

def servicios(monto, Homoclave, cuenta_origen):
    query = ("select * from tarjetas where No_tarjeta = '%s';"%cuenta_origen)
    cursor.execute(query)
    result_set = cursor.fetchall()
    
    #Servicios 
    servicios_casa = ["CFE", "CONAGUA", "IZZI", "INFINITUM"]
    homoclave_casa = [2000000000000001, 2000000000000002, 2000000000000003, 2000000000000004]
    
    if(Homoclave in homoclave_casa):
        if(monto<result_set[0][4]):
            indice = homoclave_casa.index(Homoclave)
            query2 = ("insert into Servicios values(%s, %s, %s, %s)")
            val2 = (cuenta_origen, homoclave_casa[indice], servicios_casa[indice], monto)
            cursor.execute(query2, val2)
            client.commit()
            
            #Movimientos
            fecha_actual = datetime.now()
            fecha_actual = fecha_actual.strftime('%d/%B/%Y %H:%M:%S')
            fecha_actual
            query = ("insert into Movimientos values(%s, %s, %s, %s)")
            value = (cuenta_origen, fecha_actual, -monto, 0)
            cursor.execute(query, value)
            client.commit()
            
            monto_anterior = result_set[0][4]
            monto_nuevo = monto_anterior - monto
            sql = ("UPDATE Tarjetas SET Saldo = %s where No_tarjeta= %s;")
            val = (monto_nuevo, cuenta_origen)
            cursor.execute(sql, val)
            client.commit()
        else:
            print("Saldo insuficiente para pagar.")
    else:
        print("Homoclave invalida.")
        
#Retirar 

def retirar(monto, Homoclave):
    query = ("select * from tarjetas where No_tarjeta = '%s';"%Homoclave)
    cursor.execute(query)
    result_set = cursor.fetchall()
    
    if ((len(result_set) == 1)):
        if(monto < result_set[0][4]):
            if(result_set[0][3] == 'C'):
                if(monto*1.15 < result_set[0][4]):
                    monto_anterior = result_set[0][4]
                    monto_nuevo = monto_anterior - (monto*1.15)
                    print(monto_nuevo)
                    sql = ("UPDATE Tarjetas SET Saldo = %s where No_tarjeta= %s;")
                    val = (monto_nuevo, Homoclave)
                    cursor.execute(sql, val)
                    client.commit()
                    #Movimientos
                    fecha_actual = datetime.now()
                    fecha_actual = fecha_actual.strftime('%d/%B/%Y %H:%M:%S')
                    fecha_actual
                    query = ("insert into Movimientos values(%s, %s, %s, %s)")
                    value = (Homoclave, fecha_actual, -monto, monto*0.15)
                    cursor.execute(query, value)
                    client.commit()
                else:
                    print("No tienes tanto crédito para retirar.")
            else: #HECHO
                monto_anterior = result_set[0][4]
                monto_nuevo = monto_anterior - monto
                print(monto_nuevo)
                sql = ("UPDATE Tarjetas SET Saldo = %s where No_tarjeta= %s;")
                val = (monto_nuevo, Homoclave)
                cursor.execute(sql, val)
                client.commit()
                #Movimientos
                fecha_actual = datetime.now()
                fecha_actual = fecha_actual.strftime('%d/%B/%Y %H:%M:%S')
                fecha_actual
                query = ("insert into Movimientos values(%s, %s, %s, %s)")
                value = (Homoclave, fecha_actual, -monto, 0)
                cursor.execute(query, value)
                client.commit()

        else:
            print("No tienes esa cantidad para retirar.")
    else:
        print("Tas loco mi pana.")
        
#Desbloquear
def desbloquear(cuenta):
    query = ("select * from tarjetas where No_tarjeta = '%s';"%cuenta)
    cursor.execute(query)
    result_set = cursor.fetchall()
    if(result_set):
        if(result_set[0][5] == 'B'):
            sql = ("UPDATE Tarjetas SET Estado = %s where No_tarjeta= %s;")
            val = ('D', cuenta)
            cursor.execute(sql, val)
            client.commit()
            
#Crear usuarios

def crear(n):
    #Cuenta
    #Nombre
    archivo = open("nombres.txt")
    lista = []
    for i in archivo:
        lista.append(i)
    
    lista_aux = []
    for i in range (len(lista)):
        lista_aux.append(lista[i].replace('\n',''))
    
    archivo.close()
    
    for i in range (n):
        Nombre = random.choice(lista_aux)
        
        #Fecha de nacimiento
        inicio = datetime(1932, 1, 1)
        final = datetime(2004, 11, 13) 
        random_date = inicio + (final - inicio) * random.random()
        nacimiento = random_date

        fecha_nacimiento = nacimiento.strftime("%d/%B/%Y")

        #Número de cliente
        no_client = random.randint(10000000, 99999999)
        num_aleatorio = random.randint(10, 99)
        no_cliente = str(no_client) + str(num_aleatorio)
        no_cliente = int(no_cliente)
        no_cliente

        #Dirrección y correo
        direccion = "N/A"
        correo = Nombre + "@gmail.com"

        #Contratos
        azar = random.randint(1,9)
        if no_cliente%azar == 0:
            contratos = "si"
        else:
            contratos = "N/A"
            
        #Rol
        azar_rol = random.randint(1,7)
        if azar_rol == 5:
            rol = "E"
            
        else:
            rol = "C"

        #Número de celular
        no_celular = random.randint(100000, 999999)
        num_aleatorio = random.randint(10, 99)
        no_cel = '55' + str(no_celular) + str(num_aleatorio)
        no_cel = int(no_cel)
        no_cel

        query = ("insert into Cuenta values(%s, %s, %s, %s, %s, %s, %s, %s)")
        value = (Nombre, fecha_nacimiento, no_cliente, correo, direccion, contratos, rol, no_cel)
        cursor.execute(query, value)
        
        client.commit()
        
        if rol == "E":
            no_clave = random.randint(10000000, 99999999)
            num_aleatorio = random.randint(10, 99)
            clave = str(no_clave) + str(num_aleatorio)
            clave = int(clave)
            clave
            query2 = ("insert into Ejecutivo values(%s, %s, %s)")
            val = (Nombre, no_cliente, clave)
            cursor.execute(query2, val)
            client.commit()
            
        #Tarjetas
        
        tarjetas = random.randint(2,4)
        
        for i in range(tarjetas):
            if tarjetas == 2:
                if i == 0:
                    no_t = random.randint(10000000000000, 99999999999999)
                    num_aleatorio = random.randint(10, 99)
                    no_tarjeta = str(no_t) + str(num_aleatorio)
                    no_tarjeta = int(no_tarjeta)
                    no_tarjeta

                    nip = random.randint(1000, 9999)
                    
                    Tipo_tarjeta = 'D'
                    
                    saldo = random.randint(0,5000)
                    
                    estado = 'D'
                    
                    query = ("insert into Tarjetas values(%s, %s, %s, %s, %s, %s)")
                    val = (no_cliente, no_tarjeta, nip, Tipo_tarjeta, saldo, estado)
                    cursor.execute(query, val)
                    client.commit()
                
                else:
                    no_t = random.randint(10000000000000, 99999999999999)
                    num_aleatorio = random.randint(10, 99)
                    no_tarjeta = str(no_t) + str(num_aleatorio)
                    no_tarjeta = int(no_tarjeta)
                    no_tarjeta

                    nip = random.randint(1000, 9999)
                    Tipo_tarjeta = 'C'
                    
                    saldo = 10000
                    
                    estado = 'D'
                    
                    query = ("insert into Tarjetas values(%s, %s, %s, %s, %s, %s)")
                    val = (no_cliente, no_tarjeta, nip, Tipo_tarjeta, saldo, estado)
                    cursor.execute(query, val)
                    client.commit()
                    
            elif(tarjetas>2 and i%2==0):
                no_t = random.randint(10000000000000, 99999999999999)
                num_aleatorio = random.randint(10, 99)
                no_tarjeta = str(no_t) + str(num_aleatorio)
                no_tarjeta = int(no_tarjeta)
                no_tarjeta

                nip = random.randint(1000, 9999)
                    
                Tipo_tarjeta = 'D'
                
                saldo = random.randint(0,5000)
                estado = 'D'
                    
                query = ("insert into Tarjetas values(%s, %s, %s, %s, %s, %s)")
                val = (no_cliente, no_tarjeta, nip, Tipo_tarjeta, saldo, estado)
                cursor.execute(query, val)
                client.commit()
                
            elif(tarjetas>2 and i%2!=0):
                no_t = random.randint(10000000000000, 99999999999999)
                num_aleatorio = random.randint(10, 99)
                no_tarjeta = str(no_t) + str(num_aleatorio)
                no_tarjeta = int(no_tarjeta)
                no_tarjeta
                
                nip = random.randint(1000, 9999)
                Tipo_tarjeta = 'C'
                
                saldo = 10000
                
                estado = 'D'
                    
                query = ("insert into Tarjetas values(%s, %s, %s, %s, %s, %s)")
                val = (no_cliente, no_tarjeta, nip, Tipo_tarjeta, saldo, estado)
                cursor.execute(query, val)
                client.commit()
            
            #Contratos
            if contratos == "si":
                servicios = ["Netflix", "HBO", "Spotify", "Amazon"]
                monto_servicios = [120, 150, 99, 119]
                homoclave_servicios = [1000000000000001, 1000000000000002, 1000000000000003, 1000000000000004]
                no1 = random.randint(1,4)
                
                for i in range(no1):
                    no2 = random.randint(0,3)
                    query = ("select * from suscripciones where No_tarjeta = %s and Nombre_sus = %s;")
                    values1 = (no_tarjeta, servicios[no2])
                    cursor.execute(query, values1)
                    result_set = cursor.fetchall()
                    
                    while(result_set):
                        no2 = random.randint(0,3)
                        query = ("select * from suscripciones where No_tarjeta = %s and Nombre_sus = %s;")
                        values1 = (no_tarjeta, servicios[no2])
                        cursor.execute(query, values1)
                        result_set = cursor.fetchall()
                    
                    query = ("insert into Suscripciones values(%s, %s, %s, %s)")
                    val = (no_tarjeta, monto_servicios[no2], homoclave_servicios[no2], servicios[no2])
                    cursor.execute(query, val)
                    client.commit()
            
        #Recargas
        company = ["Telcel", "Movistar", "AT&T"]
        ind = random.randint(0,2)
        saldo = random.randint(0, 200)
        query = ("insert into recargas values(%s, %s, %s)")
        val = (no_cel, company[ind], saldo)
        cursor.execute(query, val)
        client.commit()
            
#Suscripciones
def suscripciones(cuenta_origen):
    query = ("select * from tarjetas where No_tarjeta = '%s';"%cuenta_origen)
    cursor.execute(query)
    result_set = cursor.fetchall()
    
    query2 = ("select * from cuenta where No_cliente = '%s';"%result_set[0][0])
    cursor.execute(query2)
    result_set2 = cursor.fetchall()
    
    if(result_set2[0][5] == "si"):
        
        query3 = ("select * from suscripciones where No_tarjeta = '%s';"%cuenta_origen)
        cursor.execute(query3)
        result_set3 = cursor.fetchall()
        
        print("Tus suscripciones son: ")
        for i in range(len(result_set3)):
            print(i,". Suscripción ", result_set3[i][3], "debes ", result_set3[i][1])
            
        opcion = input("Selecciona cuál vas a pagar: ")
        servicios = ["Netflix", "HBO", "Spotify", "Amazon"]
        monto_servicios = [120, 150, 99, 119]
        homoclave_servicios = [1000000000000001, 1000000000000002, 1000000000000003, 1000000000000004]
        indice1 = servicios.index(opcion)


        if(opcion in servicios):
            if(monto_servicios[indice1]<result_set[0][4]):
                #Movimientos
                fecha_actual = datetime.now()
                fecha_actual = fecha_actual.strftime('%d/%B/%Y %H:%M:%S')
                fecha_actual
                query = ("insert into Movimientos values(%s, %s, %s, %s)")
                value = (cuenta_origen, fecha_actual, -monto_servicios[indice1], 0)
                cursor.execute(query, value)
                client.commit()
                
                monto_anterior = result_set[0][4]
                monto_nuevo = monto_anterior - monto_servicios[indice1]
                sql = ("UPDATE Tarjetas SET Saldo = %s where No_tarjeta= %s;")
                val = (monto_nuevo, cuenta_origen)
                cursor.execute(sql, val)
                client.commit()
            else:
                print("Saldo insuficiente para pagar.")
        else:
            print("Suscripción invalida.")
            
# menu 


cursor = client.cursor()
x = True
cont = 0
z = False
while (x):
    Usuario = input("Ingrese su tarjeta: ")
    Nip = int(input("Ingrese su nip: "))
    
    query = ("select * from tarjetas where No_tarjeta = '%s';"%Usuario)
    cursor.execute(query)
    result_set = cursor.fetchall()
    if(result_set):
        if(result_set[0][5]!='B'):
            query1 = ("select * from tarjetas where No_tarjeta = %s and Nip = %s")
            vals1 = (Usuario, Nip)
            cursor.execute(query1, vals1)
            result_set1 = cursor.fetchall()
            if(result_set1):
                query2 = ("select * from Cuenta where No_cliente = '%s';"%result_set1[0][0])
                cursor.execute(query2)
                result_set2 = cursor.fetchall()
                if(result_set2[0][6] == 'C'):
                    while (z == False):
                        print("Bienvenido")
                        print("1. Transferencias")
                        print("2. Pagar servicios")
                        print("3. Pagar suscripciones")
                        print("4. Recarga a celular")
                        print("5. Consultar saldo")
                        print("6. Ver movimientos")
                        print("7. Retirar dinero")
                        print("8. Salir")

                        opcion = int(input("Elige una opcion: "))
                        while(opcion < 1 or opcion > 8):
                            opcion = int(input("Elige una opcion: "))
                            
                        if(opcion == 5):
                            consulta(Usuario)
                            
                        if (opcion == 1): 
                            cuenta_destino = int(input("Ingrese la cuenta a transferir: "))
                            monto = int(input("Ingrese el monto a transferir: "))
                            transferencia(monto, cuenta_destino, Usuario)
                            
                        if (opcion == 2):
                            homoclave_casa = [2000000000000001, 2000000000000002, 2000000000000003, 2000000000000004]
                            print("1. CFE- ", homoclave_casa[0])
                            print("2. CONAGUA- ", homoclave_casa[1])
                            print("3. IZZI- ", homoclave_casa[2])
                            print("4. INFINITUM- ", homoclave_casa[3])
                            opcion1 = int(input("Ingresa la opción: "))
                            monto = int(input("Ingresa el monto: "))
                            
                            servicios(monto, homoclave_casa[opcion1-1], Usuario)
                            
                        if(opcion == 3):
                            suscripciones(Usuario)
                            
                        if(opcion == 4):
                            monto = int(input("¿Cuánto desea recargar a su celular? "))
                            recargas(Usuario, result_set2[0][7], monto)
                            
                        if(opcion == 6):
                            Movimientos(Usuario)
                            
                        if(opcion == 7):
                            monto = int(input("¿Cuánto desea retirar? "))
                            retirar(monto, Usuario)
                            
                        if(opcion == 8):
                            x = False
                            z = True
                            
                elif(result_set2[0][6] == 'E'):
                    while (z == False):
                        print("Bienvenido")
                        print("1. Transferencias")
                        print("2. Pagar servicios")
                        print("3. Pagar suscripciones")
                        print("4. Recarga a celular")
                        print("5. Consultar saldo")
                        print("6. Desbloquear Cuentas")
                        print("7. Ver movimientos")
                        print("8. Retirar dinero")
                        print("9. Salir")
                        opcion = int(input("Elige una opcion: "))
                        while(opcion < 1 or opcion > 9):
                            opcion = int(input("Elige una opcion: "))
                            
                            
                        if (opcion == 1): 
                                cuenta_destino = int(input("Ingrese la cuenta a transferir: "))
                                monto = int(input("Ingrese el monto a transferir: "))
                                transferencia(monto, cuenta_destino, Usuario)
                                
                        if (opcion == 2):
                            homoclave_casa = [2000000000000001, 2000000000000002, 2000000000000003, 2000000000000004]
                            print("1. CFE- ", homoclave_casa[0])
                            print("2. CONAGUA- ", homoclave_casa[1])
                            print("3. IZZI- ", homoclave_casa[2])
                            print("4. INFINITUM- ", homoclave_casa[3])
                            opcion1 = int(input("Ingresa la opción: "))
                            monto = int(input("Ingresa el monto: "))
                            
                            servicios(monto, homoclave_casa[opcion1-1], Usuario)
                            
                        if(opcion == 3):
                            suscripciones(Usuario)
                            
                        if(opcion == 4):
                            monto = int(input("¿Cuánto desea recargar a su celular? "))
                            recargas(Usuario, result_set2[0][7], monto)
                            
                        if(opcion == 5):
                            consulta(Usuario)
                            
                        if(opcion == 6):
                            Cuenta_des = int(input("Ingrese la cuenta a desbloquear: "))
                            desbloquear(Cuenta_des)
                            
                            
                        if(opcion == 7):
                            Movimientos(Usuario)
                            
                        if(opcion == 8):
                            monto = int(input("¿Cuánto desea retirar? "))
                            retirar(monto, Usuario)
                            
                        if(opcion == 9):
                            x = False
                            z = True
            else:
                cont = cont+1

            if cont == 3: 
                sql = ("UPDATE Tarjetas SET Estado = %s where No_tarjeta= %s;")
                val = ('B', Usuario)
                cursor.execute(sql, val)
                client.commit()
                x = False
                break
        else:
            print("Tarjeta Bloqueada")
            x = False
    else:
        print("Usuario invalido")
        x = False
        


        
        

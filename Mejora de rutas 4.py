#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:33:11 2023

@author: isaacchaljub
"""


# Primera parte, se encarga de leer el consolidado de pedidos y organizarlo
# según el pedido y sus posiciones asociadas

import pandas as pd
import numpy as np
import time
import random as rd
import re

pedidos=pd.read_excel('PLANTILLA PEDIDOS1.xlsx', sheet_name='PEDIDOS', header=0)
pedidos.drop_duplicates( keep='first', inplace=True, ignore_index=True)
pedidos=pedidos.iloc[:-1 , :]
tiempos=pd.read_excel('Tiempos_Desplazamiento_CEDI_Reales.xlsx', header=0)
tiempos=tiempos.set_index('Vacio')

pedidos=pedidos.drop('OBS',axis=1)

ref=pd.DataFrame(pedidos['pedido'])
ub=pd.DataFrame(pedidos['UBICACIÓN'])

peds=pd.concat([ref,ub], axis=1)

peds=peds.astype(str)

prueba=peds.groupby('pedido')['UBICACIÓN'].agg(','.join)
ind=pd.DataFrame(prueba.index)


lista_sin_separar=[]
for i in range(len(prueba)):
    lista_sin_separar.append(prueba[i])
    
lista_arreglada=[]
for line in lista_sin_separar:
    line=line.split(',')
    lista_arreglada.append(line)

lista_arreglada[0][0][0:-1]
pos=[i for i in tiempos]

def limpiar_lista(lista):
    
    aux=[]
    lst=lista.copy()
    for i in range(len(lista)):
        if lista[i][0:-1] not in pos:
            aux.append(lista[i])
            lst.remove(lista[i])
    lista=lst
    return aux, lista

# limpiar_lista(lista_arreglada[0])


sobrantes=[]
for i in range(len(lista_arreglada)):
    aux=limpiar_lista(lista_arreglada[i])
    sobrantes.append(aux[0])
    lista_arreglada[i]=aux[1]
    
    
    
######################################################################################3

# Segunda parte, emplea el GRASP para encontrar posibles mejores configuraciones


ordenes=lista_arreglada

################################################################
####################### FASE CONSTRUCTIVA ######################
################################################################


def sorted_nicely(l): #Organiza la lista por letra y número
    """ Sorts the given iterable in the way that is expected.
 
    Required arguments:
    l -- The iterable to be sorted.
 
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    comp=('Iteration %s of %d'%(iteration, total))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix} {comp}', end = printEnd)
    # print('\nIteración {0} de {1}'.format(iteration, total), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()



def funcion_costos(pedido):
    """ 
    Calcula el tiempo de ruta basado en el orden de las posiciones en el pedido pasado

    Parameters
    ----------
    ruta : list
        La ruta o el pedido para el cual se calculará el tiempo de ciclo.

    Returns
    -------
    t : int
        Tiempo de ruta.

    """
    
    t=tiempos.at['A01',pedido[0][0:-1]]
    for i in range(len(pedido)-1):
        rec=tiempos.at[pedido[i][0:-1],pedido[i+1][0:-1]]
        t=t+rec
    
    return t

ordenes=[sorted_nicely(i) for i in ordenes]


def agregar_posicion(faltantes:list, base, alpha): #Basado en valor con alpha
    """
    Se realiza la evaluación de la función de costos o incremental, y se retornan las 
    configuraciones que pasan el criterio de aceptación (RCL)
    
    Parámetros
    ---------
    
    faltantes: Lista de posiciones que aún no han sido seleccionadas
    base: Lista o ruta con las posiciones ya seleccionadas
    alpha: Parámetro de aceptación para las soluciones
    
    Returns
    -------
    RCL : list
        La lista de candidatos restringidos.

    """    
    
    res=[]
    
    # if len(base)==0:
    #     base=['A01A']
    
    for i in faltantes:
        r=[j for j in base]
        r.append(i)
        t=funcion_costos(r)
        res.append([r,t])
    
    res.sort(key=lambda x:x[1])
    RCL=[]
    for i in res:
        if i[1]<=res[0][1]+alpha*(res[-1][1]-res[0][1]):
            RCL.append(i)
    
    return RCL
        



def fase_constructiva(ruta, alpha):
    """
    Realiza la fase constructiva del GRASP, usando la función constr y seleccionando un 
    candidatos de la RCL al azar.

    Parameters
    ----------
    ruta : Lista con la ruta original o pedido a trabajar
    
    Returns
    -------
    ini : list
        La ruta inicial a ser pasada a la fase de optimización.
    
    """
   
    faltantes=ruta.copy()
    ini=[]
    
    while len(faltantes)>0:
        if len(faltantes)>1:
            res=agregar_posicion(faltantes, ini, alpha)
            
            aux=rd.choice(res)
            ini=aux[0]
            faltantes.remove(ini[-1])
        else:
            ini.append(faltantes[0])
            faltantes.remove(ini[-1])
    
    return ini


################################################################
####################### BÚSQUEDA LOCAL #########################
################################################################


def busq_unit(ruta):
    """
    Se hace la búsqueda del primer cambio de posición de dos nodos de la ruta que genere
    una mejora en la función objetivo y se retorna esta nueva configuración hallada.

    Parameters
    ----------
    ruta : list
        la ruta a la que se le quiere encontrar una mejor configuración.

    Returns
    -------
    orden : list
        la ruta modificada para la cual se halló una mejor función de utilidad.

    """
    
    orden=ruta.copy()
    
    for i in range(len(orden)-1):
        for j in range(i+1,len(orden)):
            sol=orden.copy()
            sol[i], sol[j]=sol[j], sol[i]
            if funcion_costos(sol)<funcion_costos(orden):
                orden=sol
                break
            break
    
    return orden
  

def busq_loc(pedido):
    """
    Realiza la búsqueda local para el pedido pasada como input, llamando la función de búsqueda
    unitaria busq_unit hasta que no se encuentre una configuración que logre una mejora en la
    función de costos

    Parameters
    ----------
    pedido : list
        El pedido al que se le aplicará la búsqueda local.

    Returns
    -------
    list[ruta, res]
        Retorna la nueva ruta que se encontró para el pedido junto con su función de utilidad.

    """
    
    ruta=pedido.copy()
    res=funcion_costos(ruta)
    
    while funcion_costos(busq_unit(ruta))<res:
        ruta=busq_unit(ruta)
        res=funcion_costos(ruta)
        
    return [ruta, res]


def grasp(pedido, alpha):
    """
    Aplica la función de fase constructiva y luego de fase de optimización para dar como
    resultado una nueva ruta o configuración para el pedido entregado como input

    Parameters
    ----------
    pedido : list
        El pedido o la orden para el que se quiere encontrar una mejor ruta.

    Returns
    -------
    ruta_mejorada : list
        Regresa la mejor configuración encontrada para el pedido pasado como parámetro.

    """
    
    # pedido=sorted_nicely(pedido)
    base_inicio=fase_constructiva(pedido, alpha)
    ruta_mejorada=busq_loc(base_inicio)
    
    return ruta_mejorada


def mejora(pedidos, arranques, alpha):
    """
    Aplica el grasp para cada uno de los pedidos pasados y con la cantidad de arranques
    indicados, seleccionando para cada pedido la configuración que entregue el mejor
    resultado, y regresando una lista con la nueva ruta para cada pedido, así como indicando
    el tiempo de proceso gastado, el ahorro en valor y porcentual en costos por aplicar el 
    GRASP a los pedidos, y los costos originales y modificados totales de los pedidos

    Parameters
    ----------
    pedidos : list of lists
        lista con todos los pedidos a los que se aplicará el GRASP.
    arranques : int
        la cantidad de arranques que se hará para cada pedido.

    Returns
    -------
    rutas_mejoradas : list of lists
        Lista con las nuevas configuraciones de ruta para cada pedido.

    """
    
    rutas_mejoradas=[]
    savings=0
    tiempo_original=0
    start=time.time()
    printProgressBar(0, len(pedidos), prefix = 'Progress:', suffix = 'Complete', length = 50, decimals=3)
    cont=0
    for ped in pedidos:
        
        if len(ped)==0:
            rutas_mejoradas.append(ped)
            cont+=1
            continue
        
        for i in range(arranques):
            
            mejor=grasp(ped, alpha)
            
            if i==0:
                sol=mejor
            elif mejor[1]<sol[1]:
                sol=mejor
            
        tiempo_inicial=funcion_costos(sorted_nicely(ped))
        tiempo_original=tiempo_original+tiempo_inicial
        savings=savings+(tiempo_inicial-sol[1])
        rutas_mejoradas.append(sol[0])
        cont+=1
        printProgressBar(cont, len(pedidos),prefix = 'Progress:', suffix = 'Complete', length = 50, decimals=3)
        
        
        
    end=time.time()
    print('\nEl tiempo de corrida es de', np.round(end-start,2),'segundos o',np.round((end-start)/60,2), 'minutos.' )
    print('\nEl ahorro de tiempo es de',np.round(savings/3600,2), 'horas, lo que corresponde a una reducción del',np.round((((savings)/tiempo_original)*100),1),'%')
    print('\nEl tiempo final de proceso es de', np.round((tiempo_original-savings)/3600,2), 'horas, mientras que el inicial es de', np.round(tiempo_original/3600,2),'horas')
    return rutas_mejoradas

respuesta=mejora(ordenes, 20, 0.15)

    
# pr=ordenes[0:100]
# resp_pr=mejora(pr,5)



# funcion_costos(['A1A', rut[0]])+


############## Consolidación de rutas ###################



copia=respuesta.copy()

nuevo_paso=[]
i=0
while len(copia)>0:

    if len(copia)>3:
        
        if len(copia[i])+len(copia[i+1])+len(copia[i+2])+len(copia[i+3])<=15:
            nuevo_paso.append(copia[i]+copia[i+1]+copia[i+2]+copia[i+3])
            copia.remove(copia[i+3])
            copia.remove(copia[i+2])
            copia.remove(copia[i+1])
            copia.remove(copia[i])
        
        elif len(copia[i])+len(copia[i+1])+len(copia[i+2])<=15:
            nuevo_paso.append(copia[i]+copia[i+1]+copia[i+2])
            copia.remove(copia[i+2])
            copia.remove(copia[i+1])
            copia.remove(copia[i])
            
        elif len(copia[i])+len(copia[i+1])<=15:
            nuevo_paso.append(copia[i]+copia[i+1])
            copia.remove(copia[i+1])
            copia.remove(copia[i])
        else:
            nuevo_paso.append(respuesta[i])
            copia.remove(copia[i])
    else:
        nuevo_paso.append(respuesta[i])
        copia.remove(copia[i])
    

pr=mejora(nuevo_paso, 1, 0.15)

def tiempo_tot(pedidos):
    t=0
    for i in pedidos:
        t=t+funcion_costos(i)
    return np.round(t/3600, decimals=2)

# tiempo_tot(respuesta)
# tiempo_tot(pr)


# r1=mejora(ordenes, 5, 0.15)
# r2=mejora(ordenes, 10, 0.15)
# r3=mejora(ordenes, 15, 0.15)
r4=mejora(ordenes, 20, 0.15)

# r5=mejora(nuevo_paso, 5, 0.15)
# r6=mejora(nuevo_paso, 10, 0.15)
# r7=mejora(nuevo_paso, 15, 0.15)
r8=mejora(nuevo_paso, 20, 0.15)

tiempo_tot(r4)
tiempo_tot(r8)






















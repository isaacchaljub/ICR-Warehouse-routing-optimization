# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 15:44:10 2023

@author: isaac
"""

import pandas as pd
import xlsxwriter as xl
import time


tiempos=pd.read_excel('tiempos_extendidos_reales2.xlsx', header=0)
tiempos=tiempos.set_index('Vacio')

# print(tiempos.iat[2,1])

# tiempos.iat[1,3]

# tiempos.iat[0,2]==tiempos.iat[2,0]

# tiempos.iat[1,2]-tiempos.iat[2,1]

# tiempos.iat[2,2]=tiempos.iat[1,2]-tiempos.iat[2,1]

for i in range(len(tiempos)-2):
    for j in range(len(tiempos)-2):
        if tiempos.iat[0,i+2]==tiempos.iat[j+2,0]: #Revisa si es la misma fila
            tiempos.iat[i+2,j+2]=abs(tiempos.iat[1,i+2]-tiempos.iat[j+2,1])*2
            
        elif (tiempos.iat[0,i+2]=='A' and tiempos.iat[j+2,0]=='B') or (tiempos.iat[0,i+2]=='B' and tiempos.iat[j+2,0]=='A') or (tiempos.iat[0,i+2]=='C' and tiempos.iat[j+2,0]=='E') or (tiempos.iat[0,i+2]=='E' and tiempos.iat[j+2,0]=='C') or (tiempos.iat[0,i+2]=='F' and tiempos.iat[j+2,0]=='D') or (tiempos.iat[0,i+2]=='D' and tiempos.iat[j+2,0]=='F'): #Revisa entre filas que se enfrenten (A y B, C y E, D y F)
            tiempos.iat[i+2,j+2]=abs(tiempos.iat[1,i+2]-tiempos.iat[j+2,1])*2+4
            
        elif (tiempos.iat[1,i+2]<=33 and tiempos.iat[j+2,1]>=33) or (tiempos.iat[1,i+2]>=33 and tiempos.iat[j+2,1]<=33): #Revisa si son de las primeras 33 a las últimas (33-64) o viceversa
            if (tiempos.iat[0,i+2]=='A' and tiempos.iat[j+2,0]=='C') or (tiempos.iat[0,i+2]=='B' and tiempos.iat[j+2,0]=='E') or (tiempos.iat[0,i+2]=='C' and tiempos.iat[j+2,0]=='A') or (tiempos.iat[0,i+2]=='E' and tiempos.iat[j+2,0]=='B'): #Revisa si son de la A a la C, la B a la E y viceversa
                tiempos.iat[i+2,j+2]=abs(tiempos.iat[1,i+2]-tiempos.iat[j+2,1])*2+8
            
            elif (tiempos.iat[0,i+2]=='A' and tiempos.iat[j+2,0]=='E') or (tiempos.iat[0,i+2]=='E' and tiempos.iat[j+2,0]=='A'): #Revisa si son de la A a la E
                tiempos.iat[i+2,j+2]=abs(tiempos.iat[1,i+2]-tiempos.iat[j+2,1])*2+12
             
            elif (tiempos.iat[0,i+2]=='B' and tiempos.iat[j+2,0]=='C') or (tiempos.iat[0,i+2]=='C' and tiempos.iat[j+2,0]=='B'): #Revisa si son de la B a la C
                 tiempos.iat[i+2,j+2]=abs(tiempos.iat[1,i+2]-tiempos.iat[j+2,1])*2+4
                 
             
        elif (tiempos.iat[1,i+2]<=33 and tiempos.iat[j+2,1]<=33) or (tiempos.iat[1,i+2]>=33 and tiempos.iat[j+2,1]>=33): #Revisa si son de las primeras 33 a las primeras 33 o las últimas 31 a las últimas 31
            if (tiempos.iat[0,i+2]=='A' and tiempos.iat[j+2,0]=='C') or (tiempos.iat[0,i+2]=='B' and tiempos.iat[j+2,0]=='E') or (tiempos.iat[0,i+2]=='C' and tiempos.iat[j+2,0]=='A') or (tiempos.iat[0,i+2]=='E' and tiempos.iat[j+2,0]=='B'): #Revisa si son de la A a la C, la B a la E y viceversa
                m=min(abs(tiempos.iat[1,i+2]-1)+abs(tiempos.iat[j+2,1]-1),abs(tiempos.iat[1,i+2]-31)+abs(tiempos.iat[j+2,1]-31), abs(tiempos.iat[1,i+2]-33)+abs(tiempos.iat[j+2,1]-33))
                tiempos.iat[i+2,j+2]=2*m+8
                
            elif (tiempos.iat[0,i+2]=='A' and tiempos.iat[j+2,0]=='E') or (tiempos.iat[0,i+2]=='E' and tiempos.iat[j+2,0]=='A'): #Revisa si son de la A a la E y viceversa
                m=min(abs(tiempos.iat[1,i+2]-1)+abs(tiempos.iat[j+2,1]-1),abs(tiempos.iat[1,i+2]-31)+abs(tiempos.iat[j+2,1]-31), abs(tiempos.iat[1,i+2]-33)+abs(tiempos.iat[j+2,1]-33))
                tiempos.iat[i+2,j+2]=2*m+12
            
            elif (tiempos.iat[0,i+2]=='B' and tiempos.iat[j+2,0]=='C') or (tiempos.iat[0,i+2]=='C' and tiempos.iat[j+2,0]=='B'): #Revisa si son de la B a la C y viceversa
                m=min(abs(tiempos.iat[1,i+2]-1)+abs(tiempos.iat[j+2,1]-1),abs(tiempos.iat[1,i+2]-31)+abs(tiempos.iat[j+2,1]-31), abs(tiempos.iat[1,i+2]-33)+abs(tiempos.iat[j+2,1]-33))
                tiempos.iat[i+2,j+2]=2*m+4
    
tiempos.drop(labels=['Vacio.1', 'Vacio.2'], axis=1, inplace=True)
tiempos.drop(labels=['Vacio'], axis=0, inplace=True)

writer=pd.ExcelWriter('Tiempos_Desplazamiento_Extendidos_Reales.xlsx', engine='xlsxwriter')

tiempos.to_excel(writer, sheet_name='Tiempos')

writer.save()
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 12:13:08 2020

@author: elosasso
"""

from planilla import Preferencias, Planilla
from datetime import datetime
import random


def asignar_greedy(prefs):
    
    sol = Planilla(prefs)
    
    for student in sol.estudiantes_sin_topico():
                
        for topic in prefs.preferencias_del_estudiante(student):
    
            if sol.topico_libre(topic) and sol.estudiante_libre(student):                
                sol.asignar(student, topic)
    return sol


def find_students_topics_to_change(solution, prefs):
    # Esta funcion genera una lista de estudiantes y topicos que iran intercambiando
    # topicos con el fin de buscar una vecindad que mejore el costo de la función
    # dado por la primera solucion
    
    # Creo dos listas: una para los estudiantes y otra para los topicos
    students_to_change = []
    topics_to_change = []
    
    # Recorro todos los estudiantes con un topico asignado
    # En realidad estoy recorriendo todos los estudiantes porque luego de la primera 
    # solucion todos tienen algun topico asignado
    for student in solution.estudiantes_con_topico():
        
        # Encuentro el topico asignado al estudiante 'student'
        assigned_topic = solution.topico_asignado_a_estudiante(student)
        # Determino el ranking que le corresponde a ese topico para el estudiante 'student'
        ranking = prefs.ranking_de_topico_para_estudiante(assigned_topic, student)
        
        # Como vecindad definimos todas aquellas alternativas que surgen de intercambiar
        # topicos entre estudiantes que se les asigno un topico que no era su "preferido"
        # Por este motivo, colocamos un condicional para que separe aquellos estudiantes que no
        # intercambiarán topicos de aquellos que si. Si el ranking del topico no es 0, entonces 
        # es un estudiante que se le intercambiara el topico
        if ranking != 0:
            
            students_to_change.append(student)
            topics_to_change.append(assigned_topic)
    
    return students_to_change, topics_to_change


# Cargo un ejemplo de preferencias.
prefs = Preferencias("Ejemplo10")

# Determino una primera solucion con la heurísitica 'greedy'
solucion_actual = asignar_greedy(prefs)

# Calculo el costo de la primera solucion
costo_solucion_actual = solucion_actual.calcular_costo()

# Determino los estudiantes y topicos que voy a intercambiar
students_to_change, topics_to_change = find_students_topics_to_change(solucion_actual, prefs)

pudimos_mejorar = True

while pudimos_mejorar:

    costo_mejor_vecino = float('inf')
    mejor_vecino = None
    
    for student in range(0, len(students_to_change)-1):
        
        for topic in range(student+1,len(topics_to_change)):
            
            vecino = solucion_actual.copy()
            
            # Encuentro el topico asignado al estudiante 'e'
            # assigned_topic es EL topico, no es un indice
            assigned_topic = vecino.topico_asignado_a_estudiante(students_to_change[student])
            
            # Desasigno el topico correspondiente al estudiante 'e'
            vecino.desasignar(students_to_change[student], assigned_topic) 
            
            # Encuentro el estudiante asignado al 'topic'
            # assigned_student es EL student, no es un indice 
            assigned_student = vecino.estudiante_asignado_a_topico(topics_to_change[topic])
            
            # Desasigno el topico 'topic' del estudiante correspondiente
            vecino.desasignar(assigned_student, topics_to_change[topic])
            
            # Intercambio los topicos entre el 'student' y el 'assigned_student'
            # Asigno al student
            vecino.asignar(students_to_change[student], topics_to_change[topic])
            # Asigno al assigned_student
            vecino.asignar(assigned_student, assigned_topic)
            
            # Calculo el costo de la nueva asignacion
            costo = vecino.calcular_costo()
            
            if costo < costo_mejor_vecino:
                costo_mejor_vecino = costo
                mejor_vecino = vecino
            
    # Si el mejor vecino encontrado es mejor que la solución actual,
    # lo guardamos y seguimos buscando. Si no, terminamos.
    
    if costo_mejor_vecino < costo_solucion_actual:
        print('Costo solucion actual: ', costo_solucion_actual)
        print('Costo mejor vecino: ', costo_mejor_vecino)
        pudimos_mejorar = True
        solucion_actual = mejor_vecino
        costo_solucion_actual = costo_mejor_vecino
        # Vuelvo a encontrar los estudiantes que intercambiaran topicos
        students_to_change, topics_to_change = find_students_topics_to_change(solucion_actual, prefs)
    else:
        pudimos_mejorar = False
        
   
lista1 = [1,2,3]
lista2 = [4,5,6]

for i in range(0, len(lista1)-1):
    for j in range(i+1, len(lista2)):
        print('Student: ',lista1[i]) 
        print('Topic to remove: ', lista2[i])
        print('Topic to assign: ', lista2[j])         
        
        
    
    
    
    
        
        
        
    

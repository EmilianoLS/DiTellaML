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
prefs = Preferencias("Ejemplo3")
sol = Planilla(prefs)

def asignar_backtracking(sol):

    best_assignment = None
    costo = float('inf')  # infinito
    # Caso base: No queda ningun estudiante desasignado

    if len(sol.estudiantes_sin_topico()) == 0:

        #print('No more students left')
        best_assignment = sol.copy()
        costo = best_assignment.calcular_costo()

    else:
        # Todavia estan quedando estudiantes sin nigun topico asignado

        #print('There are still some students missing!')
        for student in sol.estudiantes_sin_topico().copy():
            print('Student: ', student)
            for topic in sol.topicos_sin_estudiante().copy():
                print('Topic: ', topic)
                sol.asignar(student, topic)
                print('Estudiante ', student, 'asignado al topico ')
                solucion_temp = asignar_backtracking(sol)
                costo_temp = solucion_temp.calcular_costo()

                # Si esta asignacion es la que menor costo reporta, la guardamos

                if costo_temp < costo:
                   
                   best_assignment = solucion_temp
                   costo = costo_temp 
                
                # Paso para atras 

                sol.desasignar(student, topic)
    
    return best_assignment


solucion = asignar_backtracking(sol)
print('La mejor solucion es: ',solucion)
print('El costo de la mejor solucion: ', solucion.calcular_costo())

                








    
    
    
    
        
        
        
    

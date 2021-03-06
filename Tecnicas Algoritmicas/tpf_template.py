from planilla import Preferencias, Planilla
from datetime import datetime
import random

def find_students_topics_to_change(solution, prefs):
    # FUNCION AUXILIAR
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


def asignar_random(prefs):
    sol = Planilla(prefs)
    while len(sol.estudiantes_sin_topico()) > 0:
        e = random.choice(list(sol.estudiantes_sin_topico()))
        t = random.choice(list(sol.topicos_sin_estudiante()))
        sol.asignar(e, t)
    return sol

def asignar_greedy(prefs):
    
    sol = Planilla(prefs)
    #Recorro todos los estudiantes uno a uno
    for student in sol.estudiantes_sin_topico():
      #Recorro las preferencias del estudiante en cuestión por orden
      #de preferencia          
        for topic in prefs.preferencias_del_estudiante(student):
            #Asigno al estudiante el primer tópico desocupado 
            if sol.topico_libre(topic) and sol.estudiante_libre(student):                
                sol.asignar(student, topic)
    return sol

#
def asignar_bl(prefs, solucion_inicial):
    # Calculo el costo de la primera solucion
    costo_solucion_actual = solucion_inicial.calcular_costo()

    # Determino los estudiantes y topicos que voy a intercambiar
    students_to_change, topics_to_change = find_students_topics_to_change(solucion_inicial, prefs)

    pudimos_mejorar = True

    if costo_solucion_actual != 0:
        while pudimos_mejorar:
        
            costo_mejor_vecino = float('inf')
            mejor_vecino = None
            
            for student in range(0, len(students_to_change)-1):
                
                for topic in range(student+1,len(topics_to_change)):
                    
                    vecino = solucion_inicial.copy()
                    
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
                #print('Costo solucion actual: ', costo_solucion_actual)
                #print('Costo mejor vecino: ', costo_mejor_vecino)
                pudimos_mejorar = True
                solucion_inicial = mejor_vecino
                costo_solucion_actual = costo_mejor_vecino
                # Vuelvo a encontrar los estudiantes que intercambiaran topicos
                students_to_change, topics_to_change = find_students_topics_to_change(solucion_inicial, prefs)
            else:
                pudimos_mejorar = False
        
        return solucion_inicial
            
    else:
        return solucion_inicial

def asignar_bli(prefs, iters):

    costo_solucion = float('inf')
    solucion_final = None

    for iteration in range(0, iters):
        #print('Iteration number: ', iteration)
        solucion_actual = asignar_random(prefs)
        solucion_bl = asignar_bl(prefs, solucion_actual)

        if solucion_bl.calcular_costo() < costo_solucion:

            costo_solucion = solucion_bl.calcular_costo()
            solucion_final = solucion_bl

    return solucion_final
#
def asignar_backtracking(prefs):
    
    # Funcion de busqueda por fuerza bruta 
    # Creamos un objeto de tipo Planilla
    sol = Planilla(prefs)
    # Hallamos la solucion llamando una funcion auxiliar
    solucion = asignar_backtracking_aux(sol) 
    
    return solucion

def asignar_backtracking_aux(sol):
    
    best_assignment = None
    costo = float('inf')  # infinito
    # Caso base: No queda ningun estudiante desasignado

    if len(sol.estudiantes_sin_topico()) == 0:

        # Guardo la solucion actual y calculo su costo
        best_assignment = sol.copy()
        costo = best_assignment.calcular_costo()


    else:
        # Todavia estan quedando estudiantes sin nigun topico asignado
        # Para cada estudiante sin topico recorro todos los topicos posibles que no esten asignados
        student = min(sol.estudiantes_sin_topico())

        for topic in sol.topicos_sin_estudiante().copy():
            
            sol.asignar(student, topic)
            
            # Introduzco la recursividad al rellamara la funcion                 
            solucion_temp = asignar_backtracking_aux(sol)
            
            costo_temp = solucion_temp.calcular_costo()

            # Si esta asignacion es la que menor costo reporta, la guardamos

            if costo_temp < costo:
               
               best_assignment = solucion_temp
               costo = costo_temp 
            
            # Paso para atras 

            sol.desasignar(student, topic)
    return best_assignment

#El argumento debe ser el nombre de una secuencia de preferencias
#Por ejemplo "Ejemplo3"
def testing_algoritmos(example):

 results = {}


  # Cargo un ejemplo de preferencias.
 prefs = Preferencias(example)
  # Busco una asignación completa (con un algoritmo aleatorio en este caso),
  # calculando el tiempo de ejecución.

  # Random Algorithm

 comienzo = datetime.now()
 solucion = asignar_random(prefs)
 tiempo_usado = datetime.now() - comienzo
 results[example] = {'Random Algorithm':{'Costo': solucion.calcular_costo(),
                                            'Tiempo usado': tiempo_usado}}

  # Greedy Algorithm

 comienzo = datetime.now()
 solucion = asignar_greedy(prefs)
 tiempo_usado = datetime.now() - comienzo
 results[example].update({'Greedy Algorithm':{'Costo': solucion.calcular_costo(),
                                            'Tiempo usado': tiempo_usado}})

  # Busqueda Local Algorithm

  # Determino una primera solucion con la heurísitica 'greedy'
 comienzo = datetime.now()
 solucion_actual = asignar_greedy(prefs)
 solucion_bl = asignar_bl(prefs, solucion_actual)
 tiempo_usado = datetime.now() - comienzo
 results[example].update({'Bl Algorithm':{'Costo': solucion_bl.calcular_costo(),
                                            'Tiempo usado': tiempo_usado}})

    # Busqueda Local Iterativa Algorithm

 comienzo = datetime.now()
 solucion = asignar_bli(prefs, 50)
 tiempo_usado = datetime.now() - comienzo
 results[example].update({'Bli Algorithm':{'Costo': solucion.calcular_costo(),
                                            'Tiempo usado': tiempo_usado}})
        
 return(results)
  
#Se construye una function similar para backtracking

def testing_back(example):
    
 results = {}

 prefs = Preferencias(example)

 comienzo = datetime.now()
 solucion = asignar_backtracking(prefs)
 tiempo_usado = datetime.now() - comienzo
 results[example] = {'Backtracking Algorithm':{'Costo': solucion.calcular_costo(),
                                            'Tiempo usado': tiempo_usado}}
 
 return(results)

def main():

    examples = ['Ejemplo3', 'Ejemplo5', 'Ejemplo10', 'Ejemplo12', 'Ejemplo15', 'Ejemplo50']

    results = {}
    results_bt = {}

    for example in examples:

        results.update(testing_algoritmos(example))
        results_bt.update(testing_back(example))

    print(results)
    print(results_bt)

if __name__ == '__main__':
    main()
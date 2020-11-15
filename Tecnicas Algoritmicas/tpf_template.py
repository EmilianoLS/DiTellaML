from planilla import Preferencias, Planilla
from datetime import datetime
import random

def asignar_random(prefs):
    sol = Planilla(prefs)
    while len(sol.estudiantes_sin_topico()) > 0:
        e = random.choice(list(sol.estudiantes_sin_topico()))
        t = random.choice(list(sol.topicos_sin_estudiante()))
        sol.asignar(e, t)
    return sol

def asignar_greedy(prefs):
    
    sol = Planilla(prefs)
    
    for student in sol.estudiantes_sin_topico():
                
        for topic in prefs.preferencias_del_estudiante(student):
    
            if sol.topico_libre(topic) and sol.estudiante_libre(student):                
                sol.asignar(student, topic)
    return sol

#
#def asignar_bl(prefs, solucion_inicial):
#   COMPLETAR
#
#def asignar_bli(prefs, iters):
#   COMPLETAR
#
#def asignar_backtracking(prefs):
#   COMPLETAR

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Cargo un ejemplo de preferencias.
prefs = Preferencias("Ejemplo50")

# Busco una asignación completa (con un algoritmo aleatorio en este caso),
# calculando el tiempo de ejecución.
comienzo = datetime.now()
solucion = asignar_greedy(prefs)
tiempo_usado = datetime.now() - comienzo

# Imprimo un resumen de los resultados.
print("Preferencias", prefs)
print("Solución:", solucion)
print("Costo:", solucion.calcular_costo())
print("Tiempo:", tiempo_usado)

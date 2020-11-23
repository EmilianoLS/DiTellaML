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

#####################################################################
#Lo que alimenta esta function es un tipo "preferencias"

def asignar_backtracking(prefs):

#Primero se crea la planilla sobre la que se va a trabajar

  planilla = Planilla(prefs)
  #planilla_buena = asignar_random(prefs)
  
  if planilla.topicos_con_estudiante==prefs._cantidad:
      planilla_buena=planilla    
  else:
      for e in planilla.estudiantes_sin_topico(): 
          for t in planilla.topicos_sin_estudiante():
              #paso adelante
              planilla.asignar(e, t)
              #recursión
              planilla=asignar_backtracking(prefs)
              #guardo el mejor resultado
              if planilla.calcular_costo()<planilla_buena.calcular_costo():
                  planilla_buena=planilla
              #paso atrás
              planilla.desasignar(e, t)
  return(planilla_buena)              
              









# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Cargo un ejemplo de preferencias.
prefs = Preferencias("Ejemplo3")

# Busco una asignación completa (con un algoritmo aleatorio en este caso),
# calculando el tiempo de ejecución.
comienzo = datetime.now()
solucion = asignar_backtracking(prefs)
tiempo_usado = datetime.now() - comienzo

# Imprimo un resumen de los resultados.
print("Preferencias", prefs)
print("Solución:", solucion)
print("Costo:", solucion.calcular_costo())
print("Tiempo:", tiempo_usado)

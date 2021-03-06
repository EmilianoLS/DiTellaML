#!/usr/bin/env python

import csv
import math
import sys


def reduce_function(buffer, totals):
    """
    Reduce part of MapReduce

    :param buffer: list of (key, value) to reduce (here key is formed by the term, category and bucket).
    :param totals: dictionary where the reduced key,values are collected
    :return: nothing
    """
    # TODO aquí deben recorrer los términos, categorías, buckets y valores que hay en el buffer
    #       y por cada uno de ellos actualizar el diccionario totals.
    #       totals es un diccionario donde la clave es cada bucket, y el valor es un diccionario
    #       de categorías a un diccionario de términos y cantidades:
    #       totals[bucket][category][term] está asociado a un número entero

    total_positive = 0
    total_negative = 0
    
    # Primeramente recorro todo el buffer. En la teoria, cada vez que llegue un buffer, va a corresponder a 
    # un mismo termino, y a una misma categoria, lo que va a variar es si esta asociado a un bucket 
    # positivo o negativo
    # Por lo tanto lo que voy a hacer es contar cuantas veces aparece el termino en esta categoria
    # en un bucket y en el otro
    for element in buffer:
        # Primero chequeo el bucket al que pertenece:
            # Si es positivo, entonces incremento el contador del bucket positivo
            # Si es negativo, entonces incremento el contador del bucket negativo
        if element[2] == 'positive':

            total_positive += 1
        
        else:

            total_negative += 1
    
    # Una vez recorrido todo el buffer y ya conté todas las apariciones del term en la categoria
    # entonces puedo extraer la categoria y el term para poder actualizar el diccionario
    category = buffer[0][1]
    term = buffer[0][0]
    # Para actualizar el diccionario, es importante entender:
    #   1)  Si el diccionario esta vacio (caso del primer loop del for que llama a esta funcion). 
    #       En ese caso, se debe crear el diccionario con los buckets, y actualizarlo incorporando la categoria y el term
    #   2)  Si la categoria ya se encuentra en el diccionario. Si no es asi, entonces se debe crear, e incorporar el term
    #   3)  Si la categoria ya existe, entonces solo queda actualizar el diccionario con el nuevo term

    if not totals: # Si el diccionario esta vacio
        # Creo la key para el bucket positive
        totals['positive'] = {}

        # Agrego la category al diccionario, asi como también el term
        totals['positive'][category] = {}

        if total_positive != 0:
            totals['positive'][category].update({term : total_positive})

        # Creo la key para el bucket positive
        totals['negative'] = {}

        # Agrego la category al diccionario, asi como también el term
        totals['negative'][category] = {}

        if total_negative != 0:
            totals['negative'][category].update({term : total_negative})
    
    elif (category not in totals['positive'].keys()) or (category not in totals['positive'].keys()): # Si la categoria no existe en el diccionario
        
        totals['positive'][category] = {}

        if total_positive != 0:
            totals['positive'][category].update({term : total_positive})

        totals['negative'][category] = {}

        if total_negative != 0:
            totals['negative'][category].update({term : total_negative})
    
    else:
        
        if total_positive != 0:
            totals['positive'][category].update({term : total_positive})

        if total_negative != 0:
            totals['negative'][category].update({term : total_negative})


def calculate_tfs(totals):
    """
    Calculates the term frequencies and creates inverse indexes mapping terms to buckets and to categories

    :param totals: Reduced key,values
    :return: a tuple consisting of (term frequencies, map of term:buckets, map of term:categories)
    """
    tfs = {}
    term_buckets = {}
    term_categories = {}

    for bucket, bucket_totals in totals.items():
        tfs[bucket] = {}
        for category, category_totals in bucket_totals.items():
            tfs[bucket][category] = {}
            for term, frequency in category_totals.items():
                tfs[bucket][category][term] = frequency / sum(category_totals.values())

                if term not in term_buckets:
                    term_buckets[term] = set()
                term_buckets[term].add(bucket)

                if term not in term_categories:
                    term_categories[term] = set()
                term_categories[term].add(category)

    return tfs, term_buckets, term_categories


def calculate_tfs_idfs(tfs, term_buckets, term_categories):
    """
    Calculates a modified version of TF-IDF that better suits our problem

    :param tfs: term frequencies
    :param term_buckets: map term:buckets
    :param term_categories: map term:categories
    :return: the modified TF-IDF scores of each term per (category, bucket)
    """
    tf_idfs = {}
    n_buckets = len(tfs)
    #n_categories = len(list(tfs.values())[0])
    n_categories = {'positive': len(tfs['positive'].keys()),
                    'negative': len(tfs['negative'].keys())}


    for bucket, bucket_tfs in tfs.items():
        tf_idfs[bucket] = {}
        for category, category_tfs in bucket_tfs.items():
            tf_idfs[bucket][category] = {}
            for term, tf in category_tfs.items():
                tot_categories = n_categories[bucket]

                # Encuentro las categorias que contienen el termino. Esto lo puedo sacar de term_categories
                # El problema es que puede ser que un termino este en una categoria del bucket opuesto por lo 
                # que no deberia contar esa categoria para el idf ya que estoy contando las categorias que contienen
                # el termino DENTRO de un mismo bucket

                categories_with_term = set(term_categories[term]).intersection(set(tfs[bucket].keys()))

                # Calculo idf

                idf = math.log(tot_categories/len(categories_with_term))

                # Cargo al diccionario

                tf_idfs[bucket][category][term] = tfs[bucket][category][term]*idf
                # TODO aquí deben calcular el tfs/idfs del bucket, categoría y término y volcarlo en el diccionario tf_idfs
                

    return tf_idfs


def merge(totals):
    """
    Merge function to be applied after reducing all key,values

    :param totals: reduced key,values
    :return: the result of merging all the reduced keys
    """
    tfs, term_buckets, term_categories = calculate_tfs(totals)

    return calculate_tfs_idfs(tfs, term_buckets, term_categories)


def write_csv(category, bucket, sorted_scores):
    """
    Writes the terms and TF-IDF scores corresponding to a (category, bucket) to a csv file.

    :param category: category
    :param bucket: bucket ("negative" or "positive")
    :param sorted_scores: list of (term, score) sorted by score from highest to lowest
    """
    with open("terms_" + category + "_" + bucket + ".csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('Término', 'TF/IDF'))
        writer.writerows(sorted_scores)


def main():
    totals = {}
    cur_key = None
    buffer = []

    for input_line in sys.stdin:
        term, category, bucket, value = input_line.strip().split("\t")
        if cur_key == (term, category):
            buffer.append((term, category, bucket, int(value)))
        else:
            cur_key = (term, category)
            if buffer:
                reduce_function(buffer, totals)
                buffer = []
            else:
                buffer.append((term, category, bucket, int(value)))

    tf_idfs = merge(totals)

    for bucket, bucket_tf_idfs in tf_idfs.items():
        for category, category_tf_idfs in bucket_tf_idfs.items():
            sorted_scores = sorted(category_tf_idfs.items(), key=lambda x: x[1], reverse=True)
            write_csv(category, bucket, sorted_scores)


if __name__ == '__main__':
    main()

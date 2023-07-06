
import json
import sys
from SPARQLWrapper import SPARQLWrapper, JSON, RDF, XML
from pandas import json_normalize
import pandas as pd
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
#from django.shortcuts import render
#from django.views.decorators.csrf import csrf_exempt
#from django.http import JsonResponse
from urllib.parse import quote

endPoint = "https://dbpedia.org/sparql"
sparql = SPARQLWrapper(endPoint)

lista = ["Waste","Pollution_control_technologies","Electronic_waste"]


def get_results(query):
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    results = sparql.query().convert()
    return results

def receive_broaders_lists(list_broaders,level):

    for i in list_broaders:
      
        resource = quote(i)
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>

        select distinct ?level ?r ?c1
            {
                {VALUES (?r ?level) {(dbc:%s + %s)}

                    ?r ^skos:broader{1} ?c1.

                FILTER (!regex(?c1, "lists"))
            }
    
        }    
        """%(resource,str(level))

    resultados = get_results(query)
    return resultados["results"]["bindings"]
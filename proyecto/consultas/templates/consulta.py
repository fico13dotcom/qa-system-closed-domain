import sys
from SPARQLWrapper import SPARQLWrapper, JSON, RDF, XML
from pandas import json_normalize

# DECLARACION DEL ENDPPOINT

### http://UPS-SCLAB-04:7200/repositories/PracticaFinal
endPoint = "https://dbpedia.org/sparql"
sparql = SPARQLWrapper(endPoint)

# METODO PARA OBTENER RESULTADOS
def get_results(query):
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    results = sparql.query().convert()
    return(results)

# METODO PARA OBTENER EL QUERY
def get_reource_query(resource, level):

    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>

    select distinct ?level ?r ?c1
        {
            {VALUES (?r ?level) {(dbc:""" + resource +""" + """ + str(level) +""")}
                ?r ^skos:broader{1} ?c1.

            FILTER (!regex(?c1, "lists"))
        }
    
    }    
    """

    resultados = (get_results(query))

    df_consulta1 = json_normalize(resultados["results"]["bindings"])

    return df_consulta1


resource = "Pollution"
level = 2
resultados = get_reource_query(resource, level)

# Filter the columns that are of interest.
resultados = resultados[['level.value', 'r.value', 'c1.value']]

# Assuming your DataFrame is named df and you want to transform the 'column_name' column
column_list = resultados['c1.value'].tolist()

# Display the resulting list
print(column_list)
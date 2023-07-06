import json
from SPARQLWrapper import JSON, SPARQLWrapper
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from urllib.parse import quote


endPoint = "https://dbpedia.org/sparql"
sparql = SPARQLWrapper(endPoint)


def get_results(query):
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    results = sparql.query().convert()
    return results


def get_reource_query(resource, level):
    resource = quote(resource)
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
    """ %(resource,str(level))

    resultados = get_results(query)
    return resultados["results"]["bindings"]


@csrf_exempt
def index(request):
    if request.method == 'POST':
        valoresSeleccionados = request.POST.get('valores_seleccionados')
        print(valoresSeleccionados)
    return render(request, 'index.html')


def obtenerSubdominios(request):
    if request.method == 'POST':
        resultados = []
        nivel = request.POST.get('contador')
        if nivel == '0':
            dominiosSeleccionados = request.POST.get('dominio')
            resultado = get_reource_query(dominiosSeleccionados, nivel)
            resultados.append(resultado)
        else:
            dominiosSeleccionados = request.POST.getlist('subdominios')
            for dominio in dominiosSeleccionados:
                dominio = dominio.split(":")[-1]
                resultado = get_reource_query(dominio, nivel)
                resultados.append(resultado)

        if resultados:
            lista = []

            for resultado in resultados:
                for item in resultado:
                    url = item["c1"]["value"]
                    clave = url.split(":")[-1]
                    lista.append(clave)
            json_data = json.dumps(lista)
            return JsonResponse(json_data, safe=False)

    return JsonResponse({'error': 'No se pudo procesar la solicitud'})

"""
Test
@SantiagoSF
"""

import requests
import json
import time

from requests.models import Response


def get_series_banxico(params):
    """ Logica de consulta de la API. """

    # La url se constrye con los siguientes parametros: series a consultar
    # y fecha: puede ser una determinada, un rango u
    # 'oportuno' para el ultimo dato
    url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{0}'
    # Al agrega una nueva serie tambien es necesario agregar los indices de formateo
    # en la variable indicator de la funcion menu para poder imprimir.
    
    url = url.format(params)
    
    headers = {
        'Accept': 'application/json',
        'Bmx-Token': # Token de ejemplo, obtener el personal en el API de BANXICO
            'f2bc23ded15faf91ef32c9b4bb5a8b108f37a74519970cac4ad86d219390c796',
        'Accept-Encoding': 'gzip'
        }
    response = requests.get(url, headers=headers)
 
    if response.status_code == 200:
        content_json = response.json()
        #print("Content_json:   ",content_json, "\n\n\n")
        content_json = content_json['bmx']['series']
        #print("Content_json parsed:   ",content_json, "\n\n\n")

        data = []
        for dictionary in content_json:
            for values in dictionary['datos']:
                data.append(
                    (dictionary['titulo'][:40],
                        values['fecha'],
                        values['dato'])
                    )
    return data


def ask_series_banxico(indicator):
    """Grafica las series escogidas"""
    print("Obteniendo datos...")
     # datos default
    #series = 'SF283'
    date = '/datos/2020-01-01/2020-12-29'  # Agregar fecha despues de /datos/
    params = indicator + date

    indicator_series = get_series_banxico(params)




    return indicator_series

    #print(type(series))
    #print("Datos listos y guardados en tasa-objetivo.json")
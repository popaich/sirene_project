import requests
import json
import sys
import pandas
import io
from pprint import pprint
from pymongo import MongoClient
import inspect
from urllib import parse
import insee_variables as insee
import time

def get_informations(authorization_header):

    """
    ======================================================================================================================================
    Obtention de la date de dernière mise à jour des données de l'API concernant les établissements

    dateDernierTraitementMaximum: Toutes les données enregistrées dans le répertoire Sirene jusqu'à cette date sont accessibles par le 
    service API Sirene.Cette date intéresse un utilisateur cherchant à mettre à jour une copie des données. 
    ======================================================================================================================================
    """
    headers = {'Authorization':'Bearer %s' % authorization_header,'Accept':'application/json'}
    json_data = requests.get('https://api.insee.fr/entreprises/sirene/V3/informations', headers=headers).json()
    return json_data['datesDernieresMisesAJourDesDonnees'][1]['dateDernierTraitementMaximum']

def update_mongodb_etablissement(data):
    
    dataframe = pandas.read_csv(io.StringIO(data.decode('utf-8')),dtype=str)
    #on convertit le dataframe en json, en enlevant les valeurs nulles
    dataframe_json = json.dumps([row.dropna().to_dict() for index,row in dataframe.iterrows()])
    #on convertit le json sous forme de liste d'objets
    dataframe_list = json.loads(dataframe_json)

    client = MongoClient("mongodb://localhost:27017")
    db = client.sirene_app

    etablissement = db.etablissement

    for row in dataframe_list:
        etablissement.update_one(
            { "siret": row['siret'] },
            { "$set": row },
            upsert= True
        )


begin = time.time()

args = sys.argv[1:]

if args:

    token = args[0]
    date = get_informations(token)
    debut = 0
    nombre = 5000
    totalCount = 0

    print()
    print('dateDernierTraitementMaximum: %s' % date)
    print()

    print()
    print('traitement des mises à jour des établissements ...')
    print()

    headers = {'Authorization':'Bearer %s' % token,'Accept':'text/csv'}

    params = {
        'q': 'dateDernierTraitementEtablissement:' + date, 
        'date': date,
        'masquerValeursNulles':'true',
        'champs':insee.ETABLISSEMENT,
        'nombre': nombre,
        'debut': debut
    }

    response = requests.get(insee.API_URL_ETAB, headers=headers, params=params)
    totalCount = response.headers['X-Total-Count']
    print('reception des enregistrements {0} à {1} sur {2} terminée !'.format(debut, int(debut) + int(nombre) - 1, totalCount))

    update_mongodb_etablissement(response.content)
    print('mise à jour des enregistrements terminée !')

    while response.url != response.links['last']['url']:

        next_url = response.links['next']['url']
        query = parse.parse_qs(parse.urlsplit(next_url).query)
        debut = query['debut'][0]
        nombre = query['nombre'][0]
        response = requests.get(response.links['next']['url'], headers=headers) 
        print('reception des enregistrements {0} à {1} sur {2} terminée !'.format(debut, int(debut) + int(nombre) - 1, totalCount))

        update_mongodb_etablissement(response.content)
        print('mise à jour des enregistrements terminée !')


    end = time.time()
    elapsed = end - begin

    print()
    print('traitement des mises à jour des établissements terminé en ', int(elapsed), ' s !')
    print()

else:
    print('1er paramètre: authorization token manquant')

""" 
    url = response.links['next']['url']

    while url:
        query = parse.parse_qs(parse.urlsplit(url).query)
        debut = query['debut'][0]
        nombre = query['nombre'][0]
        response = get_data_api_insee(insee.API_URL_ETAB,token,date,insee.ETABLISSEMENT,debut,nombre)
        print('reception des enregistrements {0} à {1} sur {2} terminée...'.format(debut, debut + nombre, totalCount))
        update_mongodb_etablissement(response.content)
        print('mise à jour des enregistrements terminée ...')
        url = response.links['next']['url']
    """
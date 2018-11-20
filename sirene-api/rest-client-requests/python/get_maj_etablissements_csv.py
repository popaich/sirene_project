import requests
import json
import sys
import pandas
import io
from pprint import pprint
from pymongo import MongoClient
import inspect

args = sys.argv[1:]

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

def get_etablissements(authorization_header):

    dateDernierTraitementMaximum = get_informations(authorization_header)

    print()
    print('dateDernierTraitementMaximum: %s' % dateDernierTraitementMaximum)
    print()
    input('Appuyer sur une touche pour obtenir les établissements mis à jour ...')
    print()

    headers = {'Authorization':'Bearer %s' % authorization_header,'Accept':'text/csv'}
    params = {
        'q': 'dateDernierTraitementEtablissement:' + dateDernierTraitementMaximum + ' OR dateDernierTraitementUniteLegale:' + dateDernierTraitementMaximum, 
        'date': dateDernierTraitementMaximum,
        'masquerValeursNulles':'true'
    }

    data = requests.get('https://api.insee.fr/entreprises/sirene/siret', headers=headers, params=params).content
    dataframe = pandas.read_csv(io.StringIO(data.decode('utf-8')),dtype=str)

    df_etablissement = dataframe.filter(items=[
        'siren',
        'nic',
        'siret',
        'statutDiffusionEtablissement',
        'dateCreationEtablissement',
        'trancheEffectifsEtablissement',
        'anneeEffectifsEtablissement',
        'activitePrincipaleRegistreMetiersEtablissement',
        'dateDernierTraitementEtablissement',
        'etablissementSiege',
        'nombrePeriodesEtablissement',
        'complementAdresseEtablissement',
        'numeroVoieEtablissement',
        'indiceRepetitionEtablissement',
        'typeVoieEtablissement',
        'libelleVoieEtablissement',
        'codePostalEtablissement',
        'libelleCommuneEtablissement',
        'libelleCommuneEtrangerEtablissement',
        'distributionSpecialeEtablissement',
        'codeCommuneEtablissement',
        'codeCedexEtablissement',
        'libelleCedexEtablissement',
        'codePaysEtrangerEtablissement',
        'libellePaysEtrangerEtablissement',
        'complementAdresse2Etablissement',
        'numeroVoie2Etablissement',
        'indiceRepetition2Etablissement',
        'typeVoie2Etablissement',
        'libelleVoie2Etablissement',
        'codePostal2Etablissement',
        'libelleCommune2Etablissement',
        'libelleCommuneEtranger2Etablissement',
        'distributionSpeciale2Etablissement',
        'codeCommune2Etablissement',
        'codeCedex2Etablissement',
        'libelleCedex2Etablissement',
        'codePaysEtranger2Etablissement',
        'libellePaysEtranger2Etablissement',
        'dateDebut',
        'etatAdministratifEtablissement',
        'enseigne1Etablissement',
        'enseigne2Etablissement',
        'enseigne3Etablissement',
        'denominationUsuelleEtablissement',
        'activitePrincipaleEtablissement',
        'nomenclatureActivitePrincipaleEtablissement',
        'caractereEmployeurEtablissement'
    ])

    df_etablissement_json = json.dumps([row.dropna().to_dict() for index,row in df_etablissement.iterrows()])
    df_etablissement_to_list = json.loads(df_etablissement_json)


    for etablissement in df_etablissement_to_list:
        print()
        print(etablissement)
        print()

    #dataframe_to_json = dataframe.to_json(orient='records')
    #dataframe_to_json = json.dumps([row.dropna().to_dict() for index,row in dataframe.iterrows()])
    




"""     client = MongoClient("mongodb://localhost:27017")
    db = client.sirene_app
    collectiontest = db.collectiontest

    for etablissement in dataframe_to_list:

        collectiontest.update_one(

            { "siret": etablissement['siret'] },
            { "$set": etablissement },
            upsert= True
        ) """

        

if args:    
    get_etablissements(args[0])
else:
    print('No authorization code !')
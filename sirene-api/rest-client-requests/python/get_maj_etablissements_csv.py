import requests
import json
import sys
import pandas
import io
from pprint import pprint
from pymongo import MongoClient
import inspect
from urllib import parse

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

def get_etablissements(authorization_header, dateDernierTraitementMaximum):

    print()
    print('établissements ...')
    print()

    headers = {'Authorization':'Bearer %s' % authorization_header,'Accept':'text/csv'}
    params = {
        'q': 'dateDernierTraitementEtablissement:' + dateDernierTraitementMaximum, 
        'date': dateDernierTraitementMaximum,
        'masquerValeursNulles':'true',
        'champs':'siren, nic, siret, statutDiffusionEtablissement, dateCreationEtablissement, trancheEffectifsEtablissement, anneeEffectifsEtablissement, activitePrincipaleRegistreMetiersEtablissement, dateDernierTraitementEtablissement, etablissementSiege, nombrePeriodesEtablissement, complementAdresseEtablissement, numeroVoieEtablissement, indiceRepetitionEtablissement, typeVoieEtablissement, libelleVoieEtablissement, codePostalEtablissement, libelleCommuneEtablissement, libelleCommuneEtrangerEtablissement, distributionSpecialeEtablissement, codeCommuneEtablissement, codeCedexEtablissement, libelleCedexEtablissement, codePaysEtrangerEtablissement, libellePaysEtrangerEtablissement, complementAdresse2Etablissement, numeroVoie2Etablissement, indiceRepetition2Etablissement, typeVoie2Etablissement, libelleVoie2Etablissement, codePostal2Etablissement, libelleCommune2Etablissement, libelleCommuneEtranger2Etablissement, distributionSpeciale2Etablissement, codeCommune2Etablissement, codeCedex2Etablissement, libelleCedex2Etablissement, codePaysEtranger2Etablissement, libellePaysEtranger2Etablissement, dateDebut, etatAdministratifEtablissement, enseigne1Etablissement, enseigne2Etablissement, enseigne3Etablissement, denominationUsuelleEtablissement, activitePrincipaleEtablissement, nomenclatureActivitePrincipaleEtablissement, caractereEmployeurEtablissement',
        'nombre': 1000
    }

    r = requests.get('https://api.insee.fr/entreprises/sirene/siret', headers=headers, params=params)
    data = r.content

    print()
    print('nb total resultats: %s' % r.headers['X-Total-Count'])
    #print(r.links['next']['url'])

    url = r.links['next']['url']
    query = parse.parse_qs(parse.urlsplit(url).query)
    #print(query)
    print(query['q'][0])
    print(query['masquerValeursNulles'][0])
    print()
    
    dataframe = pandas.read_csv(io.StringIO(data.decode('utf-8')),dtype=str)
    
    #on convertit le dataframe en json, en enlevant les valeurs nulles
    dataframe_json = json.dumps([row.dropna().to_dict() for index,row in dataframe.iterrows()])
    #n convertit sous forme de liste d'objets
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
    #avant: 27908055 apres: 27908061 27908263


def get_uniteslegales(authorization_header, dateDernierTraitementMaximum):

    print()
    print('unités légales ...')
    print()

    headers = {'Authorization':'Bearer %s' % authorization_header,'Accept':'text/csv'}
    params = {
        'q': 'dateDernierTraitementUniteLegale:' + dateDernierTraitementMaximum, 
        'date': dateDernierTraitementMaximum,
        'masquerValeursNulles':'true',
        'champs':'siren, statutDiffusionUniteLegale, unitePurgeeUniteLegale, dateCreationUniteLegale, sigleUniteLegale, sexeUniteLegale, prenom1UniteLegale, prenom2UniteLegale, prenom3UniteLegale, prenom4UniteLegale, prenomUsuelUniteLegale, pseudonymeUniteLegale, identifiantAssociationUniteLegale, trancheEffectifsUniteLegale, anneeEffectifsUniteLegale, dateDernierTraitementUniteLegale, nombrePeriodesUniteLegale, categorieEntreprise, anneeCategorieEntreprise, dateDebut, etatAdministratifUniteLegale, nomUniteLegale, nomUsageUniteLegale, denominationUniteLegale, denominationUsuelle1UniteLegale, denominationUsuelle2UniteLegale, denominationUsuelle3UniteLegale, categorieJuridiqueUniteLegale, activitePrincipaleUniteLegale, nomenclatureActivitePrincipaleUniteLegale, nicSiegeUniteLegale, economieSocialeSolidaireUniteLegale, caractereEmployeurUniteLegale'
    }

    data = requests.get('https://api.insee.fr/entreprises/sirene/V3/siren', headers=headers, params=params).content
    dataframe = pandas.read_csv(io.StringIO(data.decode('utf-8')),dtype=str)
    
    #on convertit le dataframe en json, en enlevant les valeurs nulles
    dataframe_json = json.dumps([row.dropna().to_dict() for index,row in dataframe.iterrows()])
    #n convertit sous forme de liste d'objets
    dataframe_list = json.loads(dataframe_json)

    client = MongoClient("mongodb://localhost:27017")
    db = client.sirene_app

    unitelegale = db.unitelegale

    for row in dataframe_list:

        unitelegale.update_one(

            { "siren": row['siren'] },
            { "$set": row },
            upsert= True
        )

        #avant: 19987793 apres: 19987794

if args:

    dateDernierTraitementMaximum = get_informations(args[0])

    print()
    print('dateDernierTraitementMaximum: %s' % dateDernierTraitementMaximum)
    print()
    input('Appuyer sur une touche pour obtenir les mises à jour ...')
    print()

    get_etablissements(args[0], dateDernierTraitementMaximum)
    #get_uniteslegales(args[0], dateDernierTraitementMaximum)

else:
    print('No authorization code !')
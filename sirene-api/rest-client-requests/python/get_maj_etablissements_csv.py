import requests
import json
import sys
import pandas
import io

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
    df = pandas.read_csv(io.StringIO(data.decode('utf-8')))
    pretty_data = json.dumps(df.to_json(), indent=2)
    print(pretty_data)

"""     print(df.loc[[0],['siren']])
    print(df.loc[[0],['activitePrincipaleUniteLegale']]) """


if args:    
    get_etablissements(args[0])
else:
    print('No authorization code !')
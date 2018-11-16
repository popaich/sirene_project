import requests
import json
import sys

args = sys.argv[1:]


def get_informations(authorization_header):

    headers = {'Authorization':'Bearer %s' % authorization_header,'Accept':'application/json'}
    json_data = requests.get('https://api.insee.fr/entreprises/sirene/V3/informations', headers=headers).json()

    dateDernierTraitementMaximum = json_data['datesDernieresMisesAJourDesDonnees'][1]['dateDernierTraitementMaximum']

    print('dateDernierTraitementMaximum: %s' % dateDernierTraitementMaximum)

    pretty_data = json.dumps(json_data, indent=2)    
    print(pretty_data)

if args:
    get_informations(args[0])
else:
    print('No authorization code !')
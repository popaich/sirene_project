import requests
import json

headers = {'Authorization':'Bearer 0850edba-e4cc-3430-ad9b-bd2c7bf5b0e8','Accept':'application/json'}
params = {
    'q': 'dateDernierTraitementEtablissement:2018-11-13 OR dateDernierTraitementUniteLegale:2018-11-13', 
    'date': '2018-11-14',
    'masquerValeursNulles':'true'
}

r = requests.get('https://api.insee.fr/entreprises/sirene/siret', headers=headers, params=params)

pretty_data = json.dumps(r.json(), indent=2)
 
print(pretty_data)
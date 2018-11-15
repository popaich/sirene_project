import requests
import json

headers = {'Authorization':'Bearer 0850edba-e4cc-3430-ad9b-bd2c7bf5b0e8','Accept':'application/json'}

r = requests.get('https://api.insee.fr/entreprises/sirene/V3/informations', headers=headers)

pretty_data = json.dumps(r.json(), indent=2)
 
print(pretty_data)
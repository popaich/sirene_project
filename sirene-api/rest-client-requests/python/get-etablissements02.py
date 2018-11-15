""" 
------------------------------------
Test retour csv
------------------------------------
"""

import requests
import json
import pandas as csv
import io

headers = {'Authorization':'Bearer 0850edba-e4cc-3430-ad9b-bd2c7bf5b0e8','Accept':'text/csv'}
params = {
    'q': 'dateDernierTraitementEtablissement:2018-11-13 OR dateDernierTraitementUniteLegale:2018-11-13', 
    'date': '2018-11-14',
    'masquerValeursNulles':'true'
}

r = requests.get('https://api.insee.fr/entreprises/sirene/siret', headers=headers, params=params).content
c = csv.read_csv(io.StringIO(r.decode('utf-8')))

print(c)


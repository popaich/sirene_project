# API SIRENE

[Espace Sirene API](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee)

[URL Sirene API](https://api.insee.fr/entreprises/sirene/V3)

## Obtention pragrammatique d'un jeton d'accès

POST https://api.insee.fr/token

Headers:

* Content-Type application/x-www-form-urlencoded

* Authorization Basic base64(Clef du consommateur:secret du consommateur). Cf. consommateur de l'application "sirene_app"

## Service informations

* dateDernierTraitementMaximum: Toutes les données enregistrées dans le répertoire Sirene jusqu'à cette date sont accessibles par le service API Sirene.Cette date intéresse un utilisateur cherchant à mettre à jour une copie des données.

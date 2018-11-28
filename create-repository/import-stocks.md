# Création de la collection repository dans MongoDB

## Démarrage de l'instance MongoDB

`mongod –dbpath "D:\mongodb\data"`

## Import des fichiers stocks mensuels (unitelegale et etablissement)

URL pérennes sur data.gouv.fr vers les fichiers stocks:

* [Fichier stock unitelegale](https://www.data.gouv.fr/fr/datasets/r/8abfacf7-efff-4fe9-a7e5-e2a81fb2ef06)

* [Fichier stock etablissement](https://www.data.gouv.fr/fr/datasets/r/954e1608-6d31-4a92-99db-a0f0493ef377)

## mongoimport

* mongoimport --db sirene_app --collection sirene --type CSV --file D:\sirene_201806_L_M\sirene_all.csv --ignoreBlanks --drop –v --columnsHaveTypes --fieldFile D:\mongodb\sirene_src\fields.txt
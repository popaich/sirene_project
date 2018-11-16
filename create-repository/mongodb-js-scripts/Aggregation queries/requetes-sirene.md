# Reqêtes de regroupement sur collection atablissement

Compter le nombre de documents avec filtre match:

conn = new Mongo();
db = conn.getDB("sirene_app");

var data = db.etablissement.aggregate([
  {
    $match: { codeCommuneEtablissement: '42015' }
  },
  {
    $count: "nbEtablissement-belmont"
  }
]);

data.forEach(function(document){printjson(document);});

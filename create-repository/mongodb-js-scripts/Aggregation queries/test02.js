conn = new Mongo();
db = conn.getDB("sirene_app");

var data = db.etablissement.aggregate([
  { 
    $match: { $and: [{codeCommuneEtablissement: '42015' }, {etatAdministratifEtablissement: 'A' }] }
  },
  {
    // selecting the fields that we wish to retain
    $project: { _id: 0, enseigne: "$enseigne1Etablissement", siret: 1,libelleVoieEtablissement: 1}
  }
]);

data.forEach(function(document){printjson(document);}); 
/*
 $count
*/

conn = new Mongo();
db = conn.getDB("sirene_app");

var data = db.etablissement.aggregate([
  { 
    $match: { $and: [{codeCommuneEtablissement: '42015' }, {etatAdministratifEtablissement: 'A' }] }
  },
  {
    $count: "count"
  }
]);

data.forEach(function(document){printjson(document);}); 

//$match: { etatAdministratifEtablissement: 'A' }
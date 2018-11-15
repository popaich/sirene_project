conn = new Mongo();
db = conn.getDB("sirene_app");

var cursor = db.etablissement.aggregate([{ 
    $match: { codeCommuneEtablissement: '42015' },
    $match: { etatAdministratifEtablissement: 'A' }
}
]);

cursor.forEach(function(document){

    printjson(document);
  }
); 
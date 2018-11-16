/*
  jointure sur activité.
  NB: modifier lib1 à 5 pour le niveau que l'on souhaite afficher.
*/
conn = new Mongo();
db = conn.getDB("sirene_app");

var data = db.etablissement.aggregate([
  { 
    $match: { $and: [{codeCommuneEtablissement: '42015' }, {etatAdministratifEtablissement: 'A' }] }
  },
  {
    //join activitePrincipaleEtablissement
    $lookup:
    {
      from: "naf",
      localField: "activitePrincipaleEtablissement",
      foreignField: "niv5",
      as: "activitePrincipaleEtablissement_tmp"
    }
  },
  { $unwind: "$activitePrincipaleEtablissement_tmp" },
  {
    $addFields: { 
      "libelleActivitePrincipaleEtablissement": "$activitePrincipaleEtablissement_tmp.lib1",
      "enseigne": "$enseigne1Etablissement"
    }
  },
  {
    // selecting the fields that we wish to retain
    $project: { 
      _id: 0, 
      siret: 1,
      libelleActivitePrincipaleEtablissement: 1
    }
  }
]);

data.forEach(function(document){printjson(document);}); 
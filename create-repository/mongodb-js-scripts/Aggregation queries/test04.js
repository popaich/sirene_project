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
    $group:{
      _id: "$activitePrincipaleEtablissement_tmp.lib1",
      effectif: { $sum: 1 }
    }
  },
  {
    $addFields: { 
      "activite": "$_id"
    }
  },
  {
    $project: { 
      "_id": 0
    }
  },
  {
    //ordering must be 1 (for ascending) or -1 (for descending)
    $sort:{effectif:-1}
  }
  
  
]);

data.forEach(function(document){printjson(document);}); 
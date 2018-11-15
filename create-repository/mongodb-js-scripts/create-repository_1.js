conn = new Mongo();
db = conn.getDB("sirene_app");

var cursor = db.etablissement.aggregate([

  { $match: { etatAdministratifEtablissement: 'A'} },
  { $lookup: { from: "unitelegale", localField: "siren", foreignField: "siren", as: "entreprisetmp" } },
  { $addFields: { uniteLegale: { $arrayElemAt: [ "$entreprisetmp", 0 ] } } },
  { 
    $addFields: 
    {    
      adresseEtablissement: { 
        numeroVoieEtablissement: "$numeroVoieEtablissement",
        typeVoieEtablissement: "$typeVoieEtablissement",
        libelleVoieEtablissement: "$libelleVoieEtablissement",
        codePostalEtablissement: "$codePostalEtablissement",
        libelleCommuneEtablissement: "$libelleCommuneEtablissement",
        codeCommuneEtablissement: "$codeCommuneEtablissement",
        codeCedexEtablissement: "$codeCedexEtablissement",
        complementAdresseEtablissement: "$complementAdresseEtablissement",
        codePaysEtrangerEtablissement: "$codePaysEtrangerEtablissement",
        libellePaysEtrangerEtablissement: "$libellePaysEtrangerEtablissement",
        distributionSpecialeEtablissement: "$distributionSpecialeEtablissement",
        indiceRepetitionEtablissement: "$indiceRepetitionEtablissement",
        libelleCedexEtablissement: "$libelleCedexEtablissement",
        libelleCommuneEtrangerEtablissement:"$libelleCommuneEtrangerEtablissement"
      } 
    }
  },
  { 
    $addFields: 
    {    
      adresse2Etablissement: { 
        numeroVoie2Etablissement: "$numeroVoie2Etablissement",
        typeVoie2Etablissement: "$typeVoie2Etablissement",
        libelleVoie2Etablissement: "$libelleVoie2Etablissement",
        codePostal2Etablissement: "$codePostal2Etablissement",
        libelleCommune2Etablissement: "$libelleCommune2Etablissement",
        codeCommune2Etablissement: "$codeCommune2Etablissement",
        codeCedex2Etablissement: "$codeCedex2Etablissement",
        complementAdresse2Etablissement: "$complementAdresse2Etablissement",
        codePaysEtranger2Etablissement: "$codePaysEtranger2Etablissement",
        libellePaysEtranger2Etablissement: "$libellePaysEtranger2Etablissement",
        distributionSpeciale2Etablissement: "$distributionSpeciale2Etablissement",
        distributionSpeciale2Etablissement: "$distributionSpeciale2Etablissement",
        libelleCedex2Etablissement: "$libelleCedex2Etablissement",
        libelleCommuneEtranger2Etablissement:"$libelleCommuneEtranger2Etablissement"
      } 
    }
  },
  { $lookup: { from: "cog", localField: "adresseEtablissement.codeCommuneEtablissement", foreignField: "com", as: "geo" }},
  { $addFields: { territoire: { $arrayElemAt: [ "$geo", 0 ] } }},
  {
    $lookup:
    {
      from: "naf",
      localField: "activitePrincipaleEtablissement",
      foreignField: "niv5",
      as: "activiteEtablissementtmp"
    }
  },
  {
    $addFields: 
    {
      "activite": { $arrayElemAt: [ "$activiteEtablissementtmp", 0 ] }
    }
  },
  {
    $lookup:
    {
      from: "naf",
      localField: "uniteLegale.activitePrincipaleUniteLegale",
      foreignField: "niv5",
      as: "activiteUniteLegaletmp"
    }
  }, 
  {
    $addFields: 
    {
      "uniteLegale.activite": { $arrayElemAt: [ "$activiteUniteLegaletmp", 0 ] }
    }
  },
  {
    $lookup:
    {
      from: "cj",
      localField: "uniteLegale.categorieJuridiqueUniteLegale",
      foreignField: "niv3",
      as: "categoriejuridiquetmp"
    }
  }, 
  {
    $addFields: 
    {
      "uniteLegale.cj": { $arrayElemAt: [ "$categoriejuridiquetmp", 0 ] }
    }
  },
  {
    $lookup:
    {
      from: "effectif",
      localField: "trancheEffectifsEtablissement",
      foreignField: "code",
      as: "effectiftmp"
    }
  }, 
  {
    $addFields: 
    {
      "effectif": { $arrayElemAt: [ "$effectiftmp", 0 ] }
    }
  },
  {
    $lookup:
    {
      from: "effectif",
      localField: "uniteLegale.trancheEffectifsUniteLegale",
      foreignField: "code",
      as: "effectifunitelegaletmp"
    }
  }, 
  {
    $addFields: 
    {
      "uniteLegale.effectif": { $arrayElemAt: [ "$effectifunitelegaletmp", 0 ] }
    }
  },
  {
    $project: 
    {      
      // champs adresseEtablissement
      numeroVoieEtablissement: 0,
      typeVoieEtablissement: 0,
      libelleVoieEtablissement: 0,
      codePostalEtablissement: 0,
      libelleCommuneEtablissement: 0,
      codeCommuneEtablissement: 0,
      codeCedexEtablissement: 0,
      complementAdresseEtablissement: 0,
      codePaysEtrangerEtablissement: 0,
      libellePaysEtrangerEtablissement: 0,
      distributionSpecialeEtablissement: 0,
      indiceRepetitionEtablissement: 0,
      libelleCedexEtablissement: 0,
      libelleCommuneEtrangerEtablissement: 0, 
      
      // champs adresse2Etablissement
      numeroVoie2Etablissement: 0,
      typeVoie2Etablissement: 0,
      libelleVoie2Etablissement: 0,
      codePostal2Etablissement: 0,
      libelleCommune2Etablissement: 0,
      codeCommune2Etablissement: 0,
      codeCedex2Etablissement: 0,
      complementAdresse2Etablissement: 0,
      codePaysEtranger2Etablissement: 0,
      libellePaysEtranger2Etablissement: 0,
      distributionSpeciale2Etablissement: 0,
      indiceRepetition2Etablissement: 0,
      libelleCedex2Etablissement: 0,
      libelleCommuneEtranger2Etablissement: 0, 

      entreprisetmp: 0,
      activiteUniteLegaletmp: 0,
      activiteEtablissementtmp: 0,
      categoriejuridiquetmp: 0,
      effectiftmp: 0,
      effectifunitelegaletmp: 0,
      geo: 0,

      _id: 0,
      nomenclatureActivitePrincipaleEtablissement:0,
      trancheEffectifsEtablissement: 0,
      nombrePeriodesEtablissement: 0,
      "uniteLegale._id": 0,
      "uniteLegale.activite._id": 0, 
      "uniteLegale.nomenclatureActivitePrincipaleUniteLegale": 0, 

      "territoire._id": 0,
      "territoire.com": 0,
      "territoire.libcom": 0,      

      "activite._id": 0,
      "uniteLegale.cj._id": 0,
      "uniteLegale.categorieJuridiqueUniteLegale": 0,
      "uniteLegale.effectif._id": 0,
      "uniteLegale.trancheEffectifsUniteLegale": 0,
      "uniteLegale.siren": 0,
      "effectif._id": 0,
    }
  },
  {
    $out: "repository"
  } 
]);
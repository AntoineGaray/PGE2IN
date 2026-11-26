# Quiz et flashcards – Macroéconomie (M. Zumer)
# Source : notes de révision et PowerPoint V20 de M. Zumer, document n°6 (« Les pauvres contre Piketty »).
# Ne jamais renommer ni réutiliser un identifiant (macro-qNN, macro-fNN) : les points et la révision espacée en dépendent.
# Les identifiants viennent de la position : ajouter les nouvelles questions et cartes À LA FIN des listes.
# Construction : python3 tools/macro_quiz_src.py  ->  data/macro.json
import json, os

CHAPTERS = [
    ("c1a", "Ch. 1 – De Soto, le parcours du combattant et le capital mort"),
    ("c1b", "Ch. 1 – Le débat, le contrat social et le document n°6"),
    ("c2a", "Ch. 2 – Nouvelle économie : Solow, Gordon, les NTIC"),
    ("c2b", "Ch. 2 – Modèle O-ring, émergence du Sud, fin du fordisme"),
]

# (chapitre, question, [bonne réponse, 3 distracteurs], explication)
QUIZ = [
 ("c1a", "De quel pays vient Hernando de Soto ?", ["Le Pérou", "Le Chili", "L'Égypte", "Haïti"], "Né en 1941 à Arequipa, au Pérou."),
 ("c1a", "Quel institut de Soto a-t-il fondé à Lima en 1980 ?", ["L'ILD, Institut pour la liberté et la démocratie", "Le GATT", "L'USAID", "La Banque mondiale"], "L'ILD a ensuite conseillé une trentaine de gouvernements."),
 ("c1a", "À quoi répond le titre de son premier livre, L'Autre Sentier (1986) ?", ["Au Sentier lumineux, les terroristes qui avaient essayé de l'assassiner", "À un roman de Vargas Llosa", "Au consensus de Washington", "À la route de la soie"], "Il propose une autre voie que la violence pour sortir de la pauvreté."),
 ("c1a", "Quel est le sous-titre du Mystère du capital (2000) ?", ["Pourquoi le capitalisme triomphe en Occident et échoue partout ailleurs", "Le capital au XXIe siècle", "La Grande Transformation", "Civilisation matérielle, économie et capitalisme"], "C'est le livre de référence du chapitre 1."),
 ("c1a", "Quelle image tirée de Braudel décrit un capitalisme réservé à quelques secteurs ?", ["Un capitalisme « en système clos, voire enkysté » : la cloche de verre", "La main invisible", "La destruction créatrice", "Le cercle vertueux"], "Le capitalisme existe, mais sous une cloche, pour une minorité."),
 ("c1a", "Quelle explication du sous-développement de Soto rejette-t-il ?", ["Les mentalités et la culture (l'éthique protestante de Weber)", "Le coût de la légalité", "L'absence de titres de propriété", "Les défauts du système juridique"], "Pour lui, les entrepreneurs ne manquent pas : c'est le droit qui bloque."),
 ("c1a", "Que préconisait le consensus de Washington ?", ["Stabiliser la monnaie, libéraliser, privatiser", "Distribuer des titres de propriété", "Taxer le capital", "Nationaliser les banques"], "Ces politiques ont majoritairement échoué dans les pays pauvres."),
 ("c1a", "Combien de temps a-t-il fallu pour enregistrer l'entreprise d'un seul salarié de de Soto à Lima ?", ["289 jours, à raison de 6 heures par jour", "4 heures", "2 semaines", "19 ans"], "Pour un coût de 1 230 dollars."),
 ("c1a", "Que représentaient les 1 230 dollars dépensés pour légaliser l'entreprise au Pérou ?", ["31 fois le salaire minimum mensuel", "Le prix d'une machine à coudre", "La moitié d'un salaire minimum", "10 fois le PIB par habitant"], "Un coût hors de portée pour un pauvre."),
 ("c1a", "Combien d'étapes impose la municipalité de Lima pour un titre légal sur un logement ?", ["728", "207", "111", "65"], "207 = les opérations de la seule première phase pour légaliser un logement."),
 ("c1a", "Quelle part des petites entreprises industrielles de Lima est illégale ?", ["90 %", "50 %", "25 %", "10 %"], "Et 85 % du transport urbain, 60 % de la distribution alimentaire."),
 ("c1a", "Combien de temps faut-il en Haïti pour légaliser un terrain acquis, au total ?", ["19 ans", "289 jours", "5 ans", "6 mois"], "5 ans de bail, 65 formalités en 2 ans, puis l'achat."),
 ("c1a", "Que montre le laisser-passer A 38 dans le cours ?", ["Que la bureaucratie existe aussi en France", "Que l'Égypte est la plus lente", "Que la France n'a pas de bureaucratie", "Que les titres sont inutiles"], "Le cas de la France, version Astérix."),
 ("c1a", "Pour de Soto, l'illégalité des habitants des pays pauvres signifie surtout que…", ["L'État ne les respecte pas, avec des démarches aussi lourdes", "Ils refusent de respecter la loi", "Ils préfèrent l'économie souterraine par culture", "Ils ne veulent pas payer d'impôts"], "C'est l'inverse d'un manque de respect de la loi."),
 ("c1a", "Qu'est-ce que le « capital mort » ?", ["Des biens possédés mais sans titre, qui ne peuvent ni circuler ni servir de garantie", "Du capital détruit par une crise", "Des machines obsolètes", "L'épargne non investie des riches"], "Il représente jusqu'à 90 % de l'économie de certains pays."),
 ("c1a", "Quelle part des créations d'entreprises américaines passe par un emprunt gagé sur une hypothèque ?", ["70 %", "10 %", "30 %", "95 %"], "Sans titre, pas d'hypothèque, donc pas de crédit."),
 ("c1a", "Que permet un titre de propriété, selon de Soto ?", ["Rendre les biens fongibles : les diviser, les vendre, les hypothéquer", "Seulement protéger contre le vol", "Échapper à l'impôt", "Interdire la revente"], "Le titre « fixe le potentiel économique » du bien."),
 ("c1a", "Pourquoi le droit des pays pauvres est-il souvent défaillant ?", ["Il hérite du droit colonial, fait pour extraire les richesses", "Il est trop récent", "Il copie le droit américain", "Il n'existe aucune loi"], "Un droit pensé pour protéger les colons, pas pour faire circuler le capital."),
 ("c1b", "Le titre de la 3e partie du plan du prof est : la légalisation des propriétés est…", ["Une condition nécessaire mais pas suffisante", "Une condition suffisante", "Inutile", "Contraire au développement"], "Il faut aussi des dirigeants courageux et un contrat social."),
 ("c1b", "Quel groupe de Soto juge-t-il le plus conservateur dans les pays pauvres ?", ["Les juristes et les avocats", "Les entrepreneurs informels", "Les militaires", "Les étudiants"], "Il faut s'appuyer sur les quelques juristes ouverts."),
 ("c1b", "Quel exemple historique de Soto utilise-t-il pour les États-Unis ?", ["La conquête de l'Ouest : plus d'un siècle pour unifier les droits de propriété", "La guerre de Sécession", "Le New Deal", "La crise de 1929"], "Les pays pauvres d'aujourd'hui en sont au même point."),
 ("c1b", "Quelle loi l'ILD a-t-il fait voter au Pérou en 1991 ?", ["La Ley de Registro de Predios Rurales, un enregistrement cadastral", "Une loi de nationalisation", "Un impôt sur la fortune", "Le Homestead Act"], "C'est l'un des résultats concrets du cours."),
 ("c1b", "Selon de Soto, quel est « le vrai contrat social » ?", ["Le système juridique", "Le droit de vote", "L'impôt sur le revenu", "La sécurité sociale"], "D'où l'équivalence droits sociaux = droits juridiques."),
 ("c1b", "Qui avertit que la contradiction entre les peuples et l'économie de marché « fait le lit du fascisme » ?", ["Karl Polanyi, La Grande Transformation", "Max Weber", "Robert Solow", "Fernand Braudel"], "De Soto reprend cette idée."),
 ("c1b", "Comment de Soto analyse-t-il l'Europe ?", ["Sans marché juridique unifié, pas de vrai marché unique", "Elle a trop de titres de propriété", "Elle est trop centralisée juridiquement", "Elle n'a pas de bureaucratie"], "Le fractionnement juridique limite les économies d'échelle."),
 ("c1b", "Comment de Soto qualifie-t-il la crise des subprimes ?", ["Un tiers-monde de la finance en Occident, une crise de droits de propriété", "Une crise de surproduction", "Une crise purement monétaire", "Une crise des matières premières"], "Personne ne savait ce que contenaient les titres « pourris »."),
 ("c1b", "Que résume la formule r > g de Piketty ?", ["Le rendement du capital dépasse la croissance, donc les inégalités se creusent", "La croissance dépasse le rendement du capital", "Les revenus du travail augmentent plus vite que le capital", "Le taux d'intérêt est supérieur à l'inflation"], "Document n°6 : c'est la thèse attaquée par de Soto."),
 ("c1b", "Que reproche de Soto aux statistiques de Piketty ?", ["Elles ignorent les 90 % de la population mondiale qui vivent dans l'informel", "Elles sont trop récentes", "Elles ne couvrent que l'Afrique", "Elles surestiment la croissance"], "Une analyse eurocentrée."),
 ("c1b", "Selon l'enquête de l'ILD en Égypte, quelle part du revenu « du travail » vient en fait du capital ?", ["47 %", "10 %", "90 %", "25 %"], "120 chercheurs ; 360 milliards de dollars d'immobilier."),
 ("c1b", "Qui était vraiment Mohamed Bouazizi, selon de Soto ?", ["Un entrepreneur depuis l'âge de 12 ans, exproprié de son capital", "Un chômeur sans activité", "Un fonctionnaire", "Un militant politique"], "63 autres entrepreneurs ont tenté de se suicider dans les deux mois."),
 ("c1b", "Quelle phrase du document n°6 oppose l'Occident au reste du monde ?", ["« Du papier sans actifs » contre « des actifs sans papier »", "« Les ordinateurs sont partout sauf dans les statistiques »", "« Un pays a la conjoncture de ses structures »", "« Indoor plumbing beats iPads »"], "Le capital fictif contre le capital mort."),
 ("c2a", "Quelle est la phrase de Solow en 1987 ?", ["« Les ordinateurs sont partout, sauf dans les statistiques de la productivité »", "« L'âge d'or de la croissance est derrière nous »", "« Indoor plumbing beats iPads »", "« Un pays a la conjoncture de ses structures »"], "C'est le paradoxe de Solow."),
 ("c2a", "Pourquoi le paradoxe de Solow devient-il obsolète au début des années 2000 ?", ["La productivité du travail américaine se met enfin à augmenter", "Les ordinateurs disparaissent", "La croissance s'arrête", "Solow change de théorie sur le capital"], "En 2000, Solow lui-même dit que les ordinateurs sont entrés dans les statistiques."),
 ("c2a", "Quelle condition faut-il, en plus des ordinateurs, pour parler de 3e révolution industrielle ?", ["Un changement dans l'organisation du travail des entreprises", "Une baisse du prix du pétrole", "Une guerre mondiale", "Une hausse des impôts"], "La technique seule ne suffit pas."),
 ("c2a", "Quand se situe la 1re révolution industrielle selon la fiche n°1 du cours ?", ["Vers 1760-1830, surtout en Angleterre", "Vers 1860-1900, en Europe et aux États-Unis", "1913-1972", "Depuis les années 1990"], "Vapeur, train, métier à tisser."),
 ("c2a", "Quelle période la fiche n°1 appelle-t-elle l'âge d'or de la productivité ?", ["1913-1972", "1760-1830", "1995-2005", "1870-1900"], "Les effets de la 2e révolution industrielle."),
 ("c2a", "Quel est le premier argument de Gordon contre la nouvelle économie ?", ["Un effet de moyenne : la productivité n'a augmenté que dans le secteur des NTIC", "Les ordinateurs sont trop chers", "Internet n'existe pas encore", "La productivité a baissé partout"], "Une illusion d'optique dans les statistiques."),
 ("c2a", "Que montre le graphique de Gordon « Diminishing Returns in the New Economy » ?", ["Plus de puissance (MHz) n'apporte presque plus d'utilité", "L'utilité augmente sans limite", "Les prix des ordinateurs montent", "Le nombre d'ordinateurs baisse"], "Des rendements décroissants."),
 ("c2a", "Selon l'étude Olfeo 2015 du cours, combien de temps de surf personnel par jour au bureau ?", ["Environ 50 minutes", "5 minutes", "4 heures", "Aucun"], "1 h 53 sur Internet par jour, dont 44 % personnel."),
 ("c2a", "Par combien le télégraphe a-t-il multiplié la vitesse de transmission, selon Gordon ?", ["3 000", "10", "100", "1 million"], "Et divisé le coût par 100."),
 ("c2a", "Pourquoi le cours parle-t-il de « Gordon et Jésus » ?", ["Pour Gordon, ceux qui croient à la 3e RI attendent un messie qui ne viendra pas", "Gordon est théologien", "Gordon compare l'ordinateur à la Bible", "Gordon annonce une révolution religieuse"], "Les nouvelles technologies jouent le rôle du messie."),
 ("c2a", "Dans l'interview au Monde (2016), quelle période Gordon présente-t-il comme une parenthèse exceptionnelle ?", ["1870-1970 aux États-Unis", "1995-2005", "1760-1830 en Angleterre", "2008-2020"], "« L'âge d'or de la croissance est derrière nous »."),
 ("c2a", "Que répond Krugman à Gordon (2013) ?", ["Les « androïdes » (reconnaissance vocale, traduction, voiture autonome) pourraient relancer la croissance", "Gordon a raison sur tout", "La plomberie est inutile", "Il faut interdire les robots"], "Optimiste pour la croissance, inquiet pour les salaires."),
 ("c2a", "Quel exemple le prof oppose-t-il à Gordon ?", ["Un vaccin contre le Covid en un an, impossible sans ordinateurs", "Le télégraphe", "La machine à vapeur", "Le moteur à explosion"], "Gordon oublie l'ensemble des usages des NTIC."),
 ("c2a", "Quelle part de l'économie américaine représente le secteur des NTIC dans le cours ?", ["Environ 15 %", "Environ 1 %", "Environ 50 %", "Environ 80 %"], "Environ 8 % en France."),
 ("c2a", "Quel était l'objectif du sommet de Lisbonne (2000) ?", ["Faire de l'Europe l'économie de la connaissance la plus compétitive du monde", "Créer l'euro", "Taxer les géants du numérique", "Fermer les frontières"], "Pour rattraper le retard européen sur les NTIC."),
 ("c2a", "Que dit la loi de Metcalfe ?", ["La valeur d'un réseau augmente avec le carré du nombre de ses utilisateurs", "La puissance des puces double tous les deux ans", "Les coûts variables augmentent avec la production", "Le premier entrant perd toujours"], "C'est l'effet de réseau."),
 ("c2a", "Pourquoi le secteur des NTIC fabrique-t-il naturellement des monopoles ?", ["Économies d'échelle (coûts fixes élevés) et effets de réseau", "Interdiction de la concurrence par l'État", "Manque d'innovation", "Coûts variables très élevés"], "D'où de fortes barrières à l'entrée."),
 ("c2a", "Qu'est-ce qu'une licorne ?", ["Une start-up valorisée plus d'un milliard de dollars", "Une entreprise publique", "Un monopole d'État", "Une entreprise sans salariés"], "Fruit de la révolution financière américaine."),
 ("c2b", "Qui a conçu le modèle O-ring ?", ["Michael Kremer, prix Nobel 2019", "Robert Gordon", "Robert Solow", "Angus Maddison"], "Professeur à Harvard."),
 ("c2b", "D'où vient le nom O-ring ?", ["Un joint d'étanchéité : une navette perdue à cause d'une seule pièce", "Un anneau olympique", "Un circuit électronique", "Une marque de pneus"], "Le maillon faible menace toute la chaîne."),
 ("c2b", "Quelle est la leçon du modèle O-ring sur les qualifications ?", ["Les travailleurs d'une même chaîne doivent avoir un niveau proche, homogène", "Il faut mélanger tous les niveaux", "Seuls les dirigeants comptent", "La qualification n'a plus d'importance"], "D'où les appariements sélectifs."),
 ("c2b", "Pourquoi le modèle O-ring n'était-il pas possible avant l'informatique ?", ["Il faut transmettre instantanément beaucoup de données en réseau", "Les avions n'existaient pas", "Les salaires étaient trop bas", "Il n'y avait pas de sous-traitants"], "Sans cela, la seule organisation possible est la pyramide."),
 ("c2b", "Quel exemple illustre l'ancienne organisation pyramidale fordiste dans le cours ?", ["Renault à Boulogne-Billancourt", "Le Boeing 787", "Le Falcon 7X", "La Volvo S40"], "La grande usine intégrée."),
 ("c2b", "Qu'a montré la conception du Falcon 7X de Dassault ?", ["Des partenaires du monde entier ont conçu l'avion ensemble, à distance", "Un avion conçu dans une seule usine", "Un avion sans ordinateur", "Un échec commercial"], "Document n°15, sur un plateau virtuel."),
 ("c2b", "La valeur ajoutée d'une voiture comme la Volvo S40 provient d'au moins…", ["10 pays", "2 pays", "1 pays", "50 pays"], "Entre le tiers et la moitié des composants sont importés, retravaillés et réexportés."),
 ("c2b", "Quel nouveau type d'inégalités le modèle O-ring fait-il apparaître ?", ["Des inégalités à l'intérieur des groupes (intra-classes)", "Des inégalités entre classes sociales uniquement", "La fin de toute inégalité", "Des inégalités seulement entre pays"], "De petits écarts de performance donnent de grands écarts de revenus."),
 ("c2b", "Selon le cours, quel est le lien entre révolution industrielle et mondialisation ?", ["La révolution industrielle a permis la mondialisation, pas l'inverse", "La mondialisation a causé la révolution industrielle", "Elles n'ont aucun lien", "La mondialisation a bloqué la révolution industrielle"], "Comme la 1re RI a précédé la 1re mondialisation."),
 ("c2b", "Quel risque crée l'erreur de raisonnement qui part de la mondialisation ?", ["La montée du protectionnisme, qui briserait l'espoir des pays pauvres", "Une hausse de la productivité", "La fin des NTIC", "Une baisse des inégalités"], "Pour les pays pauvres, le commerce reste un espoir."),
 ("c2b", "Avant le modèle O-ring, quel pays avait réussi seul sa transition industrielle hors de l'Occident ?", ["Le Japon", "La Chine", "L'Inde", "Le Brésil"], "La fragmentation de la production ouvre aujourd'hui des niches aux pays du Sud."),
 ("c2b", "Qu'a reconstitué Angus Maddison ?", ["Le PIB par tête de toutes les zones du monde sur le très long terme (de l'an 1 à 1998)", "Le cours des actions américaines", "Les salaires des ouvriers de Ford", "Le nombre d'ordinateurs par pays"], "Ses graphiques sont en échelle semi-logarithmique."),
 ("c2b", "Quelle innovation est au cœur du mouvement des « Makers » (Chris Anderson, 2012) ?", ["Les imprimantes 3D", "Le télégraphe", "Les smartphones", "Les robots industriels"], "Organisés en FabLabs ; Obama en parle le 12 février 2013."),
 ("c2b", "Quel était l'enchaînement du fordisme ?", ["Une partie des gains de productivité reversée en salaires", "Des salaires bloqués pour financer la recherche", "La sous-traitance généralisée", "La production dans les pays du Sud"], "Grâce notamment aux syndicats, d'où l'intérêt des keynésiens."),
 ("c2b", "Que propose Rodrik face à la fin du fordisme ?", ["Un nouveau contrat social adapté aux nouvelles inégalités", "Le retour à la grande usine", "Le protectionnisme", "La suppression de la protection sociale"], "Le contrat social d'après-guerre est fragilisé."),
 ("c2b", "Quelle citation clôt le chapitre 2 ?", ["« The fault... is not in our stars, but in ourselves »", "« Où est la sagesse que nous avons perdue dans la connaissance ? »", "« Un pays a la conjoncture de ses structures »", "« You can see the computer age everywhere »"], "Shakespeare, au générique de Spellbound (Hitchcock, 1945)."),
]

CARDS = [
 ("c1a", "Hernando de Soto en 5 points", "Péruvien, né en 1941 à Arequipa, libéral.\nILD fondé à Lima en 1980.\nL'Autre Sentier (1986), Le Mystère du capital (2000).\n4e à la présidentielle de 2021 (11,6 %).\nInspire l'USAID et la Banque mondiale."),
 ("c1a", "L'expérience de de Soto à Lima", "Une petite entreprise textile, 2 machines à coudre.\n289 jours à 6 h par jour pour 1 salarié.\n1 230 $ = 31 salaires minimum.\n207 opérations, 2 ans à plein temps."),
 ("c1a", "Les chiffres du parcours du combattant", "Lima : 728 étapes pour un titre de logement ; 90 % des petites entreprises industrielles illégales.\nPhilippines : presque 100 étapes, 13 à 25 ans.\nÉgypte : 5 à 14 ans.\nHaïti : 111 étapes, 4 112 jours ; 19 ans au total."),
 ("c1a", "La cloche de verre (Braudel)", "Le capitalisme a vécu « en système clos, voire enkysté », réservé à quelques secteurs : des poches de richesse dans un océan de pauvreté."),
 ("c1a", "Le capital mort", "Des biens possédés mais sans titre : ils ne peuvent ni circuler, ni être vendus à un inconnu, ni servir de garantie. Jusqu'à 90 % de l'économie de certains pays."),
 ("c1a", "Le capital selon de Soto", "Un surplus réinvesti pour créer plus de richesse.\nIl naît du titre de propriété, qui rend les biens fongibles.\n« Extraire un potentiel invisible ».\n70 % des entreprises américaines naissent d'un emprunt gagé sur une hypothèque."),
 ("c1a", "Pourquoi le droit des pays pauvres est défaillant", "Hérité du droit colonial (fait pour extraire).\nPensé pour protéger, pas pour faire circuler.\nComparaison : l'Europe de Colbert, la conquête de l'Ouest."),
 ("c1b", "La légalisation : CN mais pas CS", "Nécessaire : recenser les droits existants, créer un système légal, protocole progressif.\nPas suffisante : il faut des chefs d'État courageux (Myerson), des juristes ouverts, l'adhésion de la population, une démocratie économique et juridique."),
 ("c1b", "Le contrat social (de Soto, Rodrik, Polanyi)", "Sans contrat social, le capitalisme sera combattu.\nLe vrai contrat social, c'est le système juridique.\nPolanyi : les inégalités font le lit du fascisme."),
 ("c1b", "Les 4 extensions de de Soto", "France : le laisser-passer A 38.\nEurope : pas de marché juridique unifié.\nPrintemps arabes : petits commerçants sans titres.\nSubprimes : un tiers-monde de la finance en Occident."),
 ("c1b", "Document n°6 : de Soto contre Piketty", "Piketty : r > g, les inégalités se creusent seules.\nDe Soto : il oublie les 90 % du monde dans l'informel.\nÉgypte : 47 % du revenu « du travail » vient du capital, 360 Md$ d'immobilier.\nBouazizi : un entrepreneur exproprié."),
 ("c1b", "Les 4 leçons du document n°6", "1. C'est l'absence de capital qui cause la pauvreté.\n2. Capital et travail ne sont pas ennemis.\n3. L'obstacle : l'incapacité à accumuler et protéger son capital.\n4. Le respect de l'individu n'est pas propre à l'Occident."),
 ("c1b", "Du papier sans actifs, des actifs sans papier", "Occident : capital fictif, des titres sans valeur réelle (dérivés, crise de 2008).\nAilleurs : des biens réels sans titres (capital mort).\nModèle : la France de la Révolution (Coquelin)."),
 ("c2a", "Nouvelle économie : les deux définitions", "Presse : le secteur des NTIC (10-15 % du PIB américain, 5-6 % du français).\nÉconomistes : une 3e révolution industrielle, technique + nouvelle organisation du travail."),
 ("c2a", "Les deux premières révolutions industrielles", "1re : Angleterre, 1760-1830 (vapeur, train, métier à tisser).\n2e : Europe et États-Unis, 1860-1900 (moteur à explosion, électricité, téléphone, eau courante).\nÂge d'or de la productivité : 1913-1972."),
 ("c2a", "Le paradoxe de Solow", "1987 : « You can see the computer age everywhere but in the productivity statistics ».\nFin du paradoxe dans les années 2000 (États-Unis : 4 % de croissance par an entre 1995 et 2005)."),
 ("c2a", "Les arguments de Gordon", "Effet de moyenne (seul le secteur NTIC progresse).\nRendements décroissants des ordinateurs.\nInternet au bureau : 30 à 40 % d'usage perso.\nLe télégraphe a fait mieux (× 3 000).\n1870-1970, une parenthèse dorée."),
 ("c2a", "Krugman contre Gordon (2013)", "« Indoor plumbing beats iPads » résume Gordon.\nMais les androïdes arrivent (voix, traduction, voiture autonome).\nOptimiste pour la croissance, inquiet pour les salaires."),
 ("c2a", "Les caractéristiques des biens NTIC", "Investissements à fonds perdus.\nÉconomies d'échelle (coûts fixes, coûts variables quasi nuls).\nEffets de réseau (Metcalfe : valeur = carré des utilisateurs).\n→ monopoles et barrières à l'entrée."),
 ("c2a", "La rente des pays producteurs de NTIC", "Bénéfices géants, amortisseur macro pour la classe moyenne, réinvestissement en recherche (cercle vertueux), first mover advantage. Les États-Unis en profitent le plus."),
 ("c2b", "Le modèle O-ring (Kremer)", "Nobel 2019. Un joint défaillant fait perdre une navette.\nUn maillon faible détruit tout : qualifications homogènes, appariements sélectifs, fragmentation de la production en réseau."),
 ("c2b", "Pyramide fordiste contre réseau O-ring", "Avant : trois pyramides au Nord, le Sud exclu (Renault Billancourt).\nAujourd'hui : un réseau de sous-traitants, d'usines et de centres d'appel entre le Nord, le Sud et les pays très pauvres (Boeing 787, Falcon 7X, Volvo S40)."),
 ("c2b", "Les nouvelles inégalités", "De petits écarts de performance, de grands écarts de revenus (l'informaticien de la navette contre celui de Carrefour).\nCarrières incertaines.\nLutte intra-classes plutôt qu'entre classes."),
 ("c2b", "Révolution industrielle et mondialisation", "La RI permet la mondialisation, pas l'inverse.\nLa fragmentation de la supply chain ouvre des niches au Sud.\nErreur inverse → protectionnisme."),
 ("c2b", "La fin du fordisme", "Fordisme : gains de productivité partagés avec les salaires (Ford, syndicats, keynésiens).\nSa fin fragilise le contrat social d'après-guerre.\nRodrik : un nouveau contrat social."),
 ("c2b", "La conclusion du cours", "La productivité repose sur les institutions (démocratie économique).\n« The fault... is not in our stars, but in ourselves » (Shakespeare, Spellbound)."),
]

def build():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    quiz = []
    for n, (ch, q, choices, expl) in enumerate(QUIZ, 1):
        assert len(choices) == 4 and len(set(choices)) == 4, q
        quiz.append({"id": f"macro-q{n:02d}", "ch": ch, "q": q, "choices": choices, "answer": 0, "explain": expl})
    cards = [{"id": f"macro-f{n:02d}", "ch": ch, "front": f, "back": b} for n, (ch, f, b) in enumerate(CARDS, 1)]
    data = {
        "id": "macro",
        "exam": "1h30 · en anglais · deux sujets au choix (chapitre 1 ou 2) · raisonnements argumentés, exemples du cours et de la vie quotidienne",
        "chapters": [{"id": i, "title": t} for i, t in CHAPTERS],
        "quiz": quiz,
        "cards": cards,
    }
    json.dump(data, open(os.path.join(root, "data", "macro.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(quiz), "QCM,", len(cards), "cartes")

if __name__ == "__main__":
    build()

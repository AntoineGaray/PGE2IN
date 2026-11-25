# Parcours guidé – Méthodes quantitatives III (Mme Levavasseur)
# Source unique : la fiche détaillée (data/fiches/mq.json) = Davenport et Kim, Keeping Up with the Quants, chap. 6.
# La partie calcul n'est PAS couverte (aucun support). La sous-partie « Questions probables » (hypothèses de Claude) est exclue.
# Ne jamais renommer ni réutiliser un identifiant (mq-pNN-qN) : les points en dépendent.
# Construction : python3 tools/build_path.py mq

DK = "Davenport et Kim, chapitre 6 : devenir un bon analyste quantitatif"

STEPS = [
 ("le-schema-de-depart", DK, "Le schéma de départ", None, [
   ("Quelles sont les trois étapes pour devenir un bon analyste selon Davenport et Kim ?",
    ["Quantitative attitude, quantitative habits, quantitative analyst", "Maths, statistiques, informatique", "Collecte, analyse, présentation", "Lire, calculer, publier"], 0,
    "L'attitude forme les habitudes, et la répétition fait l'analyste compétent."),
   ("De quel penseur les auteurs partent-ils (pensées → actions → habitudes → caractère → destin) ?",
    ["Aristote", "Voltaire", "Henry Ford", "Taleb"], 0,
    "Pour l'analyste : l'attitude quantitative forme les habitudes quantitatives."),
   ("Quel livre de vulgarisation est cité pour l'étape 1 ?",
    ["How to Lie with Statistics (Huff, 1954)", "Moneyball", "The Invisible Gorilla", "Statistics for Business and Economics"], 0,
    "Kohler (Statistics for Business and Economics) est le manuel conseillé pour l'étape 2."),
  ], ("Selon la thèse du chapitre, devenir un bon analyste est-il d'abord une question de niveau en maths ?",
      "Non : c'est une attitude (ne pas avoir peur des chiffres), des habitudes (exiger des chiffres et s'en méfier) et des connaissances qui progressent ensemble.")),

 ("etape-1-l-attitude-quantitative", DK, "Étape 1 – L'attitude quantitative", None, [
   ("Emily Rosa obtient 122 bonnes réponses sur 280 essais. Pourquoi cela ne prouve-t-il rien en faveur du therapeutic touch ?",
    ["44 % de réussite, c'est moins que le hasard (50 %)", "L'échantillon est trop grand", "Elle avait 9 ans", "Il n'y avait pas d'assignation aléatoire"], 0,
    "21 praticiens, assignation aléatoire à pile ou face, publié dans le JAMA en 1998."),
   ("Avec combien de personnes la probabilité que deux aient le même anniversaire dépasse-t-elle 50 % ?",
    ["23", "183", "50", "365"], 0,
    "Le paradoxe des anniversaires : on est « fooled by randomness »."),
   ("Usain Bolt court 100 m en environ 10 s. Quelle vitesse ?",
    ["Environ 36 km/h", "Environ 10 km/h", "Environ 60 km/h", "Environ 20 km/h"], 0,
    "0,1 km en 1/360 d'heure = 36 km/h."),
   ("Si ton revenu est très au-dessus de la moyenne, celui de ton enfant sera probablement plus bas. C'est…",
    ["La régression vers la moyenne", "La marche aléatoire", "Le paradoxe des anniversaires", "Une corrélation causale"], 0,
    "Penser en probabilités, base de la statistique inférentielle."),
  ], ("Que montre l'exemple de DJ Patil ?",
      "Qu'on peut toujours rattraper un mauvais départ : il a échoué en maths au collège et au lycée, s'est rattrapé seul jusqu'à un doctorat et a inventé le terme data scientist chez LinkedIn.")),

 ("etape-2-les-habitudes-quantitatives", DK, "Étape 2 – Les habitudes quantitatives", None, [
   ("« The plural of anecdote is not data » illustre l'habitude…",
    ["Demand numbers", "Never trust numbers", "Practice", "Ask questions"], 0,
    "Face à une intuition : avez-vous des données ?"),
   ("Que faut-il pour conclure à une causalité ?",
    ["Une expérience avec groupe test, groupe contrôle et assignation aléatoire", "Une forte corrélation", "Un grand échantillon", "Une moyenne élevée"], 0,
    "Correlation is not causation."),
   ("Comment s'appelle le sophisme « c'est arrivé en même temps, donc c'est la cause » ?",
    ["Cum hoc ergo propter hoc", "Fooled by randomness", "Moneyball", "Régression vers la moyenne"], 0,
    "Exemple : boire et cancer, avec une variable cachée (le tabac)."),
   ("Devant une moyenne, que faut-il demander ?",
    ["La dispersion, les outliers, les données manquantes et la médiane", "Seulement l'échantillon", "Seulement la source", "Rien, la moyenne suffit"], 0,
    "Devant une enquête : qui, comment, quelle formulation."),
  ], ("Quels sont les trois angles de doute de « never trust numbers » ?",
      "Relevance (le chiffre répond-il à la question, représente-t-il le groupe ?), accuracy (qui l'a produit, comment ?), correct interpretation (un même chiffre peut se lire dans deux sens).")),

 ("les-10-questions-a-poser-sur-une-analyse-quantitative", DK, "Les 10 questions à poser", None, [
   ("Laquelle fait partie des 10 questions à poser sur une analyse ?",
    ["L'échantillon est-il représentatif de la population ?", "Combien a coûté l'étude ?", "Quel logiciel a été utilisé ?", "Combien de pages fait le rapport ?"], 0,
    "Avec : la source, les outliers, les hypothèses, les approches écartées…"),
   ("Quelle est la première des 10 questions ?",
    ["Avez-vous des données pour appuyer cette hypothèse ?", "Quelle est la source des données ?", "Pourquoi cette approche ?", "Y a-t-il des outliers ?"], 0,
    "Le réflexe « demand numbers »."),
  ], ("Cite au moins cinq des 10 questions à poser.",
      "Données pour appuyer l'hypothèse ? Source ? Échantillon représentatif ? Outliers et leur poids ? Hypothèses de l'analyse ? Conditions où elles seraient invalides ? Pourquoi cette approche ? Transformations des données ? Autres approches écartées ? Probabilité que les variables indépendantes causent vraiment les variations ?")),

 ("les-6-etapes-d-une-analyse-quantitative", DK, "Les 6 étapes d'une analyse", None, [
   ("Quelle étape détermine la méthode statistique à utiliser plus tard ?",
    ["Problem recognition (and framing)", "Data analysis", "Data collection", "Results presentation"], 0,
    "Comprendre quel est le problème et pourquoi il compte."),
   ("Selon les auteurs, une question bien définie et des travaux bien revus, c'est…",
    ["Plus de la moitié du travail", "Un dixième du travail", "Inutile si on a les données", "La dernière étape"], 0,
    "Étapes 1 et 2."),
   ("Pour une relation de dépendance entre variables, quelle méthode ?",
    ["La régression", "Les tests de comparaison", "Une enquête", "La visualisation"], 0,
    "Pour comparer des groupes : les tests de comparaison."),
   ("Combien de temps consacrer à la présentation des résultats ?",
    ["Autant qu'aux cinq autres étapes", "Quelques minutes", "La moitié de l'étape 1", "Aucun, les chiffres parlent seuls"], 0,
    "Référence : les livres d'Edward Tufte."),
  ], ("Donne les 6 étapes dans l'ordre.",
      "1. Problem recognition (framing), 2. Review of previous findings, 3. Modeling (variable selection), 4. Data collection (measurement), 5. Data analysis, 6. Results presentation and action.")),

 ("etape-3-l-analyste-quantitatif", DK, "Étape 3 – L'analyste quantitatif", None, [
   ("Pourquoi rédiger un rapport, selon les auteurs ?",
    ["Pour apprendre à « raconter une histoire avec des données »", "Pour obtenir une certification", "Pour remplacer les séminaires", "Pour éviter les calculs"], 0,
    "Progresser, aider l'entreprise, diffuser une culture analytique."),
   ("Quel auteur est cité : on juge les gens à leurs questions plus qu'à leurs réponses ?",
    ["Voltaire", "Aristote", "Henry Ford", "Taleb"], 0,
    "Henry Ford est cité sur le travail en communauté."),
  ], ("Quelles sont les trois actions de l'étape 3 ?",
      "Rédiger un rapport, former une communauté d'analystes (prioriser, se répartir les 6 étapes, se présenter les travaux), organiser des séminaires réguliers, dont certains pour les non-techniciens.")),

 ("les-deux-exemples-finaux-analyses-avec-les-6-etapes", DK, "Les deux exemples finaux", None, [
   ("Sur quelles étapes Nuri s'est-elle préparée pour obtenir sa bourse ?",
    ["La collecte (4) et l'analyse (5)", "Le framing (1) et la revue (2)", "La présentation (6)", "Toutes sauf l'analyse"], 0,
    "Ce sont les étapes que font surtout les doctorants : stats, SPSS, lecture de 20 articles."),
   ("Quelle statistique Morey utilise-t-il pour évaluer Battier ?",
    ["Le plus/minus ajusté par régression", "Les points par match", "Les rebonds", "Le salaire"], 0,
    "+8 en 2006-2007, 17e de la ligue, pour un salaire moyen."),
   ("Quel a été le résultat du transfert de Battier ?",
    ["Les Rockets passent de 34-48 à 52-30", "Les Rockets perdent plus de matchs", "Battier est renvoyé", "Aucun effet mesurable"], 0,
    "Puis 55-27 avec 22 victoires d'affilée."),
  ], ("Pourquoi les statistiques individuelles de Battier étaient-elles trompeuses ?",
      "Il tournait autour de 10 points et moins de 5 rebonds par match, mais son équipe jouait mieux quand il était sur le terrain : au basket, la performance individuelle explique mal celle de l'équipe.")),
]

## Ce que couvre le Drive et ce qui manque

**Cette fiche ne te prépare pas à la partie calcul du partiel.** Le dossier ne contient qu'un seul document : le chapitre 6 de *Keeping Up with the Quants* (Davenport et Kim, Harvard Business Review Press, 2013), intitulé « Developing Quantitative Analysis Capabilities ».

- La calculatrice est autorisée à l'examen, il y aura donc probablement des calculs (statistiques descriptives, probabilités, tests, régression…). Aucun support de calcul n'est dans le Drive.
- Ce chapitre est une « methodology case study » : il porte sur la démarche et l'esprit critique face aux chiffres, pas sur les formules.
- **À faire** : ajoute les slides du cours, les TD et leurs corrigés, et les annales si tu en as. Je ferai alors une fiche formules et méthodes. Sans ces supports, je pourrais seulement deviner le programme, et je ne veux pas te faire réviser au hasard.

Le chapitre est en anglais. Les termes clés restent en anglais pour que tu les reconnaisses dans l'énoncé.

## Davenport et Kim, chapitre 6 : devenir un bon analyste quantitatif

La thèse du chapitre : on devient un bon analyste par une **attitude** (ne pas avoir peur des chiffres), des **habitudes** (exiger des chiffres et s'en méfier) et des **connaissances** qui progressent ensemble. Ce n'est pas d'abord une question de niveau en maths.

### Le schéma de départ

Les auteurs partent d'Aristote : nos pensées forment nos actions, nos actions nos habitudes, nos habitudes notre caractère, et notre caractère notre destin. Pour l'analyste, l'attitude quantitative forme les habitudes quantitatives, et la répétition fait l'analyste compétent. Les connaissances et les méthodes s'améliorent à chaque étape.

| Étape | Ce qu'on développe | Connaissances associées |
| --- | --- | --- |
| 1. Quantitative attitude | Ne pas avoir peur des chiffres, chercher les notions inconnues, être curieux, penser en probabilités | Livres de vulgarisation statistique : Huff, *How to Lie with Statistics* (1954) ; Campbell, *Flaws and Fallacies in Statistical Thinking* (1974) ; Good et Hardin, *Common Errors in Statistics* |
| 2. Quantitative habits | Exiger des chiffres, s'en méfier, se méfier de la causalité, poser des questions, pratiquer | Statistique élémentaire et méthodes de recherche (manuel conseillé : Kohler, *Statistics for Business and Economics*). Faire tous les exercices et relire trois fois |
| 3. Quantitative analyst | Rédiger un rapport, créer une communauté d'analystes, organiser des séminaires | Étudier des cas réels en groupe, apprendre les méthodes avancées au moment où on en a besoin, inviter des experts |

### Étape 1 – L'attitude quantitative

- **Ne pas avoir peur des chiffres.** Le raisonnement quantitatif est différent des connaissances mathématiques. Selon une source citée, il demande très peu de maths au-delà du niveau 6e. Ce qui compte, c'est d'extraire de l'information des données.
- **Emily Rosa** : à 9 ans, elle teste le « therapeutic touch », des thérapeutes qui disent sentir le champ d'énergie d'un patient. 21 praticiens, 280 essais, une **assignation aléatoire** à pile ou face de la main cible. Résultat : 122 bonnes réponses, soit **44 %**, alors que le hasard donne **50 %**. Les affirmations sont donc sans fondement. L'étude est publiée dans le *JAMA* en 1998, elle avait 11 ans.
- **DJ Patil** (il a inventé le terme *data scientist* chez LinkedIn) : il a échoué en maths au collège et au lycée, puis s'est rattrapé seul jusqu'à un doctorat. Le message : on peut toujours rattraper un mauvais départ.
- **Chercher les notions inconnues** : noter les termes et les chiffres qu'on ne comprend pas dans l'actualité, puis les chercher. En six mois, on devient la personne bien informée de son entourage.
- **Être curieux** : Usain Bolt court 100 m en 9,58 s. En arrondissant à 10 s, cela fait 0,1 km en 1/360 d'heure, soit **36 km/h** environ. Le record du marathon (2 h 03 min 59 s) correspond à environ **20,4 km/h**.
- **Penser en probabilités** : la plupart des adultes sont « fooled by randomness » (Taleb). Ils donnent un sens à ce qui peut arriver par hasard.
    - **Le paradoxe des anniversaires** : avec 23 personnes, la probabilité que deux aient le même anniversaire dépasse 50 %.
    - **La marche aléatoire** de la Bourse : certains gérants battent le marché plusieurs années de suite, puis finissent par rechuter.
    - **La régression vers la moyenne** : si ton revenu est très au-dessus de la moyenne, celui de ton enfant sera probablement plus bas.
    - La probabilité est la base de la **statistique inférentielle**.

### Étape 2 – Les habitudes quantitatives

Les auteurs reprennent l'idée qu'il est plus facile d'agir pour changer sa façon de penser que l'inverse.

1. **Demand numbers** : face à une idée ou une intuition, demander « avez-vous des données pour appuyer cette hypothèse ? ». Formule du chapitre : « The plural of anecdote is not data. » S'appliquer la règle à soi-même : faire une petite expérience si les données n'existent pas.
2. **Never trust numbers** : ne pas prendre un chiffre pour argent comptant. Il peut être manipulé, dépassé ou tiré d'un échantillon non représentatif. Trois angles de doute :
    - **Relevance** : le chiffre répond-il à la question, et représente-t-il le groupe visé ?
    - **Accuracy** : qui l'a produit, et comment ?
    - **Correct interpretation** : un même chiffre peut être lu dans deux sens. Exemple : « seule 1 épouse sur 22 vote différemment de son mari » peut aussi se lire « seul 1 mari sur 22 ose voter contre sa femme ».
3. **Se méfier des arguments de causalité** : **correlation is not causation**. Seule une expérience avec un groupe test, un groupe contrôle et une assignation aléatoire permet de conclure à une cause. Test de Chabris et Simons (*The Invisible Gorilla*) : aurait-on pu assigner les gens au hasard à l'une des conditions ? Si c'est impossible, trop cher ou contraire à l'éthique, l'étude n'est pas une expérience et la causalité n'est pas démontrée. Exemple : « boire beaucoup cause le cancer », alors que les gros buveurs sont peut-être aussi de gros fumeurs (une variable cachée). Le sophisme porte un nom : *cum hoc ergo propter hoc*.
4. **Ask questions** : devant une **moyenne**, demander la dispersion (l'**écart-type**), les **valeurs aberrantes** (outliers), les données manquantes et la **médiane**. Devant une **enquête**, demander qui l'a faite, comment, et avec quelle formulation des questions.
5. **Practice** : refaire les six étapes de l'analyse sur de vrais problèmes.

### Les 10 questions à poser sur une analyse quantitative

1. Avez-vous des données pour appuyer cette hypothèse ?
2. Quelle est la source des données ?
3. L'échantillon est-il représentatif de la population ?
4. Y a-t-il des valeurs aberrantes, et comment pèsent-elles sur les résultats ?
5. Quelles hypothèses sous-tendent l'analyse ?
6. Dans quelles conditions ces hypothèses et le modèle seraient-ils invalides ?
7. Pourquoi avoir choisi cette approche ?
8. Quelles transformations des données ont été nécessaires pour que le modèle colle ?
9. Quelles autres approches avez-vous envisagées, et pourquoi les avoir écartées ?
10. Quelle est la probabilité que les variables indépendantes causent vraiment les variations de la variable dépendante ? Peut-on faire d'autres analyses sur la causalité ?

### Les 6 étapes d'une analyse quantitative

1. **Problem recognition** (and framing) : comprendre quel est le problème et pourquoi il compte. C'est cette étape qui détermine la méthode statistique à utiliser plus tard.
2. **Review of previous findings** : rechercher les travaux existants, identifier les variables pertinentes et leurs liens. Selon les auteurs, une question bien définie et des travaux bien revus, c'est plus de la moitié du travail.
3. **Modeling (variable selection)** : écarter les variables qui ne servent pas la résolution, comme on dessine une caricature. Le choix dépend du but. Pour un train miniature, l'échelle compte. Pour la rentabilité d'un vrai train, ce sont le tonnage, la vitesse et la consommation.
4. **Data collection (measurement)** : vérifier d'abord si les données existent déjà en interne ou en public. Les acheter coûte presque toujours moins cher que les collecter. Sinon, soigner la conception de l'enquête (formulation des questions) ou consulter un spécialiste pour une expérience.
5. **Data analysis** : chercher des régularités et des relations entre variables. Pour **comparer des groupes**, utiliser les tests de comparaison. Pour une **relation de dépendance** entre variables, utiliser la **régression**.
6. **Results presentation and action** : y consacrer autant de temps qu'aux cinq autres étapes. Apprendre la visualisation des données, avec les livres d'Edward Tufte comme référence.

### Étape 3 – L'analyste quantitatif

- **Rédiger un rapport** pour apprendre à « raconter une histoire avec des données ». Trois buts : progresser en traitant un vrai problème, contribuer à résoudre un problème de l'entreprise, diffuser une culture analytique. Bien choisir la question, car selon Voltaire on juge les gens à leurs questions plus qu'à leurs réponses.
- **Former une communauté** d'analystes : prioriser les sujets, se répartir les six étapes, se présenter les travaux. Citation de Henry Ford sur le fait de se réunir, rester ensemble et travailler ensemble.
- **Organiser des séminaires réguliers**, dont certains accessibles aux non-techniciens.

### Les deux exemples finaux, analysés avec les 6 étapes

**Nuri et la bourse d'études.** Jinho Kim a analysé comment ses filles pouvaient obtenir une bourse de doctorat aux États-Unis. Dans la recherche, le professeur mène les étapes 1 à 3 et la rédaction. Les doctorants font surtout la collecte (4) et l'analyse (5), les étapes les plus longues. Nuri s'est donc préparée exactement là-dessus : cours de statistiques et de méthodes de recherche, formation au logiciel SPSS, lecture critique de 20 articles récents. Résultat : une bourse à Wisconsin, puis une fellowship à Stanford. Sa sœur a obtenu une fellowship à Michigan.

**Daryl Morey et Shane Battier (Houston Rockets).** Morey est le « Billy Beane du basket », en référence à *Moneyball*.

| Étape | Application |
| --- | --- |
| 1. Problem recognition | Faut-il recruter Battier, dont les statistiques individuelles sont faibles ? |
| 2. Previous findings | L'analyse sportive marche bien quand la performance individuelle explique celle de l'équipe, mais c'est plus difficile au basket. Battier tournait autour de 10 points et moins de 5 rebonds par match, pourtant son équipe jouait mieux quand il était sur le terrain |
| 3. Modeling | Coût d'acquisition, salaire, statistiques individuelles, et surtout la performance de l'équipe avec et sans lui |
| 4. Data collection | La statistique **plus/minus** : la performance de l'équipe quand le joueur est sur le terrain, comparée à quand il est sur le banc |
| 5. Data analysis | Un plus/minus **ajusté par régression** (qualité des coéquipiers et des adversaires) de **+8** en 2006-2007, 17e de la ligue, pour un salaire moyen. Le joueur échangé était 45e |
| 6. Presentation and action | Le transfert est fait. Les Rockets passent de 34-48 à 52-30 (2007-2008), puis 55-27 avec une série de 22 victoires d'affilée. Battier gagne ensuite le titre NBA avec Miami en 2012 |

### Questions probables à l'examen sur ce texte

Ce sont mes hypothèses, pas des sujets confirmés.

- Appliquer les 6 étapes à un cas donné (le plus probable).
- Expliquer pourquoi une corrélation ne prouve pas une causalité, et ce qu'il faudrait pour la prouver.
- Lister les questions à poser devant une moyenne ou une enquête.
- Interpréter l'expérience d'Emily Rosa : pourquoi 44 % ne prouve rien, et pourquoi l'assignation aléatoire compte.
- Un petit calcul de conversion ou de probabilité, dans l'esprit de l'exemple Usain Bolt ou du paradoxe des anniversaires.

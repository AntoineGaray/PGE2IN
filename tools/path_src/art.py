# Parcours guidé – Art et culture en Asie (M. Sridi)
# Source unique : la fiche détaillée (data/fiches/art.json, version du 23/11/2026).
# Point connu : la fiche place Confucius pendant les Royaumes combattants ; il a vécu juste avant (551-479 av. J.-C.).
# Ne jamais renommer ni réutiliser un identifiant (art-pNN-qN) : les points en dépendent.
# Construction : python3 tools/build_path.py art

CH1 = "Chine : des origines aux Han"
CH2 = "Chine : des Six Dynasties aux Ming"
CH3 = "Chine : des Qing à aujourd'hui"
JP = "Japon : des Jomon à aujourd'hui"
CI = "Corée et Inde"
C = "Complément"

STEPS = [
 ("les-origines-mythiques", CH1, "Les origines mythiques", None, [
   ("Que signifie Zhong Guo (中国), le nom de la Chine ?",
    ["Le Royaume du Milieu", "L'Empire céleste", "La terre jaune", "Le pays des Han"], 0,
    "La Chine se définit par sa culture plutôt que par un territoire."),
   ("Qui est Huang Di ?",
    ["L'Empereur jaune, empereur mythique vers 2700 av. J.-C.", "Le premier empereur Qin", "Le fondateur des Han", "Un philosophe taoïste"], 0,
    "Les slides le présentent avec Yan Di et montrent son mausolée."),
   ("Comment considère-t-on aujourd'hui la dynastie Xia ?",
    ["Comme semi-légendaire", "Comme la plus longue dynastie", "Comme la première dynastie non Han", "Comme une dynastie mongole"], 0,
    "Vers 2000-1600 av. J.-C."),
  ], ("Pourquoi parle-t-on de « 5 000 ans de civilisation » chinoise plutôt que d'un territoire ?",
      "Parce que les frontières ont changé en permanence : la Chine se définit par sa culture plutôt que par un territoire.")),

 ("dynastie-shang-1600-xie-s-av-j-c-la-civilisation-de-l-ecritu", CH1, "Dynastie Shang", None, [
   ("Sur quoi trouve-t-on la plus ancienne trace d'écriture chinoise ?",
    ["Des carapaces de tortue et des omoplates de bœuf (inscriptions oraculaires)", "Des rouleaux de soie", "Des lamelles de bambou", "Des tablettes d'argile"], 0,
    "Sous les Shang (1600 – XIe s. av. J.-C.)."),
   ("Quels arts caractérisent les Shang ?",
    ["Les bronzes et le jade sculpté", "La céramique bleu et blanc", "L'Opéra de Pékin", "Les laques et la peinture sur soie"], 0,
    "Ils révèlent des progrès techniques et une main-d'œuvre spécialisée nombreuse."),
   ("Que prouve le fait que l'écriture Shang soit encore lisible aujourd'hui ?",
    ["Une culture commune très ancienne", "Que l'écriture n'a jamais changé de forme", "Que les Shang étaient tous alphabétisés", "Que l'écriture vient du Japon"], 0,
    "Les caractères, d'abord très pictographiques, sont devenus abstraits."),
  ], ("Que révèle l'art des Shang sur leur société ?",
      "Des progrès techniques (extraction minière, assemblage du bronze) et une main-d'œuvre spécialisée nombreuse.")),

 ("dynastie-zhou-vers-1050-256-av-j-c-la-plus-longue", CH1, "Dynastie Zhou", None, [
   ("Qu'est-ce que le Mandat du Ciel (Tian) ?",
    ["La justification du pouvoir par un mandat céleste, au nom de la supériorité morale", "Un traité de paix avec les Shang", "Le nom de la capitale Zhou", "Un code de lois écrit"], 0,
    "Ce principe légitimera le pouvoir impérial jusqu'au XXe siècle."),
   ("Combien de temps les Zhou restent-ils au pouvoir ?",
    ["Près de 8 siècles", "Environ 4 siècles", "Moins de 40 ans", "15 ans"], 0,
    "C'est la plus longue dynastie."),
   ("Qui fonde le taoïsme, avec le yin et le yang ?",
    ["Lao Zi", "Confucius", "Qin Shi Huang", "Liu Bang"], 0,
    "Il faut suivre le Dao, la voie. C'est encore la plus grande religion née en Chine."),
   ("La pensée de Confucius fonde…",
    ["Une forme de méritocratie au cœur du système social chinois", "Le taoïsme", "Le bouddhisme chinois", "L'école légiste des Qin"], 0,
    "Attention : Confucius (551-479 av. J.-C.) a vécu juste avant la période des Royaumes combattants."),
  ], ("Pourquoi la période des Royaumes combattants est-elle un paradoxe ?",
      "Le pouvoir central s'affaiblit et les seigneurs s'affrontent, et pourtant c'est un âge d'or de la philosophie.")),

 ("dynastie-qin-221-206-av-j-c-le-modele-de-l-empire", CH1, "Dynastie Qin", None, [
   ("En quelle année Ying Zheng devient-il Qin Shi Huang Di, « le premier empereur » ?",
    ["221 av. J.-C.", "246 av. J.-C.", "206 av. J.-C.", "202 av. J.-C."], 0,
    "En 246 il devient roi à 13 ans ; en 221 il soumet le dernier État (Qi)."),
   ("Quel héritage de sa quête d'immortalité a été découvert au XXe siècle ?",
    ["L'armée de terre cuite, près de Xi'an", "La Cité interdite", "Le Grand Canal", "Le mausolée de l'Empereur jaune"], 0,
    "La quête est un échec, mais elle laisse ce site."),
   ("Quelle mesure des Qin favorise aussi le commerce ?",
    ["L'unification de l'écriture", "La route de la soie", "L'ouverture aux Européens", "L'interdiction du commerce"], 0,
    "L'écriture Qin est imposée partout."),
  ], ("Quel est l'héritage politique des Qin ?",
      "Une administration ultra-centralisée et efficace (grands travaux, Grande Muraille), la méritocratie et l'école légiste, et l'unification de l'écriture.")),

 ("dynastie-han-202-av-j-c-220-apr-j-c-le-cur-de-la-culture-chi", CH1, "Dynastie Han", None, [
   ("Sous quel empereur le confucianisme devient-il l'idéologie officielle unique ?",
    ["Wu", "Liu Bang", "Qin Shi Huang", "Kangxi"], 0,
    "Jusqu'à la chute des Qing en 1912."),
   ("Qui sont les Xiongnu ?",
    ["Une fédération de tribus semi-nomades du nord", "Les fondateurs des Han", "Des marchands de la route de la soie", "Des moines bouddhistes"], 0,
    "Ils battent les Han et leur imposent de lourds tributs."),
   ("Par quelle voie le bouddhisme entre-t-il en Chine ?",
    ["La route de la soie", "La mer, avec Zheng He", "Le Japon", "La Corée"], 0,
    "Il se diffuse ensuite dans toute l'Asie de l'Est."),
   ("Comment s'appelle le vêtement traditionnel Han, revenu à la mode ?",
    ["Le Hanfu", "Le Hanzi", "Le Hanyu", "Le kimono"], 0,
    "Hanzi = les caractères ; Hanyu = la langue."),
  ], ("Pourquoi la route de la soie est-elle qualifiée de « première mondialisation » ?",
      "Parce que c'est un réseau de commerce à grande échelle, centré sur la Chine, ouvert vers l'Asie centrale sous l'empereur Wu ; il fait aussi circuler les idées, comme le bouddhisme.")),

 ("de-la-chute-des-han-aux-song", CH2, "De la chute des Han aux Song", None, [
   ("Quelle dynastie construit le Grand Canal ?",
    ["Sui", "Tang", "Song", "Han"], 0,
    "Les Sui réunifient vite par les armes, comme les Qin."),
   ("Quelle dynastie connaît l'imprimerie et le théâtre ?",
    ["Song", "Sui", "Tang", "Yuan"], 0,
    "Les Song sont ensuite vaincus par les Mongols."),
   ("Pourquoi les Tang déclinent-ils ?",
    ["Les empereurs se désintéressent du pouvoir", "Une invasion mongole", "L'hyperinflation", "Les guerres de l'opium"], 0,
    "Ils avaient connu un nouvel âge d'or des arts."),
  ], ("Décris le cycle de l'histoire chinoise vu en cours.",
      "Un empire unifié et brillant, un déclin, une division, puis une réunification par la force. Les Sui répètent les Qin, les Tang répètent les Han.")),

 ("dynastie-yuan-1279-1368-la-chine-sous-les-mongols", CH2, "Dynastie Yuan", None, [
   ("Qui fonde la dynastie Yuan en battant les Song en 1279 ?",
    ["Kubilaï Khan, petit-fils de Gengis Khan", "Gengis Khan", "Hongwu", "Marco Polo"], 0,
    "C'est la première dynastie non Han."),
   ("Pourquoi les peintres s'isolent-ils du pouvoir sous les Yuan ?",
    ["Ils refusent de travailler pour l'envahisseur", "L'art est interdit", "Ils partent en Europe", "Ils deviennent moines"], 0,
    "Sous les Tang et les Song, l'art était contrôlé et encouragé par l'État."),
   ("Quelle céramique apparaît sous les Yuan ?",
    ["La céramique bleu et blanc", "Les céladons", "La porcelaine kraak de Delft", "Le jade sculpté"], 0,
    "Elle deviendra un succès mondial sous les Ming."),
  ], ("Quel rôle joue Marco Polo ?",
      "Il visite la Chine et devient conseiller et ambassadeur de Kubilaï.")),

 ("dynastie-ming-1368-1644-les-derniers-empereurs-han", CH2, "Dynastie Ming", None, [
   ("Quel empereur Ming installe la capitale à Pékin et construit la Cité interdite ?",
    ["Yongle", "Hongwu", "Wanli", "Kangxi"], 0,
    "Il reconstruit aussi la Grande Muraille et lance les expéditions de Zheng He."),
   ("Qui mène les expéditions maritimes vers l'Asie du Sud-Est et l'Afrique de l'Est ?",
    ["L'eunuque Zheng He", "Marco Polo", "Kubilaï Khan", "Le commodore Perry"], 0,
    "Sous Yongle."),
   ("Quelle cause du déclin des Ming apparaît sous Wanli ?",
    ["L'hyperinflation due à la dépendance à l'argent métal importé", "La guerre de l'opium", "L'invasion japonaise", "La fermeture totale du pays"], 0,
    "Puis famines au XVIIe siècle et montée des Mandchous."),
  ], ("Pourquoi la céramique est-elle un enjeu économique sous les Ming ?",
      "Au XVIe siècle, les Ming ouvrent des comptoirs aux Espagnols, Portugais et Hollandais, et la céramique (bleu et blanc) est l'un des produits chinois les plus vendus en Europe.")),

 ("complement-pour-l-expose-ming-hors-resume-du-prof", CH2, "Complément : la porcelaine bleu et blanc", C, [
   ("Avec quoi décore-t-on la porcelaine bleu et blanc ?",
    ["Le bleu de cobalt, importé de Perse au départ", "L'indigo", "Le lapis-lazuli", "Le bleu de Prusse"], 0,
    "Sous une glaçure transparente."),
   ("Où est-elle produite en masse ?",
    ["Dans les fours impériaux de Jingdezhen", "À Delft", "À Xi'an", "À Canton"], 0,
    "Delft la copiera en Europe."),
  ], ("Comment la porcelaine arrive-t-elle en Europe ?",
      "Par les Portugais, puis par la Compagnie néerlandaise des Indes orientales (porcelaine « kraak ») ; elle est ensuite copiée en Europe, par exemple à Delft.")),

 ("dynastie-qing-1644-1912-la-derniere-dynastie", CH3, "Dynastie Qing", None, [
   ("Qui fonde la dynastie Qing en 1644 ?",
    ["Les Mandchous", "Les Mongols", "Les Han", "Les Japonais"], 0,
    "Ils prennent Pékin et la Cité interdite."),
   ("Sous quel empereur les Qing atteignent-ils leur apogée (10 grandes campagnes) ?",
    ["Qianlong", "Shunzhi", "Kangxi", "Cixi"], 0,
    "La population atteint 400 millions à sa mort."),
   ("Pourquoi les Qing pratiquent-ils l'isolationnisme économique ?",
    ["Pour éviter la dépendance qui a fait tomber les Ming", "Par manque de produits à vendre", "Sur ordre des Britanniques", "À cause du bouddhisme"], 0,
    "Le commerce n'est autorisé que dans des zones contrôlées comme Canton."),
   ("Pourquoi les guerres de l'opium (1839-1842 et 1856-1860) ?",
    ["Les Britanniques veulent vendre leur opium, les Qing refusent", "Les Qing envahissent l'Inde", "Le Japon attaque la Chine", "Une révolte paysanne"], 0,
    "Le déséquilibre commercial irritait déjà la Grande-Bretagne."),
  ], ("Comment et quand tombent les Qing ?",
      "En 1912, après la révolution Xinhai et la proclamation de la République de Chine ; la Chine entre dans le XXe siècle isolée et en retard.")),

 ("republique-et-revolution-communiste", CH3, "République et révolution communiste", None, [
   ("Qui préside la République de Chine et tente un régime parlementaire ?",
    ["Sun Yat-sen", "Mao Zedong", "Cixi", "Xi Jinping"], 0,
    "Les nationalistes affrontent ensuite le mouvement communiste de Mao."),
   ("Que se passe-t-il en 1949 ?",
    ["Victoire des communistes, les nationalistes se replient à Taïwan", "Le Japon envahit la Mandchourie", "Fin de la Révolution culturelle", "Chute des Qing"], 0,
    "La Chine est dirigée depuis par le PCC."),
   ("Contre quoi luttent les Gardes rouges pendant la Révolution culturelle ?",
    ["Les « Quatre Vieilleries »", "Les Japonais", "Les nationalistes", "Les Britanniques"], 0,
    "Vieilles idées, culture, coutumes et habitudes. Dates 1966-1976 : complément classique.", C),
  ], ("Pourquoi la guerre civile est-elle mise en pause en 1936 ?",
      "Pour faire face au Japon, qui a envahi la Mandchourie en 1931 ; elle reprend après 1945.")),

 ("la-chine-d-aujourd-hui", CH3, "La Chine d'aujourd'hui", None, [
   ("Quel artiste contemporain chinois est cité dans les slides ?",
    ["Yue Minjun, et ses autoportraits au rire figé", "Hokusai", "PSY", "Zheng He"], 0,
    "Une scène qui mêle modernité, style ancien et critique sociale légère."),
   ("Que se passe-t-il depuis 2013 avec Xi Jinping ?",
    ["Le retour du contrôle et une tentation isolationniste", "Une ouverture totale", "Le retour de l'Empire", "La fin du PCC"], 0,
    "Après la période de réforme et d'ouverture."),
  ], ("Donne deux exemples de réappropriation de la culture ou de soft power chinois aujourd'hui.",
      "La mode du Hanfu (culture ancienne teintée de nationalisme), la science-fiction et le cinéma (soft power), l'art contemporain.")),

 ("les-grandes-periodes", JP, "Les grandes périodes du Japon", None, [
   ("Que signifie « jomon » ?",
    ["Marque de corde", "Terre du soleil", "Peuple de l'île", "Bronze ancien"], 0,
    "La poterie Jomon porte des motifs de cordes dans l'argile."),
   ("Quelle période voit l'arrivée du bouddhisme au Japon ?",
    ["Asuka (538 – 794)", "Heian (794 – 1185)", "Yayoi", "Edo"], 0,
    "Avec l'explosion de l'alphabétisation par les idéogrammes chinois."),
   ("L'emaki de l'époque Heian est considéré comme…",
    ["L'ancêtre du manga", "L'ancêtre du kabuki", "Une céramique", "Un château"], 0,
    "Rouleau peint qui intègre textes et dialogues au XIIe siècle."),
   ("Quel shogunat gouverne pendant l'époque Edo ?",
    ["Tokugawa", "Yamato", "Meiji", "Heian"], 0,
    "Basé à Edo (Tokyo), fermeture totale des années 1630 aux années 1850."),
  ], ("Explique le paradoxe d'Edo.",
      "La fermeture au monde a dopé l'art local : les artistes étaient soutenus par une classe marchande enrichie, et la gravure sur bois rendait les œuvres accessibles à grande échelle.")),

 ("la-fin-d-edo-et-meiji", JP, "La fin d'Edo et Meiji", None, [
   ("Que se passe-t-il en 1853 ?",
    ["Une flotte américaine impose l'ouverture commerciale du Japon", "Le Japon envahit la Corée", "Début du shogunat Tokugawa", "Hiroshima"], 0,
    "C'est le commodore Perry (complément classique)."),
   ("Qu'est-ce que l'ère Meiji ?",
    ["Le retour de l'empereur et la modernisation du Japon", "Une fermeture totale du pays", "L'occupation américaine", "Un shogunat militaire"], 0,
    "Le shogunat humilié rend le pouvoir à l'empereur."),
  ], ("Pourquoi le shogunat Tokugawa perd-il le pouvoir ?",
      "Humilié par l'ouverture imposée par la flotte américaine en 1853 (dans une économie déjà en déclin), il rend le pouvoir à l'empereur et à ses alliés : c'est le début de l'ère Meiji.")),

 ("l-expansion-militaire", JP, "L'expansion militaire", None, [
   ("En 1894, le Japon bat la Chine des Qing et annexe…",
    ["Taïwan", "La Corée", "La Mandchourie", "Hong Kong"], 0,
    "La Corée est contrôlée en 1910, la Mandchourie envahie en 1931."),
   ("Quel événement de 1941 scelle l'avenir du Japon ?",
    ["L'attaque de Pearl Harbor", "L'invasion de la Mandchourie", "La victoire contre la Russie", "Hiroshima"], 0,
    "Extension maximale en 1942, défaite en 1945."),
  ], ("Donne dans l'ordre 4 étapes de l'expansion militaire japonaise.",
      "1894 victoire contre les Qing (Taïwan), 1904-1905 victoire contre la Russie, 1910 contrôle de la Corée, 1931 Mandchourie, 1937 guerre sino-japonaise, 1941 Pearl Harbor, 1945 défaite.")),

 ("le-japon-sous-influence-americaine", JP, "Le Japon sous influence américaine", None, [
   ("Quelle trace politique de l'influence américaine est inscrite dans la Constitution ?",
    ["Le pacifisme", "Le fédéralisme", "Le régime présidentiel", "Le bipartisme"], 0,
    "Fortes influences politiques, économiques et culturelles."),
   ("Quel exemple de soft power japonais cite le cours ?",
    ["Nintendo", "Toyota", "Sony", "Uniqlo"], 0,
    "Avec la culture manga."),
  ], ("Quel exposé de la classe porte sur cette période ?",
      "« Manga Culture and US occupation after WWII » (séance 6).")),

 ("coree-grandir-entre-la-chine-et-le-japon", CI, "Corée", C, [
   ("Quelle dynastie donne son nom à la « Corée » ?",
    ["Goryeo", "Joseon", "Yamato", "Silla"], 0,
    "918 – 1392, le bouddhisme est religion d'État."),
   ("Qui crée l'alphabet hangeul ?",
    ["Le roi Sejong, sous Joseon", "Kubilaï Khan", "Le roi Goryeo", "PSY"], 0,
    "1443-1446 ; le néo-confucianisme remplace le bouddhisme."),
   ("Comment s'appelle la vague culturelle coréenne ?",
    ["La Hallyu", "La K-wave", "Le Hanfu", "Le Joseon"], 0,
    "Gangnam Style, K-pop, cinéma (Parasite)."),
  ], ("Quelle est la question du syllabus sur la Corée ?",
      "Comment la Corée est-elle devenue l'un des pays les plus influents du divertissement mondial ?")),

 ("inde-un-geant-culturel-et-artistique", CI, "Inde", C, [
   ("Quel empereur Maurya diffuse le bouddhisme dans toute l'Asie ?",
    ["Ashoka", "Shah Jahan", "Siddhartha Gautama", "Gandhi"], 0,
    "Piliers et édits, stupa de Sanchi."),
   ("Qui fait construire le Taj Mahal ?",
    ["Shah Jahan, pour son épouse Mumtaz Mahal", "Ashoka", "La East India Company", "Le sultan de Delhi"], 0,
    "XVIIe siècle, empire moghol ; les slides le placent dans la partie sultanat."),
   ("Comment McDonald's s'est-il adapté à l'Inde ?",
    ["Un menu sans bœuf ni porc, des options végétariennes, le Maharaja Mac au poulet", "Des prix plus élevés qu'en Europe", "Le même menu qu'aux États-Unis", "Uniquement des livraisons"], 0,
    "Exposé de la séance 7, lien culture-business."),
  ], ("Quelle période couvre le British Raj, et comment se termine-t-il ?",
      "1858 – 1947 : la couronne britannique gouverne directement l'Inde, jusqu'à l'indépendance avec Gandhi (non-violence, marche du sel en 1930), puis la partition Inde-Pakistan.")),
]

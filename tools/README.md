# Mise à jour des fiches de cours

Les fiches affichées sur le site (`data/fiches/*.json`) sont une copie des Claude Docs « Partiels – … ».
Elles ne se mettent pas à jour toutes seules : après une modification d'un doc, il faut régénérer la copie.

1. Exporter chaque onglet du doc (HTML) ou le transcrire en Markdown dans `tools/fiches_src/<matiere>-<detaillee|courte>.<html|xml|md>`.
2. `python3 tools/build_fiches.py tools/fiches_src data/fiches`
3. `node tools/katex_render.mjs data/fiches/*.json` (formules LaTeX, nécessite `npm i katex@0.19.1`).

Les titres reçoivent des ids générés à partir de leur texte : le sommaire est reconstruit à chaque fois.

**Version anglaise (bouton FRA / ENG)** : `tools/fiches_src/<matiere>-<detaillee|courte>-en.md`, construite par le même script (champs `html_en` et `toc_en`).
Les termes viennent des supports du cours en anglais (slides, résumés, chapitre de Davenport et Kim) ; pour la macro (cours en français), des titres et termes anglais des auteurs cités.
Les formules s'écrivent dans un bloc ```latex. Toute modification d'une fiche française doit être reportée dans sa version anglaise.
Les compléments hors cours de la macro restent en français seulement.

# Partiels types

Source : `tools/exams_src/<matiere>.md` (balises `@exam`, `@intro`, `@method`, `@part n | pastille | titre | points | minutes`, `@data`, `@q numéro | points`, `@c`).

1. `python3 tools/build_exams.py tools/exams_src data/exams` (vérifie que les points de chaque partie s'additionnent).
2. `node tools/katex_render.mjs data/exams/*.json`
3. Ajouter `"exam": "exams/<matiere>.json"` à la matière dans `data/subjects.json`.

# Parcours guidé (étape 1)

Source : `tools/path_src/<matiere>.py` (liste `STEPS` : ancre de la sous-partie dans la fiche détaillée, partie, titre, QCM, question libre).

1. `python3 tools/build_path.py <matiere>` : vérifie que chaque ancre existe dans `data/fiches/<matiere>.json` et écrit `data/path/<matiere>.json`.
   Les identifiants sont stables : une sous-partie garde son id tant que son ancre ne change pas, une question garde le sien tant que son texte ne change pas.
   Une question réécrite reçoit un nouveau numéro et l'ancien passe dans `retired` (jamais réutilisé).
2. Ajouter `"path": "path/<matiere>.json"` à la matière dans `data/subjects.json`.

Points : 10 pts par question, une seule fois par joueur (table `path_scored`, script `supabase/004_parcours_guide.sql`).
L'extrait affiché est lu directement dans la fiche : si la fiche est régénérée avec un titre de sous-partie modifié, relancer l'étape 1 (elle signale l'ancre manquante).

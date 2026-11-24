# Mise à jour des fiches de cours

Les fiches affichées sur le site (`data/fiches/*.json`) sont une copie des Claude Docs « Partiels – … ».
Elles ne se mettent pas à jour toutes seules : après une modification d'un doc, il faut régénérer la copie.

1. Exporter chaque onglet du doc (HTML) ou le transcrire en Markdown dans `tools/fiches_src/<matiere>-<detaillee|courte>.<html|xml|md>`.
2. `python3 tools/build_fiches.py tools/fiches_src data/fiches`
3. `node tools/katex_render.mjs data/fiches/*.json` (formules LaTeX, nécessite `npm i katex@0.19.1`).

Les titres reçoivent des ids générés à partir de leur texte : le sommaire est reconstruit à chaque fois.

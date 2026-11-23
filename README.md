# Révisions PGE2 – partiels du 7 au 10 décembre 2026

Site de révision pour la classe PGE2 International : quiz QCM, flashcards à révision espacée, suivi des erreurs et classement entre camarades.

**Adresse :** https://antoinegaray.github.io/PGE2IN/

## Contenu
- `data/*.json` : questions et flashcards, tirées uniquement des fiches de cours. Les éléments marqués « Complément » viennent de la fiche mais pas directement des slides du prof.
- Macroéconomie et Géopolitique en Asie : en attente des supports.

## Technique
- Site statique (HTML, CSS, JS sans dépendance) hébergé par GitHub Pages.
- Supabase (offre gratuite) pour le classement, les erreurs et la progression des flashcards. Le site n'utilise que la clé *publishable* ; les tables sont fermées (RLS sans policy) et tout passe par les fonctions `rpc_*` de `supabase/setup.sql`.
- Connexion : pseudo + mot de passe (hash bcrypt, illisible) + code de classe. Le code n'est pas dans ce dépôt. 10 essais ratés bloquent le compte 15 minutes.
- Bouton « Signaler une erreur » sur chaque question et carte : les signalements vont dans la table `reports`.
- Scripts SQL à lancer dans l'ordre : `supabase/setup.sql`, puis `supabase/002_mot_de_passe_signalements.sql`.
- Sans connexion (ou si la base Supabase est en pause), on peut réviser en mode invité : la progression reste dans le navigateur.

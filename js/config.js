// Configuration publique du site.
// La clé "publishable" est faite pour être visible dans le navigateur :
// les tables sont verrouillées (RLS) et tout passe par les fonctions rpc_*.
// Ne JAMAIS mettre ici la clé service_role.
window.APP_CONFIG = {
  supabaseUrl: "https://iwdgqhnmlfhwczmqaepn.supabase.co",
  supabaseKey: "sb_publishable_9jv7-vgTedIqLZae8v2vGw_Huep7Fo-",
  examStart: "2026-12-07",
  quizLength: 10,
  cardsPerSession: 20
};

-- =====================================================================
-- Mise à jour 002 : signalement des questions et des flashcards
-- À coller dans Supabase > SQL Editor > New query > Run, APRÈS setup.sql.
-- Ré-exécutable sans perte de données. Ne touche pas à la connexion
-- (pseudo + code de classe, inchangée).
--
-- Voir les signalements :
--   select r.created_at, p.pseudo, r.item_id, r.reason, r.comment
--   from reports r join players p on p.id = r.player_id
--   order by r.created_at desc;
-- =====================================================================

create table if not exists public.reports (
  id          bigint generated always as identity primary key,
  player_id   uuid not null references public.players(id) on delete cascade,
  item_id     text not null,
  reason      text not null,
  comment     text,
  status      text not null default 'nouveau',
  created_at  timestamptz not null default now()
);
create index if not exists reports_created_idx on public.reports (created_at desc);
alter table public.reports enable row level security;
revoke all on public.reports from anon, authenticated;

create or replace function public.rpc_report(p_token uuid, p_item_id text, p_reason text, p_comment text)
returns void
language plpgsql security definer set search_path = public
as $$
declare v_player uuid := public._player_from_token(p_token);
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  if p_reason not in ('Réponse fausse', 'Question ambiguë', 'Faute ou coquille', 'Hors programme', 'Autre') then
    raise exception 'Motif invalide' using errcode = 'P0001';
  end if;
  if p_item_id !~ '^[a-z]+-[qf][0-9]{2,3}$' then raise exception 'Question inconnue' using errcode = 'P0001'; end if;
  if (select count(*) from public.reports r
       where r.player_id = v_player and r.created_at > now() - interval '1 day') >= 30 then
    raise exception 'Limite de 30 signalements par jour atteinte' using errcode = 'P0001';
  end if;
  insert into public.reports (player_id, item_id, reason, comment)
  values (v_player, p_item_id, p_reason, nullif(left(btrim(coalesce(p_comment, '')), 500), ''));
end $$;

revoke all on function public.rpc_report(uuid, text, text, text) from public;
grant execute on function public.rpc_report(uuid, text, text, text) to anon, authenticated;

notify pgrst, 'reload schema';

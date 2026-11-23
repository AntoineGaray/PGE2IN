-- =====================================================================
-- Mise à jour 002 : mot de passe par joueur + signalement des questions
-- À coller dans Supabase > SQL Editor > New query > Run, APRÈS setup.sql.
-- Ré-exécutable sans perte de données.
--
-- Mot de passe : stocké uniquement sous forme de hash bcrypt (pgcrypto).
-- Personne ne peut le relire, pas même depuis le tableau de bord Supabase.
-- Comptes existants sans mot de passe : le premier mot de passe saisi
-- à la connexion devient le leur.
-- 10 essais ratés => compte bloqué 15 minutes.
-- =====================================================================

create extension if not exists pgcrypto with schema extensions;

alter table public.players add column if not exists pw_hash       text;
alter table public.players add column if not exists failed_logins int not null default 0;
alter table public.players add column if not exists locked_until  timestamptz;

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

-- L'ancienne connexion sans mot de passe est supprimée (sinon elle resterait une porte dérobée).
drop function if exists public.rpc_join(text, text);

create or replace function public.rpc_join(p_code text, p_pseudo text, p_password text)
returns table (token uuid, pseudo text, created boolean)
language plpgsql security definer set search_path = public, extensions
as $$
#variable_conflict use_column
declare
  v_pseudo text := btrim(coalesce(p_pseudo, ''));
  v_pw     text := coalesce(p_password, '');
  p        public.players%rowtype;
begin
  if coalesce(p_code, '') <> (select value from public.app_config where key = 'class_code') then
    raise exception 'Code de classe incorrect' using errcode = 'P0001';
  end if;
  if char_length(v_pseudo) < 2 or char_length(v_pseudo) > 20
     or v_pseudo !~ '^[[:alnum:] ._''-]+$' then
    raise exception 'Pseudo invalide (2 à 20 caractères : lettres, chiffres, espace, . _ - '')' using errcode = 'P0001';
  end if;
  if char_length(v_pw) < 6 or char_length(v_pw) > 72 then
    raise exception 'Le mot de passe doit faire au moins 6 caractères' using errcode = 'P0001';
  end if;

  select * into p from public.players where lower(players.pseudo) = lower(v_pseudo) for update;

  if found then
    if p.locked_until is not null and p.locked_until > now() then
      raise exception 'Trop d''essais ratés : réessaie dans % min', ceil(extract(epoch from p.locked_until - now()) / 60)::int using errcode = 'P0001';
    end if;
    if p.pw_hash is null then
      -- Compte créé avant les mots de passe (ou réinitialisé) : on enregistre celui-ci.
      update public.players set pw_hash = crypt(v_pw, gen_salt('bf', 10)), failed_logins = 0, locked_until = null where id = p.id;
    elsif p.pw_hash = crypt(v_pw, p.pw_hash) then
      update public.players set failed_logins = 0, locked_until = null where id = p.id;
    else
      update public.players
         set failed_logins = p.failed_logins + 1,
             locked_until = case when p.failed_logins + 1 >= 10 then now() + interval '15 minutes' else null end
       where id = p.id;
      -- On valide le compteur malgré l'erreur renvoyée : on renvoie une ligne vide + message côté client.
      return query select null::uuid, 'MOT_DE_PASSE_INCORRECT'::text, false;
      return;
    end if;
    return query select p.token, p.pseudo, false;
    return;
  end if;

  if (select count(*) from public.players) >= 200 then
    raise exception 'Classe complète' using errcode = 'P0001';
  end if;

  return query
    insert into public.players (pseudo, pw_hash) values (v_pseudo, crypt(v_pw, gen_salt('bf', 10)))
    returning players.token, players.pseudo, true;
end $$;

-- Changer son mot de passe (en étant connecté)
create or replace function public.rpc_set_password(p_token uuid, p_old text, p_new text)
returns void
language plpgsql security definer set search_path = public, extensions
as $$
declare p public.players%rowtype;
begin
  select * into p from public.players where token = p_token;
  if not found then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  if p.pw_hash is not null and p.pw_hash <> crypt(coalesce(p_old, ''), p.pw_hash) then
    raise exception 'Ancien mot de passe incorrect' using errcode = 'P0001';
  end if;
  if char_length(coalesce(p_new, '')) < 6 or char_length(p_new) > 72 then
    raise exception 'Le mot de passe doit faire au moins 6 caractères' using errcode = 'P0001';
  end if;
  update public.players set pw_hash = crypt(p_new, gen_salt('bf', 10)) where id = p.id;
end $$;

-- Signaler une question ou une carte
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

revoke all on function public.rpc_join(text, text, text)          from public;
revoke all on function public.rpc_set_password(uuid, text, text)  from public;
revoke all on function public.rpc_report(uuid, text, text, text)  from public;
grant execute on function public.rpc_join(text, text, text)         to anon, authenticated;
grant execute on function public.rpc_set_password(uuid, text, text) to anon, authenticated;
grant execute on function public.rpc_report(uuid, text, text, text) to anon, authenticated;

notify pgrst, 'reload schema';

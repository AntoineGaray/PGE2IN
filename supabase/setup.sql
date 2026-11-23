-- =====================================================================
-- Plateforme de révision PGE2 – schéma Supabase
-- À coller UNE fois dans Supabase > SQL Editor > New query > Run.
-- Le script est ré-exécutable (il ne supprime aucune donnée).
--
-- Sécurité : le site utilise seulement la clé publishable (anon).
--   * Les tables ont la RLS activée SANS aucune policy, et les droits
--     anon/authenticated sont retirés : personne ne peut les lire ou les
--     écrire directement via l'API.
--   * Tout passe par les fonctions rpc_* (SECURITY DEFINER) ci-dessous,
--     qui vérifient le code de classe ou le jeton du joueur.
--   * Le code de classe n'est PAS dans ce fichier (le dépôt est public) :
--     il se règle avec la commande séparée donnée par Claude :
--       update public.app_config set value = 'VOTRE-CODE' where key = 'class_code';
-- =====================================================================

-- ---------- Tables ----------
create table if not exists public.app_config (
  key   text primary key,
  value text not null
);
insert into public.app_config (key, value)
values ('class_code', 'A-CHANGER-' || md5(random()::text))
on conflict (key) do nothing;

create table if not exists public.players (
  id         uuid primary key default gen_random_uuid(),
  pseudo     text not null,
  token      uuid not null unique default gen_random_uuid(),
  created_at timestamptz not null default now()
);
create unique index if not exists players_pseudo_lower_idx on public.players (lower(pseudo));

create table if not exists public.attempts (
  id         bigint generated always as identity primary key,
  player_id  uuid not null references public.players(id) on delete cascade,
  subject    text not null,
  mode       text not null check (mode in ('quiz', 'cards', 'errors')),
  correct    int  not null check (correct >= 0),
  total      int  not null check (total > 0 and total <= 60 and correct <= total),
  points     int  not null default 0,
  created_at timestamptz not null default now()
);
create index if not exists attempts_player_idx on public.attempts (player_id, created_at desc);

create table if not exists public.errors (
  player_id    uuid not null references public.players(id) on delete cascade,
  question_id  text not null,
  subject      text not null,
  wrong_count  int  not null default 0,
  right_streak int  not null default 0,
  last_wrong   timestamptz,
  updated_at   timestamptz not null default now(),
  primary key (player_id, question_id)
);

create table if not exists public.player_state (
  player_id  uuid not null references public.players(id) on delete cascade,
  key        text not null,
  value      jsonb not null,
  updated_at timestamptz not null default now(),
  primary key (player_id, key)
);

-- ---------- Verrouillage : RLS sans policy + aucun droit direct ----------
alter table public.app_config   enable row level security;
alter table public.players      enable row level security;
alter table public.attempts     enable row level security;
alter table public.errors       enable row level security;
alter table public.player_state enable row level security;

revoke all on public.app_config, public.players, public.attempts, public.errors, public.player_state
  from anon, authenticated;

-- ---------- Fonction interne : jeton -> joueur ----------
create or replace function public._player_from_token(p_token uuid)
returns uuid
language sql stable security definer set search_path = public
as $$ select id from public.players where token = p_token $$;
revoke all on function public._player_from_token(uuid) from public, anon, authenticated;

-- ---------- Rejoindre la classe ----------
create or replace function public.rpc_join(p_code text, p_pseudo text)
returns table (token uuid, pseudo text)
language plpgsql security definer set search_path = public
as $$
#variable_conflict use_column
declare
  v_pseudo text := btrim(coalesce(p_pseudo, ''));
begin
  if coalesce(p_code, '') <> (select value from public.app_config where key = 'class_code') then
    raise exception 'Code de classe incorrect' using errcode = 'P0001';
  end if;
  if char_length(v_pseudo) < 2 or char_length(v_pseudo) > 20
     or v_pseudo !~ '^[[:alnum:] ._''-]+$' then
    raise exception 'Pseudo invalide (2 à 20 caractères : lettres, chiffres, espace, . _ - '')' using errcode = 'P0001';
  end if;

  return query
    select p.token, p.pseudo from public.players p where lower(p.pseudo) = lower(v_pseudo);
  if found then return; end if;

  if (select count(*) from public.players) >= 200 then
    raise exception 'Classe complète' using errcode = 'P0001';
  end if;

  return query
    insert into public.players (pseudo) values (v_pseudo)
    returning players.token, players.pseudo;
end $$;

-- ---------- Enregistrer une session (quiz, flashcards ou erreurs) ----------
create or replace function public.rpc_record(
  p_token uuid, p_subject text, p_mode text,
  p_correct int, p_total int,
  p_wrong text[] default '{}', p_right text[] default '{}')
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_player uuid := public._player_from_token(p_token);
  v_points int;
  q text;
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  if char_length(p_subject) > 30 then raise exception 'Matière invalide' using errcode = 'P0001'; end if;
  if coalesce(array_length(p_wrong, 1), 0) + coalesce(array_length(p_right, 1), 0) > 60 then
    raise exception 'Trop de questions' using errcode = 'P0001';
  end if;

  -- Barème : 10 pts par bonne réponse en quiz et en révision d'erreurs, 2 pts par carte sue.
  v_points := case when p_mode = 'cards' then 2 * p_correct else 10 * p_correct end;

  insert into public.attempts (player_id, subject, mode, correct, total, points)
  values (v_player, p_subject, p_mode, p_correct, p_total, v_points);

  foreach q in array coalesce(p_wrong, '{}') loop
    insert into public.errors (player_id, question_id, subject, wrong_count, right_streak, last_wrong)
    values (v_player, left(q, 60), p_subject, 1, 0, now())
    on conflict (player_id, question_id) do update
      set wrong_count = errors.wrong_count + 1, right_streak = 0,
          last_wrong = now(), updated_at = now();
  end loop;

  foreach q in array coalesce(p_right, '{}') loop
    update public.errors
       set right_streak = right_streak + 1, updated_at = now()
     where player_id = v_player and question_id = q;
  end loop;

  return v_points;
end $$;

-- ---------- Mes erreurs ----------
create or replace function public.rpc_errors(p_token uuid)
returns table (question_id text, subject text, wrong_count int, right_streak int, last_wrong timestamptz)
language plpgsql security definer set search_path = public
as $$
#variable_conflict use_column
declare v_player uuid := public._player_from_token(p_token);
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  return query
    select e.question_id, e.subject, e.wrong_count, e.right_streak, e.last_wrong
      from public.errors e where e.player_id = v_player
     order by e.last_wrong desc nulls last;
end $$;

-- ---------- État libre (révision espacée des flashcards, etc.) ----------
create or replace function public.rpc_state_get(p_token uuid)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare v_player uuid := public._player_from_token(p_token);
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  return coalesce((select jsonb_object_agg(s.key, s.value) from public.player_state s where s.player_id = v_player), '{}'::jsonb);
end $$;

create or replace function public.rpc_state_set(p_token uuid, p_key text, p_value jsonb)
returns void
language plpgsql security definer set search_path = public
as $$
declare v_player uuid := public._player_from_token(p_token);
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  if char_length(p_key) > 40 or pg_column_size(p_value) > 100000 then
    raise exception 'État trop volumineux' using errcode = 'P0001';
  end if;
  insert into public.player_state (player_id, key, value) values (v_player, p_key, p_value)
  on conflict (player_id, key) do update set value = excluded.value, updated_at = now();
end $$;

-- ---------- Leaderboard ----------
create or replace function public.rpc_leaderboard(p_token uuid)
returns table (pseudo text, points bigint, points_7d bigint, sessions bigint, accuracy int, streak int, is_me boolean)
language plpgsql security definer set search_path = public
as $$
#variable_conflict use_column
declare v_player uuid := public._player_from_token(p_token);
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  return query
  with days as (
    select distinct a.player_id, (a.created_at at time zone 'Europe/Paris')::date as d
      from public.attempts a
  ),
  ranked as (
    select player_id, d,
           d - (row_number() over (partition by player_id order by d))::int as grp
      from days
  ),
  runs as (
    select player_id, max(d) as last_day, count(*)::int as len
      from ranked group by player_id, grp
  ),
  streaks as (
    select player_id, max(len) filter (
             where last_day >= (now() at time zone 'Europe/Paris')::date - 1) as streak
      from runs group by player_id
  )
  select p.pseudo,
         coalesce(sum(a.points), 0)::bigint,
         coalesce(sum(a.points) filter (where a.created_at > now() - interval '7 days'), 0)::bigint,
         count(a.id)::bigint,
         case when sum(a.total) filter (where a.mode <> 'cards') > 0
              then round(100.0 * sum(a.correct) filter (where a.mode <> 'cards')
                         / sum(a.total) filter (where a.mode <> 'cards'))::int
              else null end,
         coalesce(s.streak, 0),
         p.id = v_player
    from public.players p
    left join public.attempts a on a.player_id = p.id
    left join streaks s on s.player_id = p.id
   group by p.id, p.pseudo, s.streak
   order by 2 desc, p.pseudo;
end $$;

-- ---------- Droits d'exécution : seulement les fonctions rpc_* ----------
revoke all on function public.rpc_join(text, text)                                   from public;
revoke all on function public.rpc_record(uuid, text, text, int, int, text[], text[]) from public;
revoke all on function public.rpc_errors(uuid)                                       from public;
revoke all on function public.rpc_state_get(uuid)                                    from public;
revoke all on function public.rpc_state_set(uuid, text, jsonb)                       from public;
revoke all on function public.rpc_leaderboard(uuid)                                  from public;

grant execute on function public.rpc_join(text, text)                                   to anon, authenticated;
grant execute on function public.rpc_record(uuid, text, text, int, int, text[], text[]) to anon, authenticated;
grant execute on function public.rpc_errors(uuid)                                       to anon, authenticated;
grant execute on function public.rpc_state_get(uuid)                                    to anon, authenticated;
grant execute on function public.rpc_state_set(uuid, text, jsonb)                       to anon, authenticated;
grant execute on function public.rpc_leaderboard(uuid)                                  to anon, authenticated;

notify pgrst, 'reload schema';

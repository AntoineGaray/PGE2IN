-- =====================================================================
-- Mise à jour 004 : parcours guidé (étape 1 de révision)
-- À coller dans Supabase > SQL Editor > New query > Run, APRÈS 003.
-- Ré-exécutable sans perte de données.
--
-- Règle : chaque question du parcours rapporte 10 pts UNE SEULE FOIS par
-- joueur, la première fois qu'il y répond juste (quel que soit le nombre
-- d'essais). Les fois suivantes : 0 pt, mais la session est comptée.
-- =====================================================================

-- Questions du parcours déjà payées, par joueur
create table if not exists public.path_scored (
  player_id   uuid not null references public.players(id) on delete cascade,
  question_id text not null,
  created_at  timestamptz not null default now(),
  primary key (player_id, question_id)
);
alter table public.path_scored enable row level security;
revoke all on public.path_scored from anon, authenticated;

-- Nouveau mode « path » pour les sessions
alter table public.attempts drop constraint if exists attempts_mode_check;
alter table public.attempts add constraint attempts_mode_check
  check (mode in ('quiz', 'cards', 'errors', 'daily', 'path'));

-- Enregistrement d'une session : même signature, on ajoute la règle du parcours
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
  v_new int := 0;
  v_today date := (now() at time zone 'Europe/Paris')::date;
  q text;
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  if char_length(p_subject) > 30 then raise exception 'Matière invalide' using errcode = 'P0001'; end if;
  if coalesce(array_length(p_wrong, 1), 0) + coalesce(array_length(p_right, 1), 0) > 60 then
    raise exception 'Trop de questions' using errcode = 'P0001';
  end if;

  if p_mode = 'daily' then
    if p_total > 20 then raise exception 'Défi invalide' using errcode = 'P0001'; end if;
    if exists (select 1 from public.attempts a
                where a.player_id = v_player and a.mode = 'daily'
                  and (a.created_at at time zone 'Europe/Paris')::date = v_today) then
      raise exception 'Défi du jour déjà fait : reviens demain !' using errcode = 'P0001';
    end if;
  end if;

  if p_mode = 'path' then
    -- Ne paie que les identifiants de parcours (ex. strat-p03-q2) jamais payés à ce joueur
    foreach q in array coalesce(p_right, '{}') loop
      if q ~ '^[a-z]{2,10}-p[0-9]{2,3}-q[0-9]{1,2}$' then
        insert into public.path_scored (player_id, question_id) values (v_player, q)
        on conflict do nothing;
        if found then v_new := v_new + 1; end if;
      end if;
    end loop;
  end if;

  -- Barème : 10 pts par bonne réponse (quiz, erreurs), 20 pts au défi du jour, 2 pts par carte sue,
  -- 10 pts par question du parcours réussie pour la première fois.
  v_points := case p_mode when 'cards' then 2 * p_correct
                          when 'daily' then 20 * p_correct
                          when 'path'  then 10 * v_new
                          else 10 * p_correct end;

  insert into public.attempts (player_id, subject, mode, correct, total, points)
  values (v_player, p_subject, p_mode, p_correct, p_total, v_points);

  -- Le parcours n'alimente pas « Mes erreurs » (on y retente directement la sous-partie)
  if p_mode <> 'path' then
    foreach q in array coalesce(p_wrong, '{}') loop
      insert into public.errors (player_id, question_id, subject, wrong_count, right_streak, last_wrong)
      values (v_player, left(q, 60), split_part(q, '-', 1), 1, 0, now())
      on conflict (player_id, question_id) do update
        set wrong_count = errors.wrong_count + 1, right_streak = 0,
            last_wrong = now(), updated_at = now();
    end loop;

    foreach q in array coalesce(p_right, '{}') loop
      update public.errors
         set right_streak = right_streak + 1, updated_at = now()
       where player_id = v_player and question_id = q;
    end loop;
  end if;

  return v_points;
end $$;

-- Questions du parcours déjà payées (pour afficher « déjà gagné » sur tous les appareils)
create or replace function public.rpc_path_scored(p_token uuid)
returns text[]
language plpgsql security definer set search_path = public
as $$
declare v_player uuid := public._player_from_token(p_token);
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  return coalesce((select array_agg(question_id) from public.path_scored where player_id = v_player), '{}');
end $$;

revoke all on function public.rpc_record(uuid, text, text, int, int, text[], text[]) from public;
revoke all on function public.rpc_path_scored(uuid)                                  from public;
grant execute on function public.rpc_record(uuid, text, text, int, int, text[], text[]) to anon, authenticated;
grant execute on function public.rpc_path_scored(uuid)                                  to anon, authenticated;

notify pgrst, 'reload schema';

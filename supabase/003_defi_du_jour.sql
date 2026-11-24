-- =====================================================================
-- Mise à jour 003 : défi du jour (points ×2, une fois par jour)
-- À coller dans Supabase > SQL Editor > New query > Run, APRÈS 002.
-- Ré-exécutable sans perte de données.
-- =====================================================================

-- Nouveau mode « daily » pour les sessions
alter table public.attempts drop constraint if exists attempts_mode_check;
alter table public.attempts add constraint attempts_mode_check
  check (mode in ('quiz', 'cards', 'errors', 'daily'));

create index if not exists attempts_daily_idx on public.attempts (mode, created_at desc);

-- Enregistrement d'une session : même fonction, avec la règle du défi du jour
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

  -- Barème : 10 pts par bonne réponse (quiz, erreurs), 20 pts au défi du jour, 2 pts par carte sue.
  v_points := case p_mode when 'cards' then 2 * p_correct
                          when 'daily' then 20 * p_correct
                          else 10 * p_correct end;

  insert into public.attempts (player_id, subject, mode, correct, total, points)
  values (v_player, p_subject, p_mode, p_correct, p_total, v_points);

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

  return v_points;
end $$;

-- Classement du défi du jour (aujourd'hui, heure de Paris)
create or replace function public.rpc_daily_board(p_token uuid)
returns table (pseudo text, correct int, total int, points int, done_at timestamptz, is_me boolean)
language plpgsql security definer set search_path = public
as $$
#variable_conflict use_column
declare v_player uuid := public._player_from_token(p_token);
begin
  if v_player is null then raise exception 'Session expirée, reconnecte-toi' using errcode = 'P0001'; end if;
  return query
    select p.pseudo, a.correct, a.total, a.points, a.created_at, p.id = v_player
      from public.attempts a join public.players p on p.id = a.player_id
     where a.mode = 'daily'
       and (a.created_at at time zone 'Europe/Paris')::date = (now() at time zone 'Europe/Paris')::date
     order by a.correct desc, a.created_at asc;
end $$;

revoke all on function public.rpc_daily_board(uuid) from public;
grant execute on function public.rpc_daily_board(uuid) to anon, authenticated;

notify pgrst, 'reload schema';

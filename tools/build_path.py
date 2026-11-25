#!/usr/bin/env python3
"""Construit data/path/<matière>.json à partir de tools/path_src/<matière>.py.

Identifiants stables : un identifiant de sous-partie (strat-p03) reste attaché à son ancre,
un identifiant de question (strat-p03-q2) reste attaché au texte de sa question.
Une question nouvelle ou réécrite reçoit un numéro jamais utilisé : on ne renumérote jamais.
Usage : python3 tools/build_path.py strat
"""
import json, os, re, runpy, sys, datetime

def main(subj):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = runpy.run_path(os.path.join(root, "tools", "path_src", subj + ".py"))
    out_path = os.path.join(root, "data", "path", subj + ".json")
    fiche = json.load(open(os.path.join(root, "data", "fiches", subj + ".json"), encoding="utf-8"))
    tab = next(t for t in fiche["tabs"] if t["key"] == "detaillee")
    h3 = {t["id"] for t in tab["toc"] if t["level"] == 3}

    old = json.load(open(out_path, encoding="utf-8")) if os.path.exists(out_path) else {"steps": [], "retired": []}
    step_by_anchor = {s["anchor"]: s for s in old["steps"]}
    used_steps = {s["id"] for s in old["steps"]} | {r for r in old.get("retired", []) if r.count("-") == 1}
    used_q = {q["id"] for s in old["steps"] for q in s["qcm"]} | {r for r in old.get("retired", []) if r.count("-") == 2}
    num = lambda i: int(re.search(r"(\d+)$", i).group(1))
    next_step = max([num(i) for i in used_steps] or [0]) + 1

    steps, errors = [], []
    for anchor, part, title, flag, qcm, open_q in src["STEPS"]:
        if anchor not in h3: errors.append(f"ancre absente de la fiche : {anchor}")
        prev = step_by_anchor.get(anchor)
        if prev: sid = prev["id"]
        else: sid = f"{subj}-p{next_step:02d}"; next_step += 1
        prev_q = {q["q"]: q["id"] for q in (prev["qcm"] if prev else [])}
        nq = max([num(i) for i in used_q if i.startswith(sid + "-")] or [0]) + 1
        qs = []
        for item in qcm:
            q, choices, ans, expl = item[:4]
            qflag = item[4] if len(item) > 4 else flag
            if len(choices) != 4 or len(set(choices)) != 4: errors.append(f"{sid} : 4 choix distincts attendus ({q})")
            if not 0 <= ans < len(choices): errors.append(f"{sid} : réponse hors choix ({q})")
            if q in prev_q: qid = prev_q[q]
            else: qid = f"{sid}-q{nq}"; nq += 1
            used_q.add(qid)
            d = {"id": qid, "q": q, "choices": choices, "answer": ans, "explain": expl}
            if qflag: d["flag"] = qflag
            qs.append(d)
        st = {"id": sid, "part": part, "anchor": anchor, "title": title, "qcm": qs, "open": {"q": open_q[0], "a": open_q[1]}}
        if flag: st["flag"] = flag
        steps.append(st)

    ids = [s["id"] for s in steps] + [q["id"] for s in steps for q in s["qcm"]]
    if len(ids) != len(set(ids)): errors.append("identifiants en double")
    for i in ids:
        if i.count("-") == 2 and not re.fullmatch(r"[a-z]{2,10}-p\d{2,3}-q\d{1,2}", i): errors.append(f"identifiant refusé par le serveur : {i}")
    new_ids = set(ids)
    retired = sorted(set(old.get("retired", [])) | ({s["id"] for s in old["steps"]} | {q["id"] for s in old["steps"] for q in s["qcm"]}) - new_ids)
    if errors:
        print("\n".join(errors)); sys.exit(1)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump({"subject": subj, "updated": datetime.date.today().isoformat(), "steps": steps, "retired": retired},
              open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{out_path} : {len(steps)} sous-parties, {sum(len(s['qcm']) for s in steps)} QCM, {len(retired)} identifiants retirés")

if __name__ == "__main__":
    main(sys.argv[1])

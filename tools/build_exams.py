"""Construit data/exams/<matiere>.json à partir de tools/exams_src/<matiere>.md.
Format : @exam (clé: valeur), @intro, @method, @part n | pastille | titre | points | minutes,
@data (énoncé commun de la partie), @q numéro | points, @c (corrigé de la question).
"""
import json, re, sys
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

def md(text):
    html = markdown.markdown(text.strip(), extensions=["tables", "sane_lists", "fenced_code"])
    soup = BeautifulSoup(html, "html.parser")
    for code in soup.find_all("code", class_="language-latex"):
        div = soup.new_tag("div", attrs={"class": "math"}); div.string = code.get_text()
        (code.find_parent("pre") or code).replace_with(div)
    for td in soup.find_all(["td", "th"]):
        if re.fullmatch(r"[−\-+]?[\d\s,.\u202f]+\s*(€|%|h|kg)?(/\w+)?", td.get_text(strip=True) or "x"):
            td["class"] = "num"
    for t in soup.find_all("table"):
        t.wrap(soup.new_tag("div", attrs={"class": "table-wrap"}))
    return str(soup)

def build(src):
    exam, parts, cur, key, buf = {}, [], None, None, []
    def flush():
        nonlocal buf
        text = "\n".join(buf); buf = []
        if key is None: return
        if key == "exam":
            for line in text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1); exam[k.strip()] = v.strip()
        elif key in ("intro", "method"): exam[key] = md(text)
        elif key == "data": cur["data"] = md(text)
        elif key == "q": cur["questions"][-1]["q"] = md(text)
        elif key == "c": cur["questions"][-1]["c"] = md(text)
    for line in src.splitlines():
        m = re.match(r"^@(\w+)\s*(.*)$", line)
        if m and m.group(1) in ("exam", "intro", "method", "part", "data", "q", "c"):
            flush(); tag, args = m.group(1), [a.strip() for a in m.group(2).split("|")]
            if tag == "part":
                cur = {"n": args[0], "pill": args[1], "title": args[2], "points": float(args[3]), "minutes": int(args[4]), "questions": []}
                parts.append(cur); key = None
            elif tag == "q":
                cur["questions"].append({"num": args[0], "points": float(args[1])}); key = "q"
            else:
                key = tag
            continue
        buf.append(line)
    flush()
    for p in parts:
        s = sum(q["points"] for q in p["questions"])
        assert abs(s - p["points"]) < 1e-9, f"partie {p['n']} : {s} != {p['points']}"
        for q in p["questions"]:
            assert q.get("q") and q.get("c"), f"question {q['num']} incomplète"
    exam["points"] = sum(p["points"] for p in parts)
    exam["minutes"] = sum(p["minutes"] for p in parts)
    exam["parts"] = parts
    return exam

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for f in sorted(src.glob("*.md")):
    e = build(f.read_text())
    (out / f"{f.stem}.json").write_text(json.dumps(e, ensure_ascii=False))
    print(f.stem, e["points"], "points,", e["minutes"], "min,", sum(len(p["questions"]) for p in e["parts"]), "questions")

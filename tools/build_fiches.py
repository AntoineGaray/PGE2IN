"""Construit data/fiches/<matiere>.json à partir des exports des Claude Docs.
Sources (dans fiches_src/) : <id>-<onglet>.html (export HTML), .xml (lecture XML) ou .md (transcription).
"""
import json, re, sys, unicodedata, xml.etree.ElementTree as ET
from html import escape
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
SUBJECTS = {
    "ma": "Management Accounting",
    "strat": "Management stratégique",
    "mq": "Méthodes quantitatives III",
    "art": "Art et culture en Asie",
    "rse": "Workshop RSE",
    "macro": "Macroéconomie",
}
# Date de la dernière version de chaque fiche (par défaut : 23/11/2026)
UPDATED = {"macro": "2026-11-26"}
TABS = [("detaillee", "Fiche détaillée"), ("courte", "Fiche courte")]

# ---------- XML Claude Docs -> HTML ----------
def inline(el):
    out = []
    for t in el:
        if t.tag != "text":
            continue
        s = escape(t.text or "")
        for child in t:
            inner = escape(child.text or "")
            if child.tag == "bold":
                inner = f"<strong>{inner}</strong>"
            elif child.tag == "italic":
                inner = f"<em>{inner}</em>"
            s += inner + escape(child.tail or "")
        out.append(s)
    return "".join(out)

def block(el):
    if el.tag == "paragraph":
        h = el.get("heading")
        body = inline(el)
        if h:
            return f"<h{h}>{body}</h{h}>"
        if el.find("date") is not None or el.find("mention") is not None:
            return ""  # ligne date + auteur
        return f"<p>{body}</p>"
    if el.tag == "list":
        tag = "ol" if el.get("kind") == "ordered" else "ul"
        items = []
        for li in el.findall("listItem"):
            items.append("<li>" + "".join(block(c) for c in li) + "</li>")
        return f"<{tag}>" + "".join(items) + f"</{tag}>"
    if el.tag == "table":
        rows = el.findall("row")
        head, body = [], []
        for r in rows:
            cells = r.findall("cell")
            is_head = all(c.get("header") == "true" for c in cells)
            tag = "th" if is_head else "td"
            html = "<tr>" + "".join(f"<{tag}>" + "".join(inline(p) for p in c.findall("paragraph")) + f"</{tag}>" for c in cells) + "</tr>"
            (head if is_head and not body else body).append(html)
        return "<table>" + (f"<thead>{''.join(head)}</thead>" if head else "") + f"<tbody>{''.join(body)}</tbody></table>"
    if el.tag == "video":
        # Bloc vidéo (même syntaxe que le bloc ```video des sources Markdown)
        return f'<pre><code class="language-video">{escape(el.text or "")}</code></pre>'
    return ""

def xml_to_html(xml):
    root = ET.fromstring(xml)
    return "".join(block(c) for c in root)

# ---------- Normalisation ----------
def slug(s, used):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "section"
    base, n = s, 2
    while s in used:
        s = f"{base}-{n}"; n += 1
    used.add(s)
    return s

def normalise(html, lang="fr"):
    soup = BeautifulSoup(html, "html.parser")
    for h1 in soup.find_all("h1"):
        h1.decompose()
    for atom in soup.find_all(["time", "span"], attrs={"data-atom": True}):
        p = atom.find_parent("p")
        (p or atom).decompose()
    for tag in soup.find_all(["script", "style", "iframe"]):
        tag.decompose()
    # Cases à cocher (export HTML : input disabled ; markdown : "[ ] ")
    for li in soup.find_all("li"):
        first = li.find(string=True)
        if first and re.match(r"^\s*\[ \]\s", first):
            first.replace_with(re.sub(r"^\s*\[ \]\s", "", first))
            li.insert(0, BeautifulSoup('<input type="checkbox">', "html.parser"))
            li["class"] = "task"
        elif li.find("input", attrs={"type": "checkbox"}):
            li.find("input")["disabled"] = None
            del li.find("input")["disabled"]
            li["class"] = "task"
    # Tableaux défilants sur mobile
    for t in soup.find_all("table"):
        wrap = soup.new_tag("div", attrs={"class": "table-wrap"})
        t.wrap(wrap)
    # Titres : ids propres + sommaire
    used, toc = set(), []
    for h in soup.find_all(["h2", "h3"]):
        text = h.get_text(" ", strip=True)
        h["id"] = slug(text, used)
        toc.append({"id": h["id"], "text": text, "level": int(h.name[1])})
    # Formules LaTeX : marquées pour le rendu KaTeX
    for code in soup.find_all("code", class_="language-latex"):
        pre = code.find_parent("pre")
        div = soup.new_tag("div", attrs={"class": "math"})
        div.string = code.get_text()
        (pre or code).replace_with(div)
    # Nettoyage des ids et attributs inutiles
    for el in soup.find_all(True):
        for a in list(el.attrs):
            if a not in ("id", "class", "type", "colspan", "rowspan") or (a == "id" and el.name not in ("h2", "h3")):
                del el[a]
    # Vidéos YouTube : seul contenu externe autorisé (les iframes des exports restent supprimées plus haut).
    # La fiche ne contient qu'une miniature ; l'iframe youtube-nocookie.com est créée au clic par js/app.js.
    for code in soup.find_all("code", class_="language-video"):
        pre = code.find_parent("pre")
        (pre or code).replace_with(BeautifulSoup(video_html(code.get_text(), lang), "html.parser"))
    return str(soup), toc

YT_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
def video_html(src, lang):
    """Bloc ```video : lignes « clé: valeur » (id, title, channel, duration), puis éventuellement
    une ligne --- suivie d'une note en Markdown affichée sous la vidéo."""
    head, _, note = src.partition("\n---\n")
    meta = {}
    for line in head.strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip().lower()] = v.strip()
    vid = meta.get("id", "")
    if not YT_ID.match(vid):
        raise ValueError(f"bloc video : id YouTube invalide « {vid} »")
    title = meta.get("title") or "Vidéo"
    info = " · ".join(x for x in (meta.get("channel"), meta.get("duration"), "in English" if lang == "en" else "en anglais") if x)
    play = "Play the video" if lang == "en" else "Lire la vidéo"
    note_html = f'<div class="yt-note">{markdown.markdown(note.strip())}</div>' if note.strip() else ""
    return (f'<figure class="yt" data-yt="{vid}">'
            f'<button class="yt-btn" type="button" aria-label="{escape(play)} : {escape(title)} (YouTube)">'
            f'<img class="yt-thumb" src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">'
            f'<span class="yt-play" aria-hidden="true"></span></button>'
            f'<figcaption><span class="yt-title">🎬 {escape(title)}</span><span class="yt-meta">{escape(info)}</span></figcaption>'
            f'{note_html}</figure>')

def load(sid, tab):
    for ext in ("html", "xml", "md"):
        p = SRC / f"{sid}-{tab}.{ext}"
        if p.exists():
            raw = p.read_text()
            if ext == "html":
                return raw
            if ext == "xml":
                return xml_to_html(raw)
            return markdown.markdown(raw, extensions=["tables", "sane_lists", "fenced_code"])
    raise FileNotFoundError(f"{sid}-{tab}")

OUT.mkdir(parents=True, exist_ok=True)
for sid, name in SUBJECTS.items():
    tabs = []
    for key, label in TABS:
        html, toc = normalise(load(sid, key))
        t = {"key": key, "name": label, "html": html, "toc": toc}
        # Version anglaise (bouton FRA / ENG) : <matiere>-<onglet>-en.md, termes repris des supports du cours
        try:
            t["html_en"], t["toc_en"] = normalise(load(sid, key + "-en"), "en")
        except FileNotFoundError:
            pass
        tabs.append(t)
        print(f"{sid}/{key}: {len(html)} car., {len(toc)} titres" + (f" | EN : {len(t['html_en'])} car., {len(t['toc_en'])} titres" if "html_en" in t else ""))
    (OUT / f"{sid}.json").write_text(json.dumps({"subject": sid, "title": name, "updated": UPDATED.get(sid, "2026-11-23"), "tabs": tabs}, ensure_ascii=False))

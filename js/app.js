/* Révisions PGE2 – application monopage, sans dépendance.
   Contenu : data/*.json (généré à l'avance). Classement et suivi : Supabase via rpc_*. */
(function () {
  "use strict";

  const CFG = window.APP_CONFIG;
  const $app = document.getElementById("app");
  const LS = "pge2.";
  const INTERVALS = [0, 1, 2, 4, 7]; // jours, boîtes de Leitner 0 à 4

  // ---------- Stockage local ----------
  const store = {
    get(k, d) { try { const v = localStorage.getItem(LS + k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(LS + k, JSON.stringify(v)); } catch (e) { /* plein ou privé */ } },
    del(k) { try { localStorage.removeItem(LS + k); } catch (e) { /* */ } }
  };

  let session = store.get("session", null); // {token, pseudo} ou {guest:true}
  let subjects = [];
  const subjectCache = {};
  let leaderboardCache = null;

  // ---------- Utilitaires ----------
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const shuffle = (a) => { const b = a.slice(); for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };
  const now = () => Date.now();
  const DAY = 86400000;
  const today0 = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d.getTime(); };
  const subjOf = (id) => subjects.find((s) => s.id === id);
  const qSubject = (qid) => qid.split("-")[0];

  function toast(msg, ms) {
    const t = document.getElementById("toast");
    t.textContent = msg; t.classList.add("show");
    clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove("show"), ms || 2600);
  }

  function daysToExam() {
    const d = Math.ceil((new Date(CFG.examStart + "T08:00:00").getTime() - now()) / DAY);
    return Math.max(0, d);
  }

  // ---------- API Supabase ----------
  const online = () => session && session.token;

  async function rpc(fn, args) {
    const res = await fetch(CFG.supabaseUrl + "/rest/v1/rpc/" + fn, {
      method: "POST",
      headers: { apikey: CFG.supabaseKey, "Content-Type": "application/json" },
      body: JSON.stringify(args || {})
    });
    const txt = await res.text();
    let data = null; try { data = txt ? JSON.parse(txt) : null; } catch (e) { data = txt; }
    if (!res.ok) {
      const msg = (data && data.message) || ("Erreur serveur (" + res.status + ")");
      const err = new Error(msg); err.status = res.status; err.server = true;
      if (/Session expirée/.test(msg)) { session = null; store.del("session"); }
      throw err;
    }
    return data;
  }

  // File d'attente : si l'envoi d'un résultat échoue (réseau, base en pause), on réessaie plus tard.
  function queuePush(item) { const q = store.get("queue", []); q.push(item); store.set("queue", q.slice(-50)); }
  async function flushQueue() {
    if (!online()) return;
    const q = store.get("queue", []);
    if (!q.length) return;
    const rest = [];
    for (const item of q) {
      try { await rpc("rpc_record", Object.assign({}, item, { p_token: session.token })); }
      catch (e) { if (e.server) continue; rest.push(item); }
    }
    store.set("queue", rest);
    if (q.length !== rest.length) leaderboardCache = null;
  }

  async function recordSession(subject, mode, correct, total, wrongIds, rightIds) {
    // Points locaux (mode invité) et journal d'activité
    const pts = mode === "cards" ? 2 * correct : mode === "daily" ? 20 * correct : 10 * correct;
    const log = store.get("log", []);
    log.push({ t: now(), s: subject, m: mode, c: correct, n: total, p: pts });
    store.set("log", log.slice(-500));
    if (!online() || total === 0) return pts;
    const payload = { p_subject: subject, p_mode: mode, p_correct: correct, p_total: Math.min(total, 60), p_wrong: wrongIds.slice(0, 60), p_right: rightIds.slice(0, 60) };
    try { await rpc("rpc_record", Object.assign({ p_token: session.token }, payload)); leaderboardCache = null; }
    catch (e) {
      if (!e.server) { queuePush(payload); toast("Hors ligne : résultat gardé, il sera envoyé plus tard."); }
      else { toast(e.message, 4000); if (mode === "daily") return 0; }
    }
    return pts;
  }

  // ---------- Contenu ----------
  async function loadSubjects() {
    const r = await fetch("data/subjects.json", { cache: "no-cache" });
    subjects = (await r.json()).subjects;
  }
  async function loadSubject(id) {
    if (subjectCache[id]) return subjectCache[id];
    const s = subjOf(id);
    if (!s || !s.file) throw new Error("Matière introuvable");
    const r = await fetch("data/" + s.file, { cache: "no-cache" });
    const data = await r.json();
    data.quiz.forEach((q) => { q.subject = id; });
    data.cards.forEach((c) => { c.subject = id; });
    subjectCache[id] = data;
    return data;
  }

  // ---------- Erreurs (local + serveur) ----------
  // local : { qid: { s, w (nb d'erreurs), r (bonnes réponses d'affilée), t } }
  function localErrorsUpdate(wrongIds, rightIds, subject) {
    const e = store.get("errors", {});
    wrongIds.forEach((id) => { const x = e[id] || { s: subject, w: 0, r: 0 }; x.w++; x.r = 0; x.t = now(); e[id] = x; });
    rightIds.forEach((id) => { if (e[id]) e[id].r++; });
    store.set("errors", e);
  }
  async function getErrors() {
    const local = store.get("errors", {});
    if (online()) {
      try {
        const rows = await rpc("rpc_errors", { p_token: session.token });
        rows.forEach((r) => {
          const l = local[r.question_id];
          local[r.question_id] = { s: qSubject(r.question_id), w: Math.max(r.wrong_count, l ? l.w : 0), r: r.right_streak, t: Date.parse(r.last_wrong) || (l && l.t) || 0 };
        });
        store.set("errors", local);
      } catch (e) { /* on garde le local */ }
    }
    return local;
  }
  const isOpenError = (x) => x && x.r < 2; // une erreur est « réglée » après 2 bonnes réponses d'affilée

  // ---------- Révision espacée ----------
  function srsGet() { return store.get("srs", {}); }
  function srsSet(srs) { store.set("srs", srs); }
  // État synchronisé entre appareils : chaque entrée porte un horodatage u, la plus récente gagne.
  const SYNC_KEYS = ["srs", "conf", "check"];
  async function srsSync() {
    if (!online()) return;
    try {
      const remote = (await rpc("rpc_state_get", { p_token: session.token })) || {};
      SYNC_KEYS.forEach((key) => {
        const r = remote[key] || {};
        const l = store.get(key, {});
        Object.keys(r).forEach((k) => { if (!l[k] || (r[k].u || 0) > (l[k].u || 0)) l[k] = r[k]; });
        store.set(key, l);
      });
    } catch (e) { /* hors ligne */ }
  }
  async function pushState(key) {
    if (!online()) return;
    try { await rpc("rpc_state_set", { p_token: session.token, p_key: key, p_value: store.get(key, {}) }); } catch (e) { /* plus tard */ }
  }
  const srsPush = () => pushState("srs");
  const isDue = (c, srs) => { const x = srs[c.id]; return !x || x.d <= now(); };

  // ---------- Confiance (n°8) ----------
  // conf[qid] = { c: "sure" | "doubt" | "guess", ok: 1 | 0, u }
  const CONF = { sure: "Sûr", doubt: "Hésitant", guess: "Au hasard" };
  const askConf = () => store.get("askConf", true);
  const isSureWrong = (x) => x && x.c === "sure" && x.ok === 0;

  // ---------- Checklist par chapitre (n°29) ----------
  function chapterStatus(sid, d, ch) {
    const srs = srsGet(), conf = store.get("conf", {}), check = store.get("check", {});
    const qs = d.quiz.filter((q) => q.ch === ch.id);
    const cs = d.cards.filter((c) => c.ch === ch.id);
    const answered = qs.filter((q) => conf[q.id] || store.get("qres", {})[q.id] !== undefined);
    const items = [
      { key: "fiche", label: "Fiche lue", done: !!(check[sid + ":" + ch.id] && check[sid + ":" + ch.id].v), manual: true },
      { key: "cards", label: "Cartes à jour", done: cs.length > 0 && cs.every((c) => srs[c.id] && srs[c.id].d > now()) },
      { key: "quiz", label: "Quiz ≥ 80 %", done: qs.length > 0 && mastery(qs) >= 0.8 },
      { key: "sure", label: "Aucun « sûr et faux »", done: answered.length > 0 && !qs.some((q) => isSureWrong(conf[q.id])) }
    ];
    return { items, n: items.filter((x) => x.done).length };
  }

  // ---------- Statistiques locales par question ----------
  function qresUpdate(results) { const q = store.get("qres", {}); Object.assign(q, results); store.set("qres", q); }
  function mastery(list) {
    const q = store.get("qres", {});
    if (!list.length) return 0;
    return list.filter((x) => q[x.id] === 1).length / list.length;
  }

  // ---------- Défi du jour (n°33) ----------
  // Le même défi pour toute la classe : 2 questions par matière, tirées dans un ordre fixe propre à chaque matière.
  const DAILY_START = "2026-11-25";
  const DAILY_PER_SUBJECT = 2;
  const todayKey = () => { const d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
  const dayIndex = (key) => Math.max(0, Math.round((Date.parse(key + "T12:00:00") - Date.parse(DAILY_START + "T12:00:00")) / DAY));
  function seeded(seedStr) {
    let h = 1779033703 ^ seedStr.length;
    for (let i = 0; i < seedStr.length; i++) { h = Math.imul(h ^ seedStr.charCodeAt(i), 3432918353); h = (h << 13) | (h >>> 19); }
    return function () { h = Math.imul(h ^ (h >>> 16), 2246822507); h = Math.imul(h ^ (h >>> 13), 3266489909); h ^= h >>> 16; return (h >>> 0) / 4294967296; };
  }
  async function dailyQuestions(key) {
    const idx = dayIndex(key), out = [];
    for (const s of subjects.filter((x) => x.file)) {
      const d = await loadSubject(s.id);
      const rnd = seeded("pge2-defi-" + s.id);
      const pool = d.quiz.slice().sort((a, b) => a.id.localeCompare(b.id));
      for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
      for (let k = 0; k < DAILY_PER_SUBJECT; k++) out.push(pool[(idx * DAILY_PER_SUBJECT + k) % pool.length]);
    }
    return shuffle(out);
  }
  const dailyDone = (key) => store.get("daily", {})[key || todayKey()];

  // ---------- Navigation ----------
  function setNav() {
    const h = location.hash || "#/";
    const links = [["#/", "Matières"], ["#/errors", "Mes erreurs"], ["#/lb", "Classement"]];
    const who = session ? (session.guest ? "Invité" : esc(session.pseudo)) : "Connexion";
    document.getElementById("topnav").innerHTML =
      links.map(([href, t]) => `<a href="${href}" class="${h === href || (href !== "#/" && h.startsWith(href)) ? "active" : ""}">${t}</a>`).join("") +
      `<a href="#/account" class="${h.startsWith("#/account") ? "active" : ""}">👤 ${who}</a>`;
    document.getElementById("foot-status").textContent = online() ? "Connecté·e : " + session.pseudo : (session && session.guest ? "Mode invité (progression sur cet appareil)" : "");
  }

  function parseHash() {
    const raw = (location.hash || "#/").slice(1);
    const [path, qs] = raw.split("?");
    const parts = path.split("/").filter(Boolean);
    const params = new URLSearchParams(qs || "");
    return { parts, params };
  }

  let leaveGuard = null;
  window.addEventListener("hashchange", route);

  async function route() {
    if (leaveGuard) { leaveGuard(); leaveGuard = null; }
    setNav();
    window.scrollTo(0, 0);
    const { parts, params } = parseHash();
    try {
      if (!session && parts[0] !== "account") return viewLogin();
      if (!parts.length) return viewHome();
      if (parts[0] === "account") return session ? viewAccount() : viewLogin();
      if (parts[0] === "s" && parts[1] && !parts[2]) return viewSubject(parts[1]);
      if (parts[0] === "s" && parts[2] === "quiz") return viewQuiz(parts[1], params);
      if (parts[0] === "s" && parts[2] === "cards") return viewCards(parts[1], params);
      if (parts[0] === "s" && parts[2] === "fiche") return viewFiche(parts[1], params);
      if (parts[0] === "errors" && parts[1] === "quiz") return viewErrorQuiz(params);
      if (parts[0] === "errors") return viewErrors();
      if (parts[0] === "lb") return viewLeaderboard(params);
      if (parts[0] === "daily") return viewDaily();
      location.hash = "#/";
    } catch (e) {
      $app.innerHTML = `<div class="notice err">${esc(e.message)}</div><a class="btn" href="#/">Retour</a>`;
    }
  }

  // ---------- Vue : connexion ----------
  function viewLogin() {
    $app.innerHTML = `
      <div class="hero"><div><h1>Rejoins la classe</h1>
      <p>Un pseudo et le code de classe suffisent. Pas d'e-mail, pas de mot de passe.</p></div>
      <div class="countdown"><b>J-${daysToExam()}</b><span>avant les partiels</span></div></div>
      <form class="panel" id="f-login" autocomplete="off">
        <div class="field-row">
          <div><label for="pseudo">Pseudo</label><input id="pseudo" type="text" maxlength="20" required placeholder="ex. Antoine G." value="${esc(store.get("lastPseudo", ""))}"></div>
          <div><label for="code">Code de classe</label><input id="code" type="text" required placeholder="Donné par Antoine" autocapitalize="characters" value="${esc(store.get("lastCode", ""))}"></div>
        </div>
        <p class="small muted">Utilise toujours le même pseudo : c'est lui qui retrouve ta progression sur un autre appareil. Le classement fonctionne sur la confiance, ne prends pas le pseudo d'un·e camarade.</p>
        <div id="login-msg"></div>
        <div class="actions">
          <button class="btn accent" type="submit">Entrer</button>
          <button class="btn secondary" type="button" id="guest">Réviser sans compte</button>
        </div>
      </form>`;
    document.getElementById("guest").onclick = () => {
      session = { guest: true }; store.set("session", session); location.hash = "#/"; route();
    };
    document.getElementById("f-login").onsubmit = async (ev) => {
      ev.preventDefault();
      const pseudo = document.getElementById("pseudo").value.trim();
      const code = document.getElementById("code").value.trim().toUpperCase();
      const msg = document.getElementById("login-msg");
      const btn = ev.submitter || ev.target.querySelector("button[type=submit]");
      btn.disabled = true; msg.innerHTML = "";
      try {
        const rows = await rpc("rpc_join", { p_code: code, p_pseudo: pseudo });
        const r = Array.isArray(rows) ? rows[0] : rows;
        session = { token: r.token, pseudo: r.pseudo };
        store.set("session", session); store.set("lastPseudo", r.pseudo); store.set("lastCode", code);
        await Promise.all([srsSync(), flushQueue()]);
        toast("Bienvenue " + r.pseudo + " !");
        location.hash = "#/"; route();
      } catch (e) {
        msg.innerHTML = `<div class="notice err">${esc(e.server ? e.message : "Serveur injoignable. Réessaie dans un instant, ou révise sans compte.")}</div>`;
      } finally { btn.disabled = false; }
    };
  }

  // ---------- Vue : compte ----------
  function viewAccount() {
    $app.innerHTML = `
      <h1>Mon compte</h1>
      <div class="panel">
        ${online() ? `<p>Connecté·e en tant que <b>${esc(session.pseudo)}</b>. Ta progression (cartes, erreurs, points) est enregistrée en ligne.</p>`
                   : `<p>Tu révises en <b>mode invité</b> : ta progression reste sur cet appareil et tu n'apparais pas au classement.</p>`}
        <div class="actions">
          ${online() ? "" : `<a class="btn accent" href="#/account/login" id="go-login">Rejoindre la classe</a>`}
          <button class="btn secondary" id="logout">${online() ? "Se déconnecter" : "Quitter le mode invité"}</button>
        </div>
      </div>
      <div class="panel">
        <h3>Réinitialiser cet appareil</h3>
        <p class="small muted">Efface les cartes, les erreurs et les statistiques gardées dans ce navigateur. Ce qui est en ligne n'est pas touché.</p>
        <button class="btn bad" id="reset">Effacer les données locales</button>
      </div>`;
    const gl = document.getElementById("go-login");
    if (gl) gl.onclick = (e) => { e.preventDefault(); session = null; store.del("session"); viewLogin(); setNav(); };
    document.getElementById("logout").onclick = () => { session = null; store.del("session"); leaderboardCache = null; location.hash = "#/"; route(); };
    document.getElementById("reset").onclick = () => {
      if (!confirm("Effacer toutes les données de révision de ce navigateur ?")) return;
      ["srs", "errors", "qres", "log", "queue", "conf", "check"].forEach(store.del); toast("Données locales effacées.");
    };
  }

  // ---------- Vue : accueil ----------
  async function viewHome() {
    const srs = srsGet();
    const errs = store.get("errors", {});
    const openErr = Object.values(errs).filter(isOpenError).length;
    const log = store.get("log", []);
    const todayPts = log.filter((l) => l.t >= today0()).reduce((a, l) => a + l.p, 0);

    const cards = await Promise.all(subjects.map(async (s) => {
      if (!s.file) {
        return `<div class="subject locked" style="--c:${s.color}"><h3>${esc(s.name)}</h3><div class="prof">${esc(s.prof)}</div>
          <div class="meta"><span class="pill warn">Supports manquants</span></div></div>`;
      }
      let due = 0, m = 0, nq = 0, ready = 0, nch = 0;
      try {
        const d = await loadSubject(s.id); due = d.cards.filter((c) => isDue(c, srs)).length; m = mastery(d.quiz); nq = d.quiz.length;
        nch = d.chapters.length; ready = d.chapters.filter((ch) => { const st = chapterStatus(s.id, d, ch); return st.n === st.items.length; }).length;
      } catch (e) { /* */ }
      return `<a class="subject" href="#/s/${s.id}" style="--c:${s.color}"><h3>${esc(s.name)}</h3><div class="prof">${esc(s.prof)}</div>
        <div class="meta"><span class="pill ${m >= .8 ? "ok" : ""}">Quiz maîtrisé ${Math.round(m * 100)} %</span>
        <span class="pill ${due ? "due" : "ok"}">${due ? due + " cartes à revoir" : "Cartes à jour"}</span>
        <span class="pill ${nch && ready === nch ? "ok" : ""}">${ready}/${nch} chapitres prêts</span></div></a>`;
    }));

    $app.innerHTML = `
      <div class="hero"><div><h1>${online() ? "Salut " + esc(session.pseudo) : "Révisions PGE2"}</h1>
        <p>Choisis une matière : un quiz de 10 questions ou une série de flashcards.</p></div>
        <div class="countdown"><b>J-${daysToExam()}</b><span>avant le 7 décembre</span></div></div>
      <div class="stats">
        <div class="stat"><b id="st-points">${online() ? "…" : log.reduce((a, l) => a + l.p, 0)}</b><span>points ${online() ? "au total" : "(sur cet appareil)"}</span></div>
        <div class="stat"><b>${todayPts}</b><span>points aujourd'hui</span></div>
        <div class="stat"><b id="st-streak">${online() ? "…" : "–"}</b><span>jours d'affilée</span></div>
        <a class="stat" href="#/errors" style="text-decoration:none"><b>${openErr}</b><span>erreurs à retravailler →</span></a>
      </div>
      ${!online() ? `<div class="notice">Mode invité : rien n'est envoyé au classement. <a href="#/account">Rejoindre la classe</a></div>` : ""}
      ${(() => { const dd = dailyDone(); const label = new Date().toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" });
        return `<div class="daily ${dd ? "done" : ""}"><div><div class="daily-k">🎯 Défi du jour · ${label}</div>
          ${dd ? `<div class="daily-t">Fait : ${dd.c}/${dd.n} · +${dd.p} points</div><div class="small">Un nouveau défi demain. Le même pour toute la classe.</div>`
               : `<div class="daily-t">10 questions, toutes matières · <b>points ×2</b></div><div class="small">Le même défi pour toute la classe, une seule tentative par jour.</div>`}</div>
          <div class="daily-a">${dd ? (online() ? `<a class="btn secondary" href="#/lb?p=daily">Classement du jour</a>` : "") : `<a class="btn accent" href="#/daily">Relever le défi</a>`}</div></div>`; })()}
      <h2>Matières</h2>
      <div class="grid">${cards.join("")}</div>`;

    if (online()) {
      try {
        const lb = await getLeaderboard();
        const me = lb.find((r) => r.is_me);
        if (me) {
          const a = document.getElementById("st-points"), b = document.getElementById("st-streak");
          if (a) a.textContent = me.points; if (b) b.textContent = me.streak;
        }
      } catch (e) { const a = document.getElementById("st-points"); if (a) a.textContent = "–"; }
    }
  }

  // ---------- Vue : matière ----------
  async function viewSubject(id) {
    const s = subjOf(id);
    if (!s || !s.file) { location.hash = "#/"; return; }
    $app.innerHTML = `<p class="muted">Chargement…</p>`;
    const d = await loadSubject(id);
    const srs = srsGet();
    const errs = store.get("errors", {});
    let ready = 0;
    const chapRows = d.chapters.map((ch) => {
      const qs = d.quiz.filter((q) => q.ch === ch.id);
      const cs = d.cards.filter((c) => c.ch === ch.id);
      const m = mastery(qs);
      const due = cs.filter((c) => isDue(c, srs)).length;
      const st = chapterStatus(id, d, ch);
      if (st.n === st.items.length) ready++;
      const checks = st.items.map((it) => it.manual
        ? `<label class="ck ${it.done ? "done" : ""}"><input type="checkbox" data-check="${id}:${ch.id}" ${it.done ? "checked" : ""}> ${it.label}</label>`
        : `<span class="ck ${it.done ? "done" : ""}">${it.done ? "✓" : "○"} ${it.label}</span>`).join("");
      return `<div class="chap ${st.n === st.items.length ? "ready" : ""}"><div class="chap-main"><div class="t"><b>${esc(ch.title)}</b><br><span class="muted small">${qs.length} questions · ${cs.length} cartes${due ? " · " + due + " à revoir" : ""}</span></div>
        <div style="display:flex;gap:8px;align-items:center"><span class="chap-score">${st.n}/${st.items.length}</span><div class="bar" title="Maîtrise du quiz"><i style="width:${Math.round(m * 100)}%"></i></div>
        <a class="pill" href="#/s/${id}/quiz?ch=${ch.id}">Quiz</a><a class="pill" href="#/s/${id}/cards?ch=${ch.id}">Cartes</a></div></div>
        <div class="checks">${checks}</div></div>`;
    }).join("");
    const due = d.cards.filter((c) => isDue(c, srs)).length;
    const nErr = d.quiz.filter((q) => isOpenError(errs[q.id])).length;

    $app.innerHTML = `
      <p><a href="#/" class="small muted">← Matières</a></p>
      <h1>${esc(s.name)}</h1>
      <p class="muted">${esc(s.prof)} · ${esc(d.exam || "")}</p>
      ${d.warning ? `<div class="notice">${esc(d.warning)}</div>` : ""}
      <div class="panel">
        <h3>Réviser toute la matière</h3>
        <div class="actions">
          ${s.fiche ? `<a class="btn fiche-btn" href="#/s/${id}/fiche">📄 Fiche de cours</a>` : ""}
          <a class="btn accent" href="#/s/${id}/quiz">Quiz de ${Math.min(CFG.quizLength, d.quiz.length)} questions</a>
          <a class="btn" href="#/s/${id}/cards">Flashcards ${due ? "(" + Math.min(due, CFG.cardsPerSession) + " à revoir)" : ""}</a>
          <a class="btn secondary" href="#/s/${id}/quiz?all=1">Les ${d.quiz.length} questions</a>
          ${nErr ? `<a class="btn secondary" href="#/errors/quiz?s=${id}">Mes ${nErr} erreurs</a>` : ""}
        </div>
      </div>
      <h2>Par chapitre <span class="pill ${ready === d.chapters.length ? "ok" : ""}">${ready}/${d.chapters.length} prêts</span></h2>
      <div class="chapters">${chapRows}</div>
      <p class="small muted" style="margin-top:16px">Un chapitre est prêt quand ses 4 cases sont cochées. « Fiche lue » se coche à la main, les trois autres se cochent toutes seules : toutes les cartes revues et pas à revoir aujourd'hui, au moins 80 % des questions réussies sans répondre au hasard, et aucune réponse fausse donnée en étant sûr·e. Les questions marquées « Complément » viennent de la fiche mais pas directement des slides du prof.</p>`;
    $app.querySelectorAll("[data-check]").forEach((cb) => {
      cb.onchange = () => {
        const check = store.get("check", {});
        check[cb.dataset.check] = { v: cb.checked ? 1 : 0, u: now() };
        store.set("check", check); pushState("check");
        viewSubject(id);
      };
    });
  }

  // ---------- Signaler une question ou une carte ----------
  const REASONS = ["Réponse fausse", "Question ambiguë", "Faute ou coquille", "Hors programme", "Autre"];
  function reportLink(itemId) {
    const done = store.get("reported", {})[itemId];
    return `<span class="report-slot" data-item="${esc(itemId)}">${done ? `<span class="small muted">Signalé ✓</span>` : `<button type="button" class="linkbtn small" data-report="${esc(itemId)}">Signaler une erreur</button>`}</span>`;
  }
  function wireReports(root) {
    (root || $app).querySelectorAll("[data-report]").forEach((b) => {
      b.onclick = (ev) => {
        ev.stopPropagation();
        const id = b.dataset.report;
        const slot = b.closest(".report-slot");
        if (!online()) { toast("Rejoins la classe (onglet compte) pour signaler une erreur."); return; }
        slot.innerHTML = `<div class="report-box" onclick="event.stopPropagation()">
          <select aria-label="Motif">${REASONS.map((r) => `<option>${r}</option>`).join("")}</select>
          <textarea maxlength="500" rows="2" placeholder="Qu'est-ce qui ne va pas ? Si tu connais la bonne réponse, écris-la (facultatif)"></textarea>
          <div class="actions" style="margin-top:6px"><button type="button" class="btn" data-send>Envoyer</button><button type="button" class="btn secondary" data-cancel>Annuler</button></div></div>`;
        slot.querySelector("[data-cancel]").onclick = (e) => { e.stopPropagation(); slot.outerHTML = reportLink(id); wireReports(root); };
        slot.querySelector("[data-send]").onclick = async (e) => {
          e.stopPropagation();
          const btn = e.currentTarget; btn.disabled = true;
          try {
            await rpc("rpc_report", { p_token: session.token, p_item_id: id, p_reason: slot.querySelector("select").value, p_comment: slot.querySelector("textarea").value });
            const r = store.get("reported", {}); r[id] = now(); store.set("reported", r);
            slot.innerHTML = `<span class="small muted">Signalé ✓ Merci, Antoine va vérifier.</span>`;
          } catch (err) { btn.disabled = false; toast(err.server ? err.message : "Serveur injoignable, réessaie plus tard."); }
        };
      };
    });
  }

  // ---------- Moteur de quiz ----------
  function runQuiz({ title, back, questions, subject, mode }) {
    let i = 0, correct = 0;
    const wrong = [], right = [], answers = [];
    const prepared = questions.map((q) => {
      const order = shuffle(q.choices.map((_, k) => k));
      return Object.assign({}, q, { order });
    });
    let finished = false;
    leaveGuard = () => {
      if (!finished && answers.length >= 3) toast("Quiz interrompu : les réponses données n'ont pas été comptées.");
    };

    function renderQ() {
      const q = prepared[i];
      $app.innerHTML = `
        <p><a href="${back}" class="small muted">← Quitter</a></p>
        <div class="qhead"><span>${esc(title)}</span><span>Question ${i + 1} / ${prepared.length} · ${correct} juste${correct > 1 ? "s" : ""} · <button class="linkbtn small" id="conf-toggle" title="Demander si tu étais sûr avant de corriger">Confiance : ${askConf() ? "oui" : "non"}</button></span></div>
        <div class="progress"><i style="width:${(i / prepared.length) * 100}%"></i></div>
        <div class="panel">
          <div class="question">${esc(q.q)}${q.flag ? `<span class="flag">${esc(q.flag)}</span>` : ""}</div>
          <div class="choices">${q.order.map((k, n) => `<button class="choice" data-k="${k}"><span class="k">${"ABCD"[n]}</span><span>${esc(q.choices[k])}</span></button>`).join("")}</div>
          <div id="after"></div>
        </div>`;
      $app.querySelectorAll(".choice").forEach((b) => { b.onclick = () => pick(+b.dataset.k, b); });
      document.getElementById("conf-toggle").onclick = () => {
        store.set("askConf", !askConf());
        document.getElementById("conf-toggle").textContent = "Confiance : " + (askConf() ? "oui" : "non");
      };
    }

    function pick(k, btn) {
      if (!askConf()) return answer(k, null);
      $app.querySelectorAll(".choice").forEach((b) => { b.disabled = true; });
      btn.classList.add("picked");
      document.getElementById("after").innerHTML = `
        <div class="confbar"><span>Avant de voir la correction : tu étais…</span>
          <div class="conf-btns">${Object.entries(CONF).map(([c, l]) => `<button class="btn secondary conf-${c}" data-c="${c}">${l}</button>`).join("")}</div>
          <button class="linkbtn small" id="conf-undo">Changer de réponse</button></div>`;
      document.querySelectorAll(".conf-btns button").forEach((b) => { b.onclick = () => answer(k, b.dataset.c); });
      document.getElementById("conf-undo").onclick = () => {
        $app.querySelectorAll(".choice").forEach((b) => { b.disabled = false; b.classList.remove("picked"); });
        document.getElementById("after").innerHTML = "";
      };
    }

    function answer(k, c) {
      const q = prepared[i];
      const ok = k === q.answer;
      if (ok) { correct++; if (c !== "guess") right.push(q.id); } else wrong.push(q.id);
      answers.push({ q, k, ok, c });
      $app.querySelectorAll(".choice").forEach((b) => {
        b.disabled = true;
        const bk = +b.dataset.k;
        b.classList.remove("picked");
        if (bk === q.answer) b.classList.add("correct");
        else if (bk === k) b.classList.add("wrong");
      });
      const last = i === prepared.length - 1;
      const confNote = c === "sure" && !ok ? `<div class="conf-alert">⚠️ Faux alors que tu étais sûr·e : c'est le type d'erreur le plus dangereux à l'examen, elle est mise de côté dans « Mes erreurs ».</div>`
        : c === "guess" && ok ? `<div class="conf-note">Juste, mais au hasard : elle reviendra dans tes prochains quiz.</div>` : "";
      document.getElementById("after").innerHTML = `${confNote}
        <div class="explain"><b class="${ok ? "ok" : "ko"}">${ok ? "Juste." : "Faux."}</b> ${esc(q.explain || "")}</div>
        <div class="actions" style="align-items:center;justify-content:space-between"><button class="btn accent" id="next">${last ? "Voir mon score" : "Question suivante →"}</button>${reportLink(q.id)}</div>`;
      wireReports(document.getElementById("after"));
      const nb = document.getElementById("next");
      nb.focus({ preventScroll: true });
      nb.onclick = () => { if (last) finish(); else { i++; renderQ(); window.scrollTo(0, 0); } };
    }

    async function finish() {
      if (finished) return;
      finished = true;
      $app.innerHTML = `<p class="muted">Calcul du score…</p>`;
      const qr = {}; answers.forEach((a) => { qr[a.q.id] = a.ok && a.c !== "guess" ? 1 : 0; });
      qresUpdate(qr);
      const withConf = answers.filter((a) => a.c);
      const conf = store.get("conf", {});
      let confChanged = false;
      answers.forEach((a) => {
        if (a.c) { conf[a.q.id] = { c: a.c, ok: a.ok ? 1 : 0, u: now() }; confChanged = true; }
        else if (a.ok && conf[a.q.id] && conf[a.q.id].ok === 0) { conf[a.q.id] = Object.assign({}, conf[a.q.id], { ok: 1, u: now() }); confChanged = true; }
      });
      if (confChanged) { store.set("conf", conf); pushState("conf"); }
      // Par matière (le quiz d'erreurs peut mélanger les matières)
      const bySubj = {};
      answers.forEach((a) => {
        const s = a.q.subject;
        bySubj[s] = bySubj[s] || { c: 0, n: 0, w: [], r: [] };
        bySubj[s].n++; if (a.ok) { bySubj[s].c++; if (a.c !== "guess") bySubj[s].r.push(a.q.id); } else bySubj[s].w.push(a.q.id);
      });
      let pts = 0;
      if (mode === "daily") {
        Object.keys(bySubj).forEach((s) => localErrorsUpdate(bySubj[s].w, bySubj[s].r, s));
        const allW = answers.filter((a) => !a.ok).map((a) => a.q.id);
        const allR = answers.filter((a) => a.ok && a.c !== "guess").map((a) => a.q.id);
        pts = await recordSession("daily", "daily", correct, prepared.length, allW, allR);
        const dd = store.get("daily", {}); dd[todayKey()] = { c: correct, n: prepared.length, p: pts }; store.set("daily", dd);
      } else {
        for (const s of Object.keys(bySubj)) {
          const b = bySubj[s];
          localErrorsUpdate(b.w, b.r, s);
          pts += await recordSession(s, mode, b.c, b.n, b.w, b.r);
        }
      }
      const pct = Math.round((correct / prepared.length) * 100);
      const cell = (c, ok) => withConf.filter((a) => a.c === c && a.ok === ok).length;
      const sureWrong = cell("sure", false), luckyRight = cell("guess", true);
      const matrix = withConf.length ? `<div class="panel"><h3>Ta confiance</h3>
        <table class="conf-matrix"><thead><tr><th></th><th>Juste</th><th>Faux</th></tr></thead><tbody>
        ${Object.entries(CONF).map(([c, l]) => `<tr><th>${l}</th><td class="${c === "sure" ? "good" : ""}">${cell(c, true)}</td><td class="${c === "sure" && cell(c, false) ? "danger" : ""}">${cell(c, false)}</td></tr>`).join("")}
        </tbody></table>
        <p class="small muted">${sureWrong ? `<b style="color:var(--bad)">${sureWrong} erreur${sureWrong > 1 ? "s" : ""} « sûr et faux »</b> : ce sont celles que tu ne vérifierais pas le jour J. Elles sont regroupées dans Mes erreurs. ` : "Aucune erreur « sûr et faux », bon signe. "}${luckyRight ? `${luckyRight} bonne${luckyRight > 1 ? "s" : ""} réponse${luckyRight > 1 ? "s" : ""} au hasard : pas encore acquise${luckyRight > 1 ? "s" : ""}, elle${luckyRight > 1 ? "s" : ""} reviendra dans tes prochains quiz.` : ""}</p></div>` : "";
      const verdict = pct >= 80 ? "Excellent, c'est maîtrisé." : pct >= 60 ? "Pas mal, revois les erreurs ci-dessous." : "À retravailler : relis la fiche puis refais le quiz.";
      $app.innerHTML = `
        <p><a href="${back}" class="small muted">← Retour</a></p>
        <div class="panel" style="text-align:center">
          <div class="score">${correct} / ${prepared.length}</div>
          <p><b>${pct} %</b> · +${pts} points${online() ? "" : " (mode invité)"}</p>
          <p class="muted">${verdict}</p>
          <div class="actions" style="justify-content:center">
            ${mode === "daily" ? (online() ? `<a class="btn accent" href="#/lb?p=daily">Classement du jour</a>` : "") : `<button class="btn accent" id="again">Nouveau quiz</button>`}
            <a class="btn secondary" href="#/errors">Mes erreurs</a>
            ${online() ? `<a class="btn secondary" href="#/lb">Classement</a>` : ""}
          </div>
        </div>
        ${matrix}
        ${answers.some((a) => !a.ok) ? `<h2>À revoir</h2><div class="panel">${answers.filter((a) => !a.ok).map((a) => `
          <div class="review-item"><div><b>${esc(a.q.q)}</b></div>
          <div class="small">Ta réponse : <span style="color:var(--bad)">${esc(a.q.choices[a.k])}</span>${a.c ? ` <span class="pill ${a.c === "sure" ? "warn" : ""}">${CONF[a.c]}</span>` : ""}</div>
          <div class="small">Bonne réponse : <span class="a">${esc(a.q.choices[a.q.answer])}</span></div>
          <div class="small muted">${esc(a.q.explain || "")}</div><div style="margin-top:4px">${reportLink(a.q.id)}</div></div>`).join("")}</div>` : ""}`;
      wireReports();
      const ag = document.getElementById("again"); if (ag) ag.onclick = () => route();
    }

    renderQ();
  }

  async function viewQuiz(id, params) {
    const s = subjOf(id);
    if (!s || !s.file) { location.hash = "#/"; return; }
    const d = await loadSubject(id);
    const ch = params.get("ch");
    let pool = ch ? d.quiz.filter((q) => q.ch === ch) : d.quiz.slice();
    if (!pool.length) { $app.innerHTML = `<div class="empty">Pas de question pour ce chapitre.</div>`; return; }
    // Priorité aux questions jamais vues ou ratées, puis au hasard
    const qres = store.get("qres", {});
    const weight = (q) => (qres[q.id] === 1 ? 2 : qres[q.id] === 0 ? 0 : 1) + Math.random() * 1.5;
    const all = params.get("all") === "1";
    const list = all ? shuffle(pool) : pool.map((q) => [weight(q), q]).sort((a, b) => a[0] - b[0]).map((x) => x[1]).slice(0, CFG.quizLength);
    const chap = ch ? d.chapters.find((c) => c.id === ch) : null;
    runQuiz({ title: s.short + (chap ? " · " + chap.title : ""), back: "#/s/" + id, questions: shuffle(list), subject: id, mode: "quiz" });
  }

  // ---------- Vue : défi du jour ----------
  async function viewDaily() {
    const key = todayKey();
    if (dailyDone(key)) { location.hash = "#/"; return; }
    $app.innerHTML = `<p class="muted">Préparation du défi…</p>`;
    const qs = await dailyQuestions(key);
    const label = new Date().toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" });
    runQuiz({ title: "🎯 Défi du jour · " + label + " · points ×2", back: "#/", questions: qs, subject: null, mode: "daily" });
  }

  // ---------- Vue : erreurs ----------
  async function viewErrors() {
    $app.innerHTML = `<h1>Mes erreurs</h1><p class="muted">Chargement…</p>`;
    const errs = await getErrors();
    const open = Object.entries(errs).filter(([, x]) => isOpenError(x));
    const solved = Object.entries(errs).filter(([, x]) => !isOpenError(x)).length;
    const conf = store.get("conf", {});
    const nSure = open.filter(([qid]) => isSureWrong(conf[qid])).length;
    if (!open.length) {
      $app.innerHTML = `<h1>Mes erreurs</h1><div class="panel empty">${Object.keys(errs).length ? "Toutes tes erreurs sont réglées. Bravo." : "Aucune erreur enregistrée pour l'instant. Fais un quiz : chaque question ratée arrivera ici."}</div>`;
      return;
    }
    const bySubj = {};
    open.forEach(([qid, x]) => { const s = x.s || qSubject(qid); (bySubj[s] = bySubj[s] || []).push([qid, x]); });
    const blocks = [];
    for (const sid of Object.keys(bySubj)) {
      const s = subjOf(sid); if (!s || !s.file) continue;
      const d = await loadSubject(sid);
      const items = bySubj[sid].map(([qid, x]) => [d.quiz.find((q) => q.id === qid), x]).filter(([q]) => q)
        .sort((a, b) => b[1].w - a[1].w);
      if (!items.length) continue;
      blocks.push(`<h2>${esc(s.name)} <span class="pill warn">${items.length}</span></h2>
        <div class="actions" style="margin-top:0"><a class="btn accent" href="#/errors/quiz?s=${sid}">Retravailler ces ${items.length} questions</a></div>
        <div class="panel" style="margin-top:10px">${items.map(([q, x]) => `
          <div class="review-item"><div><b>${esc(q.q)}</b></div>
          <div class="small">Réponse : <span class="a">${esc(q.choices[q.answer])}</span></div>
          <div class="small muted">${esc(q.explain || "")}</div>
          <div class="small" style="margin-top:4px">${isSureWrong(conf[q.id]) ? `<span class="pill warn">⚠️ sûr et faux</span> ` : ""}<span class="pill warn">ratée ${x.w} fois</span> ${x.r ? `<span class="pill ok">${x.r}/2 bonne réponse</span>` : ""} ${reportLink(q.id)}</div></div>`).join("")}</div>`);
    }
    $app.innerHTML = `<h1>Mes erreurs</h1>
      <p class="muted">Une question sort de la liste quand tu y réponds juste 2 fois d'affilée. ${solved ? solved + " erreur" + (solved > 1 ? "s" : "") + " déjà réglée" + (solved > 1 ? "s" : "") + "." : ""}</p>
      ${nSure ? `<div class="panel sure-panel"><h3>⚠️ ${nSure} erreur${nSure > 1 ? "s" : ""} « sûr et faux »</h3>
        <p class="small">Tu étais sûr·e de ta réponse et elle était fausse. À l'examen, ce sont celles que tu ne vérifies pas : retravaille-les en premier.</p>
        <div class="actions" style="margin-top:6px"><a class="btn bad" href="#/errors/quiz?sure=1">Retravailler ces ${nSure} questions</a></div></div>` : ""}
      <div class="actions"><a class="btn" href="#/errors/quiz">Quiz sur toutes mes erreurs (${open.length})</a></div>
      ${blocks.join("")}`;
    wireReports();
  }

  async function viewErrorQuiz(params) {
    const errs = await getErrors();
    const only = params.get("s");
    const sureOnly = params.get("sure") === "1";
    const conf = store.get("conf", {});
    const ids = Object.entries(errs).filter(([qid, x]) => isOpenError(x) && (!only || (x.s || qSubject(qid)) === only) && (!sureOnly || isSureWrong(conf[qid]))).map(([qid]) => qid);
    const qs = [];
    for (const qid of ids) {
      const sid = errs[qid].s || qSubject(qid); const s = subjOf(sid);
      if (!s || !s.file) continue;
      const d = await loadSubject(sid); const q = d.quiz.find((x) => x.id === qid);
      if (q) qs.push(q);
    }
    if (!qs.length) { location.hash = "#/errors"; return; }
    runQuiz({ title: (sureOnly ? "Mes erreurs « sûr et faux »" : "Mes erreurs") + (only ? " · " + subjOf(only).short : ""), back: "#/errors", questions: shuffle(qs).slice(0, 20), subject: only, mode: "errors" });
  }

  // ---------- Vue : flashcards ----------
  async function viewCards(id, params) {
    const s = subjOf(id);
    if (!s || !s.file) { location.hash = "#/"; return; }
    const d = await loadSubject(id);
    const ch = params.get("ch");
    const srs = srsGet();
    let pool = ch ? d.cards.filter((c) => c.ch === ch) : d.cards.slice();
    let dueCards = pool.filter((c) => isDue(c, srs));
    const extra = params.get("extra") === "1";
    if (!dueCards.length && !extra) {
      const next = pool.map((c) => srs[c.id] ? srs[c.id].d : 0).sort((a, b) => a - b)[0];
      $app.innerHTML = `<p><a href="#/s/${id}" class="small muted">← ${esc(s.short)}</a></p>
        <div class="panel empty"><h3>Tout est à jour</h3><p>Aucune carte à revoir ${ch ? "dans ce chapitre" : ""} pour le moment${next ? ", prochaine le " + new Date(next).toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" }) : ""}.</p>
        <div class="actions" style="justify-content:center"><a class="btn" href="#/s/${id}/cards?extra=1${ch ? "&ch=" + ch : ""}">Réviser quand même</a><a class="btn secondary" href="#/s/${id}/quiz${ch ? "?ch=" + ch : ""}">Faire un quiz</a></div></div>`;
      return;
    }
    if (!dueCards.length) dueCards = pool;
    // Nouvelles cartes et boîtes basses d'abord
    const queue = dueCards.map((c) => [(srs[c.id] ? srs[c.id].b : -1) + Math.random(), c]).sort((a, b) => a[0] - b[0]).map((x) => x[1]).slice(0, CFG.cardsPerSession);
    const total = queue.length;
    const failedOnce = new Set();
    let known = 0, seen = 0, flipped = false;
    const chap = ch ? d.chapters.find((c) => c.id === ch) : null;
    let finished = false;
    leaveGuard = () => { if (!finished && seen) { srsPush(); recordSession(id, "cards", known, seen, [], []); } };

    function render() {
      const c = queue[0];
      flipped = false;
      $app.innerHTML = `
        <p><a href="#/s/${id}" class="small muted">← Terminer</a></p>
        <div class="qhead"><span>${esc(s.short)}${chap ? " · " + esc(chap.title) : ""} · Flashcards</span><span>${Math.min(seen + 1, total)} / ${total}${queue.length > total - seen ? " (+ reprises)" : ""}</span></div>
        <div class="progress"><i style="width:${(seen / total) * 100}%"></i></div>
        <div class="flash" id="flash" role="button" tabindex="0" aria-label="Retourner la carte">
          <div class="flash-inner">
            <div class="face front"><span class="lbl">Question</span><div class="txt">${esc(c.front)}</div></div>
            <div class="face back"><span class="lbl">Réponse${c.flag ? " · " + esc(c.flag) : ""}</span><div class="txt">${esc(c.back)}</div></div>
          </div>
        </div>
        <p class="hint" id="hint">Touche la carte (ou Espace) pour voir la réponse.</p>
        <div class="actions" id="grade" style="justify-content:center;visibility:hidden">
          <button class="btn bad" id="again">À revoir</button>
          <button class="btn good" id="knew">Je savais</button>
        </div>
        <p class="hint" id="rep-card" style="visibility:hidden">${reportLink(c.id)}</p>`;
      wireReports(document.getElementById("rep-card"));
      const f = document.getElementById("flash");
      const flip = () => { flipped = !flipped; f.classList.toggle("flipped", flipped); document.getElementById("grade").style.visibility = "visible"; document.getElementById("rep-card").style.visibility = "visible"; document.getElementById("hint").style.visibility = "hidden"; };
      f.onclick = flip;
      f.onkeydown = (e) => { if (e.key === " " || e.key === "Enter") { e.preventDefault(); flip(); } };
      document.getElementById("again").onclick = () => grade(false);
      document.getElementById("knew").onclick = () => grade(true);
      f.focus({ preventScroll: true });
    }

    function grade(ok) {
      if (finished || !queue.length) return;
      const c = queue.shift();
      const st = srsGet();
      const cur = st[c.id] || { b: 0 };
      const firstTime = !failedOnce.has(c.id);
      if (ok) {
        const b = failedOnce.has(c.id) ? Math.max(cur.b, 1) : Math.min((cur.b || 0) + 1, INTERVALS.length - 1);
        st[c.id] = { b, d: today0() + INTERVALS[b] * DAY, u: now() };
        if (firstTime) { known++; seen++; }
      } else {
        st[c.id] = { b: 0, d: now(), u: now() };
        if (firstTime) { seen++; failedOnce.add(c.id); queue.push(c); } // une reprise en fin de série
      }
      srsSet(st);
      if (!queue.length) return done();
      render();
    }

    async function done() {
      if (finished) return;
      finished = true;
      $app.innerHTML = `<p class="muted">Enregistrement…</p>`;
      const pts = await recordSession(id, "cards", known, total, [], []);
      srsPush();
      $app.innerHTML = `<p><a href="#/s/${id}" class="small muted">← ${esc(s.short)}</a></p>
        <div class="panel" style="text-align:center"><div class="score">${known} / ${total}</div>
        <p>cartes sues du premier coup · +${pts} points</p>
        <p class="muted">Les cartes ratées reviendront dès demain, les autres de plus en plus tard (1, 2, 4 puis 7 jours).</p>
        <div class="actions" style="justify-content:center"><a class="btn accent" href="#/s/${id}/quiz${ch ? "?ch=" + ch : ""}">Enchaîner sur un quiz</a><a class="btn secondary" href="#/s/${id}">Retour à la matière</a></div></div>`;
    }

    document.onkeydown = (e) => {
      if (!document.getElementById("flash")) { document.onkeydown = null; return; }
      if (["INPUT", "TEXTAREA", "SELECT"].includes(e.target.tagName)) return;
      if (flipped && (e.key === "1" || e.key === "ArrowLeft")) grade(false);
      if (flipped && (e.key === "2" || e.key === "ArrowRight")) grade(true);
    };
    render();
  }

  // ---------- Vue : fiche de cours ----------
  const ficheCache = {};
  let katexLoaded = false;
  function ensureKatexCss() {
    if (katexLoaded) return; katexLoaded = true;
    const l = document.createElement("link"); l.rel = "stylesheet"; l.href = "css/katex/katex.min.css";
    document.head.appendChild(l);
  }

  async function viewFiche(id, params) {
    const s = subjOf(id);
    if (!s || !s.fiche) { location.hash = "#/"; return; }
    $app.innerHTML = `<p class="muted">Chargement de la fiche…</p>`;
    if (!ficheCache[id]) {
      const r = await fetch("data/" + s.fiche, { cache: "no-cache" });
      if (!r.ok) throw new Error("Fiche introuvable");
      ficheCache[id] = await r.json();
    }
    const f = ficheCache[id];
    const prefs = store.get("ficheTab", {});
    const key = params.get("tab") || prefs[id] || "detaillee";
    const tab = f.tabs.find((t) => t.key === key) || f.tabs[0];
    prefs[id] = tab.key; store.set("ficheTab", prefs);
    if (/class="katex/.test(tab.html)) ensureKatexCss();

    const toc = tab.toc.map((t) => `<a href="#" data-target="${esc(t.id)}" class="toc-l${t.level}">${esc(t.text)}</a>`).join("");
    $app.innerHTML = `
      <p><a href="#/s/${id}" class="small muted">← ${esc(s.short)}</a></p>
      <div class="fiche-head">
        <div><h1>${esc(f.title)}</h1>
        <p class="muted small">Copie des fiches de révision, mise à jour le ${new Date(f.updated).toLocaleDateString("fr-FR", { day: "numeric", month: "long" })}.</p></div>
        <div class="tabs" role="tablist">${f.tabs.map((t) => `<button role="tab" data-tab="${t.key}" class="${t.key === tab.key ? "on" : ""}">${esc(t.name)}</button>`).join("")}</div>
      </div>
      <div class="fiche-layout">
        <nav class="toc" id="toc" aria-label="Sommaire">
          <button class="toc-toggle" id="toc-toggle" aria-expanded="false">☰ Sommaire</button>
          <div class="toc-list" id="toc-list"><div class="toc-title">Sommaire</div>${toc}</div>
        </nav>
        <article class="fiche" id="fiche">${tab.html}</article>
      </div>
      <div class="fiche-foot actions">
        <a class="btn accent" href="#/s/${id}/quiz">Tester avec un quiz</a>
        <a class="btn secondary" href="#/s/${id}/cards">Flashcards</a>
        <button class="btn secondary" id="to-top">↑ Haut de page</button>
      </div>`;

    document.querySelectorAll(".fiche-head .tabs button").forEach((b) => {
      b.onclick = () => { location.hash = "#/s/" + id + "/fiche?tab=" + b.dataset.tab; };
    });
    const list = document.getElementById("toc-list");
    const toggle = document.getElementById("toc-toggle");
    toggle.onclick = () => { const open = list.classList.toggle("open"); toggle.setAttribute("aria-expanded", open); };
    list.querySelectorAll("a[data-target]").forEach((a) => {
      a.onclick = (e) => {
        e.preventDefault();
        const el = document.getElementById(a.dataset.target);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
        list.classList.remove("open"); toggle.setAttribute("aria-expanded", "false");
      };
    });
    document.getElementById("to-top").onclick = () => window.scrollTo({ top: 0, behavior: "smooth" });

    // Surligne la section en cours de lecture
    if ("IntersectionObserver" in window) {
      const links = {}; list.querySelectorAll("a[data-target]").forEach((a) => { links[a.dataset.target] = a; });
      const obs = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            Object.values(links).forEach((l) => l.classList.remove("active"));
            const l = links[en.target.id]; if (l) { l.classList.add("active"); const t = l.offsetTop; if (t < list.scrollTop || t > list.scrollTop + list.clientHeight - 30) list.scrollTop = t - 40; }
          }
        });
      }, { rootMargin: "-80px 0px -70% 0px" });
      document.querySelectorAll("#fiche h2, #fiche h3").forEach((h) => obs.observe(h));
      leaveGuard = () => obs.disconnect();
    }
  }

  // ---------- Vue : classement ----------
  async function getLeaderboard() {
    if (leaderboardCache && now() - leaderboardCache.t < 30000) return leaderboardCache.rows;
    const rows = await rpc("rpc_leaderboard", { p_token: session.token });
    leaderboardCache = { t: now(), rows };
    return rows;
  }

  async function viewLeaderboard(params) {
    if (!online()) {
      $app.innerHTML = `<h1>Classement</h1><div class="panel empty">Le classement est réservé aux camarades qui ont rejoint la classe.<div class="actions" style="justify-content:center"><a class="btn accent" href="#/account">Rejoindre la classe</a></div></div>`;
      return;
    }
    $app.innerHTML = `<h1>Classement</h1><p class="muted">Chargement…</p>`;
    let rows;
    try { await flushQueue(); leaderboardCache = null; rows = await getLeaderboard(); }
    catch (e) { $app.innerHTML = `<h1>Classement</h1><div class="notice err">${esc(e.server ? e.message : "Serveur injoignable pour le moment. Tes résultats sont gardés et seront envoyés plus tard.")}</div>`; return; }
    let period = params && params.get("p") === "daily" ? "daily" : "all";
    let dailyRows = null;
    const drawDaily = async () => {
      const tb = document.getElementById("lb");
      document.getElementById("lb-head").innerHTML = `<tr><th>#</th><th>Pseudo</th><th class="num">Score</th><th class="num">Points</th><th class="num hide-sm">Heure</th></tr>`;
      tb.innerHTML = `<tr><td colspan="5" class="muted">Chargement…</td></tr>`;
      try { dailyRows = dailyRows || await rpc("rpc_daily_board", { p_token: session.token }); }
      catch (e) { tb.innerHTML = `<tr><td colspan="5" class="muted">${e.server && /rpc_daily_board/.test(e.message) ? "Le défi du jour n'est pas encore activé." : esc(e.message)}</td></tr>`; return; }
      let rank = 0, prev = null;
      tb.innerHTML = dailyRows.map((r, n) => {
        if (r.correct !== prev) { rank = n + 1; prev = r.correct; }
        const medal = rank === 1 ? "🥇" : rank === 2 ? "🥈" : rank === 3 ? "🥉" : rank;
        return `<tr class="${r.is_me ? "me" : ""}"><td class="rank">${medal}</td><td>${esc(r.pseudo)}</td><td class="num"><b>${r.correct}/${r.total}</b></td><td class="num">${r.points}</td>
          <td class="num hide-sm">${new Date(r.done_at).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}</td></tr>`;
      }).join("") || `<tr><td colspan="5" class="empty">Personne n'a encore relevé le défi aujourd'hui.${dailyDone() ? "" : ` <a href="#/daily">Sois le premier !</a>`}</td></tr>`;
      document.querySelectorAll(".tabs button").forEach((b) => b.classList.toggle("on", b.dataset.p === period));
    };
    const draw = () => {
      if (period === "daily") return drawDaily();
      document.getElementById("lb-head").innerHTML = `<tr><th>#</th><th>Pseudo</th><th class="num">Points</th><th class="num hide-sm">Réussite quiz</th><th class="num">Série</th><th class="num hide-sm">Sessions</th></tr>`;
      const key = period === "all" ? "points" : "points_7d";
      const sorted = rows.slice().sort((a, b) => b[key] - a[key] || a.pseudo.localeCompare(b.pseudo));
      let rank = 0, prev = null;
      const body = sorted.map((r, n) => {
        if (r[key] !== prev) { rank = n + 1; prev = r[key]; }
        const medal = rank === 1 ? "🥇" : rank === 2 ? "🥈" : rank === 3 ? "🥉" : rank;
        return `<tr class="${r.is_me ? "me" : ""}"><td class="rank">${r[key] ? medal : "–"}</td><td>${esc(r.pseudo)}</td>
          <td class="num"><b>${r[key]}</b></td><td class="num hide-sm">${r.accuracy == null ? "–" : r.accuracy + " %"}</td>
          <td class="num">${r.streak ? "🔥 " + r.streak : "–"}</td><td class="num hide-sm">${r.sessions}</td></tr>`;
      }).join("");
      document.getElementById("lb").innerHTML = body || `<tr><td colspan="6" class="empty">Personne pour l'instant.</td></tr>`;
      document.querySelectorAll(".tabs button").forEach((b) => b.classList.toggle("on", b.dataset.p === period));
    };
    $app.innerHTML = `<h1>Classement</h1>
      <p class="muted">10 points par bonne réponse en quiz, 20 au défi du jour, 2 points par flashcard sue. La série compte les jours d'affilée avec au moins une session.</p>
      <div class="tabs" role="tablist"><button data-p="all">Depuis le début</button><button data-p="7d">7 derniers jours</button><button data-p="daily">🎯 Défi du jour</button></div>
      <div class="panel" style="margin-top:12px;padding:6px 12px">
        <table class="lb"><thead id="lb-head"></thead>
        <tbody id="lb"></tbody></table></div>`;
    document.querySelectorAll(".tabs button").forEach((b) => { b.onclick = () => { period = b.dataset.p; draw(); }; });
    draw();
  }

  // ---------- Démarrage ----------
  (async function start() {
    try { await loadSubjects(); }
    catch (e) { $app.innerHTML = `<div class="notice err">Impossible de charger le contenu. Recharge la page.</div>`; return; }
    if (online()) { srsSync(); flushQueue(); }
    route();
  })();
})();

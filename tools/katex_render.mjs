import katex from 'katex'; import fs from 'fs';
// Rend toutes les formules <div class="math">…</div> trouvées dans n'importe quel texte du JSON (fiches et partiels types).
const re = /<div class="math">([\s\S]*?)<\/div>/g;
for (const f of process.argv.slice(2)) {
  let n = 0;
  const walk = (v) => {
    if (typeof v === 'string') return v.replace(re, (m, tex) => {
      if (tex.includes('class="katex')) return m;
      n++; tex = tex.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');
      return '<div class="math">' + katex.renderToString(tex, {displayMode:true, throwOnError:false, output:'html'}) + '</div>';
    });
    if (Array.isArray(v)) return v.map(walk);
    if (v && typeof v === 'object') { for (const k in v) v[k] = walk(v[k]); return v; }
    return v;
  };
  const d = walk(JSON.parse(fs.readFileSync(f,'utf8')));
  fs.writeFileSync(f, JSON.stringify(d)); console.log(f, n, 'formules');
}

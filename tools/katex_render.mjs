import katex from 'katex'; import fs from 'fs';
for (const f of process.argv.slice(2)) {
  const d = JSON.parse(fs.readFileSync(f,'utf8')); let n=0;
  for (const t of d.tabs) t.html = t.html.replace(/<div class="math">([\s\S]*?)<\/div>/g, (m, tex) => {
    n++; tex = tex.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');
    return '<div class="math">' + katex.renderToString(tex, {displayMode:true, throwOnError:false, output:'html'}) + '</div>';
  });
  fs.writeFileSync(f, JSON.stringify(d)); console.log(f, n, 'formules');
}

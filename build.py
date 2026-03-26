#!/usr/bin/env python3
"""Build the complete index.html for Lucille & Sun's Tokyo List v4."""
import json, math

with open("places_enriched.json") as f:
    places = json.load(f)

for p in places:
    p["score"] = p["rating"] * math.log(p.get("reviews", 1) + 1)

top_sorted = sorted(places, key=lambda x: x["score"], reverse=True)
top_names = [p["name"] for p in top_sorted[:20]]

for p in places:
    if p["area"] == "Tokyo":
        p["area"] = ""

cat_counts = {}
for p in places:
    cat_counts[p["cat"]] = cat_counts.get(p["cat"], 0) + 1
cats_sorted = sorted(cat_counts.items(), key=lambda x: -x[1])

area_counts = {}
for p in places:
    if p["area"]:
        area_counts[p["area"]] = area_counts.get(p["area"], 0) + 1
areas_sorted = sorted(area_counts.items(), key=lambda x: -x[1])

js_places = json.dumps(places, ensure_ascii=False)
js_top = json.dumps(top_names, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lucille & Sun's Tokyo List</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500&family=Noto+Sans+JP:wght@300;400;500&family=Shippori+Mincho:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{
--washi:#F5F0E8;--washi-warm:#FAF7F0;--sumi:#1C1917;--sumi-light:#44403C;--sumi-faded:#78716C;
--beni:#B91C1C;--beni-soft:#DC2626;--kincha:#C4922A;--kincha-light:#F5EDD8;
--stone:#D6D3D1;--stone-dark:#A8A29E;
--font-display:'Cormorant Garamond','Shippori Mincho',serif;
--font-body:'DM Sans','Noto Sans JP',sans-serif;
--font-jp:'Shippori Mincho','Noto Sans JP',serif;
--shadow-sm:0 1px 3px rgba(28,25,23,0.05);--shadow-md:0 4px 16px rgba(28,25,23,0.07);
--shadow-lg:0 8px 30px rgba(28,25,23,0.1);
}}
html{{scroll-behavior:smooth;overflow-x:hidden}}
body{{font-family:var(--font-body);background:var(--washi);color:var(--sumi);line-height:1.6;font-weight:300;-webkit-font-smoothing:antialiased}}

@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes bounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(6px)}}}}

/* Hero */
.hero{{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem;position:relative;overflow:hidden;background:var(--washi-warm)}}
.hero::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 20% 40%,rgba(185,28,28,0.03) 0%,transparent 60%),radial-gradient(ellipse at 80% 60%,rgba(30,58,95,0.02) 0%,transparent 60%)}}
.hero-content{{position:relative;z-index:1;text-align:center;max-width:680px}}
.hero-kanji{{font-family:var(--font-jp);font-size:clamp(0.8rem,1.2vw,1rem);color:var(--beni);letter-spacing:0.6em;margin-bottom:1.5rem;font-weight:400;opacity:0;animation:fadeUp 1s ease-out 0.2s forwards}}
.hero-title{{font-family:var(--font-display);font-size:clamp(3.2rem,8vw,7rem);font-weight:300;line-height:0.92;letter-spacing:-0.03em;color:var(--sumi);margin-bottom:1rem;opacity:0;animation:fadeUp 1s ease-out 0.4s forwards}}
.hero-title em{{font-style:italic;color:var(--beni)}}
.hero-subtitle{{font-size:clamp(0.85rem,1.2vw,1rem);color:var(--sumi-faded);max-width:460px;margin:0 auto 2.5rem;font-weight:300;letter-spacing:0.02em;opacity:0;animation:fadeUp 1s ease-out 0.6s forwards}}
.hero-stats{{display:flex;gap:3rem;justify-content:center;opacity:0;animation:fadeUp 1s ease-out 0.8s forwards}}
.hero-stat{{text-align:center;cursor:pointer;transition:color 0.2s}}
.hero-stat:hover .hero-stat-num{{color:var(--beni)}}
.hero-stat-num{{font-family:var(--font-display);font-size:2.5rem;font-weight:300;color:var(--sumi);transition:color 0.2s}}
.hero-stat-label{{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.2em;color:var(--stone-dark);margin-top:0.2rem}}
.scroll-hint{{position:absolute;bottom:2rem;left:50%;transform:translateX(-50%);opacity:0;animation:fadeUp 1s ease-out 1.2s forwards}}
.scroll-hint svg{{width:18px;color:var(--stone-dark);animation:bounce 2s ease-in-out infinite}}

/* Toolbar */
.toolbar{{position:sticky;top:0;z-index:100;background:rgba(245,240,232,0.92);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(214,211,209,0.5);padding:0.8rem 2rem;transition:box-shadow 0.3s}}
.toolbar.scrolled{{box-shadow:var(--shadow-md)}}
.toolbar-inner{{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap}}
.toolbar-logo{{font-family:var(--font-display);font-size:1.15rem;font-weight:400;white-space:nowrap}}
.toolbar-logo em{{font-style:italic;color:var(--beni)}}
.search-box{{flex:1;min-width:180px;position:relative}}
.search-box input{{width:100%;padding:0.55rem 1rem 0.55rem 2.2rem;border:1px solid var(--stone);border-radius:6px;background:white;font-family:var(--font-body);font-size:0.85rem;outline:none;transition:border 0.2s}}
.search-box input:focus{{border-color:var(--beni)}}
.search-box svg{{position:absolute;left:0.7rem;top:50%;transform:translateY(-50%);width:14px;color:var(--sumi-faded)}}
.result-count{{font-size:0.75rem;color:var(--sumi-faded);white-space:nowrap}}

/* Category quick-nav (clickable pills that jump to section) */
.cat-nav{{max-width:1200px;margin:0 auto;padding:1rem 2rem 0.5rem}}
.cat-nav-label{{font-size:0.65rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--sumi-faded);margin-bottom:0.4rem}}
.cat-pills{{display:flex;gap:0.3rem;flex-wrap:wrap}}
.cat-pill{{padding:0.28rem 0.65rem;border:1px solid var(--stone);border-radius:20px;background:transparent;font-family:var(--font-body);font-size:0.72rem;color:var(--sumi-light);cursor:pointer;transition:all 0.2s;white-space:nowrap;text-decoration:none}}
.cat-pill:hover{{border-color:var(--beni);color:var(--beni)}}
.cat-pill.active{{background:var(--sumi);color:white;border-color:var(--sumi)}}
.cat-pill-count{{opacity:0.5;margin-left:0.15rem}}

/* Area pills */
.area-nav{{max-width:1200px;margin:0 auto;padding:0.3rem 2rem 0}}
.area-nav-label{{font-size:0.65rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--sumi-faded);margin-bottom:0.4rem}}
.area-pills{{display:flex;gap:0.3rem;flex-wrap:wrap}}
.area-pill{{padding:0.25rem 0.6rem;border:1px solid var(--stone);border-radius:20px;background:transparent;font-family:var(--font-body);font-size:0.72rem;color:var(--sumi-light);cursor:pointer;transition:all 0.2s;white-space:nowrap}}
.area-pill:hover{{border-color:var(--sumi-light);color:var(--sumi)}}
.area-pill.active{{background:var(--sumi);color:white;border-color:var(--sumi)}}

/* Sections */
.section{{max-width:1200px;margin:0 auto;padding:2.5rem 2rem}}
.section-header{{margin-bottom:1.2rem}}
.section-title{{font-family:var(--font-display);font-size:clamp(1.8rem,3vw,2.5rem);font-weight:300;letter-spacing:-0.02em}}
.section-title em{{font-style:italic;color:var(--beni)}}
.section-sub{{color:var(--sumi-faded);font-size:0.9rem;margin-top:0.3rem}}

/* Top Picks — compact horizontal strip with category info */
.top-strip{{display:flex;gap:0.7rem;overflow-x:auto;padding-bottom:0.5rem;scrollbar-width:thin;scrollbar-color:var(--stone) transparent}}
.top-strip::-webkit-scrollbar{{height:4px}}
.top-strip::-webkit-scrollbar-thumb{{background:var(--stone);border-radius:2px}}
.top-chip{{flex-shrink:0;background:white;border-radius:8px;padding:0.55rem 0.9rem;text-decoration:none;color:inherit;border:1px solid rgba(214,211,209,0.4);transition:all 0.2s;display:flex;align-items:center;gap:0.5rem}}
.top-chip:hover{{border-color:var(--beni);box-shadow:var(--shadow-md);transform:translateY(-1px)}}
.top-chip-rank{{font-family:var(--font-display);font-size:1rem;font-weight:300;color:var(--beni);opacity:0.4;min-width:1.2rem}}
.top-chip-info{{display:flex;flex-direction:column;gap:0.1rem;min-width:0}}
.top-chip-name{{font-family:var(--font-display);font-size:0.88rem;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:210px;line-height:1.2}}
.top-chip-detail{{display:flex;align-items:center;gap:0.4rem;font-size:0.68rem;color:var(--sumi-faded)}}
.top-chip-detail .star{{font-size:0.68rem}}
.top-chip-cat{{font-size:0.62rem;color:var(--sumi-faded);background:rgba(0,0,0,0.04);padding:0.05rem 0.3rem;border-radius:2px}}

/* Category sections — adaptive layout */
.cat-section{{margin-bottom:2rem;scroll-margin-top:120px}}
.cat-section .section-inner{{max-width:1200px;margin:0 auto;padding:0 2rem}}
.cat-header{{display:flex;align-items:baseline;gap:0.8rem;margin-bottom:0.8rem;padding-bottom:0.5rem;border-bottom:1px solid var(--stone)}}
.cat-name{{font-family:var(--font-display);font-size:1.4rem;font-weight:400;letter-spacing:-0.01em}}
.cat-count{{font-size:0.78rem;color:var(--sumi-faded)}}

/* Adaptive grid: fewer items = fewer columns, no wasted space */
.cat-grid{{display:grid;gap:0.7rem}}
.cat-grid.cols-1{{grid-template-columns:1fr}}
.cat-grid.cols-2{{grid-template-columns:repeat(2,1fr)}}
.cat-grid.cols-3{{grid-template-columns:repeat(3,1fr)}}
.cat-grid.cols-4{{grid-template-columns:repeat(auto-fill,minmax(270px,1fr))}}

.place-card{{background:white;border-radius:8px;padding:0.85rem 1rem;text-decoration:none;color:inherit;transition:all 0.2s;display:block;border:1px solid rgba(214,211,209,0.3)}}
.place-card:hover{{box-shadow:var(--shadow-md);transform:translateY(-1px);border-color:var(--stone)}}
.place-card-name{{font-family:var(--font-display);font-size:0.95rem;font-weight:500;margin-bottom:0.25rem;line-height:1.3}}
.place-card-meta{{display:flex;align-items:center;gap:0.4rem;flex-wrap:wrap;font-size:0.75rem;color:var(--sumi-faded)}}
.star{{color:var(--kincha);font-weight:500}}
.reviews{{color:var(--sumi-faded)}}
.price-tag{{color:var(--beni);font-weight:400}}
.area-badge{{display:inline-block;padding:0.08rem 0.35rem;border-radius:3px;background:var(--kincha-light);color:var(--kincha);font-size:0.66rem;font-weight:500}}
.type-tag{{font-size:0.66rem;color:var(--sumi-faded);background:rgba(0,0,0,0.04);padding:0.06rem 0.3rem;border-radius:3px}}

.no-results{{text-align:center;padding:4rem 2rem;color:var(--sumi-faded)}}
.no-results p{{font-size:1.1rem}}

.back-top{{position:fixed;bottom:2rem;right:2rem;width:42px;height:42px;border-radius:50%;background:var(--sumi);color:white;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:all 0.3s;z-index:50;box-shadow:var(--shadow-md)}}
.back-top.visible{{opacity:1;pointer-events:auto}}
.back-top:hover{{background:var(--beni);transform:scale(1.1)}}
.back-top svg{{width:18px}}

.footer{{text-align:center;padding:3rem 2rem;border-top:1px solid var(--stone);color:var(--sumi-faded);font-size:0.8rem}}
.footer a{{color:var(--beni);text-decoration:none}}

@media(max-width:640px){{
.hero-stats{{gap:1.5rem}}
.hero-stat-num{{font-size:2rem}}
.toolbar-inner{{gap:0.8rem}}
.toolbar-logo{{font-size:1rem}}
.section{{padding:1.5rem 1rem}}
.cat-section .section-inner{{padding:0 1rem}}
.cat-nav,.area-nav{{padding-left:1rem;padding-right:1rem}}
.cat-grid.cols-2,.cat-grid.cols-3{{grid-template-columns:1fr}}
.cat-grid.cols-4{{grid-template-columns:1fr}}
.top-chip-name{{max-width:140px}}
}}
@media(min-width:641px) and (max-width:900px){{
.cat-grid.cols-3{{grid-template-columns:repeat(2,1fr)}}
.cat-grid.cols-4{{grid-template-columns:repeat(2,1fr)}}
}}
</style>
</head>
<body>

<section class="hero">
  <div class="hero-content">
    <p class="hero-kanji">東京 · TOKYO</p>
    <h1 class="hero-title">Lucille &amp; Sun's<br><em>Tokyo</em> List</h1>
    <p class="hero-subtitle">A personal collection of places we love in Tokyo — shops, cafés, restaurants, museums, and hidden gems curated over years of exploring.</p>
    <div class="hero-stats">
      <div class="hero-stat" onclick="document.getElementById('directory').scrollIntoView()">
        <div class="hero-stat-num" id="stat-places">105</div>
        <div class="hero-stat-label">Places</div>
      </div>
      <div class="hero-stat" onclick="document.getElementById('cat-nav-section').scrollIntoView()">
        <div class="hero-stat-num" id="stat-cats">0</div>
        <div class="hero-stat-label">Categories</div>
      </div>
      <div class="hero-stat" onclick="document.getElementById('top-picks').scrollIntoView()">
        <div class="hero-stat-num">20</div>
        <div class="hero-stat-label">Top Picks</div>
      </div>
    </div>
  </div>
  <div class="scroll-hint">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
  </div>
</section>

<nav class="toolbar" id="toolbar">
  <div class="toolbar-inner">
    <div class="toolbar-logo">Lucille &amp; Sun's <em>Tokyo</em></div>
    <div class="search-box">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input type="text" id="search-input" placeholder="Search places, areas, categories...">
    </div>
    <span class="result-count" id="result-count">105 places</span>
  </div>
</nav>

<!-- Category quick-nav pills -->
<div class="cat-nav" id="cat-nav-section">
  <div class="cat-nav-label">Categories</div>
  <div class="cat-pills" id="cat-pills"></div>
</div>

<!-- Area filter -->
<div class="area-nav">
  <div class="area-nav-label">Areas</div>
  <div class="area-pills" id="area-pills"></div>
</div>

<!-- Top Picks -->
<section class="section" id="top-picks" style="padding-bottom:1rem">
  <div class="section-header">
    <h2 class="section-title"><em>Top</em> Picks</h2>
    <p class="section-sub">Highest rated by Google reviews</p>
  </div>
  <div class="top-strip" id="top-strip"></div>
</section>

<!-- Directory grouped by category -->
<div id="directory"></div>

<footer class="footer">
  <p>Made with care by Lucille &amp; Sun &middot; Data from <a href="https://maps.google.com" target="_blank">Google Maps</a></p>
</footer>

<button class="back-top" id="back-top" onclick="window.scrollTo({{top:0}})">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<script>
const PLACES = {js_places};
const TOP_NAMES = new Set({js_top});

function gmapsUrl(p) {{
  const area = p.area ? p.area + ' ' : '';
  return 'https://www.google.com/maps/search/' + encodeURIComponent(p.name + ' ' + area + 'Tokyo');
}}
function fmt(n) {{ return n.toLocaleString(); }}
function esc(s) {{ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;'); }}

function cardMeta(p) {{
  let h = '<span class="star">\\u2605 ' + p.rating + '</span>';
  h += '<span class="reviews">(' + fmt(p.reviews) + ')</span>';
  if (p.price) h += '<span class="price-tag">' + esc(p.price) + '</span>';
  if (p.area) h += '<span class="area-badge">' + esc(p.area) + '</span>';
  if (p.gmaps_type) h += '<span class="type-tag">' + esc(p.gmaps_type) + '</span>';
  return h;
}}

let activeArea = 'all';
let activeCat = 'all';
let searchQuery = '';

function getVisiblePlaces() {{
  return PLACES.filter(p => {{
    const q = searchQuery.toLowerCase();
    const matchQ = !q || p.name.toLowerCase().includes(q) || p.cat.toLowerCase().includes(q) || p.area.toLowerCase().includes(q) || (p.gmaps_type && p.gmaps_type.toLowerCase().includes(q));
    const matchArea = activeArea === 'all' || p.area === activeArea;
    const matchCat = activeCat === 'all' || p.cat === activeCat;
    return matchQ && matchArea && matchCat;
  }});
}}

// Top Picks with category label
function renderTopPicks() {{
  const strip = document.getElementById('top-strip');
  const tops = PLACES.filter(p => TOP_NAMES.has(p.name))
    .sort((a,b) => (b.rating * Math.log(b.reviews+1)) - (a.rating * Math.log(a.reviews+1)));
  strip.innerHTML = tops.map((p, i) =>
    '<a class="top-chip" href="' + gmapsUrl(p) + '" target="_blank" rel="noopener">' +
    '<span class="top-chip-rank">' + (i+1) + '</span>' +
    '<div class="top-chip-info">' +
    '<span class="top-chip-name">' + esc(p.name) + '</span>' +
    '<div class="top-chip-detail"><span class="star">\\u2605 ' + p.rating + '</span>' +
    '<span class="reviews">(' + fmt(p.reviews) + ')</span>' +
    '<span class="top-chip-cat">' + esc(p.cat) + '</span>' +
    (p.area ? '<span class="area-badge">' + esc(p.area) + '</span>' : '') +
    '</div></div></a>'
  ).join('');
}}

// Category pills (click to jump)
function renderCatPills() {{
  const counts = {{}};
  PLACES.forEach(p => counts[p.cat] = (counts[p.cat]||0)+1);
  const sorted = Object.entries(counts).sort((a,b) => b[1]-a[1]);
  const el = document.getElementById('cat-pills');
  el.innerHTML = '<button class="cat-pill active" data-val="all">All</button>' +
    sorted.map(([c,n]) => '<button class="cat-pill" data-val="' + esc(c) + '">' + esc(c) + '<span class="cat-pill-count">' + n + '</span></button>').join('');
}}

function renderAreaPills() {{
  const areas = {{}};
  PLACES.forEach(p => {{ if (p.area) areas[p.area] = (areas[p.area]||0)+1; }});
  const sorted = Object.entries(areas).sort((a,b) => b[1]-a[1]);
  const el = document.getElementById('area-pills');
  el.innerHTML = '<button class="area-pill active" data-val="all">All</button>' +
    sorted.map(([a,c]) => '<button class="area-pill" data-val="' + esc(a) + '">' + esc(a) + ' (' + c + ')</button>').join('');
}}

function colsClass(n) {{
  if (n <= 2) return 'cols-2';
  if (n <= 4) return 'cols-3';
  return 'cols-4';
}}

function renderDirectory() {{
  const visible = getVisiblePlaces();
  const dir = document.getElementById('directory');
  document.getElementById('result-count').textContent = visible.length + ' places';

  if (!visible.length) {{
    dir.innerHTML = '<div class="no-results"><p>No places found</p></div>';
    return;
  }}

  // Group by category, maintain order by count desc
  const groups = {{}};
  visible.forEach(p => {{
    if (!groups[p.cat]) groups[p.cat] = [];
    groups[p.cat].push(p);
  }});

  // Sort categories by count desc
  const catOrder = Object.keys(groups).sort((a,b) => groups[b].length - groups[a].length);

  // Sort each group by rating desc
  for (const cat in groups) {{
    groups[cat].sort((a,b) => b.rating - a.rating || b.reviews - a.reviews);
  }}

  dir.innerHTML = catOrder.map(cat => {{
    const items = groups[cat];
    const id = 'cat-' + cat.replace(/[^a-zA-Z0-9]/g, '-');
    return '<section class="cat-section" id="' + id + '">' +
      '<div class="section-inner">' +
      '<div class="cat-header"><h3 class="cat-name">' + esc(cat) + '</h3><span class="cat-count">' + items.length + ' places</span></div>' +
      '<div class="cat-grid ' + colsClass(items.length) + '">' +
      items.map(p =>
        '<a class="place-card" href="' + gmapsUrl(p) + '" target="_blank" rel="noopener">' +
        '<div class="place-card-name">' + esc(p.name) + '</div>' +
        '<div class="place-card-meta">' + cardMeta(p) + '</div></a>'
      ).join('') +
      '</div></div></section>';
  }}).join('');
}}

// Events
document.getElementById('search-input').addEventListener('input', e => {{
  searchQuery = e.target.value;
  renderDirectory();
}});

document.getElementById('cat-pills').addEventListener('click', e => {{
  const btn = e.target.closest('.cat-pill');
  if (!btn) return;
  document.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  activeCat = btn.dataset.val;
  renderDirectory();
  // If selecting a specific category, scroll to it
  if (activeCat !== 'all') {{
    const id = 'cat-' + activeCat.replace(/[^a-zA-Z0-9]/g, '-');
    const el = document.getElementById(id);
    if (el) setTimeout(() => el.scrollIntoView({{behavior:'smooth'}}), 100);
  }}
}});

document.getElementById('area-pills').addEventListener('click', e => {{
  if (e.target.classList.contains('area-pill')) {{
    document.querySelectorAll('.area-pill').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    activeArea = e.target.dataset.val;
    renderDirectory();
  }}
}});

// Toolbar scroll
const toolbar = document.getElementById('toolbar');
const observer = new IntersectionObserver(([e]) => {{
  toolbar.classList.toggle('scrolled', !e.isIntersecting);
}}, {{ threshold: 0 }});
observer.observe(document.querySelector('.hero'));

// Back to top
window.addEventListener('scroll', () => {{
  document.getElementById('back-top').classList.toggle('visible', window.scrollY > 600);
}});

// Stats
const cats = new Set(PLACES.map(p => p.cat));
document.getElementById('stat-places').textContent = PLACES.length;
document.getElementById('stat-cats').textContent = cats.size;

// Init
renderTopPicks();
renderCatPills();
renderAreaPills();
renderDirectory();
</script>
</body>
</html>'''

with open("index.html", "w") as f:
    f.write(html)

print(f"Done! {len(html)} bytes, {len(places)} places, {len(cats_sorted)} categories")

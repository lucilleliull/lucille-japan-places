#!/usr/bin/env python3
"""Build the complete index.html for Lucille & Sun's Tokyo List."""
import json, math

# Load enriched data
with open("places_enriched.json") as f:
    places = json.load(f)

# Compute weighted scores for Top Picks
for p in places:
    p["score"] = p["rating"] * math.log(p.get("reviews", 1) + 1)

# Sort for top picks
top_sorted = sorted(places, key=lambda x: x["score"], reverse=True)
top_names = [p["name"] for p in top_sorted[:20]]

# Get unique areas and categories
areas = sorted(set(p["area"] for p in places))
cats = sorted(set(p["cat"] for p in places))

# Build JS data
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

.hero{{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem;position:relative;overflow:hidden;background:var(--washi-warm)}}
.hero::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 20% 40%,rgba(185,28,28,0.03) 0%,transparent 60%),radial-gradient(ellipse at 80% 60%,rgba(30,58,95,0.02) 0%,transparent 60%)}}
.hero-content{{position:relative;z-index:1;text-align:center;max-width:680px}}
.hero-kanji{{font-family:var(--font-jp);font-size:clamp(0.8rem,1.2vw,1rem);color:var(--beni);letter-spacing:0.6em;margin-bottom:1.5rem;font-weight:400}}
.hero-title{{font-family:var(--font-display);font-size:clamp(2.8rem,6vw,5rem);font-weight:300;line-height:1.1;letter-spacing:-0.03em;color:var(--sumi);margin-bottom:1rem}}
.hero-title em{{font-style:italic;color:var(--beni)}}
.hero-sub{{color:var(--sumi-faded);font-size:1.05rem;letter-spacing:0.02em;margin-bottom:2rem}}
.hero-stats{{display:flex;gap:2.5rem;justify-content:center;margin-top:2.5rem}}
.hero-stat{{text-align:center}}
.hero-stat-num{{font-family:var(--font-display);font-size:2rem;font-weight:300;color:var(--sumi)}}
.hero-stat-label{{font-size:0.75rem;text-transform:uppercase;letter-spacing:0.15em;color:var(--stone-dark);margin-top:0.2rem}}
.scroll-hint{{position:absolute;bottom:2rem;left:50%;transform:translateX(-50%);text-align:center}}
.scroll-hint span{{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.2em;color:var(--stone-dark);display:block;margin-bottom:0.5rem}}
@keyframes bounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(6px)}}}}
.scroll-hint svg{{width:18px;color:var(--stone-dark);animation:bounce 2s ease-in-out infinite}}

.toolbar{{position:sticky;top:0;z-index:100;background:rgba(245,240,232,0.92);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(214,211,209,0.5);padding:0.8rem 2rem;transition:box-shadow 0.3s}}
.toolbar.scrolled{{box-shadow:var(--shadow-md)}}
.toolbar-inner{{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap}}
.toolbar-logo{{font-family:var(--font-display);font-size:1.15rem;font-weight:400;white-space:nowrap}}
.toolbar-logo em{{font-style:italic;color:var(--beni)}}
.search-box{{flex:1;min-width:200px;position:relative}}
.search-box input{{width:100%;padding:0.55rem 1rem 0.55rem 2.2rem;border:1px solid var(--stone);border-radius:6px;background:white;font-family:var(--font-body);font-size:0.85rem;outline:none;transition:border 0.2s}}
.search-box input:focus{{border-color:var(--beni)}}
.search-box svg{{position:absolute;left:0.7rem;top:50%;transform:translateY(-50%);width:14px;color:var(--sumi-faded)}}
.result-count{{font-size:0.75rem;color:var(--sumi-faded);white-space:nowrap}}

.section{{max-width:1200px;margin:0 auto;padding:3rem 2rem}}
.section-header{{margin-bottom:2rem}}
.section-title{{font-family:var(--font-display);font-size:clamp(1.8rem,3vw,2.5rem);font-weight:300;letter-spacing:-0.02em}}
.section-title em{{font-style:italic;color:var(--beni)}}
.section-sub{{color:var(--sumi-faded);font-size:0.9rem;margin-top:0.5rem}}

.top-picks-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.2rem}}
.top-card{{background:white;border-radius:10px;padding:1.2rem 1.4rem;text-decoration:none;color:inherit;border:1.5px solid transparent;transition:all 0.25s;position:relative;overflow:hidden;display:block}}
.top-card::before{{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:var(--beni);opacity:0;transition:opacity 0.25s}}
.top-card:hover{{border-color:var(--beni);box-shadow:var(--shadow-lg);transform:translateY(-2px)}}
.top-card:hover::before{{opacity:1}}
.top-rank{{position:absolute;top:0.6rem;right:1rem;font-family:var(--font-display);font-size:2rem;font-weight:300;color:rgba(185,28,28,0.1);line-height:1}}
.top-card-name{{font-family:var(--font-display);font-size:1.15rem;font-weight:500;margin-bottom:0.4rem;padding-right:2rem;line-height:1.3}}
.top-card-meta{{display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;font-size:0.78rem;color:var(--sumi-faded)}}
.star{{color:var(--kincha);font-weight:500}}
.reviews{{color:var(--sumi-faded)}}
.price-tag{{color:var(--beni);font-weight:400}}
.area-badge{{display:inline-block;padding:0.12rem 0.45rem;border-radius:3px;background:var(--kincha-light);color:var(--kincha);font-size:0.7rem;font-weight:500;letter-spacing:0.03em}}
.cat-tag{{font-size:0.7rem;color:var(--sumi-faded);background:rgba(0,0,0,0.04);padding:0.1rem 0.4rem;border-radius:3px}}

.filter-section{{margin-bottom:1rem}}
.filter-label{{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--sumi-faded);margin-bottom:0.4rem}}
.filter-row{{display:flex;gap:0.35rem;flex-wrap:wrap}}
.filter-btn{{padding:0.3rem 0.7rem;border:1px solid var(--stone);border-radius:20px;background:transparent;font-family:var(--font-body);font-size:0.75rem;color:var(--sumi-light);cursor:pointer;transition:all 0.2s;white-space:nowrap}}
.filter-btn:hover{{border-color:var(--sumi-light);color:var(--sumi)}}
.filter-btn.active{{background:var(--sumi);color:white;border-color:var(--sumi)}}

.directory-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;margin-top:1.5rem}}
.place-card{{background:white;border-radius:8px;padding:1rem 1.2rem;text-decoration:none;color:inherit;transition:all 0.2s;display:block;border:1px solid rgba(214,211,209,0.4)}}
.place-card:hover{{box-shadow:var(--shadow-md);transform:translateY(-1px);border-color:var(--stone)}}
.place-card-name{{font-family:var(--font-display);font-size:1rem;font-weight:500;margin-bottom:0.35rem;line-height:1.3}}
.place-card-meta{{display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;font-size:0.78rem;color:var(--sumi-faded)}}

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
.toolbar-inner{{gap:0.8rem}}
.toolbar-logo{{font-size:1rem}}
.section{{padding:2rem 1rem}}
.top-picks-grid,.directory-grid{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>

<section class="hero" id="hero">
<div class="hero-content">
<div class="hero-kanji">東 京 案 内</div>
<h1 class="hero-title">Lucille &amp; Sun's<br><em>Tokyo</em> List</h1>
<p class="hero-sub">A curated guide to our favorite places in Tokyo</p>
<div class="hero-stats">
<div class="hero-stat"><div class="hero-stat-num" id="stat-places">105</div><div class="hero-stat-label">Places</div></div>
<div class="hero-stat"><div class="hero-stat-num" id="stat-areas">20</div><div class="hero-stat-label">Areas</div></div>
<div class="hero-stat"><div class="hero-stat-num" id="stat-cats">20</div><div class="hero-stat-label">Categories</div></div>
</div>
</div>
<div class="scroll-hint">
<span>Explore</span>
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
</div>
</section>

<nav class="toolbar" id="toolbar">
<div class="toolbar-inner">
<div class="toolbar-logo">L&amp;S <em>Tokyo</em></div>
<div class="search-box">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
<input type="text" id="search-input" placeholder="Search places, areas, categories...">
</div>
<span class="result-count" id="result-count">105 places</span>
</div>
</nav>

<section class="section" id="top-picks">
<div class="section-header">
<h2 class="section-title"><em>Top</em> Picks</h2>
<p class="section-sub">Highest rated places by Google reviews</p>
</div>
<div class="top-picks-grid" id="top-grid"></div>
</section>

<section class="section" id="directory">
<div class="section-header">
<h2 class="section-title">All <em>Places</em></h2>
<p class="section-sub" id="places-subtitle">105 places across Tokyo</p>
</div>
<div class="filter-section">
<div class="filter-label">Area</div>
<div class="filter-row" id="area-filters"></div>
</div>
<div class="filter-section">
<div class="filter-label">Category</div>
<div class="filter-row" id="cat-filters"></div>
</div>
<div class="directory-grid" id="dir-grid"></div>
</section>

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
  return 'https://www.google.com/maps/search/' + encodeURIComponent(p.name + ' ' + p.area + ' Tokyo');
}}

function fmt(n) {{ return n.toLocaleString(); }}

function cardMeta(p) {{
  let h = '<span class="star">\\u2605 ' + p.rating + '</span>';
  h += '<span class="reviews">(' + fmt(p.reviews) + ')</span>';
  if (p.price) h += '<span class="price-tag">' + p.price + '</span>';
  h += '<span class="area-badge">' + p.area + '</span>';
  h += '<span class="cat-tag">' + p.cat + '</span>';
  return h;
}}

// Top Picks
function renderTopPicks() {{
  const grid = document.getElementById('top-grid');
  const tops = PLACES.filter(p => TOP_NAMES.has(p.name))
    .sort((a,b) => (b.rating * Math.log(b.reviews+1)) - (a.rating * Math.log(a.reviews+1)));
  grid.innerHTML = tops.map((p, i) => `
    <a class="top-card" href="${{gmapsUrl(p)}}" target="_blank" rel="noopener">
      <span class="top-rank">#${{i+1}}</span>
      <div class="top-card-name">${{p.name}}</div>
      <div class="top-card-meta">${{cardMeta(p)}}</div>
    </a>`).join('');
}}

// Filters
let activeArea = 'all';
let activeCat = 'all';

function getAreas() {{
  const m = {{}};
  PLACES.forEach(p => m[p.area] = (m[p.area]||0)+1);
  return Object.entries(m).sort((a,b) => b[1]-a[1]);
}}

function getCats() {{
  const m = {{}};
  PLACES.forEach(p => m[p.cat] = (m[p.cat]||0)+1);
  return Object.entries(m).sort((a,b) => b[1]-a[1]);
}}

function renderFilters() {{
  const af = document.getElementById('area-filters');
  const cf = document.getElementById('cat-filters');
  const areas = getAreas();
  const cats = getCats();
  af.innerHTML = '<button class="filter-btn active" data-val="all">All</button>' +
    areas.map(([a,c]) => `<button class="filter-btn" data-val="${{a}}">${{a}} (${{c}})</button>`).join('');
  cf.innerHTML = '<button class="filter-btn active" data-val="all">All</button>' +
    cats.map(([c,n]) => `<button class="filter-btn" data-val="${{c}}">${{c}} (${{n}})</button>`).join('');
}}

function filterAndRender() {{
  const q = document.getElementById('search-input').value.toLowerCase();
  const filtered = PLACES.filter(p => {{
    const matchQ = !q || p.name.toLowerCase().includes(q) || p.cat.toLowerCase().includes(q) || p.area.toLowerCase().includes(q);
    const matchArea = activeArea === 'all' || p.area === activeArea;
    const matchCat = activeCat === 'all' || p.cat === activeCat;
    return matchQ && matchArea && matchCat;
  }});
  
  const grid = document.getElementById('dir-grid');
  if (!filtered.length) {{
    grid.innerHTML = '<div class="no-results"><p>No places found</p></div>';
  }} else {{
    grid.innerHTML = filtered.map(p => `
      <a class="place-card" href="${{gmapsUrl(p)}}" target="_blank" rel="noopener">
        <div class="place-card-name">${{p.name}}</div>
        <div class="place-card-meta">${{cardMeta(p)}}</div>
      </a>`).join('');
  }}
  
  document.getElementById('result-count').textContent = filtered.length + ' places';
  document.getElementById('places-subtitle').textContent = filtered.length + ' places across Tokyo';
}}

// Events
document.getElementById('search-input').addEventListener('input', filterAndRender);

document.getElementById('area-filters').addEventListener('click', e => {{
  if (e.target.classList.contains('filter-btn')) {{
    document.querySelectorAll('#area-filters .filter-btn').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    activeArea = e.target.dataset.val;
    filterAndRender();
  }}
}});

document.getElementById('cat-filters').addEventListener('click', e => {{
  if (e.target.classList.contains('filter-btn')) {{
    document.querySelectorAll('#cat-filters .filter-btn').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    activeCat = e.target.dataset.val;
    filterAndRender();
  }}
}});

// Toolbar scroll
const toolbar = document.getElementById('toolbar');
const observer = new IntersectionObserver(([e]) => {{
  toolbar.classList.toggle('scrolled', !e.isIntersecting);
}}, {{ threshold: 0 }});
observer.observe(document.querySelector('.hero'));

// Back to top
const backBtn = document.getElementById('back-top');
window.addEventListener('scroll', () => {{
  backBtn.classList.toggle('visible', window.scrollY > 600);
}});

// Stats
const areas = new Set(PLACES.map(p => p.area));
const cats = new Set(PLACES.map(p => p.cat));
document.getElementById('stat-places').textContent = PLACES.length;
document.getElementById('stat-areas').textContent = areas.size;
document.getElementById('stat-cats').textContent = cats.size;

// Init
renderTopPicks();
renderFilters();
filterAndRender();
</script>
</body>
</html>'''

with open("index.html", "w") as f:
    f.write(html)

print(f"Done! {len(html)} bytes written")
print(f"Places: {len(places)}, Top picks: {len(top_names)}, Areas: {len(areas)}, Categories: {len(cats)}")

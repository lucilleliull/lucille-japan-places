#!/usr/bin/env python3
"""
Enrich places with Google Maps data using the textSearch endpoint.
Uses the public Google Maps API through the Places API (New) with no API key 
by using the Google Maps embed/internal search endpoint.
"""
import json, re, sys, time, urllib.parse, urllib.request, ssl, os

PLACES = [
  {"name":"Ramen Takahashi","cat":"Ramen","area":"Tokyo"},
  {"name":"Birkenstock","cat":"Shopping","area":"Tokyo"},
  {"name":"Blue Bottle Coffee Ginza Cafe","cat":"Coffee","area":"Ginza"},
  {"name":"Glitch Coffee and Roasters GINZA","cat":"Coffee","area":"Ginza"},
  {"name":"BONGENCOFFEE Ginza","cat":"Coffee","area":"Ginza"},
  {"name":"Hard Off","cat":"Shopping","area":"Tokyo"},
  {"name":"Fujisan Shokupan","cat":"Bakery","area":"Tokyo"},
  {"name":"Longtemps","cat":"Bakery","area":"Tokyo"},
  {"name":"APPLE PIE lab","cat":"Bakery","area":"Tokyo"},
  {"name":"mont-bell Tokyo Kyobashi","cat":"Shopping","area":"Kyobashi"},
  {"name":"NAKAO SHOP & OFFICE","cat":"Craft & Design","area":"Tokyo"},
  {"name":"NAKAO FACTORY WORKS & Sohbi","cat":"Craft & Design","area":"Tokyo"},
  {"name":"TSUCHI-YA ガラスの器と工芸","cat":"Craft & Design","area":"Tokyo"},
  {"name":"器 まえさか","cat":"Craft & Design","area":"Tokyo"},
  {"name":"Kama-Asa","cat":"Craft & Design","area":"Kappabashi"},
  {"name":"Takaso","cat":"Craft & Design","area":"Kappabashi"},
  {"name":"Dr.Goods","cat":"Craft & Design","area":"Tokyo"},
  {"name":"ATELIER(アトリエ) 丸の内","cat":"Fashion","area":"Marunouchi"},
  {"name":"Shihara Dover Street Market Ginza","cat":"Fashion","area":"Ginza"},
  {"name":"minä perhonen materiaali","cat":"Fashion","area":"Tokyo"},
  {"name":"Tsutaya Books Daikanyama","cat":"Books","area":"Daikanyama"},
  {"name":"Isetan Shinjuku","cat":"Department Store","area":"Shinjuku"},
  {"name":"URBANIC30 AOYAMA","cat":"Fashion","area":"Aoyama"},
  {"name":"CA4LA Daikanyama Shop","cat":"Fashion","area":"Daikanyama"},
  {"name":"Margaret Howell","cat":"Fashion","area":"Tokyo"},
  {"name":"STUDIO NICHOLSON SHIBUYA PARCO","cat":"Fashion","area":"Shibuya"},
  {"name":"BEAMS JAPAN SHIBUYA","cat":"Fashion","area":"Shibuya"},
  {"name":"Beams Japan","cat":"Fashion","area":"Shinjuku"},
  {"name":"FIT TWO","cat":"Fashion","area":"Tokyo"},
  {"name":"cotogoto","cat":"Craft & Design","area":"Tokyo"},
  {"name":"The Okura Tokyo","cat":"Hotel","area":"Toranomon"},
  {"name":"JOURNAL STANDARD LUXE","cat":"Fashion","area":"Tokyo"},
  {"name":"JOURNAL STANDARD 表参道 ladies店","cat":"Fashion","area":"Omotesando"},
  {"name":"The Conran Shop","cat":"Interior","area":"Tokyo"},
  {"name":"MIDTOWN CHRISTMAS イルミネーション","cat":"Experience","area":"Roppongi"},
  {"name":"国立西洋美术馆","cat":"Museum","area":"Ueno"},
  {"name":"proto 器とタカラモノ","cat":"Craft & Design","area":"Tokyo"},
  {"name":"deps.","cat":"Craft & Design","area":"Tokyo"},
  {"name":"東京都庭園美術館","cat":"Museum","area":"Meguro"},
  {"name":"Ｆ・Ｍ・Ｎ","cat":"Craft & Design","area":"Tokyo"},
  {"name":"COMME des GARÇONS Aoyama Store","cat":"Fashion","area":"Aoyama"},
  {"name":"ARTS&SCIENCE Aoyama women flagship","cat":"Fashion","area":"Aoyama"},
  {"name":"Arts & Science Marunouchi","cat":"Fashion","area":"Marunouchi"},
  {"name":"LOVELESS AOYAMA","cat":"Fashion","area":"Aoyama"},
  {"name":"LE LABO Aoyama Store","cat":"Beauty","area":"Aoyama"},
  {"name":"エイチ ビューティー＆ユース","cat":"Fashion","area":"Tokyo"},
  {"name":"江户东京建筑园","cat":"Museum","area":"Koganei"},
  {"name":"YAECA APARTMENT STORE","cat":"Fashion","area":"Tokyo"},
  {"name":"YAECA Ebisu","cat":"Fashion","area":"Ebisu"},
  {"name":"Sippo","cat":"Café","area":"Tokyo"},
  {"name":"日本杂货 &清酒吧 DEARYOU 表参道店","cat":"Bar","area":"Omotesando"},
  {"name":"JAPAN PEARLS","cat":"Shopping","area":"Tokyo"},
  {"name":"Coverchord Nakameguro","cat":"Fashion","area":"Nakameguro"},
  {"name":"MHL Daikanyama","cat":"Fashion","area":"Daikanyama"},
  {"name":"Nanamica Daikanyama","cat":"Fashion","area":"Daikanyama"},
  {"name":"Forest Gate Daikanyama","cat":"Shopping","area":"Daikanyama"},
  {"name":"KITTE Marunouchi","cat":"Shopping","area":"Marunouchi"},
  {"name":"L'Appartement Aoyama","cat":"Fashion","area":"Aoyama"},
  {"name":"L'Appartement 東京店","cat":"Fashion","area":"Tokyo"},
  {"name":"AURALEE","cat":"Fashion","area":"Tokyo"},
  {"name":"BLAMINK TOKYO","cat":"Fashion","area":"Tokyo"},
  {"name":"LAND OF TOMORROW 丸之内店","cat":"Shopping","area":"Marunouchi"},
  {"name":"フリーデザイン Free Design","cat":"Interior","area":"Tokyo"},
  {"name":"SOU·SOU KYOTO Aoyama Store","cat":"Fashion","area":"Aoyama"},
  {"name":"The Harvest Kitchen General Store","cat":"Shopping","area":"Tokyo"},
  {"name":"Popeye Camera Flagship Store","cat":"Shopping","area":"Tokyo"},
  {"name":"うつわと雑貨 トラシー","cat":"Craft & Design","area":"Tokyo"},
  {"name":"Cinq","cat":"Craft & Design","area":"Tokyo"},
  {"name":"Pacific Furniture Service","cat":"Interior","area":"Tokyo"},
  {"name":"MoMA Design Store表参道","cat":"Interior","area":"Omotesando"},
  {"name":"Encounter Madu Aoyama","cat":"Interior","area":"Aoyama"},
  {"name":"Artek Tokyo Store","cat":"Interior","area":"Tokyo"},
  {"name":"Mid-Century MODERN","cat":"Interior","area":"Tokyo"},
  {"name":"合羽桥道具街","cat":"Craft & Design","area":"Kappabashi"},
  {"name":"Tool Shop Nobori","cat":"Craft & Design","area":"Kappabashi"},
  {"name":"LOST AND FOUND TOKYO STORE","cat":"Interior","area":"Tokyo"},
  {"name":"club d by D&DESIGN","cat":"Interior","area":"Tokyo"},
  {"name":"OZEKI Tokyo Gallery","cat":"Craft & Design","area":"Tokyo"},
  {"name":"D&DEPARTMENT TOKYO","cat":"Interior","area":"Tokyo"},
  {"name":"LEMAIRE恵比寿","cat":"Fashion","area":"Ebisu"},
  {"name":"Kyuko","cat":"Craft & Design","area":"Tokyo"},
  {"name":"Ginza Kagari - Soba","cat":"Ramen","area":"Ginza"},
  {"name":"TRAVELER'S FACTORY STATION","cat":"Stationery","area":"Tokyo"},
  {"name":"Kizuna","cat":"Restaurant","area":"Tokyo"},
  {"name":"DOLCE TACUBO CAFFE","cat":"Café","area":"Tokyo"},
  {"name":"DOLCE TACUBO","cat":"Restaurant","area":"Tokyo"},
  {"name":"Miko Sushi Ginza","cat":"Sushi","area":"Ginza"},
  {"name":"PÂTISSERIE ASAKO IWAYANAGI","cat":"Bakery","area":"Tokyo"},
  {"name":"BIEN-ETRE MAISON","cat":"Café","area":"Tokyo"},
  {"name":"Shinjuku Kitamura Camera","cat":"Shopping","area":"Shinjuku"},
  {"name":"Tokyo Midtown Design Hub","cat":"Museum","area":"Roppongi"},
  {"name":"东京中城","cat":"Shopping","area":"Roppongi"},
  {"name":"21_21 设计视野","cat":"Museum","area":"Roppongi"},
  {"name":"草月会館","cat":"Culture","area":"Tokyo"},
  {"name":"Museum of Contemporary Art Tokyo (MOT)","cat":"Museum","area":"Kiyosumi"},
  {"name":"Rāmenya Shima","cat":"Ramen","area":"Tokyo"},
  {"name":"Tsukiji Itadori Uogashi Senryo","cat":"Sushi","area":"Tsukiji"},
  {"name":"Imahan Annex","cat":"Restaurant","area":"Tokyo"},
  {"name":"MERCER BRUNCH ROPPONGI","cat":"Restaurant","area":"Roppongi"},
  {"name":"OMO5 Tokyo Gotanda by Hoshino Resorts","cat":"Hotel","area":"Gotanda"},
  {"name":"Daikanyama Issai Kassai","cat":"Craft & Design","area":"Daikanyama"},
  {"name":"Roppongi Inakaya","cat":"Restaurant","area":"Roppongi"},
  {"name":"ART AQUARIUM MUSEUM","cat":"Museum","area":"Ginza"},
  {"name":"GINZA SIX","cat":"Shopping","area":"Ginza"},
  {"name":"宫下公园","cat":"Park","area":"Shibuya"},
]

OUTPUT = "places_enriched.json"

def fetch_gmaps_data(name, area):
    """Fetch place data from Google Maps search page, extract from embedded JSON."""
    query = f"{name} {area} Tokyo Japan"
    url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"
    
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    
    try:
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  ERROR fetching: {e}", file=sys.stderr)
        return {}
    
    result = {}
    
    # The Google Maps page contains embedded data in window.APP_INITIALIZATION_STATE
    # and various JSON-like structures. Extract what we can.
    
    # Rating - look in the page data
    # Common pattern: ,4.5,  or [4.5, 
    # More specific: the rating often appears near review count
    rating_review = re.findall(r'(\d\.\d),(\d+),', html)
    for r, c in rating_review:
        rating = float(r)
        count = int(c)
        if 1.0 <= rating <= 5.0 and count > 5:
            result["rating"] = rating
            result["reviews"] = count
            break
    
    # Address patterns
    # Japanese addresses often contain 〒 or district names
    addr_match = re.search(r'(〒\d{3}-\d{4}[^"\\]{5,80})', html)
    if addr_match:
        result["address"] = addr_match.group(1).strip()
    else:
        # Try English-style address
        addr_match = re.search(r'"(\d+-\d+[^"]{3,60}(?:Tokyo|Chiyoda|Minato|Shibuya|Shinjuku|Meguro|Setagaya|Toshima|Taito|Chuo|Bunkyo|Koto)[^"]{0,40})"', html)
        if addr_match:
            result["address"] = addr_match.group(1).strip()[:120]
    
    # Price level
    price_match = re.search(r'PRICE_LEVEL_(\w+)', html)
    if price_match:
        level = price_match.group(1)
        price_map = {"INEXPENSIVE": "¥", "MODERATE": "¥¥", "EXPENSIVE": "¥¥¥", "VERY_EXPENSIVE": "¥¥¥¥"}
        result["price"] = price_map.get(level, level)
    else:
        yen_match = re.search(r'"(¥{1,4})"', html)
        if yen_match:
            result["price"] = yen_match.group(1)
    
    # Google Maps URL (place-specific)
    place_url = re.search(r'(https://www\.google\.com/maps/place/[^"\\]+)', html)
    if place_url:
        result["gmaps_url"] = place_url.group(1)
    
    return result


def main():
    # Load existing progress
    if os.path.exists(OUTPUT):
        with open(OUTPUT) as f:
            enriched = json.load(f)
        done_names = {p["name"] for p in enriched}
        print(f"Resuming from {len(enriched)} places already done")
    else:
        enriched = []
        done_names = set()
    
    total = len(PLACES)
    for i, p in enumerate(PLACES):
        if p["name"] in done_names:
            continue
        
        print(f"[{i+1}/{total}] {p['name']} ({p['area']})...", end=" ", flush=True)
        data = fetch_gmaps_data(p["name"], p["area"])
        
        entry = {**p, **data}
        enriched.append(entry)
        done_names.add(p["name"])
        
        # Save progress
        with open(OUTPUT, "w") as f:
            json.dump(enriched, f, ensure_ascii=False, indent=2)
        
        if data:
            parts = []
            if "rating" in data: parts.append(f"★{data['rating']}")
            if "reviews" in data: parts.append(f"{data['reviews']}r")
            if "price" in data: parts.append(data["price"])
            if "address" in data: parts.append("📍")
            print(" | ".join(parts) if parts else "partial")
        else:
            print("no data")
        
        time.sleep(2)  # Polite delay
    
    # Summary
    with_rating = sum(1 for p in enriched if "rating" in p)
    with_addr = sum(1 for p in enriched if "address" in p)
    with_price = sum(1 for p in enriched if "price" in p)
    print(f"\n=== DONE: {len(enriched)} places ===")
    print(f"  Rating: {with_rating}/{len(enriched)}")
    print(f"  Address: {with_addr}/{len(enriched)}")
    print(f"  Price: {with_price}/{len(enriched)}")


if __name__ == "__main__":
    main()

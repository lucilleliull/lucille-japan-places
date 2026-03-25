#!/usr/bin/env python3
"""
Enrich places using Wanderlog (aggregates Google Maps data).
Wanderlog search returns rating, reviewCount, address.
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

def search_wanderlog(name, area):
    """Search Wanderlog for place details."""
    query = f"{name} {area} Tokyo"
    url = f"https://wanderlog.com/search?q={urllib.parse.quote(query)}&type=place"
    
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html",
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return {}
    
    result = {}
    
    # Extract rating
    m = re.search(r'"rating"\s*:\s*(\d\.?\d?)', html)
    if m:
        result["rating"] = float(m.group(1))
    
    # Extract review count
    m = re.search(r'"userRatingCount"\s*:\s*(\d+)', html)
    if m:
        result["reviews"] = int(m.group(1))
    
    # Address
    m = re.search(r'"formattedAddress"\s*:\s*"([^"]+)"', html)
    if m:
        result["address"] = m.group(1)
    
    # Price level
    m = re.search(r'"priceLevel"\s*:\s*"([^"]+)"', html)
    if m:
        level = m.group(1)
        price_map = {"PRICE_LEVEL_INEXPENSIVE": "¥", "PRICE_LEVEL_MODERATE": "¥¥", 
                     "PRICE_LEVEL_EXPENSIVE": "¥¥¥", "PRICE_LEVEL_VERY_EXPENSIVE": "¥¥¥¥"}
        result["price"] = price_map.get(level, level)
    
    return result


def search_google_textsearch(name, area):
    """Use Google's internal Places API text search (no key needed, browser endpoint)."""
    query = f"{name} {area} Tokyo"
    # Google Maps has an internal textsearch endpoint
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={urllib.parse.quote(query)}&language=en"
    
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except:
        return {}
    
    if data.get("status") != "OK" or not data.get("results"):
        return {}
    
    place = data["results"][0]
    result = {}
    if "rating" in place:
        result["rating"] = place["rating"]
    if "user_ratings_total" in place:
        result["reviews"] = place["user_ratings_total"]
    if "formatted_address" in place:
        result["address"] = place["formatted_address"]
    if "price_level" in place:
        price_map = {1: "¥", 2: "¥¥", 3: "¥¥¥", 4: "¥¥¥¥"}
        result["price"] = price_map.get(place["price_level"], str(place["price_level"]))
    
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
        
        # Try Wanderlog first
        data = search_wanderlog(p["name"], p["area"])
        
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
        
        time.sleep(1)
    
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

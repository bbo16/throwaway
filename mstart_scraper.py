"""
m-start.de Regatta Scraper

Scrapet Regattaergebnisse von resy.m-start.de über die interne getter.php API.

Strategie:
1. Playwright öffnet die Seite (rendert JS)
2. Alle getter.php-Requests werden abgefangen und das q-Token extrahiert
3. Anschließend werden alle func-Endpunkte direkt mit requests abgefragt
4. Export als CSV / JSON / SQL

Installation:
    pip install playwright requests beautifulsoup4
    playwright install chromium

Verwendung:
    python mstart_scraper.py "https://resy.m-start.de/tables.php?q=..."
    python mstart_scraper.py "https://resy.m-start.de/tables.php?q=..." --csv --json
    python mstart_scraper.py "https://resy.m-start.de/tables.php?q=..." --headless false
"""

import re, sys, json, csv, time, argparse
import requests
from urllib.parse import urlparse, urlencode, parse_qs
from pathlib import Path
from bs4 import BeautifulSoup

# ── Bekannte func-Endpunkte der getter.php API ────────────────────────────────
# Abgeleitet aus den Tab-Labels auf der Seite
FUNCS = [
    'upcoming',        # Letzte / nächste Rennen
    'races',           # Start-/Ergebnislisten (alle Rennen)
    'startlist',       # Startliste eines Rennens (braucht race_id)
    'results',         # Ergebnis eines Rennens (braucht race_id)
    'athletes',        # Athleten-Liste
    'clubs',           # Vereine
    'meldeergebnis',   # Meldeergebnis
]

BASE_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'de-DE,de;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/26.1 Safari/605.1.15',
}


# ── Token-Extraktion via Playwright ──────────────────────────────────────────

def get_token_via_playwright(page_url: str, headless: bool = True) -> dict:
    """
    Öffnet die Seite im Browser, fängt den ersten getter.php-Request ab
    und gibt dessen q-Token + die Basis-URL zurück.
    """
    from playwright.sync_api import sync_playwright

    token_info = {}
    parsed = urlparse(page_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    with sync_playwright() as p:
        # Try default path first, fall back to any installed chromium
        import glob as _glob
        import os as _os
        chrome_paths = sorted(_glob.glob(
            '/root/.cache/ms-playwright/chromium-*/chrome-linux/chrome'))
        executable = chrome_paths[-1] if chrome_paths else None
        launch_opts = {'headless': headless}
        if executable:
            launch_opts['executable_path'] = executable
        # Configure proxy if environment has one
        proxy_url = _os.environ.get('HTTPS_PROXY') or _os.environ.get('https_proxy')
        if proxy_url:
            proxy_parsed = urlparse(proxy_url)
            proxy_cfg = {'server': f'{proxy_parsed.scheme}://{proxy_parsed.hostname}:{proxy_parsed.port}'}
            if proxy_parsed.username:
                proxy_cfg['username'] = proxy_parsed.username
            if proxy_parsed.password:
                proxy_cfg['password'] = proxy_parsed.password
            launch_opts['proxy'] = proxy_cfg
        browser = p.chromium.launch(**launch_opts)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        intercepted = []

        def on_request(request):
            if 'getter.php' in request.url:
                intercepted.append(request.url)

        page.on('request', on_request)

        print(f"Öffne {page_url} …")
        page.goto(page_url, wait_until='networkidle', timeout=30000)

        # Kurz warten damit alle Tabs geladen werden
        page.wait_for_timeout(2000)

        # Auch auf die andere Tabs klicken um alle Endpunkte zu triggern
        for tab_text in ['Athleten', 'Vereine', 'Start-/Ergebnislisten']:
            try:
                tab = page.get_by_text(tab_text, exact=False).first
                if tab:
                    tab.click()
                    page.wait_for_timeout(1000)
            except Exception:
                pass

        browser.close()

    print(f"Abgefangene getter.php Requests: {len(intercepted)}")
    for url in intercepted:
        print(f"  {url[:120]}…")

    if not intercepted:
        raise RuntimeError("Keine getter.php Requests abgefangen. "
                           "Prüfe ob die URL korrekt ist.")

    # q-Token aus erstem Request extrahieren
    first = intercepted[0]
    qs = parse_qs(urlparse(first).query)
    token_info = {
        'q': qs.get('q', [None])[0],
        'base_url': base_url,
        'all_intercepted': intercepted,
        'funcs_seen': list({parse_qs(urlparse(u).query).get('func', ['?'])[0]
                           for u in intercepted}),
    }
    return token_info


# ── Direkte API-Abfragen ──────────────────────────────────────────────────────

def fetch_func(base_url: str, q: str, func: str,
               extra_params: dict = None) -> str | None:
    """Ruft einen getter.php-Endpunkt ab und gibt den Response-Text zurück."""
    params = {
        'func': func,
        'q': q,
        '_': int(time.time() * 1000),
    }
    if extra_params:
        params.update(extra_params)

    url = f"{base_url}/includes/getter.php"
    headers = {
        **BASE_HEADERS,
        'Referer': f"{base_url}/tables.php?q={q}",
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"  ✗ {func}: {e}")
        return None


def parse_html_table(html: str) -> list[dict]:
    """Parst eine HTML-Tabelle in eine Liste von Dicts."""
    if not html or not html.strip():
        return []

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    all_rows = []

    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        if not headers:
            # Erste Zeile als Header behandeln
            first_row = table.find('tr')
            if first_row:
                headers = [td.get_text(strip=True)
                           for td in first_row.find_all(['td','th'])]

        for tr in table.find_all('tr')[1:]:
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            if cells and len(cells) == len(headers):
                all_rows.append(dict(zip(headers, cells)))
            elif cells:
                all_rows.append({f'col{i}': v for i, v in enumerate(cells)})

    return all_rows


def try_json(text: str):
    """Versucht JSON zu parsen, gibt None zurück bei Fehler."""
    try:
        return json.loads(text)
    except Exception:
        return None


# ── Haupt-Scraper ─────────────────────────────────────────────────────────────

def scrape(page_url: str, headless: bool = True) -> dict:
    """
    Vollständiger Scrape einer m-start-Regattaseite.
    Gibt ein Dict mit allen Datensätzen zurück.
    """
    # 1. Token via Playwright holen
    token_info = get_token_via_playwright(page_url, headless=headless)
    q = token_info['q']
    base_url = token_info['base_url']

    if not q:
        raise RuntimeError("q-Token konnte nicht extrahiert werden.")

    print(f"\nToken: {q[:40]}…")
    print(f"Bereits gesehene funcs: {token_info['funcs_seen']}\n")

    data = {}

    # 2. Alle bekannten Endpunkte abrufen
    for func in FUNCS:
        print(f"Fetching func={func} …", end=' ', flush=True)
        html = fetch_func(base_url, q, func)

        if not html:
            print("leer")
            continue

        # JSON oder HTML?
        parsed = try_json(html)
        if parsed:
            data[func] = parsed
            count = len(parsed) if isinstance(parsed, list) else '(object)'
            print(f"✓ JSON, {count} Einträge")
        else:
            rows = parse_html_table(html)
            if rows:
                data[func] = rows
                print(f"✓ HTML-Tabelle, {len(rows)} Zeilen")
            else:
                # Roh-HTML aufbewahren für manuelle Analyse
                data[func] = {'raw_html': html[:2000]}
                print(f"? Unbekanntes Format ({len(html)} Zeichen)")

    # 3. Falls races vorhanden: Detail-Ergebnisse pro Rennen holen
    if 'races' in data and isinstance(data['races'], list):
        race_ids = []
        for race in data['races']:
            # ID könnte in verschiedenen Feldern stehen
            for key in ('id', 'race_id', 'Rennen', '#'):
                if key in race and str(race[key]).isdigit():
                    race_ids.append(str(race[key]))
                    break

        if race_ids:
            print(f"\n{len(race_ids)} Rennen gefunden, lade Einzelergebnisse …")
            data['race_results'] = {}
            for race_id in race_ids[:50]:  # max 50 um nicht zu fluten
                html = fetch_func(base_url, q, 'results',
                                  extra_params={'race_id': race_id})
                if html:
                    parsed = try_json(html) or parse_html_table(html)
                    if parsed:
                        data['race_results'][race_id] = parsed
            print(f"✓ {len(data['race_results'])} Rennen-Ergebnisse geladen")

    return data


# ── Export ────────────────────────────────────────────────────────────────────

def export_json(data: dict, path: str):
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✓ JSON: {path}")


def export_csv(data: dict, stem: str):
    for func, rows in data.items():
        if not isinstance(rows, list) or not rows:
            continue
        if not isinstance(rows[0], dict):
            continue
        path = f"{stem}_{func}.csv"
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(),
                                    extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        print(f"✓ CSV: {path} ({len(rows)} Zeilen)")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description='Scrapet Regattaergebnisse von resy.m-start.de')
    ap.add_argument('url', help='URL der Regatta-Seite (tables.php?q=...)')
    ap.add_argument('--csv', action='store_true', help='CSV-Export')
    ap.add_argument('--json', action='store_true',
                    help='JSON-Export (default)')
    ap.add_argument('--headless', default='true', choices=['true','false'],
                    help='Browser headless starten (default: true)')
    args = ap.parse_args()

    headless = args.headless == 'true'
    stem = 'regatta_mstart'

    print(f"Scrape: {args.url}\n")
    data = scrape(args.url, headless=headless)

    print(f"\n── Ergebnisse ──────────────────────────────")
    for key, val in data.items():
        count = len(val) if isinstance(val, (list, dict)) else '?'
        print(f"  {key}: {count} Einträge")

    if args.csv:
        export_csv(data, stem)
    if args.json or not args.csv:
        export_json(data, f'{stem}.json')


if __name__ == '__main__':
    main()

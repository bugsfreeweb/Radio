import requests
import json
import re
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List
import logging  # For better Actions logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_THUMB = "https://tonetune.netlify.app/assets/tonetune.png"
OUTPUT_DIR = "dailyupdated"
CACHE_THRESHOLD = timedelta(hours=24)
session = requests.Session()
session.headers.update({'User-Agent': 'Radio-Collector/1.0'})  # Polite UA
adapter = requests.adapters.HTTPAdapter(max_retries=2)
session.mount('http://', adapter)
session.mount('https://', adapter)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fresh verified sources
SOURCES = {
    "worldfm": [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/radio.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/world.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/europe.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/north_america.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/south_america.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/africa.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/australia.m3u",
        "https://raw.githubusercontent.com/Free-TV/IPTV/main/radio.m3u",
        "https://raw.githubusercontent.com/Pulham/Internet-Radio-HQ-URL-playlists/main/world_radio.m3u",
        "https://gist.githubusercontent.com/casaper/ddec35d21a0158628fccbab7876b7ef3/raw/bbc.m3u",
    ],
    "world_public_radio": [
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/bd/bd.m3u",
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/ae/ae.m3u",
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/ae/ae_exclusiveradio.m3u",
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/ag/ag.m3u",
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/al/al.m3u",
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/am/am.m3u",
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/il/il.m3u",
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/in/in.m3u",
        "https://raw.githubusercontent.com/iprd-org/iprd/main/streams/it/it.m3u",
    ],
    "bollywood": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/fm_cube/india.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/india.m3u",
        "https://raw.githubusercontent.com/sdbabhishek/Indian-Bollywood-online-Radio-Music-Stream-links/main/bollywood.m3u",
        "https://raw.githubusercontent.com/ArnoldSchiller/m3u-radio-music-playlists/main/indian.m3u",
    ],
    "hollywood": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/pop.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/80s.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/90s.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/rock.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/english.m3u",
        "https://raw.githubusercontent.com/Pulham/Internet-Radio-HQ-URL-playlists/main/english_pop_rock.m3u",
    ],
    "dance_edm": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/dance.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/electronic.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/techno.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/eurodance.m3u",
        "https://raw.githubusercontent.com/Pulham/Internet-Radio-HQ-URL-playlists/main/edm_dance.m3u",
    ],
    "jazz_blues": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/jazz.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/blues.m3u",
        "https://raw.githubusercontent.com/Pulham/Internet-Radio-HQ-URL-playlists/main/jazz_blues.m3u",
    ],
    "classical": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/classical.m3u",
        "https://raw.githubusercontent.com/Pulham/Internet-Radio-HQ-URL-playlists/main/classical.m3u",
    ],
    "audiobooks": [
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/audiobooks.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/a/a.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/b/b.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/c/c.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/fm_cube/audiobooks.m3u",
    ],
    "relax_chill": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/chill.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/ambient.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/lounge.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/chillout.m3u",
    ],
    "quran": [
        "https://raw.githubusercontent.com/mp3quran/mp3quran/master/quran_radio.m3u",
        "https://raw.githubusercontent.com/nimda95/quran-iptv/master/quranicaudio.m3u8",
        "https://gist.githubusercontent.com/hthmkhlf/544038a4f089b5d0d491544c5dc2b58e/raw/awesome.m3u",
        "https://raw.githubusercontent.com/quran/quran.com-fe/master/public/audio/mishary/playlist.m3u",  # Mishary recitation MP3s
        "https://raw.githubusercontent.com/quran/quran.com-fe/master/public/audio/sudais/playlist.m3u",  # Sudais MP3s
        "http://stream.radiostation.ir:8000/quran",  # Live Quran radio
        "https://gist.githubusercontent.com/Fazzani/722f67c30ada8bac4602f62a2aaccff6/raw/playlist.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/quran.m3u",
    ]
}

# [Rest of the functions remain the same as previous version: load_cached_streams, save_streams, parse_m3u, check_stream, collect_and_save]

def load_cached_streams(category: str) -> List[Dict[str, Any]]:
    filepath = os.path.join(OUTPUT_DIR, f"{category}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            streams = json.load(f)
            now = datetime.now().isoformat()
            for s in streams:
                if 'last_checked' not in s:
                    s['last_checked'] = now
            return streams
    return []

def save_streams(category: str, streams: List[Dict[str, Any]]):
    filepath = os.path.join(OUTPUT_DIR, f"{category}.json")
    for s in streams:
        s['last_checked'] = datetime.now().isoformat()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(streams, f, indent=2, ensure_ascii=False)

def parse_m3u(content: str) -> List[Dict[str, Any]]:
    streams = []
    lines = [l.strip() for l in content.split('\n')]
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF:"):
            name_match = re.search(r",(.+)", line)
            name = name_match.group(1).strip() if name_match else "Unknown"
            
            desc_match = re.search(r'group-title="([^"]*)"', line)
            description = desc_match.group(1) if desc_match else "Radio Station"
            
            logo_match = re.search(r'tvg-logo="([^"]*)"', line)
            thumb = logo_match.group(1) if logo_match else DEFAULT_THUMB
            
            if i + 1 < len(lines) and lines[i+1].startswith("http"):
                url = lines[i+1]
                if any(ext in url.lower() for ext in ['m3u8', 'mp3', 'aac', 'ogg']):  # Stricter audio filter
                    streams.append({
                        "name": name,
                        "description": description,
                        "url": url,
                        "thumb": thumb,
                        "status": "pending"
                    })
            i += 2
        else:
            i += 1
    return streams

def check_stream(stream: Dict[str, Any]) -> Dict[str, Any] | None:
    url = stream["url"]
    try:
        r = session.head(url, timeout=20, allow_redirects=True)  # Increased timeout
        if r.status_code in (200, 206):
            return stream
    except:
        try:
            r = session.get(url, timeout=20, stream=True)
            if r.status_code in (200, 206):
                return stream
        except:
            pass
    return None

def collect_and_save(category: str, urls: List[str]):
    cached = load_cached_streams(category)
    cached_dict = {s['url']: s for s in cached if s.get('status') == 'active'}
    seen = set((s['url'], s['name'].lower()) for s in cached)
    
    all_streams = list(cached)
    needs_check = []

    logger.info(f"Collecting {category} (cached: {len(cached)})...")
    failed_sources = 0
    for url in urls:
        try:
            logger.info(f"  → Fetching {url}")
            r = session.get(url, timeout=30)
            if r.status_code == 200:
                new_streams = parse_m3u(r.text)
                for s in new_streams:
                    key = (s['url'], s['name'].lower())
                    if key not in seen:
                        seen.add(key)
                        if s['url'] in cached_dict:
                            last_check = datetime.fromisoformat(cached_dict[s['url']]['last_checked'])
                            if (datetime.now() - last_check) < CACHE_THRESHOLD:
                                logger.info(f"  → Cache hit: {s['name']}")
                                all_streams.append(cached_dict[s['url']])
                                continue
                        s['status'] = 'pending'
                        needs_check.append(s)
            else:
                logger.warning(f"  → HTTP {r.status_code} for {url}")
                failed_sources += 1
        except Exception as e:
            logger.error(f"Failed {url}: {e}")
            failed_sources += 1

    if failed_sources > 0:
        logger.warning(f"  → {failed_sources} sources failed for {category}")

    # Parallel check
    if needs_check:
        logger.info(f"  → Checking {len(needs_check)} streams (max_workers=100)...")
        with ThreadPoolExecutor(max_workers=100) as executor:  # Reduced for stability
            futures = [executor.submit(check_stream, s) for s in needs_check]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    result['status'] = 'active'
                    all_streams.append(result)
                    logger.info(f"  → Active: {result['name'][:50]}...")

    # Dedup
    final_streams = []
    final_seen = set()
    for s in all_streams:
        key = (s['url'], s['name'].lower())
        if key not in final_seen and s.get('status') == 'active':
            final_seen.add(key)
            final_streams.append(s)

    save_streams(category, final_streams)
    logger.info(f"Saved {len(final_streams)} active → {category}.json")

if __name__ == "__main__":
    logger.info(f"Radio Update Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for cat, urls in SOURCES.items():
        collect_and_save(cat, urls)
    logger.info("Done! 🚀")

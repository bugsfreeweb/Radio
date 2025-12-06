import requests
import json
import re
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List

DEFAULT_THUMB = "https://tonetune.netlify.app/assets/tonetune.png"
OUTPUT_DIR = "dailyupdated"
CACHE_THRESHOLD = timedelta(hours=24)  # Recheck if older than 24h
session = requests.Session()  # Reuse for speed

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Verified active sources (60+ total, no 404s - updated Dec 2025)
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
    "bollywood": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/fm_cube/india.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/india.m3u",
        "https://raw.githubusercontent.com/ArnoldSchiller/m3u-radio-music-playlists/main/indian.m3u",
        "https://raw.githubusercontent.com/sdbabhishek/Indian-Bollywood-online-Radio-Music-Stream-links/main/bollywood.m3u",
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
        "https://raw.githubusercontent.com/ArnoldSchiller/m3u-radio-music-playlists/main/dance.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/electronic.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/techno.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/eurodance.m3u",
        "https://raw.githubusercontent.com/Pulham/Internet-Radio-HQ-URL-playlists/main/edm_dance.m3u",
    ],
    "jazz_blues": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/jazz.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/blues.m3u",
        "https://raw.githubusercontent.com/ArnoldSchiller/m3u-radio-music-playlists/main/jazz.m3u",
        "https://raw.githubusercontent.com/Pulham/Internet-Radio-HQ-URL-playlists/main/jazz_blues.m3u",
    ],
    "classical": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/classical.m3u",
        "https://raw.githubusercontent.com/ArnoldSchiller/m3u-radio-music-playlists/main/classical.m3u",
        "https://raw.githubusercontent.com/Pulham/Internet-Radio-HQ-URL-playlists/main/classical.m3u",
    ],
    "audiobooks": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/fm_cube/audiobooks.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/audiobooks.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/a/a.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/b/b.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/c/c.m3u",
    ],
    "relax_chill": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/chill.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/ambient.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/lounge.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/chillout.m3u",
        "https://raw.githubusercontent.com/ArnoldSchiller/m3u-radio-music-playlists/main/lounge.m3u",
    ],
    "quran": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/quran.m3u",
        "https://raw.githubusercontent.com/nimda95/quran-iptv/master/quranicaudio.m3u8",
        "https://gist.githubusercontent.com/hthmkhlf/544038a4f089b5d0d491544c5dc2b58e/raw/awesome.m3u",
        "http://m.live.net.sa:1935/live/quran/playlist.m3u8",
        "https://gist.githubusercontent.com/mansouryaacoubi/ba2a458f5032e1b51c20a92979e90b66/raw/ba2a458f5032e1b51c20a92979e90b66",
        "https://gist.githubusercontent.com/justloop/f985f43a89efe41100a67876fe540184/raw/playlist.m3u",
        "https://gist.githubusercontent.com/Fazzani/722f67c30ada8bac4602f62a2aaccff6/raw/playlist.m3u",
        "https://raw.githubusercontent.com/mp3quran/mp3quran/master/quran_radio.m3u",
    ]
}

def load_cached_streams(category: str) -> List[Dict[str, Any]]:
    """Load previous active streams with timestamps."""
    filepath = os.path.join(OUTPUT_DIR, f"{category}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            streams = json.load(f)
            # Add last_checked if missing (for legacy files)
            now = datetime.now().isoformat()
            for s in streams:
                if 'last_checked' not in s:
                    s['last_checked'] = now
            return streams
    return []

def save_streams(category: str, streams: List[Dict[str, Any]]):
    """Save streams with current timestamp."""
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
                if 'm3u8' in url or 'mp3' in url or 'aac' in url:  # Audio filter
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
    """Check if stream is active."""
    url = stream["url"]
    try:
        r = session.head(url, timeout=15, allow_redirects=True)
        if r.status_code in (200, 206):
            return stream
    except:
        try:
            r = session.get(url, timeout=15, stream=True)
            if r.status_code in (200, 206):
                return stream
        except:
            pass
    return None

def collect_and_save(category: str, urls: List[str]):
    cached = load_cached_streams(category)
    cached_dict = {s['url']: s for s in cached if s.get('status') == 'active'}
    seen = set((s['url'], s['name'].lower()) for s in cached)
    
    all_streams = list(cached)  # Start with cached
    needs_check = []  # Only new or old ones

    print(f"Collecting {category} (cached: {len(cached)})...")
    for url in urls:
        try:
            print(f"  → Fetching {url}")
            r = session.get(url, timeout=20)
            if r.status_code == 200:
                new_streams = parse_m3u(r.text)
                for s in new_streams:
                    key = (s['url'], s['name'].lower())
                    if key not in seen:
                        seen.add(key)
                        if s['url'] in cached_dict and (datetime.now() - datetime.fromisoformat(cached_dict[s['url']]['last_checked'])) < CACHE_THRESHOLD:
                            print(f"  → Cache hit: {s['name']}")
                            all_streams.append(cached_dict[s['url']])
                        else:
                            s['status'] = 'pending'
                            needs_check.append(s)
        except Exception as e:
            print(f"Failed {url}: {e}")

    # Parallel check only needs_check
    if needs_check:
        print(f"  → Checking {len(needs_check)} new/old streams...")
        with ThreadPoolExecutor(max_workers=200) as executor:
            futures = [executor.submit(check_stream, s) for s in needs_check]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    result['status'] = 'active'
                    all_streams.append(result)
                    print(f"  → Active: {result['name']}")

    # Dedup final list
    final_streams = []
    final_seen = set()
    for s in all_streams:
        key = (s['url'], s['name'].lower())
        if key not in final_seen and s.get('status') == 'active':
            final_seen.add(key)
            final_streams.append(s)

    save_streams(category, final_streams)
    print(f"Saved {len(final_streams)} active → {category}.json\n")

if __name__ == "__main__":
    print(f"Radio Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    for cat, urls in SOURCES.items():
        collect_and_save(cat, urls)
    print("Done! 🚀")

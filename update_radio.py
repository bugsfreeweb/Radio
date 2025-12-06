import requests
import json
import re
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_THUMB = "https://tonetune.netlify.app/assets/tonetune.png"
OUTPUT_DIR = "dailyupdated"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

SOURCES = {
    "worldfm": [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/radio.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/world.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/europe.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/north_america.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/south_america.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/asia.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/africa.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/australia.m3u",
        "https://gist.githubusercontent.com/casaper/ddec35d21a0158628fccbab7876b7ef3/raw/bbc.m3u",
    ],
    "bollywood": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/fm_cube/india.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/bollywood.m3u",
        "https://raw.githubusercontent.com/ArnoldSchiller/m3u-radio-music-playlists/main/indian.m3u",
    ],
    "hollywood": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/pop.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/80s.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/90s.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/rock.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/english.m3u",
    ],
    "dance_edm": [
        "https://raw.githubusercontent.com/ArnoldSchiller/m3u-radio-music-playlists/main/dance.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/electronic.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/techno.m3u",
    ],
    "jazz_blues": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/jazz.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/blues.m3u",
    ],
    "classical": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/classical.m3u",
    ],
    "audiobooks": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/fm_cube/audiobooks.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-audiobooks/main/audiobooks.m3u",
    ],
    "relax_chill": [
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/chill.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/ambient.m3u",
        "https://raw.githubusercontent.com/junguler/m3u-radio-music-playlists/main/lounge.m3u",
    ],
    "quran": [  # Added for Al-Quran/MP3 recitations and radios
        "https://raw.githubusercontent.com/nimda95/quran-iptv/master/quranicaudio.m3u8",  # Multi-recitation Quran
        "https://gist.githubusercontent.com/hthmkhlf/544038a4f089b5d0d491544c5dc2b58e/raw/awesome.m3u",  # Includes Quran streams
        "http://m.live.net.sa:1935/live/quran/playlist.m3u8",  # Mekka Quran radio
        "https://gist.githubusercontent.com/mansouryaacoubi/ba2a458f5032e1b51c20a92979e90b66/raw/ba2a458f5032e1b51c20a92979e90b66",  # Mekka Quran IPTV
        "https://gist.githubusercontent.com/justloop/f985f43a89efe41100a67876fe540184/raw/playlist.m3u",  # Has QURAN entries
        "https://gist.githubusercontent.com/Fazzani/722f67c30ada8bac4602f62a2aaccff6/raw/playlist.m3u",  # CHANNEL QURAN
    ]
}

def parse_m3u(content):
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
                streams.append({
                    "name": name,
                    "description": description,
                    "url": url,
                    "thumb": thumb
                })
            i += 2
        else:
            i += 1
    return streams

def check_stream(stream):
    url = stream["url"]
    try:
        r = requests.head(url, timeout=15, allow_redirects=True)
        if r.status_code in (200, 206):
            return stream
    except:
        try:
            r = requests.get(url, timeout=15, stream=True)
            if r.status_code in (200, 206):
                return stream
        except:
            pass
    return None

def collect_and_save(category, urls):
    all_streams = []
    seen = set()

    print(f"Collecting streams for {category}...")
    for url in urls:
        try:
            print(f"  → Fetching {url}")
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                streams = parse_m3u(r.text)
                for s in streams:
                    key = (s["url"], s["name"].lower())
                    if key not in seen:
                        seen.add(key)
                        all_streams.append(s)
        except Exception as e:
            print(f"Failed {url}: {e}")

    # Parallel check active
    active_streams = []
    if all_streams:
        print(f"  → Checking {len(all_streams)} unique streams in parallel...")
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(check_stream, s) for s in all_streams]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    result["status"] = "active"
                    active_streams.append(result)

    # Save
    filepath = os.path.join(OUTPUT_DIR, f"{category}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(active_streams, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(active_streams)} active stations → {filepath}\n")

if __name__ == "__main__":
    print(f"Radio Collection Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    for cat, urls in SOURCES.items():
        collect_and_save(cat, urls)
    print("All done!")

# Tone & Tune Radio 🎵📻

**A beautiful, offline-first, Progressive Web App (PWA) radio player**  
Live internet radio streaming with equalizer, sleep timer, favorites, queue, dark/light theme, and full PWA install support.

Live Demo → https://tonetune.netlify.app

<img src="https://raw.githubusercontent.com/bugsfreeweb/radio/main/assets/logo.png" alt="Bugsfree radio" width="50%"/>

---

### Features

| Feature                     | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| **Live Radio Streaming**     | Play thousands of online radio stations worldwide                           |
| **Built-in Default Stations**| Comes with popular stations (BBC, Radio Paradise, KEXP, Worldwide FM, etc.)|
| **External Playlist Support**| Load stations from JSON or M3U/M3U8 playlists (local file or remote URL)   |
| **Favorites System**         | Mark and quickly access your favorite stations                              |
| **Play Queue**               | Add upcoming stations to queue                                              |
| **3-Band Equalizer**         | Bass / Mid / Treble control using Web Audio API                             |
| **Sleep Timer**              | Auto-stop playback after selected minutes                                   |
| **Dark / Light Theme**       | Automatic persistence                                                       |
| **Full PWA Support**         | Installable on mobile & desktop, works offline (cached UI)                  |
| **Responsive Design**        | Looks great on phones, tablets, and desktops                                |
| **Media Session API**        | Control playback from lock screen / notification (Android & desktop)       |
| **Import / Export**          | Backup or share your station list as JSON                                   |
| **Add / Edit / Delete**      | Full CRUD for custom stations                                               |
| **Online / Offline Indicator**| Real-time connection status                                                 |

---

### Tech Stack

- Pure HTML5 + CSS3 + Vanilla JavaScript (no frameworks)
- Web Audio API (equalizer)
- Service Worker + Manifest (PWA)
- LocalStorage persistence
- Media Session API
- Responsive & mobile-first design

---

### Installation & Usage

1. **Clone or download the repo**
   ```bash
   git clone https://github.com/bugsfreeweb/radio-pub.git
   cd radio-pub
2. Open index.html in your browser – that’s it! No build step needed.
3. (Optional) Deploy anywhere:
- Netlify → Drag & drop the folder
- Vercel / GitHub Pages / Firebase Hosting → all work perfectly

4. Install as app – Click the install button or use browser “Add to Home Screen”.


## How to Add Your Own Stations
You have multiple ways:
1. Manually (inside the app)

- Click + Add Station → fill name, description, stream URL, thumbnail (optional)

2. Load from external source

- Choose a category in the dropdown (World FM, Top40, Al-Quran) → loads from public GitHub JSON files

3. Import playlist

- Supports JSON and M3U/M3U8 formats
- Paste content, upload file, or enter remote URL

4. Replace default stations
- Edit the default array inside js (around line 30) or reset to defaults anytime from the menu.

## Credits & License
* Developed by Bugsfree Studio
* https://bugsfree.netlify.app
* License: MIT – feel free to fork, modify, and use commercially or personally.
* Icons: Font Awesome Free
* Fonts: Google Fonts (Inter)

# Enjoy listening!
If you like this project, please give it a STAR – it means the world to indie developers.

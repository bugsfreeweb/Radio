# Tone & Tune Radio Player

A professional-grade web-based radio player application that allows users to stream live radio stations from around the world with advanced audio controls and modern features.

# Live Demo → 
- https://tonetune.netlify.app

<img src="https://raw.githubusercontent.com/bugsfreeweb/radio/main/assets/logo.png" alt="Bugsfree radio" width="60%"/>

## 🎵 Features

### Core Functionality
- **Live Radio Streaming**: Access to high-quality radio stations worldwide
- **12 Pre-configured Stations**: BBC World Service, Radio Paradise, 181.FM, KEXP, and more
- **Audio Playback Controls**: Play, pause, stop, volume control, and progress tracking
- **Station Management**: Add, edit, delete, and organize radio stations

### Advanced Audio Features
- **3-Band Equalizer**: Bass, Mid, and Treble controls for audio customization
- **Sleep Timer**: Automatic playback stopping (15, 30, 45, 60 minutes)
- **Play Queue**: Manage sequential listening with navigation controls
- **Favorites System**: Mark and quickly access favorite stations
- **Media Session Integration**: Control playback from browser notifications and lock screen

### Data Management
- **Import/Export Support**: JSON, TXT, M3U, M3U8, and MP3 file formats
- **Online Station Sources**: Integration with World-FM, Top40, and Al-Quran radio APIs
- **Local Storage**: Automatic saving of stations, favorites, and user preferences
- **Data Persistence**: All user settings and preferences are retained between sessions

### User Interface
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Splash Screen**: Professional 3-second loading animation
- **Modern UI Components**: Clean, intuitive interface design
- **Real-time Status**: Live/offline indicators and connection status
- **Notification System**: User-friendly alerts and confirmations

## 🚀 Getting Started

### Quick Start
1. **Let's start**: `index.html`
2. **Open in Browser**: Double-click the file or open in your web browser
3. **Allow Audio**: Click "Play" when prompted to enable audio playback
4. **Select Station**: Click any station card to load it
5. **Start Streaming**: Press the play button to begin listening

### Server Setup (Optional)
For development or testing with external features:

```bash
# Start local server
python -m http.server 8001

# Access the application
http://localhost:8001/index.html
```

### Browser Compatibility
- **Chrome**: Full support (recommended)
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support
- **Mobile Browsers**: Responsive design supported

## 📁 File Structure

```
index.html
├── HTML Structure
│   ├── Splash Screen (3-second animation)
│   ├── Main Player Interface
│   ├── Station Grid Display
│   └── Modal Components
├── Assets
│   ├── All assets here
├── Images
│   ├── All images here
├── CSS Styling
│   ├── Responsive Design
│   ├── Modern UI Components
│   ├── Mobile Optimization
│   └── Animation Effects
└── JavaScript Functionality
    ├── Audio Management
    ├── Station Operations
    ├── Equalizer Controls
    ├── Timer Functions
    ├── Data Import/Export
    └── Local Storage Integration
```

## 🎛️ Usage Guide

### Adding New Stations
1. Click the **menu icon** (☰) in the left center
2. Select **"Add Station"**
3. Fill in the required fields:
   - **Station Name**: Display name for the station
   - **Description**: Brief description or genre
   - **Stream URL**: Direct audio stream URL
   - **Thumbnail**: Optional image URL
4. Click **"Add Station"** to save

### Using the Equalizer
1. Open the **menu icon** (☰)
2. Select **"Equalizer"**
3. Adjust the three frequency bands:
   - **Bass** (200Hz): Low-frequency emphasis
   - **Mid** (1000Hz): Vocal and instrument range
   - **Treble** (3000Hz): High-frequency clarity
4. Use **"Reset"** to return to default settings

### Sleep Timer
1. Open the **menu icon** (☰)
2. Select **"Sleep Timer"**
3. Choose duration: 15, 30, 45, or 60 minutes
4. Playback will automatically stop after the selected time

### Importing Station Data
1. Open the **menu icon** (☰)
2. Select **"Import Data"**
3. Choose input method:
   - **File Upload**: JSON, M3U, M3U8 formats
   - **URL Import**: Direct link to station data
   - **Text Input**: Paste station information directly

### Managing Favorites
- Click the **heart icon** (♥) on any station card to mark as favorite
- Favorites are automatically saved and accessible across sessions
- Use the **filter** to show only favorite stations

## 🔧 Technical Details

### Audio Technology
- **HTML5 Audio API**: Native browser audio playback
- **Web Audio API**: Advanced audio processing and equalization
- **CORS Support**: Cross-origin resource sharing for external streams
- **Media Session**: System-level media controls integration

### Streaming Protocols
- **HTTP/HTTPS**: Direct stream access
- **MP3**: Compressed audio streams
- **AAC**: Advanced Audio Coding streams
- **HLS**: HTTP Live Streaming support
- **M3U/M3U8**: Playlist format support

### Browser APIs Used
- **Local Storage**: Data persistence
- **Media Session**: System controls integration
- **Notifications**: User alert system
- **Responsive Design**: CSS Grid and Flexbox

### Performance Optimizations
- **Lazy Loading**: Stations load on demand
- **Efficient DOM Manipulation**: Minimal reflows and repaints
- **Memory Management**: Proper cleanup of audio resources
- **Error Recovery**: Automatic retry and fallback mechanisms

## 🎯 Default Stations

The application comes pre-configured with 12 popular radio stations:

1. **BBC World Service** - International News
2. **Radio Paradise** - Eclectic Mix
3. **181.FM - The Buzz** - Alternative Rock
4. **KEXP 90.3** - Seattle Public Radio
5. **BBC Youth Contemporary** - BBC Youth Programming
6. **BBC Radio 1Xtra** - Hip Hop and R&B
7. **BBC Radio 1Dance** - Dance Music
8. **BBC Adult Contemporary** - Adult Hit Radio
9. **BBC Radio 6 Music** - Alternative Music
10. **Worldwide FM (A)** - Global Music (Primary)
11. **Worldwide FM (B)** - Global Music (Backup)
12. **Radio Today-FM from Dhaka Bangladesh** - Regional Pop

## 🛠️ Customization

### Adding Custom Stations
Edit the `stations` array in the JavaScript section:

```javascript
stations.push({
    name: "Your Station Name",
    description: "Station Description",
    url: "https://your-stream-url.com/stream",
    thumb: "https://your-thumbnail-url.com/image.jpg",
    status: "active"
});
```

### Modifying UI Themes
The application uses CSS custom properties for easy theme customization. Modify the `:root` section in the CSS to change colors, spacing, and fonts.

### Custom Data Sources
Add new station sources by modifying the `SOURCES` object:

```javascript
const SOURCES = {
    'custom-source': 'https://your-api-endpoint.com/stations.json'
};
```

## 🔍 Troubleshooting

### Audio Not Playing
- Ensure your browser allows audio autoplay
- Check that the stream URL is valid and accessible
- Verify your internet connection is stable
- Try a different station to isolate the issue

### Station Loading Issues
- Confirm the stream URL format is supported
- Check for CORS restrictions on external streams
- Ensure the stream server is online and accessible

### Performance Issues
- Clear browser cache and reload the application
- Close unnecessary browser tabs to free up memory
- Use a modern browser for optimal performance

### Mobile Device Issues
- Ensure you have a stable internet connection
- Some streams may require higher bandwidth
- Use headphones for better audio quality

## 📄 Credits

### Development
- **Original Design & Code**: User-created application
- **Audio Technology**: HTML5 Audio API and Web Audio API
- **UI Framework**: Custom CSS and JavaScript
- **Icons**: Font Awesome icon library

### Data Sources
- **BBC Radio**: BBC World Service streams
- **Radio Paradise**: Independent internet radio
- **181.FM**: Commercial internet radio network
- **KEXP**: Seattle Public Radio
- **Worldwide FM**: Global music streaming
- **Radio Today-FM from Dhaka Bangladesh**: International radio directory

### External Dependencies
- **Font Awesome**: Icon library (CDN)
- **Google Fonts**: Web typography (CDN)

## 📜 License

This application is created for personal and educational use. The source code and design are provided as-is for learning and customization purposes.

### Usage Rights
- ✅ Personal use and customization
- ✅ Educational and learning purposes
- ✅ Modification and adaptation
- ❌ Commercial distribution without permission
- ❌ Resale or redistribution as-is

### Disclaimer
- Streaming content is provided by third-party sources
- The application does not host any audio content
- Users are responsible for complying with local copyright laws
- Streaming quality depends on source availability and internet connection

## 🤝 Support

For questions, issues, or feature requests:
- Review this README for common solutions
- Check browser console for error messages
- Verify stream URLs are working independently
- Test with different browsers and devices

---

**Tone & Tune Radio Player** - Bringing the world of radio to your browser with professional-grade streaming technology and intuitive user experience.

# Cross Browser CRT Mod

A cross-browser compatible version of the Opera GX CRT shader mod. This extension works on **any Chromium-based browser** (Chrome, Edge, Brave, Opera, Vivaldi) and can be adapted for Firefox.

## Features

- **CRT Shader Effect** — Real-time WebGL scanline, shadow mask, chromatic aberration, and vignette effects applied as a full-page overlay
- **Two Shader Modes** — Flat CRT and Curved CRT (with barrel distortion)
- **Adjustable Intensity** — Control how strong the effect appears (0–100%)
- **Keyboard Sounds** — Retro mechanical keyboard sounds generated via Web Audio API
- **CSS Fallback** — Graceful degradation to CSS-only scanlines if WebGL is unavailable
- **Zero Dependencies** — Pure vanilla JavaScript, no external libraries required

## Installation

### Chrome / Edge / Brave / Opera / Vivaldi

1. Open `chrome://extensions` (or your browser's equivalent extensions page)
2. Enable **Developer mode** (toggle in the top-right corner)
3. Click **Load unpacked**
4. Select the `Cross_Browser_CRT` folder (this directory)
5. The extension icon will appear in your toolbar

### Firefox (with minor adjustments)

1. Change `"service_worker"` in manifest.json to `"scripts": ["background.js"]` under a `"background"` key
2. Open `about:debugging#/runtime/this-firefox`
3. Click **Load Temporary Add-on**
4. Select the `manifest.json` file

## Usage

1. Click the extension icon in your browser toolbar
2. Toggle **CRT Shader** to enable the visual effect
3. Choose between **Flat** or **Curved** CRT modes
4. Adjust the **Intensity** slider to your preference
5. Toggle **Keyboard Sounds** for retro typing feedback

## How It Works

### Shader Effects (WebGL)
The extension injects a full-viewport `<canvas>` overlay with WebGL shaders that simulate:
- **Scanlines** — Horizontal lines mimicking CRT phosphor rows
- **Shadow Mask** — RGB subpixel pattern emulation
- **Chromatic Aberration** — Color channel separation at screen edges
- **Vignette** — Darkened corners like a real CRT
- **Barrel Distortion** (curved mode) — Screen curvature effect

### Keyboard Sounds (Web Audio API)
Uses the Web Audio API oscillator to generate synthetic mechanical keyboard sounds with no audio files needed.

### Architecture
```
Cross_Browser_CRT/
├── manifest.json          # Extension manifest (Manifest V3)
├── background.js          # Service worker for state management
├── content.js             # Content script (shaders + sounds)
├── css/
│   └── mod-base.css       # Base CSS variables
├── icons/                 # Extension icons
├── popup/
│   ├── popup.html         # Control panel UI
│   ├── popup.css          # Control panel styles
│   └── popup.js           # Control panel logic
└── README.md              # This file
```

## Comparison with Opera GX Mod

| Feature | Opera GX Mod | Cross Browser Mod |
|---------|-------------|-------------------|
| Shader Language | SkSL (Skia) | WebGL GLSL |
| Sound Files | Audio file references | Web Audio API synthesis |
| Theme Integration | `env(-opera-gx-*)` | CSS custom properties |
| Browser Support | Opera GX only | Any Chromium browser |
| Installation | `opera:extensions` | Standard extension loading |
| Manifest | Opera mod schema | Standard Manifest V3 |

## Browser Compatibility

| Browser | Status |
|---------|--------|
| Google Chrome | ✅ Fully supported |
| Microsoft Edge | ✅ Fully supported |
| Brave | ✅ Fully supported |
| Opera / Opera GX | ✅ Fully supported |
| Vivaldi | ✅ Fully supported |
| Firefox | ⚠️ Requires manifest adjustment (see above) |

## License

Same license as the parent repository.

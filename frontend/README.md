# NetworkBuster Frontend

A Vite-based frontend for NetworkBuster, packaged as a Windows desktop application via Electron.

## Development

```bash
cd frontend
npm install
npm run dev
```

## Build the web assets

```bash
npm run build
```

Outputs static assets to `frontend/dist/`.

## Run as a desktop app (Electron)

```bash
npm run electron
```

## Package a Windows executable

```bash
npm run dist:win
```

This builds the frontend and uses `electron-builder` to produce a Windows installer/executable
under `frontend/release/`.

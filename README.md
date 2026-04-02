# BMLTelemetry Viewer

BMLTelemetry Viewer is a local desktop tool to visualize BeatMyLanding telemetry data.
:
- main page: flight plan / landings list
- detail page: telemetry metrics + charts (touchdown profile + rollout track)

## Features

- Loads all JSON product landings from configured folder
- Group landings by date with card interface
- Displays aircraft data, scores, and fallback details
- Dual-axis chart: vertical speed + rollout groundspeed
- Refresh button for folder content reload
- GitHub Actions: build exe + release on tag

## Quick start

1. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Edit `config.cfg` to point to your landing data (e.g. `demoData`):

```json
{
  "landingslocation": "./demoData"
}
```

3. Run in development mode:

```bash
python main.py
```

## Build executable (PyInstaller)

```bash
pyinstaller --noconfirm --onefile --name BMLTelemetryViewer --add-data "config.cfg;." main.py
```

## GitHub Actions (build + release)

Workflow: `.github/workflows/build-release.yml`

- `push` tags `v*` or manual dispatch
- Windows build job creates `dist/BMLTelemetryViewer.exe`
- Upload artifact
- Release job creates GitHub release + attaches EXE

> Note: `demoData` is excluded from git and release assets.

## .gitignore

Key ignored entries:
- `__pycache__/`, `*.py[cod]`, `.pytest_cache`
- `venv/`, `.env/`, `ENV/`
- `/demoData/`

## Notes

- Keep `config.cfg` next to executable (PyInstaller bundle includes it)
- If using GitHub release, tag a new version:

```bash
git tag v1.0.1
git push --tags
```

Template is fully customizable.  Enjoy analyzing your landings!
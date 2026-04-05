# BMLTelemetry Viewer

WIP

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
- Automated CI using GitHub Actions 

## Notes

- (optional) Keep `config.cfg` next to executable for custom telemetry folder path
- Data for testing can be generated using `demo_data_generator.py` script from branch `demoData`
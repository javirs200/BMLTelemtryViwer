import os
import json
from datetime import datetime

base = os.path.abspath(os.path.dirname(__file__))
folder = os.path.join(base, 'demoData', '2026-03')
os.makedirs(folder, exist_ok=True)

for i, fpm in enumerate([-3293, -532, -457], start=1):
    filename = f"2026-03-27_21{i:02d}430Z_Anon_{abs(fpm):04d}fpm.json"
    path = os.path.join(folder, filename)

    data = {
        "schema_version": 1,
        "app_version": "0.2.22.0",
        "session_id": f"anon-session-{i:03d}",
        "landing_id": f"00000000-0000-0000-0000-{i:012d}",
        "timestamp_zulu": f"2026-03-27T21:{44+i:02d}:30Z",
        "aircraft_title": "Generic Aircraft",
        "airport_icao": "XXXX",
        "departure_airport_icao": "YYYY",
        "touchdown_fpm": fpm,
        "touchdown_groundspeed_kt": 120 + i,
        "touchdown_ias_kt": 120 + i,
        "max_g": 1.2 + i*0.1,
        "bounce_count": i % 5,
        "airborne_time_seconds_total": 300 + i * 10,
        "touchdown_profile": [
            {"t_ms": -1000 + j*50, "vertical_speed_fpm": -500 - j * 10}
            for j in range(20)
        ],
        "rollout_track": [
            {"t_ms": j*50, "groundspeed_kt": 120 - j*0.2}
            for j in range(20)
        ],
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

print(f"Created 3 anonymized demo files in {folder}")

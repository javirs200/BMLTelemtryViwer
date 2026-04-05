import os
import json
import random
import uuid
from datetime import datetime, timedelta

random.seed(98765)

base = os.path.abspath(os.path.dirname(__file__))
root = os.path.join(base, 'demoData')
os.makedirs(root, exist_ok=True)

months = [(2026, 3), (2026, 4), (2026, 5)]
days_per_month = 4
files_per_day = 5

airport_codes = ['CCCC', 'DDDD', 'EEEE', 'FFFF', 'GGGG']
aircraft_models = ['PC-12 NGX', 'Cessna 172', 'Boeing 737', 'Airbus A320', 'N12345']

def random_time(time_start, minutes_span):
    drop = random.randint(0, minutes_span * 60)
    result = time_start + timedelta(seconds=drop)
    return result

count = 0
for month_year in months:
    year, month = month_year
    for day_i in range(days_per_month):
        day = 10 + day_i * 5
        date_base = datetime(year, month, day, 18, 0, 0)
        folder = os.path.join(root, f"{year}-{month:02d}")
        os.makedirs(folder, exist_ok=True)

        for file_i in range(files_per_day):
            count += 1
            t = random_time(date_base, 180)
            landing_id = str(uuid.uuid4())
            session_id = str(uuid.uuid4())

            filename = f"{t.strftime('%Y-%m-%d_%H%M%SZ')}_Anon_{file_i+1}.json"
            path = os.path.join(folder, filename)

            touchdown_fpm = random.randint(-4800, -300)
            touchdown_groundspeed = random.randint(90, 140)
            touchdown_ias = touchdown_groundspeed + random.randint(0, 10)

            chrono = int(random.uniform(200, 650))

            touchdown_profile = []
            for j in range(25):
                tms = -2000 + j * 90
                touchdown_profile.append({
                    "t_ms": tms,
                    "vertical_speed_fpm": round(random.uniform(-1000, -50) * (1 - j / 25.0), 1),
                    "g_force": round(random.uniform(0.8, 3.8), 2),
                    "radio_alt_ft": round(max(0, 30 - j * 0.9), 1),
                    "groundspeed_kt": round(random.uniform(100, 130) * (1 - j / 100.0), 1),
                    "ias_kt": round(random.uniform(95, 135) * (1 - j / 105.0), 1),
                    "heading_deg_true": round(random.uniform(190, 230), 1),
                    "on_ground": False if j < 20 else True,
                })

            rollout_track = []
            for j in range(30):
                rollout_track.append({
                    "t_ms": j * 50,
                    "lat": round(random.uniform(33.0, 33.3), 6),
                    "lon": round(random.uniform(35.5, 35.9), 6),
                    "heading_deg_true": round(random.uniform(190, 230), 1),
                    "bank_deg": round(random.uniform(-5, 5), 1),
                    "groundspeed_kt": round(120 - j * 0.2 + random.uniform(-1,1), 1),
                    "cross_track_error_ft": None,
                    "cross_track_abs_ft": None,
                    "centerline_error_norm": None,
                    "track_vs_runway_axis_deg": None,
                })

            data = {
                "schema_version": 1,
                "app_version": "0.2.22.0",
                "session_id": session_id,
                "landing_id": landing_id,
                "timestamp_zulu": t.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "aircraft_title": random.choice(aircraft_models),
                "aircraft_category": "Airplane",
                "airport_icao": random.choice(airport_codes),
                "departure_airport_icao": random.choice(airport_codes),
                "departure_runway_ident": f"{random.randint(1, 36):02d}",
                "position": {"lat": round(random.uniform(32.7, 33.4), 6), "lon": round(random.uniform(35.5, 35.9), 6), "alt_ft_msl": round(random.uniform(300, 1000), 1)},
                "heading_deg_true": round(random.uniform(180, 240), 1),
                "touchdown_sideslip_deg": round(random.uniform(-10, 10), 1),
                "touchdown_sideslip_reason": "computed_primary",
                "runway_ident": f"{random.randint(1, 36):02d}",
                "touchdown_fpm": touchdown_fpm,
                "touchdown_groundspeed_kt": touchdown_groundspeed,
                "touchdown_ias_kt": touchdown_ias,
                "max_g": round(random.uniform(1.0, 4.0), 2),
                "bounce_count": random.randint(0, 4),
                "touchdown_radio_alt_ft": round(random.uniform(0, 60), 1),
                "airborne_time_seconds_total": chrono,
                "airborne_time_seconds_scored": chrono - random.uniform(0, 4),
                "touchdown_profile": touchdown_profile,
                "rollout_track": rollout_track,
                "environment": {
                    "ambient_temp_c": round(random.uniform(5, 25), 1),
                    "barometer_pressure_inhg": round(random.uniform(29.5, 30.5), 2),
                    "visibility_m": random.randint(2000, 15000),
                    "in_cloud": False,
                    "precip_state": random.randint(0, 4),
                },
                "user": {
                    "agent_id": str(uuid.uuid4()),
                    "user_id": f"anon-{random.randint(1000,9999)}",
                    "anonymous_mode": True,
                },
                "settings": {"overlay_enabled": True},
                "upload_attempted": True,
                "upload_success": False,
                "upload_message": '{"ok":true,"inserted":false,"id":"' + str(uuid.uuid4()) + '"}',
            }

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

print(f"Created {count} anonymized demo files in {root}")

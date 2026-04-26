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

def generate_calm_landing():
    """Generate a calm, smooth landing profile."""
    touchdown_fpm = random.randint(-800, -400)  # Gentle descent
    touchdown_groundspeed = random.randint(95, 115)
    touchdown_ias = touchdown_groundspeed + random.randint(0, 5)

    # Smooth touchdown profile
    touchdown_profile = []
    for j in range(25):
        tms = -2000 + j * 90
        # Gradual decrease in vertical speed
        vs_progress = 1 - (j / 25.0)
        vertical_speed = -400 * vs_progress - 50  # Smooth transition
        touchdown_profile.append({
            "t_ms": tms,
            "vertical_speed_fpm": round(vertical_speed, 1),
            "g_force": round(random.uniform(0.9, 1.3), 2),  # Low G forces
            "radio_alt_ft": round(max(0, 25 - j * 0.8), 1),
            "groundspeed_kt": round(touchdown_groundspeed * (0.8 + 0.2 * vs_progress), 1),
            "ias_kt": round(touchdown_ias * (0.8 + 0.2 * vs_progress), 1),
            "heading_deg_true": round(random.uniform(195, 205), 1),  # Straight approach
            "on_ground": False if j < 22 else True,
        })

    # Straight rollout track
    rollout_track = []
    centerline_offset = random.uniform(-2, 2)  # Small offset
    for j in range(30):
        rollout_track.append({
            "t_ms": j * 50,
            "lat": round(random.uniform(33.0, 33.3), 6),
            "lon": round(random.uniform(35.5, 35.9), 6),
            "heading_deg_true": round(random.uniform(195, 205), 1),
            "bank_deg": round(random.uniform(-1, 1), 1),
            "groundspeed_kt": round(max(20, touchdown_groundspeed - j * 1.5 + random.uniform(-2, 2)), 1),
            "cross_track_error_ft": None,
            "cross_track_abs_ft": None,
            "centerline_error_norm": round(centerline_offset + random.uniform(-1, 1), 2),
            "track_vs_runway_axis_deg": None,
        })

    return {
        'touchdown_fpm': touchdown_fpm,
        'touchdown_groundspeed': touchdown_groundspeed,
        'touchdown_ias': touchdown_ias,
        'max_g': round(random.uniform(1.0, 1.5), 2),
        'bounce_count': 0,
        'touchdown_radio_alt': round(random.uniform(0, 10), 1),
        'touchdown_profile': touchdown_profile,
        'rollout_track': rollout_track
    }

def generate_off_center_landing():
    """Generate an off-center landing profile."""
    touchdown_fpm = random.randint(-1200, -600)
    touchdown_groundspeed = random.randint(100, 125)
    touchdown_ias = touchdown_groundspeed + random.randint(0, 8)

    # Normal touchdown profile but with lateral drift
    touchdown_profile = []
    for j in range(25):
        tms = -2000 + j * 90
        vs_progress = 1 - (j / 25.0)
        vertical_speed = -600 * vs_progress - 100
        touchdown_profile.append({
            "t_ms": tms,
            "vertical_speed_fpm": round(vertical_speed, 1),
            "g_force": round(random.uniform(1.0, 2.0), 2),
            "radio_alt_ft": round(max(0, 30 - j * 0.9), 1),
            "groundspeed_kt": round(touchdown_groundspeed * (0.8 + 0.2 * vs_progress), 1),
            "ias_kt": round(touchdown_ias * (0.8 + 0.2 * vs_progress), 1),
            "heading_deg_true": round(random.uniform(185, 215), 1),  # Slight crab angle
            "on_ground": False if j < 20 else True,
        })

    # Off-center rollout track
    rollout_track = []
    centerline_offset = random.choice([-15, 15]) + random.uniform(-5, 5)  # Significant offset
    for j in range(30):
        rollout_track.append({
            "t_ms": j * 50,
            "lat": round(random.uniform(33.0, 33.3), 6),
            "lon": round(random.uniform(35.5, 35.9), 6),
            "heading_deg_true": round(random.uniform(190, 210), 1),
            "bank_deg": round(random.uniform(-3, 3), 1),
            "groundspeed_kt": round(max(25, touchdown_groundspeed - j * 1.2 + random.uniform(-3, 3)), 1),
            "cross_track_error_ft": None,
            "cross_track_abs_ft": None,
            "centerline_error_norm": round(centerline_offset + random.uniform(-2, 2), 2),
            "track_vs_runway_axis_deg": None,
        })

    return {
        'touchdown_fpm': touchdown_fpm,
        'touchdown_groundspeed': touchdown_groundspeed,
        'touchdown_ias': touchdown_ias,
        'max_g': round(random.uniform(1.2, 2.2), 2),
        'bounce_count': random.randint(0, 1),
        'touchdown_radio_alt': round(random.uniform(0, 20), 1),
        'touchdown_profile': touchdown_profile,
        'rollout_track': rollout_track
    }

def generate_bumping_landing():
    """Generate a bumpy landing with bounces."""
    touchdown_fpm = random.randint(-2000, -1000)
    touchdown_groundspeed = random.randint(110, 135)
    touchdown_ias = touchdown_groundspeed + random.randint(0, 10)
    bounce_count = random.randint(2, 4)

    # Bumpy touchdown profile with oscillations
    touchdown_profile = []
    for j in range(25):
        tms = -2000 + j * 90
        vs_progress = 1 - (j / 25.0)

        # Add bounce oscillations
        bounce_factor = 1.0
        if bounce_count > 0 and j > 15:
            bounce_phase = (j - 15) % 4
            if bounce_phase < 2:
                bounce_factor = 0.3  # Bounce up
            else:
                bounce_factor = 1.8  # Bounce down

        vertical_speed = (-800 * vs_progress - 200) * bounce_factor
        touchdown_profile.append({
            "t_ms": tms,
            "vertical_speed_fpm": round(vertical_speed, 1),
            "g_force": round(random.uniform(1.5, 4.0) * bounce_factor, 2),  # High G on bounces
            "radio_alt_ft": round(max(0, 35 - j * 1.0), 1),
            "groundspeed_kt": round(touchdown_groundspeed * (0.8 + 0.2 * vs_progress) + random.uniform(-5, 5), 1),
            "ias_kt": round(touchdown_ias * (0.8 + 0.2 * vs_progress) + random.uniform(-5, 5), 1),
            "heading_deg_true": round(random.uniform(190, 230), 1),
            "on_ground": False if j < 18 else True,
        })

    # Erratic rollout track
    rollout_track = []
    centerline_offset = random.uniform(-8, 8)
    for j in range(30):
        rollout_track.append({
            "t_ms": j * 50,
            "lat": round(random.uniform(33.0, 33.3), 6),
            "lon": round(random.uniform(35.5, 35.9), 6),
            "heading_deg_true": round(random.uniform(190, 230), 1),
            "bank_deg": round(random.uniform(-8, 8), 1),  # More bank due to instability
            "groundspeed_kt": round(max(30, touchdown_groundspeed - j * 1.0 + random.uniform(-8, 8)), 1),
            "cross_track_error_ft": None,
            "cross_track_abs_ft": None,
            "centerline_error_norm": round(centerline_offset + random.uniform(-3, 3), 2),
            "track_vs_runway_axis_deg": None,
        })

    return {
        'touchdown_fpm': touchdown_fpm,
        'touchdown_groundspeed': touchdown_groundspeed,
        'touchdown_ias': touchdown_ias,
        'max_g': round(random.uniform(2.5, 4.0), 2),
        'bounce_count': bounce_count,
        'touchdown_radio_alt': round(random.uniform(0, 30), 1),
        'touchdown_profile': touchdown_profile,
        'rollout_track': rollout_track
    }

count = 0
landing_types = ['calm', 'off_center', 'bumping']
landing_generators = {
    'calm': generate_calm_landing,
    'off_center': generate_off_center_landing,
    'bumping': generate_bumping_landing
}

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

            # Cycle through landing types for variety
            landing_type = landing_types[file_i % len(landing_types)]
            landing_data = landing_generators[landing_type]()

            filename = f"{t.strftime('%Y-%m-%d_%H%M%SZ')}_{landing_type.title()}_{file_i+1}.json"
            path = os.path.join(folder, filename)

            chrono = int(random.uniform(200, 650))

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
                "touchdown_fpm": landing_data['touchdown_fpm'],
                "touchdown_groundspeed_kt": landing_data['touchdown_groundspeed'],
                "touchdown_ias_kt": landing_data['touchdown_ias'],
                "max_g": landing_data['max_g'],
                "bounce_count": landing_data['bounce_count'],
                "touchdown_radio_alt_ft": landing_data['touchdown_radio_alt'],
                "airborne_time_seconds_total": chrono,
                "airborne_time_seconds_scored": chrono - random.uniform(0, 4),
                "touchdown_profile": landing_data['touchdown_profile'],
                "rollout_track": landing_data['rollout_track'],
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

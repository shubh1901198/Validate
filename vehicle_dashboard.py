import time
import random
import configparser
import os
import logging

# --- CONFIGURATION ---
CONFIG_FILE = "config.ini"
LOG_FILE = "dashboard.log"

# --- LOGGING SETUP ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def initialize_dashboard():
    print("--- Vehicle Dashboard Application Initialized ---")
    data = {
        "Speed_Km_hr": 0,
        "RPM": 0,
        "Battery_Level_Pct": 100.0
    }
    return data

def load_thresholds():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        print(f"🚨 ERROR: Configuration file '{CONFIG_FILE}' not found!")
        print("Using default hardcoded thresholds.")
        return {
            "Speed_Km_hr": 110,
            "RPM": 6000,
            "Battery_Level_Pct": 10
        }

    config.read(CONFIG_FILE)
    try:
        thresholds = {
            "Speed_Km_hr": config.getfloat('THRESHOLDS', 'SPEED_KM_HR'),
            "RPM": config.getfloat('THRESHOLDS', 'RPM'),
            "Battery_Level_Pct": config.getfloat('THRESHOLDS', 'BATTERY_LEVEL_PCT')
        }
        return thresholds
    except configparser.Error as e:
        print(f"🚨 ERROR reading config file: {e}")
        print("Using default hardcoded thresholds.")
        return {
            "Speed_Km_hr": 110,
            "RPM": 6000,
            "Battery_Level_Pct": 10
        }

def get_real_time_data(current_data):
    speed_change = random.randint(-15, 15)
    new_speed = max(0, current_data["Speed_Km_hr"] + speed_change)
    current_data["Speed_Km_hr"] = new_speed

    new_rpm = max(800, min(6500, new_speed * 30 + random.randint(-400, 400)))
    current_data["RPM"] = new_rpm

    drain_factor = 0.01 + (current_data["RPM"] / 1500000)
    new_battery = max(0.0, current_data["Battery_Level_Pct"] - drain_factor)
    current_data["Battery_Level_Pct"] = round(new_battery, 2)

    return current_data

def display_dashboard(data):
    print("\n-------------------------------------------")
    print("      *** Real-Time Vehicle Status ***")
    print("-------------------------------------------")
    print(f"  🏎️  Speed: {data['Speed_Km_hr']: <4.0f} Km/hr")
    rpm_bar = "█" * (int(data['RPM'] / 1000))
    print(f"  ⚙️  RPM:   {data['RPM']: <4.0f} RPM ({rpm_bar})")

    battery_level = int(data['Battery_Level_Pct'] / 10)
    battery_icon = "🔋" if data['Battery_Level_Pct'] > 20 else "🪫"
    battery_bar = "█" * battery_level + "░" * (10 - battery_level)
    print(f"  {battery_icon} Battery: {data['Battery_Level_Pct']: <5.2f} % [{battery_bar}]")
    print("-------------------------------------------")

def check_alerts(data, thresholds):
    alerts = []

    if data["Speed_Km_hr"] > thresholds["Speed_Km_hr"]:
        alerts.append(f"🛑 HIGH SPEED ALERT! Speed: {data['Speed_Km_hr']} Km/hr (Threshold: {thresholds['Speed_Km_hr']})")

    if data["RPM"] > thresholds["RPM"]:
        alerts.append(f"⚠️ HIGH RPM ALERT! RPM: {data['RPM']} (Threshold: {thresholds['RPM']})")

    if data["Battery_Level_Pct"] < thresholds["Battery_Level_Pct"]:
        alerts.append(f"🪫 LOW BATTERY ALERT! Battery: {data['Battery_Level_Pct']}% (Threshold: {thresholds['Battery_Level_Pct']}%)")

    if alerts:
        print("\n*** SYSTEM ALERTS ***")
        for alert in alerts:
            print(alert)
        print("*********************")

    return alerts

def log_data(data, alerts):
    logging.info(f"Speed: {data['Speed_Km_hr']} Km/hr, RPM: {data['RPM']}, Battery: {data['Battery_Level_Pct']}%")
    for alert in alerts:
        logging.warning(alert)

def run_monitoring_cycle(target_cycles=10):
    vehicle_data = initialize_dashboard()
    thresholds = load_thresholds()

    print("\n--- Starting Monitoring Cycle ---")
    print(f"Alert Thresholds: Speed > {thresholds['Speed_Km_hr']} Km/hr, RPM > {thresholds['RPM']}, Battery < {thresholds['Battery_Level_Pct']}%")

    vehicle_data["Speed_Km_hr"] = 120
    print(f"(Initial speed manually set to {vehicle_data['Speed_Km_hr']} Km/hr for immediate check)")

    for cycle in range(1, target_cycles + 1):
        print(f"\n======== CYCLE {cycle}/{target_cycles} ========")
        vehicle_data = get_real_time_data(vehicle_data)
        display_dashboard(vehicle_data)
        alerts = check_alerts(vehicle_data, thresholds)
        log_data(vehicle_data, alerts)
        time.sleep(0.5)

    print("\n--- Monitoring Cycle Complete ---")

# --- EXECUTION ---
if __name__ == "__main__":
    run_monitoring_cycle(target_cycles=10)

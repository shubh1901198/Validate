import time
import random
import configparser
import os # To check if config.ini exists

# --- 1. CONFIGURATION / INITIALIZATION ---
CONFIG_FILE = "config.ini"

def initialize_dashboard():
    """Sets initial values and simulation parameters."""
    print("--- Vehicle Dashboard Application Initialized ---")
    data = {
        "Speed_Km_hr": 0,
        "RPM": 0,
        "Battery_Level_Pct": 100.0
    }
    return data

def load_thresholds():
    """Loads threshold values from the config.ini file."""
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

# --- 2. DATA ACQUISITION SIMULATION ---
def get_real_time_data(current_data):
    """Simulates fetching new data from the vehicle's ECU."""
    
    # Introduce more variability for simulation purposes, especially for speed
    speed_change = random.randint(-15, 15) 
    new_speed = max(0, current_data["Speed_Km_hr"] + speed_change)
    current_data["Speed_Km_hr"] = new_speed

    # RPM calculation adjusted to simulate a running engine even at low speed
    new_rpm = max(800, min(6500, new_speed * 30 + random.randint(-400, 400)))
    current_data["RPM"] = new_rpm

    # Battery drain related to RPM/speed
    drain_factor = 0.01 + (current_data["RPM"] / 1500000) 
    new_battery = max(0.0, current_data["Battery_Level_Pct"] - drain_factor)
    current_data["Battery_Level_Pct"] = round(new_battery, 2)
    return current_data

# --- 3. UI RENDERING / DISPLAY ---
def display_dashboard(data):
    """Renders the current data to the console (simulating the UI)."""
    print("\n-------------------------------------------")
    print("      *** Real-Time Vehicle Status ***")
    print("-------------------------------------------")
    print(f"  🏎️  Speed: **{data['Speed_Km_hr']: <4.0f} Km/hr**") 
    rpm_bar = "█" * (int(data['RPM'] / 1000))
    print(f"  ⚙️  RPM:   **{data['RPM']: <4.0f}** Revolutions/Min ({rpm_bar})")
    
    battery_level = int(data['Battery_Level_Pct'] / 10)
    battery_icon = "🔋" if data['Battery_Level_Pct'] > 20 else "🪫"
    battery_bar = "█" * battery_level + "░" * (10 - battery_level)
    print(f"  {battery_icon} Battery: **{data['Battery_Level_Pct']: <5.2f} %** [{battery_bar}]")
    print("-------------------------------------------")

# --- 4. ALERTING LOGIC ---
def check_alerts(data, thresholds):
    """Compares current data against thresholds and prints alerts."""
    alerts = []
    
    if data["Speed_Km_hr"] > thresholds["Speed_Km_hr"]:
        alerts.append(f"🛑 **HIGH SPEED ALERT!** Current Speed: {data['Speed_Km_hr']:.0f} Km/hr (Threshold: {thresholds['Speed_Km_hr']:.0f})")

    if data["RPM"] > thresholds["RPM"]:
        alerts.append(f"⚠️ **HIGH RPM ALERT!** Current RPM: {data['RPM']:.0f} RPM (Threshold: {thresholds['RPM']:.0f})")

    if data["Battery_Level_Pct"] < thresholds["Battery_Level_Pct"]:
        alerts.append(f"🪫 **LOW BATTERY ALERT!** Current: {data['Battery_Level_Pct']:.2f} % (Threshold: {thresholds['Battery_Level_Pct']:.0f} %)")

    if alerts:
        print("\n*** SYSTEM ALERTS ***")
        for alert in alerts:
            print(alert)
        print("*********************")
        
    return alerts

# --- 5. EXECUTION LOOP ---
def run_monitoring_cycle(target_cycles=5):
    """Initializes and runs the data acquisition, display, and alert cycle."""
    
    vehicle_data = initialize_dashboard()
    thresholds = load_thresholds()
    
    print("\n--- Starting Monitoring Cycle ---")
    print(f"Alert Thresholds: Speed > {thresholds['Speed_Km_hr']:.0f} Km/hr, RPM > {thresholds['RPM']:.0f}, Battery < {thresholds['Battery_Level_Pct']:.0f} %")
    
    # Manually set initial high speed to force an alert in the first cycle
    initial_speed = 120 
    vehicle_data["Speed_Km_hr"] = initial_speed
    print(f"(Initial speed manually set to {initial_speed} Km/hr for immediate check)")
    
    for cycle in range(1, target_cycles + 1):
        print(f"\n======== CYCLE {cycle}/{target_cycles} ========")
        
        # 1. Acquire new data
        vehicle_data = get_real_time_data(vehicle_data)
        
        # 2. Display dashboard
        display_dashboard(vehicle_data)
        
        # 3. Check and display alerts
        check_alerts(vehicle_data, thresholds)
        
        # Pause for simulation visibility
        time.sleep(0.5) 
        
    print("\n--- Monitoring Cycle Complete ---")


# The original manual test is now superseded by the full monitoring loop
# Keeping it for reference, but changing execution to the new loop
# def run_manual_speed_test(target_speed):
#     ...

# --- EXECUTION ---
# Run the new monitoring test
run_monitoring_cycle(target_cycles=10)
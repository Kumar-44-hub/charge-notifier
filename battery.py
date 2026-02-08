import psutil

def get_battery_status():
    battery = psutil.sensors_battery()

    if battery is None:
        return None

    percent = battery.percent
    plugged = battery.power_plugged

    return percent, plugged


if __name__ == "__main__":
    status = get_battery_status()

    if status is None:
        print("Battery information not available")
    else:
        percent, plugged = status
        print(f"Battery: {percent}%")
        print("Charger Plugged In" if plugged else "Charger Unplugged")

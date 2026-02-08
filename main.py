import time
from battery import get_battery_status
from sound import play_plugged_sound, play_unplugged_sound
from notifier import notify_90
from state import BatteryState
from full_charge_popup import show_full_charge_popup
from usage_tracker import UsageTracker
from settings import load_settings
from tray import TrayIcon

CHECK_INTERVAL = 10  # seconds


def main():
    state = BatteryState()
    usage_tracker = UsageTracker(break_minutes=60)  # 1 hour
    settings = load_settings()

    monitoring_enabled = True

    print("Charge Notifier started...")

    def start_monitoring():
        nonlocal monitoring_enabled
        monitoring_enabled = True

    def stop_monitoring():
        nonlocal monitoring_enabled
        monitoring_enabled = False

    tray = TrayIcon(start_monitoring, stop_monitoring)
    import threading
    threading.Thread(target=tray.run, daemon=True).start()

    status = get_battery_status()
    if status is not None:
        percent, plugged = status
        state.last_plugged = plugged
        if percent >= 90:
            state.notified_90 = True
        if percent >= 100:
            state.notified_100 = True

    while True:
        if not monitoring_enabled:
            time.sleep(1)
            continue

        status = get_battery_status()
        if status is None:
            time.sleep(CHECK_INTERVAL)
            continue

        percent, plugged = status

        if state.has_plug_state_changed(plugged):
            if settings.get("sounds_enabled", True):
                play_plugged_sound() if plugged else play_unplugged_sound()

            if not plugged:
                state.reset_notifications_if_unplugged(plugged)

        if plugged and percent >= 90 and not state.notified_90:
            notify_90(percent)
            state.notified_90 = True

        if plugged and percent >= 100 and not state.notified_100:
            show_full_charge_popup()
            state.notified_100 = True

        if settings.get("break_reminder_enabled", True):
            usage_tracker.check_break_time()

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

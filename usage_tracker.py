import time
import ctypes
from plyer import notification


class UsageTracker:
    def __init__(self, break_minutes=60):  # 1 hour
        self.break_seconds = break_minutes * 60
        self.start_time = time.time()
        self.last_alert_unit = 0

    def get_idle_time(self):
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint),
            ]

        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))

        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000  # seconds

    def check_break_time(self):
        idle_time = self.get_idle_time()

        # Reset if system idle / locked
        if idle_time > 600:   # 10 minutes
            self.start_time = time.time()
            self.last_alert_unit = 0
            return

        active_seconds = time.time() - self.start_time
        active_hours = int(active_seconds // self.break_seconds)

        if active_hours > 0 and active_hours > self.last_alert_unit:
            self.show_break_notification(active_hours)
            self.last_alert_unit = active_hours

    def show_break_notification(self, hours):
     if hours == 1:
        message = (
            f"⏱️ USING CONTINUOUSLY: {hours} HOUR\n"
            f"🙂 TIME FOR A SHORT BREAK 👣"
        )
     elif hours == 2:
        message = (
            f"⏱️ USING CONTINUOUSLY: {hours} HOURS\n"
            f"⚠️ PLEASE TAKE A BREAK NOW 👣"
        )
     else:
        message = (
            f"⏱️ USING CONTINUOUSLY: {hours} HOURS\n"
            f"🚨 LONG USAGE DETECTED — REST YOUR EYES & BODY 👣"
        )

     notification.notify(
        title="Charge Notifier",
        message=message,
        timeout=20
     )


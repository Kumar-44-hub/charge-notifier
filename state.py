class BatteryState:
    def __init__(self):
        self.last_plugged = None
        self.notified_90 = False
        self.notified_100 = False

    def has_plug_state_changed(self, current_plugged):
        if self.last_plugged is None:
            self.last_plugged = current_plugged
            return False

        if current_plugged != self.last_plugged:
            self.last_plugged = current_plugged
            return True

        return False

    def reset_notifications_if_unplugged(self, plugged):
        if not plugged:
            self.notified_90 = False
            self.notified_100 = False

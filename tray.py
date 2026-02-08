import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw


def create_image():
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="black")
    return image


class TrayIcon:
    def __init__(self, on_start, on_stop):
        self.on_start = on_start
        self.on_stop = on_stop

        self.icon = Icon(
            "Charge Notifier",
            create_image(),
            "Charge Notifier",
            menu=Menu(
                MenuItem("Start Monitoring", self.start),
                MenuItem("Stop Monitoring", self.stop),
                MenuItem("Exit", self.exit_app),
            ),
        )

    def start(self, icon, item):
        self.on_start()

    def stop(self, icon, item):
        self.on_stop()

    def exit_app(self, icon, item):
        self.on_stop()
        icon.stop()
        sys.exit(0)

    def run(self):
        # IMPORTANT: this must NOT be daemon
        self.icon.run()

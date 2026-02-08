from plyer import notification

def notify_90(percent):
    notification.notify(
        title="Charge Notifier",
        message=f"Battery reached {percent}%",
        timeout=5
    )

"""Helper Functions for TSkr"""
import os
import requests
from pushover_complete import PushoverAPI
from . import db
from .models import Notification

def send_notification(initiator, *args, **kwargs):
    """Send Notification via Pushover"""
    if "image" in kwargs and kwargs["image"]:
        img_url = kwargs["image"]
        kwargs["image"] = requests.get(img_url, stream=True).content
    pusher = PushoverAPI(os.environ.get("PUSHOVER_TOKEN"))
    response = pusher.send_message(os.environ.get("PUSHOVER_USER"), *args, **kwargs)
    kwargs["message"] = args[0]
    if "image" in kwargs:
        kwargs["image"] = img_url
    new = Notification(initiator, args[0][:2000], kwargs, response)
    db.session.add(new)
    db.session.commit()
    return response

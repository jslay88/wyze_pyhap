import logging

from wyze_sdk import Client
from wyze_sdk.models import devices

from .devices.bulbs import WyzeBulb
from .devices.thermostat import WyzeThermostat
from .settings import settings


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


client = Client(
    email=settings.WYZE_USERNAME,
    password=settings.WYZE_PASSWORD,
    totp_key=settings.WYZE_TOTP,
)


def get_wyze_devices(driver):
    _devices = []
    for device in client.devices_list():
        print(f"nickname: {device.nickname}")
        print(f"online: {device.is_online}")
        print(f"model: {device.product.model}")
        if isinstance(device, devices.Bulb):
            _devices.append(WyzeBulb(driver, device.nickname, client, device))
            continue
        if isinstance(device, devices.Thermostat):
            _devices.append(WyzeThermostat(driver, device.nickname, client, device))
    return _devices

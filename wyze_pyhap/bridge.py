import logging
import signal

from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver

from .discovery import get_wyze_devices
from .settings import settings
from .utils import discover_interface_address


logger = logging.getLogger(__name__)


def run():
    driver = AccessoryDriver(
        address=settings.BIND_ADDRESS
        if settings.BIND_ADDRESS
        else discover_interface_address(settings.BIND_INTERFACE_NAME),
        persist_file=settings.ACCESSORY_STATE_PATH,
    )
    bridge = Bridge(driver, "Wyze HomeKit Bridge")

    # Wyze Devices
    for device in get_wyze_devices(driver):
        bridge.add_accessory(device)

    # Add Bridge with all accessories
    driver.add_accessory(accessory=bridge)
    signal.signal(signal.SIGTERM, driver.signal_handler)
    driver.start()

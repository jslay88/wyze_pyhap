import logging
from typing import Union

from colorutils import Color
from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_LIGHTBULB
from wyze_sdk.api.client import Client
from wyze_sdk.models.devices import Bulb, MeshBulb


logger = logging.getLogger(__name__)


class WyzeBulb(Accessory):
    category = CATEGORY_LIGHTBULB

    def __init__(
        self,
        driver: AccessoryDriver,
        device_name: str,
        wyze_client: Client,
        wyze_bulb: Union[Bulb, MeshBulb],
        *args,
        **kwargs,
    ):
        super(WyzeBulb, self).__init__(driver, device_name, *args, **kwargs)

        self.client = wyze_client
        self.bulb = wyze_bulb

        self._state = False
        self._hue = 0
        self._saturation = 100
        self._brightness = 100
        self._set_queue = None

        if isinstance(wyze_bulb, MeshBulb):
            service = self.add_preload_service(
                "Lightbulb", chars=["Brightness", "Hue", "Saturation"]
            )
            self.char_hue = service.configure_char("Hue", setter_callback=self.set_hue)
            self.char_saturation = service.configure_char(
                "Saturation", setter_callback=self.set_saturation
            )
        else:
            service = self.add_preload_service("Lightbulb", chars=["Brightness"])
        self.char_on = service.configure_char("On", setter_callback=self.set_state)
        self.char_brightness = service.configure_char(
            "Brightness", setter_callback=self.set_brightness
        )

    # On Off State
    def set_state(self, value):
        logger.info(f"Setting State to {value} for {self.bulb.nickname}...")
        if isinstance(value, str):
            if value.lower() == "on":
                self.client.bulbs.turn_on(
                    device_mac=self.bulb.mac, device_model=self.bulb.product.model
                )
                return
            self.client.bulbs.turn_off(
                device_mac=self.bulb.mac, device_model=self.bulb.product.model
            )
            return

        if isinstance(value, (int, float)):
            if value > 0:
                self.client.bulbs.turn_on(
                    device_mac=self.bulb.mac, device_model=self.bulb.product.model
                )
                return
            self.client.bulbs.turn_off(
                device_mac=self.bulb.mac, device_model=self.bulb.product.model
            )
            return

        if isinstance(value, bool):
            if value:
                self.client.bulbs.turn_on(
                    device_mac=self.bulb.mac, device_model=self.bulb.product.model
                )
                return
            self.client.bulbs.turn_off(
                device_mac=self.bulb.mac, device_model=self.bulb.product.model
            )
            return

    # Color
    def set_hue(self, value):
        logger.info(f"Setting Hue to {value} for {self.bulb.nickname}...")
        self._hue = value
        if self._set_queue is None:
            self.set_color()

    def set_saturation(self, value):
        logger.info(f"Setting Saturation to {value} for {self.bulb.nickname}")
        self._saturation = value * 0.01
        if self._set_queue is None:
            self.set_color()

    def set_brightness(self, value):
        logger.info(f"Setting Brightness to {value} for {self.bulb.nickname}...")
        self._brightness = value
        if value == 0:
            return
        self.client.bulbs.set_brightness(
            device_mac=self.bulb.mac,
            device_model=self.bulb.product.model,
            brightness=value,
        )

    def set_color(self):
        logger.info("Setting color")
        _hex = Color(hsv=(self._hue, self._saturation, 1)).hex
        self.client.bulbs.set_color(
            device_mac=self.bulb.mac,
            device_model=self.bulb.product.model,
            color=_hex[1:],
        )
        self._set_queue = None

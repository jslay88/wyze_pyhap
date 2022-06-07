import logging

from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_THERMOSTAT
from wyze_sdk.api.client import Client
from wyze_sdk.models.devices import Thermostat


logger = logging.getLogger(__name__)

"""
Required:
CurrentHeatingCoolingState
TargetHeatingCoolingState -> set_system_mode
CurrentTemperature
TargetTemperature
TemperatureDisplayUnits

Optional:
CurrentRelativeHumidity
TargetRelativeHumidity
CoolingThresholdTemperature -> set_temperature
HeatingThresholdTemperature -> set_temperature
"""


class WyzeThermostat(Accessory):
    category = CATEGORY_THERMOSTAT

    def __init__(
        self,
        driver: AccessoryDriver,
        device_name: str,
        wyze_client: Client,
        wyze_thermostat: Thermostat,
        *args,
        **kwargs,
    ):
        super(WyzeThermostat, self).__init__(driver, device_name, *args, **kwargs)

        self.client = wyze_client
        self.device = wyze_thermostat

        self._current_humidity = 0
        self._current_temp = 32
        self._target_temp = 32
        self._heating_temp = 32
        self._cooling_temp = 32
        self._mode = 0

        service = self.add_preload_service(
            "Thermostat",
            chars=[
                "CoolingThresholdTemperature",
                "HeatingThresholdTemperature",
                "CurrentRelativeHumidity",
            ],
        )
        self.char_current_heating_cooling_state = service.configure_char(
            "CurrentHeatingCoolingState", getter_callback=self.get_mode
        )
        self.char_target_heating_cooling_state = service.configure_char(
            "TargetHeatingCoolingState", setter_callback=self.set_mode
        )
        self.char_current_temperature = service.configure_char(
            "CurrentTemperature", getter_callback=self.get_current_temperature
        )
        self.char_target_temperature = service.configure_char(
            "TargetTemperature",
            getter_callback=self.get_target_temperature,
            setter_callback=self.set_target_temperature,
        )
        self.char_current_relative_humidity = service.configure_char(
            "CurrentRelativeHumidity",
            getter_callback=self.get_current_relative_humidity,
        )
        self.char_cooling_threshold_temperature = service.configure_char(
            "CoolingThresholdTemperature",
            getter_callback=self.get_cooling_threshold_temperature,
            setter_callback=self.set_cooling_threshold_temperature,
        )
        self.char_heating_threshold_temperature = service.configure_char(
            "HeatingThresholdTemperature",
            getter_callback=self.get_heating_threshold_temperature,
            setter_callback=self.set_heating_threshold_temperature,
        )

    def set_mode(self, value: int):
        logger.info(f"Set Mode: {value}")
        self._mode = value

    def get_mode(self):
        logger.info(f"Getting Mode: {self._mode}...")
        return self._mode

    def get_current_temperature(self):
        logger.info(f"Getting Current Temperature: {self._current_temp}")
        return self._current_temp

    def set_target_temperature(self, value):
        logger.info(f"Setting Target Temperature: {value}")
        self._target_temp = value

    def get_target_temperature(self):
        logger.info(f"Getting Target Temperature: {self._target_temp}")
        return self._target_temp

    def get_current_relative_humidity(self):
        logger.info(f"Getting Current Relative Humidity: {self._current_humidity}")
        return self._current_humidity

    def set_cooling_threshold_temperature(self, value):
        logger.info(f"Setting Cooling Threshold Temperature: {value}")
        self._cooling_temp = value

    def get_cooling_threshold_temperature(self):
        logger.info(f"Getting Cooling Threshold Temperature: {self._cooling_temp}")
        return self._cooling_temp

    def set_heating_threshold_temperature(self, value):
        logger.info(f"Setting Heating Threshold Temperature: {value}")
        self._heating_temp = value

    def get_heating_threshold_temperature(self):
        logger.info(f"Getting Heating Threshold Temperature: {self._heating_temp}")
        return self._heating_temp

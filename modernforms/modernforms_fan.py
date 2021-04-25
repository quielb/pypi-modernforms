"""Module for Controlling ModernForms Fans with option light kit."""
import requests
from . import exceptions
from datetime import date, datetime

DEFAULT_TIMEOUT = 5
DEFAULT_HEADERS = {"Content-Type": "application/json"}

Y = 2000  # dummy leap year to allow input X-02-29 (leap day)
seasons = [
    ("winter", (date(Y, 1, 1), date(Y, 3, 20))),
    ("spring", (date(Y, 3, 21), date(Y, 6, 20))),
    ("summer", (date(Y, 6, 21), date(Y, 9, 22))),
    ("autumn", (date(Y, 9, 23), date(Y, 12, 20))),
    ("winter", (date(Y, 12, 21), date(Y, 12, 31))),
]


def get_season():
    """ Gets current season """
    now = date.today()
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons if start <= now <= end)


fanSeasonDirections = {
    "winter": "reverse",
    "summer": "forward",
    "autumn": "reverse",
    "spring": "forward",
}
currentSeason = get_season()
seasonDirection = fanSeasonDirections[currentSeason]


class ModernFormsFan:
    """Class representing a fan.

    Constructor has one required parameter.
    IP or host name of fan to control.
    """

    def __init__(self, host, timeout=DEFAULT_TIMEOUT):
        """Initialize a fan."""
        self._api_endpoint = "http://" + host + "/mf"
        self._timeout = timeout
        self._data = {}
        

    @property
    def light_on(self):
        """Get the light state.

        True if on. False if off.
        """
        return self._data["lightOn"]

    @light_on.setter
    def light_on(self, state: bool):
        """Set the light state.

        True on. False off.
        API ignores invalid values
        """
        self._set_device_state({"lightOn": state})

    def toggleLight(self):
        """ Toggles light state. """
        state = not self._data["lightOn"]
        self._set_device_state({"lightOn": state})

    @property
    def light_brightness(self) -> int:
        """Get the light brightness.

        Returns int between 0 and 100.
        """
        return self._data["lightBrightness"]

    @light_brightness.setter
    def light_brightness(self, brightness: int) -> None:
        """Set the light brightness.

        Any integer is accepted.
        API ignores invalid values.
        """
        self._set_device_state({"lightBrightness": brightness})

    @property
    def fan_on(self) -> bool:
        """Get the fan state.

        True if on. False if off.
        """
        return self._data["fanOn"]

    @fan_on.setter
    def fan_on(self, state: bool) -> None:
        """Set the fan state.

        True on. False off.
        API ignores invalid values
        """
        self.set_device_state({"fanOn": state})

    def toggleFan(self, direction: bool = seasonDirection):
        """Toggles the fan state.

        Also automatically detects which season it is and spins the fan in the corresponding direction for that season.
        This can be overriden by setting the direction parameter to something else.
        """

        state = not self._data["fanOn"]
        self._set_device_state({"fanDirection": direction, "fanOn": state})

    @property
    def fan_speed(self) -> int:
        """Get the fan speed.

        Returns int between 1 and 6.
        """
        return self._data["fanSpeed"]

    @fan_speed.setter
    def fan_speed(self, speed: int) -> None:
        """Set the fan_speed.

        Any integer is accepted.
        API ignores invalid values.
        """
        self._set_device_state({"fanSpeed": speed})

    @property
    def fan_direction(self) -> str:
        """Get the fan direction.

        Returns string of either forward or reverse.
        """
        return self._data["fanDirection"]

    @fan_direction.setter
    def fan_direction(self, direction: str) -> None:
        """Set the fan direction.

        Any string is accepted.
        API ignores invalid values.
        """
        self._set_device_state({"fanDirection": direction})

    def set_light(self, state: bool, brightness: int = None) -> None:
        """Set light state.

        Function to set all possible params of the light in a single API call.
        Instead of individual API calls by each setter.
        """
        payload = {"lightOn": state}
        if brightness is not None:
            payload["lightBrightness"] = brightness
        self._set_device_state(payload)

    def set_fan(self, state: bool, speed: int = None, direction: str = None) -> None:
        """Set fan state.

        Set all possible params of the fan in a single API call.
        Instead of individual API calls by each setter.
        """
        payload = {"fanOn": state}
        if speed is not None:
            payload["fanSpeed"] = speed
        if direction is not None:
            payload["fanDirection"] = direction
        self._set_device_state(payload)

    def get_device_state(self, data=None):
        """Get refresh data from fan.

        Can be called directly.
        If called with no state data will poll the fan and update _data.
        If state data is passed in will use that to update state
        instead hitting API.
        Function returns Dict of fan state data.
        """
        result_body = None
        if data is None:
            self._set_device_state({"queryDynamicShadowData": 1})
        else:
            result_body = data

        if result_body is not None:
            self._data.update(result_body)

        if "fanType" not in self._data:
            self._set_device_state({"queryStaticShadowData": 1})
            
        return self._data

    def _set_device_state(self, payload) -> None:
        """Set state of fan based on JSON data passed in.

        Calls the fan API via POST and sends a JSON body.
        After the call to the API completes the fan returns a
        response of its current state.  That is forwarded back
        to get_device_state to update the fans in memory state.
        There is no need to poll the fan after issuing a command.
        """
        try:
            api = requests.post(
                self._api_endpoint,
                json=payload,
                headers=DEFAULT_HEADERS,
                timeout=self._timeout,
            )
        except requests.exceptions.ConnectionError:
            raise exceptions.ConnectionError from requests.exceptions.ConnectionError
        except requests.exceptions.ReadTimeout:
            raise exceptions.Timeout from requests.exceptions.ReadTimeout
        else:
            result_body = api.json()
            self.get_device_state(result_body)
            api.close()

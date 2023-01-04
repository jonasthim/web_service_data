# fti_ws/__init__.py

import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_RESOURCES,
    STATE_UNKNOWN,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_ENDPOINT = "endpoint"
CONF_LOCATION = "location"

DEFAULT_NAME = "fti_ws"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_LOCATION): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the FTI WDSL sensors."""
    from zeep import Client
    from zeep.transports import Transport
    from zeep.exceptions import Fault
    from requests import Session
    from requests.auth import HTTPBasicAuth
    from requests.structures import CaseInsensitiveDict
    import xml.etree.ElementTree as ET

    location = config[CONF_LOCATION]
    name = config[CONF_NAME]
    endpoint = "https://ftiws.ftiab.se/fti_ws/fti_ws.asmx?WSDL"

    session = Session()
    session.auth = HTTPBasicAuth('username', 'password')
    session.verify = False
    session.headers = CaseInsensitiveDict()
    session.headers["Content-Type"] = "text/xml;charset=UTF-8"
    session.headers["SOAPAction"] = "http://tempuri.org/GetWDSLData"

    transport = Transport(session=session)
    client = Client(endpoint, transport=transport)

    try:
        result = client.service.GetWDSLData(Location=location)
    except Fault as error:
        _LOGGER.error(error)
        return

    wdsl_data = {}
    root = ET.fromstring(result)
    for child in root:
        wdsl_data[child.tag] = child.text

    sensors = []
    for key, value in wdsl_data.items():
        sensors.append(FTIWDSLSensor(key, value))
    add_entities(sensors, True)

class FTIWDSLSensor(Entity):
    """Representation of a FTI WDSL sensor."""

    def __init__(self, name, data):
        """Initialize the sensor."""
        self._name = name
        self._state = data
        self._data = data

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return {
            "data": self._data,
        }


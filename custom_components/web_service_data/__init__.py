import voluptuous as vol

from homeassistant.helpers import config_validation as cv

# Define the configuration schema for the module
CONFIG_SCHEMA = vol.Schema({
    vol.Required('wsdl_url'): cv.string
})

# Import the sensor module
from . import sensor

# Define the name of the module's platform
PLATFORM_SCHEMA = sensor.PLATFORM_SCHEMA.extend({
    vol.Required('platform'): 'web_service_data'
})

# Define the setup function for the module
async def async_setup(hass, config):
    return sensor.async_setup_platform(hass, config, PLATFORM_SCHEMA)

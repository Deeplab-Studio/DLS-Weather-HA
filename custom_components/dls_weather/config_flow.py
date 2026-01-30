from homeassistant import config_entries
from .const import DOMAIN
import voluptuous as vol

class DLSWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            ip = user_input["ip"]
            url = f"http://{ip}/api/weather"

            return self.async_create_entry(
                title=f"DLS Weather ({ip})",
                data={"ip": ip, "url": url},
            )

        schema = vol.Schema({
            vol.Required("ip"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)

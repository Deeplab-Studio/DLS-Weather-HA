import aiohttp
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import logging

_LOGGER = logging.getLogger(__name__)

class DLSCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, url):
        self.url = url
        super().__init__(
            hass,
            _LOGGER,
            name="DLS Weather",
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=5) as resp:
                    return await resp.json()
        except Exception as e:
            _LOGGER.error("DLS fetch failed: %s", e)
            return {}

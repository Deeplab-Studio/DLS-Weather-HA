from .const import DOMAIN
from .coordinator import DLSCoordinator

async def async_setup_entry(hass, entry):
    url = entry.data["url"]
    coordinator = DLSCoordinator(hass, url)

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception:
        pass

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

SENSORS = {
    "temperature": ("Temperature", "°C", "temperature"),
    "humidity": ("Humidity", "%", "humidity"),
    "pressure": ("Pressure", "hPa", "pressure"),
    "air_quality": ("Air Quality", None, None),
    "uv_index": ("UV Index", None, "uv_index"),
    "wind_speed": ("Wind Speed", "m/s", "wind_speed"),
    "wind_dir": ("Wind Direction", "°", None),
    "rain_rate": ("Rain Rate", "mm/h", "precipitation_intensity"),
    "rain_daily": ("Daily Rain", "mm", "precipitation"),
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for key, (name, unit, device_class) in SENSORS.items():
        entities.append(DLSSensor(coordinator, key, name, unit, device_class))

    async_add_entities(entities)


class DLSSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, name, unit, device_class):
        super().__init__(coordinator)
        self._key = key

        # Entity attributes
        self._attr_name = f"DLS {name}"
        self._attr_unique_id = f"dls_weather_{key}"
        self._attr_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = "measurement"

        ICONS = {
            "temperature": "mdi:thermometer",
            "humidity": "mdi:water-percent",
            "pressure": "mdi:gauge",
            "air_quality": "mdi:blur",
            "uv_index": "mdi:weather-sunny",
            "wind_speed": "mdi:weather-windy",
            "wind_dir": "mdi:compass",
            "rain_rate": "mdi:weather-rainy",
            "rain_daily": "mdi:cup-water",
        }
        self._attr_icon = ICONS.get(key)

    @property
    def native_value(self):
        """Return the sensor value (NULL SAFE)."""
        if not self.coordinator.data:
            return None

        value = self.coordinator.data.get(self._key)

        # JSON null veya eksik alan
        if value is None:
            return None

        # String ise float'a çevir
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

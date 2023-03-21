#!/usr/bin/env python3

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity
)

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensors from a config entry created in the integrations UI."""

    api = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for stop in api.get_stop_keys():
        entities.append(MetrolinkAnnouncementSensor(api, stop)),

        entities.append(MetrolinkDestinationNameSensor(api, stop, 0)),
        entities.append(MetrolinkDestinationWaitSensor(api, stop, 0)),

        entities.append(MetrolinkDestinationNameSensor(api, stop, 1)),
        entities.append(MetrolinkDestinationWaitSensor(api, stop, 1)),

        entities.append(MetrolinkDestinationNameSensor(api, stop, 2))
        entities.append(MetrolinkDestinationWaitSensor(api, stop, 2))

    async_add_entities(entities, update_before_add=True)


class MetrolinkAnnouncementSensor(SensorEntity):
    """List of the next bins to be collected"""

    def __init__(self, api, stop):
        self.api = api
        self.stop = stop

        self._attr_name = self.api.get_stop_name(self.stop) + " announcement"
        self._attr_icon = "mdi:message-alert-outline"
        self._attr_unique_id = api.get_unique_sensor_id(self.stop, "announcement")
    

    async def async_update(self) -> None:
        await self.api.update()

        announcement = self.api.get_stop_announcement(self.stop)
        if announcement == "":
            announcement = "None"

        self._attr_native_value = announcement


class MetrolinkDestinationNameSensor(SensorEntity):
    """Destination name"""

    def __init__(self, api, stop, dest_i):
        self.api = api
        self.stop = stop
        self.dest_i = dest_i

        self._attr_name = self.api.get_stop_name(self.stop) + " destination name " + str(self.dest_i + 1)
        self._attr_icon = "mdi:tram"
        self._attr_unique_id = api.get_unique_sensor_id(self.stop, "destination_name_" + str(self.dest_i + 1))
    

    async def async_update(self) -> None:
        await self.api.update()
        self._attr_native_value = self.api.get_stop_destination_name(self.stop, self.dest_i)


class MetrolinkDestinationWaitSensor(SensorEntity):
    """Destination name"""

    def __init__(self, api, stop, dest_i):
        self.api = api
        self.stop = stop
        self.dest_i = dest_i

        self._attr_name = self.api.get_stop_name(self.stop) + " destination wait " + str(self.dest_i + 1)
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_native_unit_of_measurement = "min"
        self._attr_icon = "mdi:timer-outline"
        self._attr_unique_id = api.get_unique_sensor_id(self.stop, "destination_wait_" + str(self.dest_i + 1))
    

    async def async_update(self) -> None:
        await self.api.update()
        self._attr_native_value = self.api.get_stop_destination_wait(self.stop, self.dest_i)
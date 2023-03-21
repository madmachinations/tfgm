#!/usr/bin/env python3

import logging
from .tfgm import TransportForGreaterManchesterApi

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tfgm"
CONF_API_KEY = "api_key"
CONF_PID_REFS = "pid_refs"


async def async_setup_entry(hass, entry):
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})

    api = TransportForGreaterManchesterApi(
        entry.data[CONF_API_KEY],
        entry.data[CONF_PID_REFS].replace(" ", "").split(",")
    )
    await api.connect()

    if api.failed == False:

        hass.data[DOMAIN][entry.entry_id] = api

        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "sensor")
        )

        return True
    
    else:
        return False
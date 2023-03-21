# Transport For Greater Manchester (TFGM) Metrolink HomeAssistant Custom Component

This is a custom component for HomeAssistant.

It connect into the TFGM API and will get live Metrolink information for particular stops.

It creates sensors which will show you the same information you see on the information screen when you're stood on the platform. Detailing which trams are coming next, their destinations and how long until each of them arrive. It also will show station announcements.

For each stop you track, these sensors will be created:

- Announcements: Shows the current announcement for that station, or "None" if there is none.
- Destination 1 Name: The destination of the next tram to arrive
- Destination 1 Wait: The number of minutes until the next tram arrives
- Destination 2 Name: The destination of the second tram to arrive
- Destination 2 Wait: The number of minutes until the second tram arrives
- Destination 3 Name: The destination of the third tram to arrive
- Destination 3 Wait: The number of minutes until the third tram arrives

## Things you will need

First you will need to create an account for the TFGM API:

https://developer.tfgm.com/

Once logged in, you can subscribe to their "Open" product. This is their open API. Having done so it will give you your API key.

You will need the primary API key shortly, so keep this to hand.

Next you need to find some IDs for the stops you want to track information for.

To do this, go to the API documentation, and go to the `Metrolinks` page.

There will be a button on here to "Try it", press this.

By default, the `$top` parameter here is set to 10. Set this to something large like 9000. Now press send.

A bunch of data should now have appeared which shows information for all the different stops, lines and directions on the Metrolink network.

Press CTRL and F, or CMD and F on a Mac, and search for the name of a stop you want to try.

You will see there are several entries.

`StationLocation` holds the name of that stop.

When `Direction` is `Incoming` this is trams heading towards the city centre. When `Direction` is `Outgoing`, this is trams heading away from the city centre.

You will see for each one, there are some destinations listed. Find the block of data that is showing the correct stop and destinations for the direction of travel you want to track.

Once you have found it, make a note of the `PIDREF`.

You can repeat this process and make note of as many PIDREFs as you want to track. Once you have them all, you can move on to the installation.

If you feel able and you want to be able to search this data in more advanced ways, you can find the specification for setting filters and such here:

https://learn.microsoft.com/en-us/dynamics-nav/using-filter-expressions-in-odata-uris

## Installation

Copy the `tfgm` folder into the `custom_components` directory in your home assistant config folder. If one doesn't exist, you will need to create it.

Restart Home Assistant

Once restarted, go to the Devices and Integrations settings, and press to add a new integration. Search for `TFGM`.

The setup will ask you for your API Key first, paste this in.

Next it will ask you for your PID Refs. If you are tracking more than one, they need to be separated by a comma. For example, if I wanted to track `AIR-TPID01` and `BCH-TPID02`. I would enter that like this `AIR-TPID01,BCH-TPID02`.

Once these two fields have been filled out, that's it! Hit next.

You will now have 7 sensors per stop you are tracking.
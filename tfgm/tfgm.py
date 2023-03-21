#!/usr/bin/env python3

import aiohttp
import datetime
import hashlib


class TransportForGreaterManchesterApi:
    
    def __init__(self, api_key: str, pid_refs: list):
        self.api_key = api_key
        self.pid_refs = pid_refs
    
    
    async def connect(self):
        try:
            await self.__update()
        except:
            self.failed = True
        else:
            self.failed = False
    

    async def _get_request(self, endpoint: str, params: dict={}):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.tfgm.com/odata/" + endpoint, params=params, headers={
                "Ocp-Apim-Subscription-Key": self.api_key
            }) as response:
                return await response.json()
    

    def __get_pid_ref_filter_str(self):
        filter = ""
        for pid_ref in self.pid_refs:
            if filter != "":
                filter = filter + " or "
            filter = filter + "PIDREF eq '" + pid_ref + "'"
        return filter


    def __convert_stop_data_to_entity_id(self, stop_data: dict):
        station = stop_data['StationLocation']
        station = station.replace("'", "")
        station = station.replace(" ", "_")
        station = station.lower()

        direction = stop_data['Direction'].lower()

        return station + "__" + direction


    async def __update(self):
        response = await self._get_request("Metrolinks", {
            "$filter": self.__get_pid_ref_filter_str()
        })
        
        metrolink = {}

        for stop_data in response["value"]:
            metrolink[self.__convert_stop_data_to_entity_id(stop_data)] = {
                "announcement": stop_data['MessageBoard'],
                "station_name": stop_data['StationLocation'].replace("'",""),
                "destinations": [
                    {
                        "destination": stop_data['Dest0'],
                        "wait": stop_data['Wait0']
                    },
                    {
                        "destination": stop_data['Dest1'],
                        "wait": stop_data['Wait1']
                    },
                    {
                        "destination": stop_data['Dest2'],
                        "wait": stop_data['Wait2']
                    },
                ]
            }

        self.metrolink_data = metrolink
        self.last_updated = datetime.datetime.now()


    async def update(self):
        now = datetime.datetime.now()
        diff = now - self.last_updated

        if diff.total_seconds() >= 60:
            await self.__update()
            return True
        else:
            return False
    

    def get_stop_keys(self):
        found = []
        for key in self.metrolink_data.keys():
            found.append(key)
        return found


    def get_stop_announcement(self, stop_key):
        return self.metrolink_data[stop_key]['announcement']


    def get_stop_name(self, stop_key):
        return self.metrolink_data[stop_key]['station_name']


    def get_stop_destination_name(self, stop_key, dest_i):
        return self.metrolink_data[stop_key]['destinations'][dest_i]['destination']


    def get_stop_destination_wait(self, stop_key, dest_i):
        return self.metrolink_data[stop_key]['destinations'][dest_i]['wait']


    def get_unique_sensor_id(self, stop_key, description):
        unique_name = self.api_key+"__"+stop_key+"__"+str(description)
        return hashlib.md5(str(unique_name).encode("utf-8")).hexdigest()
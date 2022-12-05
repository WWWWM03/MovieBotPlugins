import asyncio
import ctypes
import datetime
import inspect
import logging
import threading
import time
from enum import Enum
from typing import Dict
from pypresence import Presence
import time
from plexapi.server import PlexServer
from threading import Timer


baseurl = 'http://192.168.50.190:32400'
token = 'i4CPSgyCxaE9zwXZhVpJ'
plex = PlexServer(baseurl, token)
import discord


def _update():

    sessions = plex.sessions()
    if sessions == []:

        return
    elif sessions[0].TYPE == 'movie':
        sessions = sessions[0]
        title = sessions.title
    else:
        sessions = sessions[0]
        title = sessions.grandparentTitle + ' - ' + sessions.parentTitle + ' - ' + sessions.title
    photo = 'http://43.134.198.180:5244/d/GoogleDrive/%E5%85%AC%E7%94%A8/123.jpg'
    # viewOffset = sessions.viewOffset // 1000
    # second = viewOffset % 60
    # minute = (viewOffset - viewOffset // 3600 * 3600) // 60
    # hour = viewOffset // 3600
    # remaining_duration = (float(sessions.duration) - viewOffset) / 60
    # endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sessions.viewOffset + time.time()))
    # endtime = sessions.viewOffset + time.time()
    return title, photo



intents = discord.Intents.default()
intents.message_content = True
result = _update()

client = discord.Client(intents=intents)

aaa = discord.Activity(application_id = 1049283090255712276,name = result[0])
client.activity = aaa
client.run('MTA0OTI4MzA5MDI1NTcxMjI3Ng.GisHIV.iol_Heiodsxt1eeZChQrT9AYT3dx9S_korq8EA')

time.sleep(15)

from pypresence import Presence
import time
from plexapi.server import PlexServer
from threading import Timer
import re
from moviebotapi.core.models import MediaType
from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
SERVER_URL = 'http://192.168.50.190:1329'
ACCESS_KEY = '123524'
server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))

baseurl = 'http://192.168.50.190:32400'
token = 'i4CPSgyCxaE9zwXZhVpJ'
plex = PlexServer(baseurl, token)
app = Presence("1049283090255712276")
app.connect()

def _update():
    sessions = plex.sessions()
    photo1 = 'http://43.134.198.180:5244/d/GoogleDrive/%E5%85%AC%E7%94%A8/123.jpg'
    r = re.compile(r'(?<=\<Guid:tmdb://)\d+\.?\d*')
    if sessions == []:
        app.update(state="摸鱼ing....",large_image = photo1)
        return
    elif sessions[0].TYPE == 'movie':
        sessions = sessions[0]
        tmdbid = str(r.findall(str(sessions.guids))).strip('[]').strip("'")
        meta = server.tmdb.get(MediaType.Movie, int(tmdbid))
        title = sessions.title
    else:
        sessions = sessions[0]
        tmdbid = str(r.findall(str(sessions.guids))).strip('[]').strip("'")
        meta = server.tmdb.get(MediaType.TV, int(tmdbid))
        title = sessions.grandparentTitle + ' - ' + sessions.parentTitle + ' - ' + sessions.title

    if meta == None:
        photo = photo1
    else:
        photo = 'https://www.themoviedb.org/t/p/w300_and_h450_bestv2' + meta.poster_path
    beensee_time = sessions.viewOffset // 1000
    duration = sessions.duration // 1000
    if sessions.lastViewedAt == None:
        endtime = None
    else:
        begain_time = time.mktime(time.strptime(str(sessions.lastViewedAt), '%Y-%m-%d %H:%M:%S'))
        endtime = begain_time + duration - beensee_time

    app.update(state=title, details="正在播放",
               large_image=photo, large_text="MovieBot",
               small_image=photo1, small_text="Plex",
               end=endtime)
def loop_func(func, second):
    print('开始轮询')
    while True:
        timer = Timer(second, func)
        timer.start()
        timer.join()

loop_func(_update, 1)
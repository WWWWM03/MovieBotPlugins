from pypresence import Presence
import time
from plexapi.server import PlexServer
from threading import Timer


baseurl = 'http://192.168.50.190:32400'
token = 'i4CPSgyCxaE9zwXZhVpJ'
plex = PlexServer(baseurl, token)
app = Presence("1049283090255712276")
app.connect()


def _update():
    sessions = plex.sessions()
    if sessions == []:
        app.update(state="摸鱼ing....", large_image="plex")
        return
    elif sessions[0].TAG == 'Movie':
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
    # remaining_duration = round(float(sessions.duration) - viewOffset / 60, 0)
    # endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sessions.viewOffset))
    # endtime = time.mktime(time.strptime(str(endtime), '%Y-%m-%d %H:%M:%S'))
    app.update(state=title, details="正在播放",
               large_image=photo, large_text="MovieBot",
               small_image="moviebot", small_text="MovieBot"
               )

def loop_func(func, second):
    while True:
        timer = Timer(second, func)
        timer.start()
        timer.join()

loop_func(_update, 1)
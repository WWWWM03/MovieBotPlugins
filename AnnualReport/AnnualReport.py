from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math
from plexapi.server import PlexServer
import re
import requests
import datetime
from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from moviebotapi.core.models import MediaType
from moviebotapi.subscribe import SubStatus

# '''PLEX配置'''
# baseurl = 'http://192.168.50.190:32400'
# token = 'i4CPSgyCxaE9zwXZhVpJ'
# plex = PlexServer(baseurl, token)

'''Mbot配置'''
SERVER_URL = 'http://192.168.50.190:1329'
ACCESS_KEY = '123524'
server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))

def download_img(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        response = requests.get(SERVER_URL + result)
        filename = result.split('/')[-1]
        # 将图片数据保存到本地
        with open(f'{filename}', 'wb') as f:
            f.write(response.content)
        return result

    return wrapper


class AnnualReport:
    def __init__(self):
        self.user_nickname = self.user_nickname()
        self.user_img = self.user_img()
        # self.mr_logo = self.mr_logo()
        self.user_gmt_create = self.user_gmt_create()

    def user_nickname(self):
        return server.user.get(1).nickname

    @download_img
    def user_img(self):
        return server.user.get(1).avatar

    # @download_img
    # def mr_logo(self):
    #     return '/favicon.ico'

    def user_gmt_create(self):
        return server.user.get(1).gmt_create

    def mbot_subscribe(self):
        '获取mbot订阅信息'
        mbot_subscribe = []
        mbotlist = server.subscribe.list()
        mbotlist.reverse()
        movie = 0
        episode = 0
        for meta in mbotlist:
            if meta.gmt_create.year == 2022 and meta.poster_path != None:
                mbot_subscribe.append(f'{SERVER_URL}{meta.poster_path}')
                if meta.media_type == MediaType.Movie:
                    movie += 1
                else:
                    episode += 1
            else:
                pass
        return mbot_subscribe ,movie ,episode

    def get_plex_iswatched(self):
        '获取plex上已观看的电影和电视剧的海报，返回thumbUrl'
        tmdbidlist = []
        unwatched = []
        thumburl = []
        moviecount = 0
        episodecount = 0
        for video in plex.library.search():
            if video.TAG == 'Directory' and video.TYPE == 'show' or video.TAG == 'Video' and video.TYPE == 'movie':
                if video.isPlayed and video.title and video.type and video.guids:
                    if video.TYPE == 'show':
                        episodecount += 1
                    else:
                        moviecount += 1
                    dict = {}
                    r = re.compile(r'(?<=\<Guid:tmdb://)\d+\.?\d*')
                    # print(dict)
                    thumburl.append(video.thumbUrl)
                    tmdbidlist.append(dict)
                    unwatched.append(video)
                else:
                    pass
            else:
                pass
        return thumburl ,moviecount ,episodecount

    def download_img(self, thumburl):
        '下载图像'
        # 遍历图片 URL 列表
        for url in thumburl:
            # 下载图片数据
            response = requests.get(url)
            # 获取图片名称
            filename = url.split('/')[-1]
            # 将图片数据保存到本地
            with open(f'./image/{filename}.jpg', 'wb') as f:
                f.write(response.content)

    def report_image(self, image_list: list):
        import io
        '获取image_list列表中每一个路径下所有图片并用Image.open方法写入列表images'
        images = []
        cia = 0
        for path in image_list:
            response = requests.get(path)
            binary_data = response.content
            try:
                images.append(Image.open(io.BytesIO(binary_data)))
                cia += 1
                print(cia)
            except:
                pass

        # 计算每张图片的宽度和高度
        widths, heights = zip(*(i.size for i in images))

        total_width = 1000
        www = 200
        hhh = 300

        max_height = math.ceil(len(heights) / 7) * hhh * 2

        # 创建一张新图片
        result = Image.new('RGBA', (total_width, max_height), color=(18, 12, 10))
        for count in range(0, len(images), 7):
            sublist = images[count:count + 7]
            rownum = count // 7
            if rownum % 2 == 0:
                '左对齐'
                x_offset = www * 2
                # result.paste(sublist[-1].resize((www * 2, hhh * 2)), (0, i // 7 * hhh * 2))
                for i in range(len(sublist)):
                    # print(i)
                    if 0 <= i < 3:
                        if x_offset == total_width:
                            x_offset = www * 2
                        if rownum == 0:
                            y_offset = rownum * hhh
                        else:
                            y_offset = rownum * hhh * 2
                        result.paste(sublist[i].resize((www, hhh)), (x_offset, y_offset))
                        x_offset += www
                    elif 6 > i >= 3:
                        if x_offset == total_width:
                            x_offset = www * 2
                        if rownum == 0:
                            y_offset = rownum * hhh + hhh
                        else:
                            y_offset = rownum * hhh * 2 + hhh
                        result.paste(sublist[i].resize((www, hhh)), (x_offset, y_offset))
                        x_offset += www
                    else:
                        result.paste(sublist[i].resize((www * 2, hhh * 2)), (0, count // 7 * hhh * 2))
                        pass
            else:
                '右对齐'
                x_offset = 0
                # result.paste(sublist[-1].resize((www * 2, hhh * 2)), (hhh * 2, i // 7 * hhh * 2))
                for i in range(len(sublist)):
                    if 0 <= i < 3:
                        if x_offset == hhh * 2:
                            x_offset = 0
                        if rownum == 0:
                            y_offset = rownum * hhh
                        else:
                            y_offset = rownum * hhh * 2
                        result.paste(sublist[i].resize((www, hhh)), (x_offset, y_offset))
                        x_offset += www
                    elif 6 > i >= 3:
                        if x_offset == hhh * 2:
                            x_offset = 0
                        if rownum == 0:
                            y_offset = rownum * hhh + hhh
                        else:
                            y_offset = rownum * hhh * 2 + hhh
                        result.paste(sublist[i].resize((www, hhh)), (x_offset, y_offset))
                        x_offset += www
                    else:
                        result.paste(sublist[i].resize((www * 2, hhh * 2)), (hhh * 2, count // 7 * hhh * 2))
                        pass

        # 保存图片海报墙
        # self.circle_corner(result).save('poster.png')
        return self.circle_corner(result)
        # result.save('poster.png')

    def circle_corner(self, img, radii=30, two_corner=True, save_path=None):

        # 白色区域透明可见，黑色区域不可见
        circle = Image.new('L', (radii * 2, radii * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)

        img = img.convert("RGBA")
        w, h = img.size

        # 画角
        alpha = Image.new('L', img.size, 255)
        alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
        alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
        alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
        alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角

        img.putalpha(alpha)
        if save_path:
            img.save(save_path, 'PNG', quality=100)

        return img

    def final_report(self, image_list: list, moviecount: int = None, episodcount: int = None):
        '''计算self.user_gmt_create距离现在过去了多少天'''
        # 获取当前时间
        now = datetime.datetime.now()
        # 将字符串转换为时间格式
        gmt_create = datetime.datetime.strptime(str(self.user_gmt_create), '%Y-%m-%d %H:%M:%S')
        # 计算时间差
        delta = now - gmt_create
        # 获取时间差的天数
        days = delta.days

        '最终海报墙'
        # image = Image.open('poster.png')
        image = self.report_image(image_list)
        '获取imagesize的宽和高并同时相加100'
        image_width, image_height = image.size
        width = image_width + 80
        height = image_height + 1200

        result = Image.new('RGBA', (width, height), color=(18, 12, 10))
        top = Image.open('top.png')
        bottom = Image.open('bottom.png')
        avatar = Image.open('avatar.jpg')

        # 创建画笔
        draw = ImageDraw.Draw(result)

        # 设置文本样式
        bold_font = ImageFont.truetype('ALIBABA-Font-Bold.otf', 100)
        regular_font = ImageFont.truetype('ALIBABA-Font-Regular.otf', 100)

        result.paste(avatar.resize((150, 150)), (700, 630))
        result.paste(top, (0, 0), mask=top)
        result.paste(image, (40, 1100), mask=image)
        result.paste(bottom, (0, 400 + image_height), mask=bottom)

        # 在图像上绘制文本
        # 电影观看数量
        # draw.text((440, 920), f'{moviecount}', font=bold_font, fill=(245, 214, 174),align='center')
        # # 剧集观看数量
        # draw.text((745, 920), f'{episodcount}', font=bold_font, fill=(245, 214, 174),align='center')

        if moviecount < 10:
            draw.text((490, 920), f'0{moviecount}', font=bold_font, fill=(245, 214, 174), align='center')
        elif 9 < moviecount < 100:
            draw.text((490, 920), f'{moviecount}', font=bold_font, fill=(245, 214, 174), align='center')
        elif 99 < moviecount < 1000:
            draw.text((440, 920), f'{moviecount}', font=bold_font, fill=(245, 214, 174), align='center')
        else:
            draw.text((440, 920), f'999', font=bold_font, fill=(245, 214, 174), align='center')

        if episodcount < 10:
            draw.text((795, 920), f'0{episodcount}', font=bold_font, fill=(245, 214, 174), align='center')
        elif 9 < episodcount < 100:
            draw.text((795, 920), f'{episodcount}', font=bold_font, fill=(245, 214, 174), align='center')
        elif 99 < episodcount < 1000:
            draw.text((745, 920), f'{episodcount}', font=bold_font, fill=(245, 214, 174), align='center')
        else:
            draw.text((745, 920), f'999', font=bold_font, fill=(245, 214, 174), align='center')


        # 年度
        draw.text((490, 795), f'2022', font=regular_font, fill=(209, 183, 149))
        # # 昵称
        # draw.text((490, 795), f'尊敬的{self.user_nickname()}', font=regular_font, fill=(209, 183, 149))

        jpg = result.convert('RGB')
        # 保存图像
        jpg.save('AnnualReport.jpg')

    def run_report(self, data: list, moviecount: int, episodcount: int):
        # self.get_plex_iswatched()  # 获取已观看的影视剧
        # self.download_img(AnnualReport().get_plex_iswatched() )  # 下载Plex已观看图片至本地
        # self.report_image(data)  # 生成海报墙
        self.final_report(data, moviecount, episodcount)  # 包装海报，生成最终海报墙

image_list ,moviecount ,episodecount= AnnualReport().mbot_subscribe()
AnnualReport().run_report(data=image_list, moviecount=moviecount, episodcount=episodecount)
'''
    data: 带有海报图片完整路径的列表
    moviecount: 电影观看数量
    episodcount: 剧集观看数量
    '''

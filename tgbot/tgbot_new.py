# !/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.


from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from moviebotapi.subscribe import SubStatus
SERVER_URL = ''
ACCESS_KEY = ''
server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))
DEVELOPER_CHAT_ID = 5414216757

#
# from typing import Dict, Any
# from mbot.openapi import mbot_api
# from mbot.core.plugins import PluginContext, PluginMeta
# from mbot.core.params import ArgSchema, ArgType
# from mbot.core.plugins import PluginContext, plugin, PluginCommandContext, PluginCommandResponse, PluginMeta
# from mbot.core.event.models import EventType
# from moviebotapi.subscribe import SubStatus
# from moviebotapi import MovieBotServer
#
# server = mbot_api
import html
import json
import traceback

import math
import urllib
from moviebotapi.core.models import MediaType
from moviebotapi.douban import DoubanRankingType
from enum import Enum
import asyncio
import threading
import time
from telegram.constants import MessageAttachmentType, ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import ForceReply, Update
import logging

from telegram import (
    Bot,
    GameHighScore,
    InputMedia,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    LabeledPrice,
    MessageId,
    ReplyKeyboardMarkup
)

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
_LOGGER = logging.getLogger(__name__)




class TgBotSub:

    def __init__(self):
        self.TGbotTOKEN = 'kxrijBGeiM'
        # self.chatid_list = ''.split(",")
        self.chatid_list = ['']
        self.proxy = None

    def set_config(self, TGbotTOKEN: str, chatid_list: str, proxy: str):
        self.TGbotTOKEN = TGbotTOKEN
        self.chatid_list = chatid_list.split(",") if chatid_list else None
        self.proxy = proxy if proxy else None

    def download_image(self, photo_url):
        f = open('../../tgbot/out.jpg', 'wb')
        f.write(urllib.request.urlopen(photo_url).read())
        f.close()
        photo =  open('../../tgbot/out.jpg', 'rb')
        return photo

    def inlinekeyboard(self, keyboardlist: list, step: int):
        '''内联键盘格式化'''
        _LOGGER.info('inlinekeyboard')
        keyboard = []
        for i in keyboardlist:
            aaa = InlineKeyboardButton(i[0], callback_data=i[1])
            keyboard.append(aaa)
        keyboard_final = [keyboard[i:i + step] for i in range(0, len(keyboard), step)]

        return keyboard_final

    def strB2Q(self, ustring):
        """半角转全角"""
        rstring = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code == 32:  # 半角空格直接转化
                inside_code = 12288
            elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
                inside_code += 65248
            rstring += chr(inside_code)
        return rstring

    def douban_search(self, media_name: str, markup_len: int, markup_max):
        '''豆瓣搜索'''
        _LOGGER.info('douban_search')
        douban_result_list = server.douban.search(media_name)

        if douban_result_list == []:
            return False
        # if len(douban_result_list) >= 10:
        #     douban_result_list = douban_result_list[:10]

        markup_len_max = math.ceil(len(douban_result_list) / 5)
        _LOGGER.info(f'第{markup_len}页')
        douban_result_list = douban_result_list[markup_len * 5 - 5:markup_len * 5]
        # markup_len = 1
        #
        # if markup_len == 1:
        #     _LOGGER.info('第一页')
        #     douban_result_list = douban_result_list[markup_len * 5 - 5:markup_len * 5]
        # elif 1 < markup_len < markup_len_max:
        #     _LOGGER.info('中间页')
        #     douban_result_list = douban_result_list[markup_len * 5 - 5:markup_len * 5]
        # elif markup_len == markup_len_max:
        #     _LOGGER.info('最后一页')
        #     douban_result_list = douban_result_list[markup_len * 5 - 5:markup_len * 5]

        mr_caption = []
        mr_idlist = []
        mr_poster_path = []
        num = 1
        idlist = []
        duiqi1 = []
        for i in douban_result_list:
            id = str(i.id)
            cn_name = i.cn_name.upper().replace("1", "１").replace("2", "２").replace("3", "３").replace("4", "４").replace("5", "５").replace("6", "６").replace("7", "７").replace("8", "８").replace("9", "９").replace("0", "０")

            if len(cn_name) > 11:
                cn_name = cn_name[:11] + '⋯'
            rating = str(i.rating)
            poster_path = i.poster_url
            url = i.url
            status = i.status
            if rating == 'nan':
                rating = f'⭐️0.0'
            else:
                rating = f'⭐️{str(rating)}'
            if status == 0:
                status = '🛎'
            elif status == 1:
                status = '✅'
            elif status == 2:
                status = '🔁'
            else:
                status = '📥'
            # set_num = "%02d" % num
            cn_name = self.strB2Q(cn_name)
            caption = self.algin(status + cn_name , 1) + rating
            mr_poster_path.append(poster_path)
            idlist.append(id)
            mr_idlist.append(f'details-{id}-{media_name}-{markup_len}-{markup_max}')
            duiqi1.append(caption)
            num += 1

        # print(duiqi1)
        mr_caption_final = ''.join(
            str(i) for i in mr_caption) + '\n📥未订阅 | ✔已完成' + '\n🛎️订阅中 | 🔁洗版中' +  '\n\n⬇⬇⬇请点对应的序号⬇⬇⬇'
        mr_keybord = []
        mr_count = []
        y = 1
        for i in mr_idlist:
            mr_count.append(str(y))
            mr_keybord.append(str(i))
            y += 1

        test = []
        for i in zip(duiqi1, mr_keybord):
            test.append(i)

        markup = self.inlinekeyboard(keyboardlist=test, step=1)
        markup.append(self.page(id,media_name,markup_len,markup_len_max))
        markup.append([InlineKeyboardButton('🔚关闭', callback_data=f'delete-1-')])

        return mr_caption_final, mr_idlist[0].split("-")[1] , markup ,mr_poster_path[0]

    def page(self,id,media_name,current_page,max_page):

        _next = "下一页 >"
        _previous = "< 上一页"

        if current_page == 1:
            _LOGGER.info('已是最前')
            _previous  = "已是最前"
        elif current_page == max_page:
            _LOGGER.info('已是最后')
            _next = "已是最后"

        markup =  [InlineKeyboardButton(_previous, callback_data=f'callback_page-{id}-{media_name}-{current_page-1}-{max_page}'),
                   InlineKeyboardButton(_next, callback_data=f'callback_page-{id}-{media_name}-{current_page+1}-{max_page}')]
        return markup

    async def callback_page(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        _LOGGER.info('callback_page')
        await query.answer()


    def douban_get(self, media_id: str):
        _LOGGER.info('douban_get')
        doubandetils = server.douban.get(media_id)
        cn_name = doubandetils.cn_name
        rating = str(doubandetils.rating)
        intro = doubandetils.intro
        release_year = doubandetils.release_year
        doubanid = doubandetils.id
        cover_image = doubandetils.cover_image
        actor = doubandetils.actor
        media_type = str(doubandetils.media_type)
        premiere_date = doubandetils.premiere_date  # 上映时间
        season_index = doubandetils.season_index  # 季
        trailer_video_url = str(doubandetils.trailer_video_url)  # 预告片
        genres = doubandetils.genres
        episode_count = doubandetils.episode_count  # 集
        if rating == '0.0':
            rating = f' | ⭐0.0'
        else:
            rating = f' | ⭐{rating}'

        if len(actor) >= 3:
            actor = doubandetils.actor[0:4]
        if not actor:
            actor = ''
        else:
            actor = '演员：#' + ' #'.join(i.name for i in actor) + '\n'

        if not genres:
            genres = ''
        else:
            genres = '流派：#' + ' #'.join(i for i in doubandetils.genres) + '\n'

        if len(intro) >= 200:
            intro = f'简介：{intro[0:200]}......'
        elif len(intro) == 0:
            intro = ''

        if media_type == 'MediaType.Movie':
            caption_button = f'🎬*{cn_name}*{rating}\n\n上映时间：{premiere_date}\n{actor}{genres}{intro}'
        else:
            caption_button = f'📺*{cn_name}*{rating}\n\n第{season_index}季 共{episode_count}集\n上映时间：{premiere_date}\n{actor}{genres}{intro}'

        # _LOGGER.info(f"{self.caption_button} ")


        return caption_button , '1',cover_image ,media_type


    async def menu_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = str(update.message.chat_id)

        if self.chatid_list[0] == '':
            await update.message.reply_text(
                f"当前用户chat_id：{chat_id} ，Movie—Bot插件未设置chat_id，所有用户都可以访问！！")
            _LOGGER.info(f"当前用户chat_id：{chat_id} ，Movie—Bot插件未设置chat_id")
        elif chat_id not in self.chatid_list:
            await update.message.reply_text(f"UserID: {chat_id}\n你未经授权！不可使用此机器人")
            _LOGGER.info(f"chat_id：{chat_id} , 未经授权")
            return
        else:
            await update.message.reply_text(f"正在搜索 {update.message.text}")
            _LOGGER.info(f"chat_id：{chat_id} , 正在搜索 {update.message.text}")

        _LOGGER.info(f"menu_list")

        if self.douban_search(update.message.text, 1, 1):
            result = self.douban_search(update.message.text, 1, 1)
        else:
            _LOGGER.info(f"{update.message.text} 搜索结果为空")
            await update.message.reply_text(f"{update.message.text} 搜索结果为空")
            return
        result_details = self.douban_get(result[1])

        image = self.get_x_details(result[1], str(result_details[3]))

        if image == None or image.background_url == None:
            image = result[3]
        else:
            image = image.background_url


        sub = [InlineKeyboardButton('🛎️订阅', callback_data=f'sub-{result[1]}-{update.message.text}')]
        result[2].insert(0, sub)
        reply_markup1 = InlineKeyboardMarkup(result[2])

        try:
            _LOGGER.info('url')
            await update.message.reply_photo(
                reply_markup=reply_markup1,
                photo=image,
                caption=result_details[0],
                parse_mode=ParseMode.MARKDOWN)
        except:
            _LOGGER.info('本地')
            image1 = self.download_image(image)
            await update.message.reply_photo(
                reply_markup=reply_markup1,
                photo=image1,
                caption=result_details[0],
                parse_mode=ParseMode.MARKDOWN)



    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        _LOGGER.info('button')
        doubanid = query.data.split('-')[1]
        media_name = query.data.split('-')[2]
        try:
            page = int(query.data.split('-')[3])
        except:
            page = 1

        if page < 1:
            page = 1
            await query.answer()
            return
        elif page > int(query.data.split('-')[4]):
            page = int(query.data.split('-')[4])
            await query.answer()
            return

        result = self.douban_search(media_name,page,query.data.split('-')[4])
        result_details = self.douban_get(doubanid)

        image = self.get_x_details(doubanid, str(result_details[3]))

        # if result_details[2] != '':

        if image == None or image.background_url == None:
            image = result_details[2]
        else:
            image = image.background_url


        sub = [InlineKeyboardButton('🛎️订阅', callback_data=f'sub-{doubanid}-{media_name}-1')]
        result[2].insert(0,sub)
        reply_markup1 = InlineKeyboardMarkup(result[2])
        # if result[1] == []:
        #     _LOGGER.info(f"{update.message.text} 搜索结果为空")
        #     await update.message.reply_text(f"{update.message.text} 搜索结果为空")
        #     return
        try:
            _LOGGER.info('url')
            await query.edit_message_media(reply_markup=reply_markup1,
                                           media=InputMediaPhoto(
                                               media=image,
                                               caption=result_details[0],
                                               parse_mode=ParseMode.MARKDOWN))
        except:
            _LOGGER.info('本地')
            image1 = self.download_image(image)
            await query.edit_message_media(reply_markup=reply_markup1,
                                           media=InputMediaPhoto(
                                               media=image1,
                                               caption=result_details[0],
                                               parse_mode=ParseMode.MARKDOWN))


        await query.answer()




    def get_x_details(self, doubanid: int, type: str):
        if type == 'MediaType.Movie':
            return server.meta.get_media_by_douban(MediaType.Movie, doubanid)
        else:
            return server.meta.get_media_by_douban(MediaType.TV, doubanid)


    def is_Chinese(self,ch):
        '''如果ch包含中文全角字符，返回True'''
        if '\u4e00' <= ch <= '\u9fff' or '\uFF21' <= ch <= '\uFF3A' or ch in ["⋯","，","　","１","２","３","４","５","６","７","８","９","０","《","》","：","·"]:
            return True
        return False



    def algin(self,title_key, max_english):
        chinese_count = 0
        english_count = 0
        for j in str(title_key):
            if self.is_Chinese(j):
                chinese_count = chinese_count + 1
            else:
                english_count = english_count + 1

        temp = max_english - english_count
        while temp > 0:
            title_key = title_key + ' '
            temp = temp - 1
        title_key = title_key.ljust(14, chr(12288))
        print(title_key + '-')
        return title_key

    def pad_len(self,string, length):
        return length - len(string.encode('GBK')) + len(string)

    async def error_handler(self,update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        _LOGGER.error(msg=f"处理更新时出现异常：{context.error}",exc_info=context.error)

    def ranking_list(self):
        count = 1
        ranking_id_list = []
        ranking_name_list = []
        ranking_callback = []
        ranking_caption = []
        for list in DoubanRankingType:
            ranking_name_list.append(list.value)
            ranking_id_list.append(list.name)
            ranking_callback.append(f'rank-{list.name}')
            set_count = "%02d" % count
            ranking_caption.append(f'`{set_count}`.{list.value}\n')
            count += 1
        ranking_caption_final = ''.join(
            str(i) for i in ranking_caption) + '\n\n⬇⬇⬇请点对应的序号⬇⬇⬇'
        callback_keybord = []
        callback_count = []
        y = 1
        for i in ranking_id_list:
            callback_count.append(str(y))
            callback_keybord.append(str(i))
            y += 1
        callback_keybord_final = []
        callback_count1 = 1
        for y in ranking_callback:
            aaa = InlineKeyboardButton(callback_count1, callback_data=y)
            callback_keybord_final.append(aaa)
            callback_count1 += 1
        step = 5
        a = callback_keybord_final
        b = [a[i:i + step] for i in range(0, len(a), step)]
        b.append([InlineKeyboardButton('🔚关闭', callback_data=f'delete-1-')])
        keyboard = b
        ranking_reply_markup1 = InlineKeyboardMarkup(keyboard)
        return ranking_caption_final, ranking_reply_markup1




###### 回复



    async def backtomenu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        doubanid = query.data.split('-')[1]


        #
        # result = self.douban_search(self.inputmessage)
        #
        # await query.edit_message_media(
        #     reply_markup=result[2],
        #     media=InputMediaPhoto(
        #         media=result[1][0],
        #         caption=result[0],
        #         parse_mode=ParseMode.MARKDOWN
        #     )
        # )
        await query.answer()

    async def doubansub(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
        x = query.data.split('-')
        server.subscribe.sub_by_douban(x[1])
        backbutton = InlineKeyboardMarkup([
            [InlineKeyboardButton('🔙返回', callback_data=f'back-{x[1]}-{x[2]}-1-1')],
            [InlineKeyboardButton('🔚关闭', callback_data=f'delete-1-')]
        ])
        await query.edit_message_caption(f" 已提交订阅 ✔", reply_markup=backbutton)
        await query.answer()

    async def deletekeyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
        await query.delete_message()
        await query.answer()

    async def ranking_list_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        result = self.ranking_list()
        await update.message.reply_text(text=result[0], reply_markup=result[1], parse_mode=ParseMode.MARKDOWN)

    async def get_ranking_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        rank_id = query.data.split("-")[1]
        rank_name = DoubanRankingType[rank_id].value
        ranking_list_result = server.douban.list_ranking(DoubanRankingType[rank_id])
        count = 1
        ranking_list_result_caption = []
        ranking_list_caption_final = []
        for i in ranking_list_result:
            cn_name = i.cn_name
            comment = i.comment
            desc = i.desc
            media_type = i.media_type
            poster_path = i.poster_path
            rank = i.rank
            rating = i.rating
            if rating == 'nan':
                rating = f'⭐️0.0'
            else:
                rating = f'⭐️{rating}'
            release_year = i.release_year
            url = i.url
            set_count = "%02d" % count
            ranking_list_result_caption.append(f'`{set_count}`. `{rating}`|[{cn_name}]({url})\n')
            count += 1
        ranking_list_caption_final = rank_name + "\n" + ''.join(
            str(i) for i in ranking_list_result_caption) + '\n\n⬇⬇⬇请点对应的序号⬇⬇⬇'

        keyboard1 = [
            [
                InlineKeyboardButton('🔙返回', callback_data=f'back-1-'),
            ],
            [
                InlineKeyboardButton('🔚关闭', callback_data=f'delete-1-')
            ]
        ]
        reply_markup_doubansub = InlineKeyboardMarkup(keyboard1)

        await query.message.edit_text(text=ranking_list_caption_final,
                                      reply_markup=reply_markup_doubansub,
                                      parse_mode=ParseMode.MARKDOWN)
        await query.answer()
        # await context.bot.send_message(chat_id=5414216757, text='123')

        # result = self.ranking_list()
        # await update.message.reply_text(text=result[0], reply_markup=result[1], parse_mode=ParseMode.MARKDOWN)

    # async def ranking_list_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #     query = update.callback_query
    #     result = self.ranking_list()
    #     await query.message.reply_text(text= result[0],
    #                                    reply_markup=result[1])
    #     await query.answer()

    # server.douban.list_ranking(DoubanRankingType.movie_real_time_hotest)

    def start_bot(self) -> None:
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            application = Application.builder().token(self.TGbotTOKEN).proxy_url(self.proxy).get_updates_proxy_url(
                self.proxy).build()
            # application.add_handler(CommandHandler("rebootmr", rebootmr))
            # application.add_handler(CommandHandler("help", help_command))
            application.add_handler(CallbackQueryHandler(self.button, pattern="^back"))
            application.add_handler(CallbackQueryHandler(self.button, pattern="^callback_page"))
            application.add_handler(CallbackQueryHandler(self.deletekeyboard, pattern="^delete"))
            application.add_handler(CallbackQueryHandler(self.get_ranking_list, pattern="^rank"))
            application.add_handler(CallbackQueryHandler(self.button, pattern="^details"))
            # application.add_handler(CallbackQueryHandler(self.ranking_list_menu, pattern="^rank"))
            application.add_handler(CallbackQueryHandler(self.doubansub, pattern="^sub"))
            application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Text(['榜单', '吃了么']), self.menu_list))
            application.add_handler(MessageHandler(filters.Text(['榜单']), self.ranking_list_menu))
            application.add_error_handler(self.error_handler)
            application.run_polling(stop_signals=None, close_loop=False)
        except Exception as e:
            _LOGGER.info(f"连接超时，请检查网络。错误： {e}")
            return
        finally:
            loop.close()
            pass


TgBotSub().start_bot()

# !/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.


import asyncio
import threading
import time

from typing import Dict, Any
from mbot.openapi import mbot_api
from mbot.core.plugins import PluginContext, PluginMeta
from mbot.core.params import ArgSchema, ArgType
from mbot.core.plugins import PluginContext, plugin, PluginCommandContext, PluginCommandResponse, PluginMeta
from mbot.core.event.models import EventType
from moviebotapi.subscribe import SubStatus
from moviebotapi import MovieBotServer

server = mbot_api

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
        self.TGbotTOKEN = None
        self.chatid_list = []
        self.proxy = None

    def set_config(self, TGbotTOKEN: str, chatid_list: str ,proxy: str ):
        self.TGbotTOKEN = TGbotTOKEN
        self.chatid_list = chatid_list.split(",") if chatid_list.split(",") else None
        self.proxy = proxy if proxy else None

    def douban_search(self, media_name: str):
        douban_result_list = server.douban.search(media_name)
        if len(douban_result_list) >=10:
            douban_result_list = douban_result_list[:10]
        mr_caption = []
        mr_idlist = []
        mr_poster_path = []
        num = 1
        for i in douban_result_list:
            id = str(i.id)
            cn_name = i.cn_name
            rating = str(i.rating)
            poster_path = i.poster_url
            url = i.url
            status = i.status
            if rating == 'nan':
                rating = f'⭐️0.0'
            else:
                rating = f'⭐️{rating}'
            if status == 0:
                status = '🛎️'
            elif status == 1:
                status = '✔'
            elif status == 2:
                status = '🔁'
            else:
                status = '📥'
            set_num = "%02d" % num
            caption = f'`{set_num}`.{status}|`{rating}`|[{cn_name}]({url})\n'
            mr_caption.append(caption)
            mr_poster_path.append(poster_path)
            mr_idlist.append(f'{id}-{num}')
            # _LOGGER.info(f'{id}-{num}')
            num += 1
        mr_caption_final = ''.join(str(i) for i in mr_caption) + '\n\n📥未订阅 | ✔已完成' + '\n\n🛎️订阅中 | 🔁洗版中' + '\n\n️️️️请点对应的序号️️️️'

        mr_keybord = []
        mr_count = []
        y = 1
        for i in mr_idlist:
            mr_count.append(str(y))
            mr_keybord.append(str(i))
            y += 1
        mr_keybord_final = []
        count1 = 1
        for y in mr_keybord:
            aaa = InlineKeyboardButton(count1, callback_data=y)
            mr_keybord_final.append(aaa)
            count1 += 1
        step = 5
        a = mr_keybord_final
        b = [a[i:i + step] for i in range(0, len(a), step)]
        b.append([InlineKeyboardButton('关闭', callback_data=f'delete-1-')])
        keyboard = b
        reply_markup1 = InlineKeyboardMarkup(keyboard)
        # _LOGGER.info(f"{media_name} 返回搜索结果：\n{mr_caption_final}")

        return mr_caption_final, mr_poster_path, reply_markup1

    def douban_get(self, media_id: str):
        doubandetils = server.douban.get(media_id)
        cn_name = doubandetils.cn_name
        self.cn_name = cn_name
        rating = str(doubandetils.rating)
        intro = doubandetils.intro
        release_year = doubandetils.release_year
        doubanid = doubandetils.id
        self.cover_image = doubandetils.cover_image
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

        if len(intro) >= 100:
            intro = f'{intro[0:100]}......'
        elif len(intro) == 0:
            intro = '暂无简介'

        if media_type == 'MediaType.Movie':
            self.caption_button = f'片名：*{cn_name}*{rating}\n类型：{media_type.split(".")[1]}\n上映时间：{premiere_date}\n{actor}{genres}简介：{intro}'
        else:
            self.caption_button = f'剧名：*{cn_name}*{rating}\n类型：{media_type.split(".")[1]}\n第{season_index}季 共{episode_count}集\n上映时间：{premiere_date}\n{actor}{genres}简介：{intro}'

        # _LOGGER.info(f"{self.caption_button} ")
        keyboard = [
            [
                InlineKeyboardButton('订阅', callback_data=f'sub-{doubanid}-'),
                InlineKeyboardButton('返回', callback_data=f'back-{doubanid}-'),
            ],
            [
                InlineKeyboardButton('关闭', callback_data=f'delete-{doubanid}-')
            ]
        ]
        self.reply_markup_button = InlineKeyboardMarkup(keyboard)



        keyboard1 = [
            [
                InlineKeyboardButton('返回', callback_data=f'back-{doubanid}-'),
            ],
            [
                InlineKeyboardButton('关闭', callback_data=f'delete-{doubanid}-')
            ]
        ]
        self.reply_markup_doubansub = InlineKeyboardMarkup(keyboard1)

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
            await update.message.reply_text(f"正在搜索 {update.message.text} 中.....")
            _LOGGER.info(f"chat_id：{chat_id} , 正在搜索 {update.message.text} 中 ")
        # _LOGGER.info(f"menu_list")
        self.inputmessage = update.message.text
        result = self.douban_search(update.message.text)
        if result[1] == []:
            _LOGGER.info(f"{update.message.text} 搜索结果为空")
            await update.message.reply_text(f"{update.message.text} 搜索结果为空")
            return
        await update.message.reply_photo(
            reply_markup=result[2],
            photo=result[1][0],
            caption=result[0],
            parse_mode=ParseMode.MARKDOWN
        )

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        doubanid = query.data.split('-')[0]
        self.num = query.data.split('-')[1]
        # _LOGGER.info(f"num : {self.num} ")
        self.douban_get(doubanid)
        await query.edit_message_media(reply_markup=self.reply_markup_button,
                                       media=InputMediaPhoto(
                                           media=self.cover_image,
                                           caption=self.caption_button,
                                           parse_mode=ParseMode.MARKDOWN
                                       )
                                       )
        await query.answer()

    async def backtomenu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        self.num = query.data.split('-')[2]
        #
        result = self.douban_search(self.inputmessage)

        await query.edit_message_media(
            reply_markup=result[2],
            media=InputMediaPhoto(
                media=result[1][0],
                caption=result[0],
                parse_mode=ParseMode.MARKDOWN
            )
        )
        await query.answer()

    async def doubansub(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        x = query.data.split('-')
        # _LOGGER.info(f"订阅")

        server.subscribe.sub_by_douban(x[1])
        await query.edit_message_caption(f"{self.cn_name} 已提交订阅 ✔",reply_markup=self.reply_markup_doubansub)
        # await query.message.reply_text(f"{self.cn_name} 已提交订阅")
        await query.answer()




    async def deletekeyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
        #
        # x = query.data.split('-')
        # # _LOGGER.info(f"订阅")
        #
        # server.subscribe.sub_by_douban(x[1])
        await query.delete_message()

        await query.answer()


    def start_bot(self, config: Dict) -> None:
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            application = Application.builder().token(self.TGbotTOKEN).proxy_url(self.proxy).get_updates_proxy_url(self.proxy).build()
            # application.add_handler(CommandHandler("rebootmr", rebootmr))
            # application.add_handler(CommandHandler("help", help_command))
            application.add_handler(CallbackQueryHandler(self.backtomenu, pattern="^back"))
            application.add_handler(CallbackQueryHandler(self.deletekeyboard, pattern="^delete"))
            application.add_handler(CallbackQueryHandler(self.button, pattern="^\d"))
            application.add_handler(CallbackQueryHandler(self.doubansub, pattern="^sub"))
            application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Text(['重启Movie-Bot']), self.menu_list))
            # application.add_handler(MessageHandler(filters.Text(['重启Movie-Bot']), rebootmr))
            application.run_polling(stop_signals=None, close_loop=False)
        finally:
            loop.close()
            pass

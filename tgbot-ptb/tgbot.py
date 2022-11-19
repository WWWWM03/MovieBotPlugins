##分条


# # --------------------------------------------------
# from moviebotapi import MovieBotServer
# from moviebotapi.core.session import AccessKeySession
# from moviebotapi.subscribe import SubStatus
# SERVER_URL = 'http://192.168.50.190:1329'
# ACCESS_KEY = '123524'
# server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))
# --------------------------------------------------

# -------------------------------------------------


# -------------------------------------------------
# !/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.
import asyncio
import threading
import time
from typing import Dict

from mbot.openapi import mbot_api
from mbot.core.plugins import PluginContext, PluginMeta
from mbot.core.params import ArgSchema, ArgType
from mbot.core.plugins import plugin, PluginCommandContext, PluginCommandResponse, PluginMeta
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



chatid_list=[
            '5414216757',
            '1663257876',
            '901504969'
]



async def echo1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    _LOGGER.info(f"echo1")
    mr_result = server.douban.search(update.message.text)
    chat_id = str(update.message.chat_id)
    if chat_id not in chatid_list:
        await update.message.reply_text(f"未经授权！")
        _LOGGER.info(f"chat_id：{chat_id} , 未经授权")
        return
    else:
        await update.message.reply_text(f"正在搜索 {update.message.text} 中.....")
        _LOGGER.info(f"chat_id：{chat_id} , 正在搜索 ")
    x = 0
    mr_caption = []
    mr_idlist = []
    mr_poster_path = []
    # if len(mr_result) > 8:
    #     mr_result = mr_result[0:8]
    for i in mr_result:
        cn_name = i.cn_name
        rating = str(i.rating)
        if rating == 'nan':
            rating = f''
        else:
            rating = f'   ⭐{rating}'
        url = i.url
        status = i.status
        if status == 0:
            status = '🛎️'
        elif status == 1:
            status = '✔'
        elif status == 2:
            status = '🔁'
        else:
            status = ' '


        poster_path = i.poster_url
        id = str(i.id)
        name_sel = str(cn_name)
        rating_sel = str(rating)
        poster_path_sel = str(poster_path)
        #
        # caption_1 = "{:<2}\t.\t{:<5}\t[{:<1}]({})\t{}\n".format(x+1,status,cn_name,url,rating)
        #



        caption_1 = f'{x+1} . {status} [{cn_name}]({url}){rating}\n'






        mr_caption.append(caption_1)
        mr_idlist.append(f'{id}-1-{update.message.text}-{x+1}')
        mr_poster_path.append(poster_path)
        x+=1
    mr_caption_final = ''.join(str(i) for i in mr_caption)
    mr_caption_final = mr_caption_final + '\n\n↓↓↓↓请点对应的序号↓↓↓↓'
    mr_keybord = []
    mr_count = []

    y = 1
    for i in mr_idlist:
        mr_count.append(str(y))
        mr_keybord.append(str(i))
        y+=1
    mr_keybord_final = []
    count1 = 1
    for  y in (mr_keybord):
        aaa = InlineKeyboardButton(count1, callback_data=y)
        mr_keybord_final.append(aaa)
        count1+=1

    step = 7
    a = mr_keybord_final
    b = [a[i:i + step] for i in range(0, len(a), step)]
    keyboard = b
    reply_markup1 = InlineKeyboardMarkup(keyboard)
    _LOGGER.info(f"返回搜索结果：\n{mr_caption_final}")
    await update.message.reply_photo(reply_markup=reply_markup1, photo=mr_poster_path[0],
                                     caption=f"{mr_caption_final} ",
                                     parse_mode=ParseMode.MARKDOWN)


# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query
#     x = query.data.split('/', 1)
#     server.subscribe.sub_by_douban(x[0])
#     _LOGGER.info(f"{x[1]} 已提交订阅")
#     await query.message.reply_text(f"{x[1]} 已提交订阅")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    _LOGGER.info(f"button")
    x = query.data.split('-')
    doubandetils = server.douban.get(x[0])
    cn_name = doubandetils.cn_name
    rating = str(doubandetils.rating)
    intro = doubandetils.intro
    release_year = doubandetils.release_year
    doubanid = doubandetils.id
    cover_image = doubandetils.cover_image
    actor = doubandetils.actor
    media_type = str(doubandetils.media_type)
    premiere_date = doubandetils.premiere_date # 上映时间
    season_index = doubandetils.season_index # 季
    trailer_video_url = str(doubandetils.trailer_video_url) # 预告片
    genres = doubandetils.genres
    episode_count = doubandetils.episode_count # 集
    if rating == '0.0':
        rating = f''
    else:
        rating = f'⭐{rating}'
    if len(actor) >= 3:
        actor = doubandetils.actor[0:4]
    if not actor:
        actor = ''
    else:
        actor = '演员：#' + ' #'.join(i.name for i in actor) +'\n'


    if not genres:
        genres = ''
    else:
        genres = '流派：#' + ' #'.join(i for i in doubandetils.genres) +'\n'

    if len(intro) >= 100:
        intro =f'{intro[0:100]}......'
    elif len(intro) == 0:
        intro = '暂无简介'


    if media_type == 'MediaType.Movie':
        caption = f'{x[3]} . *{cn_name}*   {media_type.split(".")[1]}\n上映时间：{premiere_date}  {rating}\n\n简介：{intro}\n{actor}{genres}'
    else:
        caption = f'{x[3]} . *{cn_name}*   {media_type.split(".")[1]}\n第{season_index}季，共{episode_count}集\n上映时间：{premiere_date}  {rating}\n\n简介：{intro}\n{actor}{genres}'


    _LOGGER.info(f"{caption} ")
    keyboard = [
                [
                InlineKeyboardButton('订阅', callback_data=f'sub-{doubanid}-'),
                InlineKeyboardButton('返回', callback_data=f'back-{doubanid}-{x[2]}-{x[3]}'),
            ]
    ]
    reply_markup1 = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.edit_message_media(reply_markup=reply_markup1,
                                   media=InputMediaPhoto(
                                       media=cover_image,
                                       caption=caption,
                                       parse_mode=ParseMode.MARKDOWN
                                        )
                                   )


    # _LOGGER.info(f"{trailer_video_url} ")
    #
    # await query.edit_message_media(reply_markup=reply_markup1,
    #                                media=InputMediaVideo(
    #                                    media=trailer_video_url,
    #                                    caption=caption,
    #                                    parse_mode=ParseMode.MARKDOWN,
    #                                    thumb=cover_image,
    #                                    supports_streaming=True
    #                                     )
    #                                )



    # await query.message.reply_photo(reply_markup=reply_markup1, photo=cover_image,
    #                                  caption=caption,
    #                                  parse_mode=ParseMode.MARKDOWN)
    # await query.message.reply_text(f"{x[1]} 已提交订阅")

async def backtomenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    query = update.callback_query

    x = query.data.split('-')
    mr_result = server.douban.search(x[2])
    # await query.message.reply_text(f"正在搜索 {x[2]} 中.....")
    # _LOGGER.info(f" 正在搜索 ")
    _LOGGER.info(f" backtomenu ")
    xx = 0
    mr_caption = []
    mr_idlist = []
    mr_poster_path = []
    # if len(mr_result) > 8:
    #     mr_result = mr_result[0:8]
    for i in mr_result:
        cn_name = i.cn_name
        rating = i.rating
        if rating != rating:
            rating = f''
        else:
            rating = f'   ⭐{rating}'
        status = i.status
        if status == 0:
            status = '🛎️'
        elif status == 1:
            status = '✔'
        elif status == 2:
            status = '🔁'
        else:
            status = ' '

        url = i.url
        poster_path = i.poster_url
        id = str(i.id)
        name_sel = str(cn_name)
        rating_sel = str(rating)
        poster_path_sel = str(poster_path)
        caption_1 = f'{xx+1} . {status} [{cn_name}]({url}){rating}\n'
        mr_caption.append(caption_1)
        # mr_caption.append(f'{xx+1} . [{cn_name}]({url}) | {rating}\n')
        mr_idlist.append(f'{id}-1-{x[2]}-{[xx+1]}')
        mr_poster_path.append(poster_path)
        xx+=1
    mr_caption_final = ''.join(str(i) for i in mr_caption)
    mr_caption_final = mr_caption_final + '\n\n↓↓↓↓请点对应的序号↓↓↓↓'
    mr_keybord = []
    mr_count = []

    y = 1
    for i in mr_idlist:
        mr_count.append(str(y))
        mr_keybord.append(str(i))
        y+=1
    mr_keybord_final = []
    count1 = 1
    for  y in (mr_keybord):
        aaa = InlineKeyboardButton(count1, callback_data=y)
        mr_keybord_final.append(aaa)
        count1+=1

    step = 7
    a = mr_keybord_final
    b = [a[i:i + step] for i in range(0, len(a), step)]
    keyboard = b
    reply_markup1 = InlineKeyboardMarkup(keyboard)
    _LOGGER.info(f"返回搜索结果：\n{mr_caption_final}")
    # await query.message.edit_caption(reply_markup=reply_markup1,
    #                                  caption=f"{mr_caption_final} ",
    #                                  parse_mode=ParseMode.MARKDOWN)

    await query.answer()
    await query.edit_message_media(reply_markup=reply_markup1,
                                   media=InputMediaPhoto(
                                       media=mr_poster_path[0],
                                       caption=mr_caption_final,
                                       parse_mode=ParseMode.MARKDOWN
                                        )
                                   )


        # update.message.reply_photo(reply_markup=reply_markup1, photo=mr_poster_path[0],
        #                              caption=f"{mr_caption_final} ",
        #                              parse_mode=ParseMode.MARKDOWN)


# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query
#     x = query.data.split('/', 1)
#     server.subscribe.sub_by_douban(x[0])
#     _LOGGER.info(f"{x[1]} 已提交订阅")
#     await query.message.reply_text(f"{x[1]} 已提交订阅")



async def doubansub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    x = query.data.split('-')
    _LOGGER.info(f"订阅")


    server.subscribe.sub_by_douban(x[1])
    await query.message.reply_text(f"{x[2]} 已提交订阅")


async def rebootmr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    server.common.restart_app(3)
    await update.message.reply_text(f"3秒后将重启Movie-Bot....")
    _LOGGER.info(f"3秒后将重启Movie-Bot....")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    list_id = [
        ['重启Movie-Bot', 'help', 'help'],
        ['help', 'help', 'help'],
        ['help', 'help', 'help']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=list_id, resize_keyboard=True, one_time_keyboard=True, selective=False,
                                       input_field_placeholder="请点击豆瓣id")

    await update.message.reply_text(f"1. 请直接输入您想查询的关键词\n"
                                    f"2. 重启Movie-Bot机器人  ------  /rebootmr\n"
                                    f"3. 重启Movie-Bot机器人  ------  /rebootmr\n"
                                    f"4. 重启Movie-Bot机器人  ------  /rebootmr\n"
                                    f"5. 重启Movie-Bot机器人  ------  /rebootmr\n"
                                    f"6. 重启Movie-Bot机器人  ------  /rebootmr\n")
                                    # reply_markup = reply_markup)


# def main() -> None:
#     """Run the bot."""
#     application = Application.builder().token("5627xxxU").build()
#     application.add_handler(CommandHandler("rebootmr", rebootmr))
#     application.add_handler(CommandHandler("help", help_command))
#     application.add_handler(CallbackQueryHandler(backtomenu, pattern="^back"))
#     application.add_handler(CallbackQueryHandler(button, pattern="^\d"))
#     application.add_handler(CallbackQueryHandler(doubansub, pattern="^sub"))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Text(['重启Movie-Bot']), echo1))
#     application.add_handler(MessageHandler(filters.Text(['重启Movie-Bot']), rebootmr))
#     application.run_polling()

# main()



def start_bot(config: Dict) -> None:
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        application = Application.builder().token("562xxxEizJU").build()
        application.add_handler(CommandHandler("rebootmr", rebootmr))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(backtomenu, pattern="^back"))
        application.add_handler(CallbackQueryHandler(button, pattern="^\d"))
        application.add_handler(CallbackQueryHandler(doubansub, pattern="^sub"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Text(['重启Movie-Bot']), echo1))
        application.add_handler(MessageHandler(filters.Text(['重启Movie-Bot']), rebootmr))
        application.run_polling(stop_signals=None, close_loop=False)
    finally:
        loop.close()
        pass


@plugin.after_setup
def main(plugin: PluginMeta, config: Dict):
    thread = threading.Thread(target=start_bot, args=(config,))
    thread.start()

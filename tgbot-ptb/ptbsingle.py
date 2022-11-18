##分条


# --------------------------------------------------
from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from moviebotapi.subscribe import SubStatus
SERVER_URL = 'http://192.168.50.190:1329'
ACCESS_KEY = '123524'
server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))
# --------------------------------------------------

#-------------------------------------------------
# import time
# from mbot.openapi import mbot_api
# from mbot.core.plugins import PluginContext, PluginMeta
# from mbot.core.params import ArgSchema, ArgType
# from mbot.core.plugins import plugin, PluginCommandContext, PluginCommandResponse, PluginMeta
# from mbot.core.event.models import EventType
# from moviebotapi.subscribe import SubStatus
# from moviebotapi import MovieBotServer
#
# server = mbot_api
#
# @plugin.command(name='tgbot1', title='tgbot1', desc='tgbot1', icon='HourglassFull', run_in_background=True)
# def echo(ctx: PluginCommandContext):
#     main()
#     return PluginCommandResponse(True, f'跑完了')

#-------------------------------------------------
#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.


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
            '1663257876'
]




async def echo1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
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
        rating = i.rating
        if rating != rating:
            rating = f'暂无评分'
        else:
            rating = f'⭐{rating}'
        url = i.url
        poster_path = i.poster_url
        id = str(i.id)
        name_sel = str(cn_name)
        rating_sel = str(rating)
        mr_caption.append(f'{x+1} . [{cn_name}]({url}) | {rating}\n')
        mr_idlist.append(f'{id}/{name_sel}({rating_sel})')
        mr_poster_path.append(poster_path)
        x+=1
    mr_caption_final = ''.join(str(i) for i in mr_caption)
    mr_caption_final = mr_caption_final + '\n\n请点击下面的按钮'
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

    step = 8
    a = mr_keybord_final
    b = [a[i:i + step] for i in range(0, len(a), step)]
    keyboard = b
    reply_markup1 = InlineKeyboardMarkup(keyboard)
    _LOGGER.info(f"返回搜索结果：{mr_caption_final}")
    await update.message.reply_photo(reply_markup=reply_markup1, photo=mr_poster_path[0],
                                     caption=f"{mr_caption_final} ",
                                     parse_mode=ParseMode.MARKDOWN)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    x = query.data.split('/', 1)
    server.subscribe.sub_by_douban(x[0])
    _LOGGER.info(f"{x[1]} 已提交订阅")
    await query.message.reply_text(f"{x[1]} 已提交订阅")

async def rebootmr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    server.common.restart_app(3)
    await update.message.reply_text(f"3秒后将重启Movie-Bot....")
    _LOGGER.info(f"3秒后将重启Movie-Bot....")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(f"1. 请直接输入您想查询的关键词\n"
                                    f"2. 重启Movie-Bot机器人  ------  /rebootmr\n"
                                    f"3. 重启Movie-Bot机器人  ------  /rebootmr\n"
                                    f"4. 重启Movie-Bot机器人  ------  /rebootmr\n"
                                    f"5. 重启Movie-Bot机器人  ------  /rebootmr\n"
                                    f"6. 重启Movie-Bot机器人  ------  /rebootmr\n")


def main() -> None:
    """Run the bot."""
    application = Application.builder().token("56211EizJU").build()
    application.add_handler(CommandHandler("rebootmr", rebootmr))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo1))
    application.run_polling()

main()
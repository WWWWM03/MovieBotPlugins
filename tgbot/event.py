import logging
from typing import Dict, Any
import threading
from mbot.core.event.models import EventType
from mbot.core.plugins import plugin
from mbot.core.plugins import PluginContext, PluginMeta
from .tgbot import TgBotSub

_LOGGER = logging.getLogger(__name__)
tgbot = TgBotSub()


@plugin.after_setup
def main(plugin: PluginMeta, config: Dict):
    tgbot.set_config(config.get('TGbotTOKEN'), config.get('chat_id') , config.get('proxy'))
    _LOGGER.info(f"{plugin.manifest.title}加载成功，TGbotTOKEN:{config.get('TGbotTOKEN')},chat_id:{config.get('chat_id')},Proxy：{config.get('proxy')}")
    thread = threading.Thread(target=tgbot.start_bot, args=(config,))
    thread.start()
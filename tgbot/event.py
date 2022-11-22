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
    token = config.get('TGbotTOKEN')
    chat_id = config.get('chat_id')
    proxy = config.get('proxy')
    base_url = config.get('base_url')
    if not token or not chat_id:
        _LOGGER.info(f'TG Bot缺少配置，停止启动，请完成插件配置')
        return
    tgbot.set_config(token, chat_id, proxy, base_url)
    _LOGGER.info(
        f"{plugin.manifest.title}加载成功，Base_url：{base_url},TGbotTOKEN:{token},chat_id:{chat_id},Proxy：{proxy}")
    thread = threading.Thread(target=tgbot.start_bot, args=(config,))
    thread.start()

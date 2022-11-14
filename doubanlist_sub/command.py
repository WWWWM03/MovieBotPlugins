# import time
# import logging
#
# from mbot.core.params import ArgSchema, ArgType
# from mbot.core.plugins import plugin, PluginCommandContext, PluginCommandResponse
# from .douban_sub import DoubanList_Sub
# _LOGGER = logging.getLogger(__name__)
#
# @plugin.command(name='doubansub', title='豆瓣片单订阅', desc='输入豆瓣片单id号即订阅影片！', icon='List')
# def echo(ctx: PluginCommandContext, name: ArgSchema(ArgType.String, '输入纯数字', '请输入豆瓣片单id！')):
#     try:
#         _LOGGER.info(f'豆瓣listId：{name} 加载成功')
#         return PluginCommandResponse(True, f'豆瓣listId：{name} 加载成功')
#     finally:
#         DoubanList_Sub.mb_sub(name)
#
#
#
#
#
# # @plugin.command(name='async', title='延迟测试', desc='点击后休息5秒完成', icon='HourglassFull', run_in_background=True)
# # def echo(ctx: PluginCommandContext):
# #     time.sleep(5)
# #     return PluginCommandResponse(True, f'跑完了')

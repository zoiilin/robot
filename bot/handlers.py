# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     handlers
   Description :
   Author :       Lychlov
   date：          2018/12/3
-------------------------------------------------
   Change Activity:
                   2018/12/3:
-------------------------------------------------
"""
import re
from werobot import WeRoBot
from werobot.replies import TextReply
from werobot.replies import ArticlesReply, Article
from .django_api import check_auth, new_query
from .commando_query import call_fx_api
from .alarm_query import old_alarm_query, fuzzy_query
from bot.base_conf import APP_URL

myrobot = WeRoBot(token='loyowanwancc')


# app_id='wx242d734cd4057dc5', app_secret='a1ffde51020438f076e43e3b19973648',
#                   encoding_aes_key='S24igTjZOhFawPXnUbLslXjs4LMwsEEyp7lJ4fUn1xI'

@myrobot.subscribe
def hello(message):
    return '欢迎您使用“网络维护一点通”！\n' + '您的ID为：' + message.source + '\n请联系管理员添加为内部用户。'


@myrobot.image
@myrobot.voice
def unknown(message):
    return '暂不支持的消息类型，敬请期待。'


@myrobot.filter(re.compile('帮助'))
def help(message):
    return '''
    '''


@myrobot.filter(re.compile('我的ID'))
def id_check(message):
    return '您的ID是：%s\n请联系管理员注册内部用户' % message.source


@myrobot.filter(re.compile('^10[1-9].*'))
def old_alarm_handler(message):
    source = message.source
    if not check_auth(source):
        return '您不是授权用户，无法使用该功能。'
    content = message.content
    query_id, url = old_alarm_query(content)
    print(new_query(source, query_id, url))
    reply = ArticlesReply(message=message)
    article = Article(
        title="告警详情",
        description="南阳网络运维一点通",
        img="https://github.com/apple-touch-icon-144.png",
        url=APP_URL + "?open_id=%s&uuid=%s" % (source, query_id))
    reply.add_article(article)
    return reply
    # return old_alarm_query(content)


@myrobot.filter(re.compile('^[3-6][0-3][1-9].*'))
def old_commando_handler(message):
    return "功能正在开发，敬请期待。。。"
    # source = message.source
    # content = message.content
    # if not check_auth(source):
    #     return '您不是授权用户，无法使用该功能。'
    # result = call_fx_api('chengzhikun', content)
    # return result


@myrobot.handler
def fuzzy(message):
    source = message.source
    content = message.content
    if not check_auth(source):
        return '您不是授权用户，无法使用该功能。'
    # myrobot.client.send_text_message(user_id=source, content='正在根据关键字“%s”进行模糊告警查询，请稍后' % content)
    query_id, url = fuzzy_query(content)
    print(new_query(source, query_id, url))
    print(url)
    # result = fuzzy_query(content)
    # return result
    reply = ArticlesReply(message=message)
    article = Article(
        title="告警详情",
        description="南阳网络运维一点通",
        img='http://robot.loyowanwan.cc/static/pics/gumpla.jpg',
        url=APP_URL + "?open_id=%s&uuid=%s" % (source, query_id))
    reply.add_article(article)
    return reply

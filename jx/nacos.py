# coding: utf-8
# from __future__ import absolute_import  # 如果是py2就取消这行的注释

from jx.util import logger
import asyncio
import threading


# BUG: ConnectionResetError: [Errno 54] Connection reset by peer (当页面频繁刷新时出现)
# TODO: https://www.django-rest-framework.org/api-guide/throttling


# This is only loaded once while starting by django->TEMPLATES->'BACKEND': 'django.template.backends.jinja2.Jinja2'
# https://blog.csdn.net/dashoumeixi/article/details/97344828
loop = asyncio.new_event_loop()


async def heartbeat():
    while True:
        await asyncio.sleep(6)
        logger.info("nacos heartbeat from kpi server")


def ioloop(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(heartbeat())


def start_ioloop():
    thread_handler = threading.Thread(target=ioloop, args=(loop,))
    thread_handler.start()


start_ioloop()

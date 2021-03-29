# from __future__ import absolute_import  # 如果是py2就取消这行的注释

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment, FileSystemLoader

# Start Nacos client with heartbeat
import jx.nacos


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env

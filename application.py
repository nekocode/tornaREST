# coding:utf-8

import os

from url import urls
import tornado.web

app = tornado.web.Application(
    handlers=urls,
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    allow_remote_access=True
)


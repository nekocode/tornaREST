# coding:utf-8

from handler.api.base import APINotFoundHandler
from handler.api.user.logopt import LoginHandler, LogoutHandler
from handler.api.user.profile import ProfileHandler, AvatarUploadHandler
from handler.api.user.register import RegisterHandler, SchoolsHandler
from tornado.options import options


urls = [
    [r'/api/user/schools', SchoolsHandler],
    [r'/api/user/register', RegisterHandler],
    [r'/api/user', ProfileHandler],
    [r'/api/user/avatar', AvatarUploadHandler],
    [r'/api/user/login', LoginHandler],
    [r'/api/user/logout', LogoutHandler],

    [r'.*', APINotFoundHandler],
]

# Add subpath to urls
for u in urls:
    u[0] = options.subpath + u[0]


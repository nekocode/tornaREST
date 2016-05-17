# coding:utf-8

import tornado
from tornado import gen
from tornado.web import HTTPError

from util.token import token_manager
from handler.api import errors
from handler.api.base import BaseHandler
from data.collections import User


class LoginHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        mobile = self.get_argument('mobile', None)
        pwd = self.get_argument('pwd', None)

        user = None
        if mobile is None or mobile == '' or pwd is None or pwd == '':
            # 没有传入手机密码，刷新 Token
            uid = self.is_logined()
            user = yield User.objects.get(uid)

        else:
            # 传入手机密码，执行登录
            users = yield User.objects.filter(mobile=mobile).find_all()
            if len(users) == 0:
                # 未找到该用户
                raise HTTPError(**errors.status_22)

            if users[0].password != pwd:
                # 密码有误
                raise HTTPError(**errors.status_23)

            user = users[0]

        # 登陆成功
        user = user.to_dict()
        user['token'] = token_manager.create_token(str(user['id']))
        self.write_json(user)


class LogoutHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    @gen.coroutine
    def delete(self):
        uid = self.is_logined()

        # 注销成功，清除 token
        token_manager.clear_token(uid)
        self.write_json({})




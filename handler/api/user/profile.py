# coding:utf-8

import tornado
from tornado import gen
from tornado.web import HTTPError

from handler.api.base import BaseHandler
from data.collections import User


class ProfileHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        uid = self.is_logined()

        user_id = self.get_argument('id', uid)
        user_id = user_id if user_id != '' else uid

        self.vaildate_id(user_id)

        user = yield User.objects.get(user_id)
        self.vaildate_resource(user)
        self.write_json(user.to_dict())

    @tornado.web.asynchronous
    @gen.coroutine
    def put(self):
        uid = self.is_logined()
        user = yield User.objects.get(uid)
        self.vaildate_resource(user)

        need_edit = 0
        nickname = self.get_argument('nickname', None)
        if self.vaildate_nickname(nickname):
            user.nickname = nickname
            need_edit += 1

        gender = self.get_argument('gender', '')
        if gender in ['0', '1']:
            user.gender = int(gender)
            need_edit += 1

        description = self.get_argument('description', None)
        if self.vaildate_description(description):
            user.description = description
            need_edit += 1

        if need_edit != 0:
            yield user.save()

        self.write_json(user.to_dict())

    # TODO：对昵称和描述进行限制
    @staticmethod
    def vaildate_nickname(nickname):
        if nickname is not None and len(nickname) > 0:
            return True
        else:
            return False

    @staticmethod
    def vaildate_description(description):
        if description is not None and len(description) > 0:
            return True
        else:
            return False


class AvatarUploadHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        uid = self.is_logined()

        url = self.upload_file_from_request('avatar', 'avatar/')

        user = yield User.objects.get(uid)
        self.check_none(user)

        user.avatar_url = url
        yield user.save()

        self.write_json(user.to_dict())



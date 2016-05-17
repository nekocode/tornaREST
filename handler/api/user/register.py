# coding:utf-8

from bson import ObjectId
import tornado
from tornado import gen
from tornado.web import HTTPError

from handler.api import errors
from handler.api.base import BaseHandler
from data.collections import User, School
from util.token import token_manager


class RegisterHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        # 注册用户 TODO: 手机号验证
        mobile = self.get_argument('mobile')
        pwd = self.get_argument('pwd')
        users = yield User.objects.filter(mobile=mobile).find_all()
        if len(users) != 0:
            # 手机号码已经被注册
            raise HTTPError(**errors.status_21)

        school_id = self.get_argument('school_id')
        self.vaildate_id(school_id)

        school = yield School.objects.get(self.get_argument('school_id'))
        self.check_none(school)

        # 注册成功
        user = User(mobile=mobile, password=pwd, nickname='test', school_id=ObjectId(school_id))
        yield user.save()

        user = user.to_dict()
        user['token'] = token_manager.create_token(str(user['id']))
        self.write_json(user)


class SchoolsHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        # 获取所有学校列表
        schools = yield School.objects.find_all()
        self.write_json([school.to_dict() for school in schools])



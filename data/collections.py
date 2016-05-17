# coding:utf-8

from motorengine import Document, StringField, IntField, DateTimeField, \
    ReferenceField


class BaseDocument(Document):
    def to_dict(self):
        data = super(Document, self).to_son()
        data['id'] = self._id
        return data


class School(BaseDocument):
    name = StringField(required=True)
    verifier = StringField()


class User(BaseDocument):
    mobile = StringField(required=True)
    password = StringField(required=True)
    nickname = StringField(required=True)
    gender = IntField(required=True, default=1)
    description = StringField()
    avatar_url = StringField()

    school_id = ReferenceField(reference_document_type=School)

    like_count = IntField(required=True, default=0)
    follower_count = IntField(required=True, default=0)
    following_count = IntField(required=True, default=0)

    create_time = DateTimeField(required=True, auto_now_on_insert=True, auto_now_on_update=False)

    def to_dict(self):
        data = super(User, self).to_dict()
        del data['password']
        return data

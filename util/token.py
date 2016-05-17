# coding:utf-8

import time

import config
from data.redis import redis
from util.crypt import AESCrypto


class TokenManager:
    def __init__(self, aes_key, token_timeout):
        self.crypto = AESCrypto(aes_key)
        self.timeout = token_timeout

    def create_token(self, uid):
        rt = int(time.time())
        token = self.crypto.encrypt('%d@%s' % (rt, uid))
        redis.set('token:' + uid, token)
        return token

    def validate_token(self, token):
        rt = int(time.time())
        token_raw = self.crypto.decrypt(token)

        if token_raw is None:
            return False, None

        try:
            sp = token_raw.split('@')
            tk_rt = int(sp[0])
            tk_uid = sp[1]

            active_token = redis.get('token:' + tk_uid)
            if token != active_token:
                return False, None

            if tk_rt <= rt and (rt-tk_rt) <= self.timeout:
                return True, tk_uid
            else:
                # token is outdated
                return False, None

        except Exception as e:
            print('Validate token: %s' % e)
            return False, None

    @staticmethod
    def clear_token(uid):
        redis.delete('token:' + uid)


token_manager = TokenManager(config.AES_KEY, config.TOKEN_TIMEOUT)


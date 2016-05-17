# coding:utf-8

import base64
import random
import string
from Crypto.Cipher import AES
from hashlib import md5


class PKCS7Encoder:
    block_size = 32

    def __init__(self):
        pass

    def encode(self, text):
        # 对需要加密的明文进行填充补位
        text_length = len(text)
        # 计算需要填充的位数
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        # 获得补位所用的字符
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, decrypted):
        # 删除解密后明文的补位字符
        pad = ord(decrypted[-1])
        if pad < 1 or pad > self.block_size:
            pad = 0
        return decrypted[:-pad]


class AESCrypto:
    def __init__(self, aes_key):
        self.key = aes_key
        # 设置加解密模式为 AES 的 CBC 模式
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        # 16 位随机字符串添加到明文开头
        text = self.get_random_str() + text
        # 使用自定义的填充方式对明文进行补位填充
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)

        try:
            # 加密
            cryptor = AES.new(self.key, self.mode, self.key[:16])
            ciphertext = cryptor.encrypt(text)
            return base64.b64encode(ciphertext)
        except Exception:
            return None

    def decrypt(self, text):
        try:
            cryptor = AES.new(self.key, self.mode, self.key[:16])
            # 使用 BASE64 对密文进行解码，然后 AES-CBC 解密
            plain_text = cryptor.decrypt(base64.b64decode(text))
        except Exception:
            return None

        try:
            # 去掉补位字符串
            pkcs7 = PKCS7Encoder()
            plain_text = pkcs7.decode(plain_text)
            # 去除 16 位随机字符串
            content = plain_text[16:]
        except Exception:
            return None

        return content

    @staticmethod
    def get_random_str():
        # 随机生成 16 位字符串
        return ''.join(random.sample(string.hexdigits, 16))


def md5_data(data):
    m = md5()
    m.update(data)
    return m.hexdigest()









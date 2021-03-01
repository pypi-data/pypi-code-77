import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from binascii import b2a_hex, a2b_hex
from base64 import b64encode, b64decode

BLOCK_SIZE = 16


def encrypt(data: bytes, key: str, mode=AES.MODE_ECB, block_size=BLOCK_SIZE):
    data = pad(data, block_size)
    key = pad(key.encode(encoding='utf-8'), block_size)

    cipher = AES.new(key, mode)
    # 为了避免结果直接保存出现编码转换问题，这里选择转换成hex来存
    return b2a_hex(cipher.encrypt(data))


def decrypt(encrypted_data: bytes, key: str, mode=AES.MODE_ECB, block_size=BLOCK_SIZE):
    # 吧16进制转成2进制再处理

    key = pad(key.encode(encoding='utf-8'), block_size)
    cipher = AES.new(key, mode)

    encrypted_data = a2b_hex(encrypted_data)
    return unpad(cipher.decrypt(encrypted_data), block_size)


def md5(text: str, encoding="utf-8"):
    return hashlib.md5(text.encode(encoding)).hexdigest()


if __name__ == '__main__':
    pass
    # key = "shirkhan"
    # txt = b'hello world'
    # enc = encrypt(txt, key)
    # print(enc)
    # print(encrypt(txt, key))
    # # print(decrypt(enc,key).decode())

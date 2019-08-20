# coding=gbk
# ������̣�����python
__auther__ = 'Mr.Hu'


import requests
import random
import base64

from Crypto.Cipher import AES
import json
import binascii


class Music_api():
    # ���ô�JS�ļ���ȡ��RSA��ģ����Э�̵�AES�Գ���Կ��RSA�Ĺ�Կ����Ҫ��Ϣ
    def __init__(self):
        self.modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'
        self.url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        self.HEADER = {}
        self.setHeader()
        self.secKey = self.getRandom()

    # ����16�ֽڼ�256λ�������
    def getRandom(self):
        string = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        res = ""
        for i in range(16):
            res += string[int(random.random() * 62)]
        return res

    # AES���ܣ���seckey��text����
    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey.encode('utf-8'), 2, '0102030405060708'.encode('utf-8'))
        ciphertext = encryptor.encrypt(text.encode('utf-8'))
        ciphertext = base64.b64encode(ciphertext).decode("utf-8")
        return ciphertext

    # ����ģ�����㣬�� x^y mod mo
    def quickpow(self, x, y, mo):
        res = 1
        while y:
            if y & 1:
                res = res * x % mo
            y = y // 2
            x = x * x % mo
        return res

    # rsa����
    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        a = int(binascii.hexlify(str.encode(text)), 16)
        b = int(pubKey, 16)
        c = int(modulus, 16)
        rs = self.quickpow(a, b, c)
        return format(rs, 'x').zfill(256)

    # ��������ͷ
    def setHeader(self):
        self.HEADER = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'https://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'

        }

    # ������Ӧ������������Ӷ������б�
    # �����������ܲ���Ϊ��
    # ������nonce��text������������1
    # Ȼ���������seckey��������1��������2
    # ����ù�Կ����seckey��������3
    # ���У�����2��Ϊ��������е�params������3��ΪencSeckey�ֶ�
    # ���������շ�����ͨ��˽Կ��������3���seckey(�����)
    # Ȼ����seckey��������2�������1
    # ������ͳһЭ�̵���Կnonce��������1���ջ��text
    def search(self, s, offset, type="1"):
        text = {"hlpretag": "<span class=\"s-fc7\">",
                "hlposttag": "</span>",
                "#/discover": "",
                "s": s,
                "type": type,
                "offset": offset,
                "total": "true",
                "limit": "30",
                "csrf_token": ""}
        text = json.dumps(text)
        params = self.aesEncrypt(self.aesEncrypt(text, self.nonce), self.secKey)
        encSecKey = self.rsaEncrypt(self.secKey, self.pubKey, self.modulus)
        data = {
            'params': params,
            'encSecKey': encSecKey
        }
        result = requests.post(url=self.url,
                               data=data,
                               headers=self.HEADER).json()
        return result

    # ��ȡָ�������б�(�൱��������)
    def get_music_list(self, keywords):
        music_list = []
        for offset in range(1):
            result = Music_api().search(keywords, str(offset))
            result = result['result']['songs']
            # �޳���Ȩ
            for music in result:
                # if music['copyright'] == 1 and music['fee'] == 8:
                if (music['privilege']['fee'] == 0 or music['privilege']['payed']) and music['privilege']['pl'] > 0 and \
                        music['privilege']['dl'] == 0:
                    continue
                if music['privilege']['dl'] == 0 and music['privilege']['pl'] == 0:
                    continue
                    # if music['fee'] == 8:
                music_list.append(music)
        return music_list


def start(a):
    res2 = Music_api().get_music_list(a)
    keys = []
    vs = []
    res4=[]
    for l in range(len(res2)-1):
        res2 = Music_api().get_music_list(a)[l]
        j = 0
        for k, v in res2.items():
            if j in [0, 1]:
                keys.append(k)
                vs.append(v)
            j += 1
        keys.append("artist_id")
        keys.append('artist')
        ar = res2.get('ar')
        if len(ar) > 1:
            s_id=str((ar[0].get('id')))+'/'+str((ar[1].get('id')))
            vs.append(s_id)
            s_name=str((ar[0].get('name')))+'/'+str((ar[1].get('name')))
            vs.append(s_name)

        else:
            s_id = str((ar[0].get('id')))
            vs.append(s_id)
            s_name = str((ar[0].get('name')))
            vs.append(s_name)
        res3 = dict(zip(keys, vs))
            # print(vs)
        # ��Ӧǰ��
        res3['mp3']=res3.pop('id')
        res3['title']=res3.pop('name')
        ids=res3['mp3']
        ids2=f'http://music.163.com/song/media/outer/url?id={ids}.mp3'
        res3['mp3']=ids2
        res4.append(res3)
    return res4

if __name__=="__main__":
    a=start('�ܽ���')
    print(a)
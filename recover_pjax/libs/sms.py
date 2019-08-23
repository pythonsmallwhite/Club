# -*-coding:GBK -*-
import urllib.request
import urllib
import json
import logging

logger = logging.getLogger('apis')


def send_sms(mobile, captcha):
    # flag���ڱ�Ƿ��Ͷ����Ƿ�ɹ�
    flag = True
    # ����Ƕ���API��ַ
    url = 'https://open.ucpaas.com/ol/sms/sendsms'
    # ׼��һ��ͷ,����body�ĸ�ʽ
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    # ��������׼����Post����ֵ������ֵ���ֵ����ʽ
    values = {
        "sid": "44f39b4b0b7581cbdba8027874fe20e7",
        "token": "60706485823888d71ca026f8aaba8a83",
        "appid": "1826aa023ce54c3889f079c6afa8a75c",
        "templateid": "489760",
        "param": str(captcha),
        "mobile": mobile,
    }

    try:
        # ���ֵ��ʽ����bytes��ʽ
        data = json.dumps(values).encode('utf-8')
        logger.info(f"�������Ͷ���: {data}")
        # ����һ��request,�������ǵĵ�ַ�����ݡ�ͷ
        request = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        # html = '{"code":"000000","count":"1","create_date":"2018-07-23 13:34:06","mobile":"15811564298","msg":"OK","smsid":"852579cbb829c08c917f162b267efce6","uid":""}'
        code = json.loads(html)["code"]
        print(code)
        if code == "000000":
            logger.info(f"���ŷ��ͳɹ���{html}")
            flag = True
        else:
            logger.info(f"���ŷ���ʧ�ܣ�{html}")
            flag = False
    except Exception as ex:
        logger.info(f"������,����ԭ��{ex}")
        flag = False
    print(flag)
    return flag


if __name__ == "__main__":
    # ���Զ��Žӿ��Ƿ��ǹ���
    send_sms("13736665365", "123456")
import requests
import argparse
import time
from bs4 import BeautifulSoup
import json
from PIL import Image
from time import sleep
"""
    README:
    python xk.py --xh MG20330064 --pw 34D2C0A9BDCE3EAD13E80D55CAE0C457574C9DECDA63AD2C --st 0.1
"""

bjdms = {
    "20201-033-081200D02-1592649131637" : "分布式算法入门",
    "20201-033-085401C02-1592649131522" : "信息技术前沿及行业应用",
    "20201-033-085401C01-1592649131579" : "分布式计算研究导引",
    "20201-4330-10284A001-1590476519355": "硕士生英语（硕士英语听力02）",
    "20201-033-085401D23-1594298344259" : "自然语言处理（自然语言处理）",
    "20201-033-085401D22-1592649131696" : "神经网络及其应用（神经网络及其应用）",
    "20201-033-085401D08-1592649131115" : "MapReduce海量数据并行处理（MapReduce海量数据并行处理）",
    "20201-033-081200D19-1590054822275" : "并发算法与理论（并发算法与理论）" 
}

def get_time_c():
    time_c = int(time.time()*1000)
    return time_c


def get_yzm(cookies):
    res = requests.get("http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/login/4/vcode.do?timestamp="+str(get_time_c()), cookies=cookies)
    tmp_soup = BeautifulSoup(res.content)
    t = json.loads(tmp_soup.html.body.p.text)
    vtoken = t['data']['token']
    res = requests.get("http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/login/vcode/image.do?vtoken="+str(vtoken), cookies=cookies)

    with open('t.jpeg', 'wb') as f:
        f.write(res.content)
    return vtoken

def main(args):

    response  = requests.get("http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/index_nju.html")
    cookies = response.cookies

    while True: # 输入验证码直到正确
        vtoken = get_yzm(cookies)
        img=Image.open('t.jpeg')
        img.show()
        yzm = input()
        data = {
            'loginName': args.xh,
            'loginPwd': args.pw,
            'verifyCode': yzm,
            'vtoken': vtoken
        }
        res = requests.post('http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/login/check/login.do?timestrap='+str(get_time_c()), data, cookies=cookies)
        cookies = res.cookies
        try:
            tmp = json.loads(res.text)
            print(tmp["code"])
            if tmp["code"] == "1":
                break
            else:
                print("验证码错误")
        except Exception:
            print("访问次数过多,5min后再尝试")
            exit()

    res = requests.get('http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/xsxkHome/loadPublicInfo_course.do', cookies=cookies)
    tmp = json.loads(res.text)
    csrfToken = tmp['csrfToken']

    data = {
        'csrfToken': csrfToken,
        'lx': 2,
    }

    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8',
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "yjsxk.nju.edu.cn",
        "Origin": "http://yjsxk.nju.edu.cn",
        "Referer": "http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/course_nju.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    input("回车键开始抢课")
    while True:
        for bjdm in bjdms.keys():
            data["bjdm"] = bjdm
            print(data)
            res = requests.post("http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/choiceCourse.do?_="+str(get_time_c()), headers=header, data=data, cookies=cookies)
            try:
                tmp = json.loads(res.text)
                print(res.text)
                print(bjdms[bjdm], tmp["msg"])
                if tmp["code"] == "1":
                    bjdms.pop(bjdm)
            except Exception:
                pass
        sleep(args.st)
        print("未选择的课程有", bjdms)
        if len(bjdms) == 0:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xh', type=str, default="MG20330064", help='学号')
    parser.add_argument('--pw', type=str, default="34D2C0A9BDCE3EAD13E80D55CAE0C457574C9DECDA63AD2C", help='加密后48位的密码')
    parser.add_argument('--st', type=float, default=1, help='sleep time')
    args = parser.parse_args()
    print("args:", args)
    main(args)

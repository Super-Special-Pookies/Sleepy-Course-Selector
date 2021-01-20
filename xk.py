import requests
import argparse
import time
from bs4 import BeautifulSoup
import json
from PIL import Image
from time import sleep
import execjs
"""
    README:
    python xk.py --xh MG20330000 --pw 12345678 --st 0.1
"""


bjdms = {
    # "20201-033-081200D02-1592649131637" : "分布式算法入门",
    "20201-033-081200D15-1590054822235": "矩阵论及其应用（矩阵论及其应用）",
    "20201-033-085401C02-1592649131522" : "信息技术前沿及行业应用",
    "20201-033-085401C01-1592649131579" : "分布式计算研究导引",
    "20201-4330-10284A001-1590476519355": "硕士生英语（硕士英语听力02）",
    "20201-033-085401D23-1594298344259" : "自然语言处理（自然语言处理）",
    "20201-033-085401D22-1592649131696" : "神经网络及其应用（神经网络及其应用）",
    "20201-033-085401D08-1592649131115" : "MapReduce海量数据并行处理（MapReduce海量数据并行处理）",
    "20201-033-081200D19-1590054822275" : "并发算法与理论（并发算法与理论）" 
}

def get_DESPW(pw):
    js_code = ""
    with open("DES.js", "r") as f:
        js_code = "".join(f.readlines())
    DES = execjs.compile(js_code)
    return DES.call("strEncSimple", pw)


def get_time_c():
    time_c = int(time.time()*1000)
    return time_c


def get_yzm(cookies):
    res = requests.get("http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/login/4/vcode.do?timestamp="+str(get_time_c()), cookies=cookies)
    tmp_soup = BeautifulSoup(res.text)
    t = json.loads(tmp_soup.text)
    vtoken = t['data']['token']
    res = requests.get("http://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/login/vcode/image.do?vtoken="+str(vtoken), cookies=cookies)

    with open('t.jpeg', 'wb') as f:
        f.write(res.content)
    return vtoken

def main(args):
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": 'zh-CN,zh;q=0.9',
        "Connection": "keep-alive",
        "Content-Length": "138",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "yjsxk.nju.edu.cn",
        "Origin": "https://yjsxk.nju.edu.cn",
        "Referer": "https://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/index_nju.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = requests.get("https://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/index_nju.html")
    cookies = response.cookies

    while True:   # 输入验证码直到正确
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
        res = requests.post('https://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/login/check/login.do?timestrap='+str(get_time_c()), data=data, headers=header, cookies=cookies)
        cookies = res.cookies
        try:
            tmp = json.loads(res.text)
            print(tmp["code"])
            if tmp["code"] == "1":
                break
            elif tmp["code"] == "2":
                print("密码错误！")
            else:
                print("验证码错误！")
        except Exception:
            print("访问次数过多,5min后再尝试")
            exit()

    while True:
        try:
            res = requests.get('https://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/xsxkHome/loadPublicInfo_course.do', cookies=cookies)
            tmp = json.loads(res.text)
            print(tmp)
            csrfToken = tmp['csrfToken']
            break
        except Exception:
            print("---------------------------选课还未开始------------------------------")

    data = {
        'csrfToken': csrfToken,
        'lx': 2,
    }


    input("回车键开始抢课")
    while True:
        for bjdm in bjdms.keys():
            data["bjdm"] = bjdm
            print(data)
            res = requests.post("https://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/choiceCourse.do?_="+str(get_time_c()), headers=header, data=data, cookies=cookies)
            try:
                tmp = json.loads(res.text)
                print(res.text)
                print(bjdms[bjdm], tmp["msg"])
                if str(tmp["code"]) == "1":
                    bjdms.pop(bjdm)
            except Exception:
                pass
        sleep(args.st)
        print("未选择的课程有", bjdms)
        if len(bjdms) == 0:
            break
        print("如果出现页面已过期说明爬虫脚本没用了!!!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xh', type=str, default="MG20330000", help='学号')
    parser.add_argument('--pw', type=str, default="onmygod!", help='密码')
    parser.add_argument('--st', type=float, default=0.01, help='sleep time')
    args = parser.parse_args()
    args.pw = get_DESPW(args.pw)
    print("args:", args)
    main(args)

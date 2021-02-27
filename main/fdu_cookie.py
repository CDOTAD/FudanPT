import re


import requests
from bs4 import BeautifulSoup


class FduCookie:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'accept-encoding': "gzip, deflate",
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    def get_suffix(self) -> str:
        """
        获取“复试结果查询”页面的 url 后缀
        :return:
        """
        url = 'https://gsas.fudan.edu.cn/ssfs/index'
        text_response = requests.request('GET', url, headers={**self.headers, 'cookie': self.cookie}).text
        soups = BeautifulSoup(text_response, 'html.parser')
        tag = soups.select_one('section[class=\"container\"] > script[type =\"text/javascript\"]')
        # print(tag)
        if tag is None:
            return None
        # print(tag.string)
        # clean whitespace
        script = ''.join(tag.string.split())

        suffix = re.search(r'#kscjcx.*?window\.location\.href=\'(.*?)\'', script).group(1)
        return suffix

    def get_score(self, suffix) -> dict:
        url = 'https://gsas.fudan.edu.cn' + suffix
        text_response = requests.request('GET', url, headers={**self.headers, 'cookie': self.cookie}).text
        soups = BeautifulSoup(text_response, 'html.parser')

        score = None
        ky_type = None  # 学硕/专硕
        tags = soups.select('div[class=\"info-status\"] > div[class=\"info-item\"] > dl')
        for tag in tags:
            if "初试总成绩" in tag.dt.string:
                score = int(tag.dd.string)
            elif "复试专业" in tag.dt.string:
                ky_type_desc = str(tag.dd.string).split()[0]
                if ky_type_desc in ['081201', '081202', '081203', '083900']:  # 计算机软件与理论
                    ky_type = 1
                elif ky_type_desc == "085400":  # 电子信息
                    ky_type = 0
                else:
                    ky_type = 2

        uid = None
        name = soups.select('div[class=\"info-group info-sub-group\"] > h1')
        name = name[0].string

        tags = soups.select('div[class=\"info-group info-sub-group\"] > div[class=\"info-item\"] > dl')
        for tag in tags:
            if "考生编号" in tag.dt.string:
                uid = int(tag.dd.string)

        return {'uid': uid, 'st_name': name, 'score': score, 'type': ky_type}



if __name__ == '__main__':
    # global_cookie = "iPlanetDirectoryPro=AQIC5wM2LY4SfcwVTKQoC3%2FQknyZBaOre%2FfYykJR7%2FttYlM%3D%40AAJTSQACMDE%3D%23; NSC_Xfc-DpoufouTxjudi-443=ffffffff096ca61a45525d5f4f58455e445a4a423660; JSESSIONID=0A65FA87EB1BFD07D581E93FFEA43B4A.yzbm_server2; cn_com_southsoft_gms=013e765c-2e33-4199-a46d-ff9637f8139a"
    global_cookie = "NSC_Xfc-DpoufouTxjudi-443=ffffffff096ca61a45525d5f4f58455e445a4a423660; cn_com_southsoft_gms=12e2f7ff-0e39-427d-95f2-318a14e7bff1"
    fducookie = FduCookie(global_cookie)
    suffix = fducookie.get_suffix()
    print(fducookie.get_score(suffix))



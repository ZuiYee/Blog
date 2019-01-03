#!/usr/bin/env python

import base64
import re
from urllib.parse import urlencode
from urllib import parse
import requests
from bs4 import BeautifulSoup
import http.cookiejar
from pyquery import PyQuery as pq
from ZFCheckCode import recognizer
from .models import Score


sdj_dict = {
    # 上午12节
    '12': "'1'|'1','0','0','0','0','0','0','0','0'",
    # 上午34节
    '34': "'2'|'0','3','0','0','0','0','0','0','0'",
    # 下午56节
    '56': "'3'|'0','0','5','0','0','0','0','0','0'",
    # 下午78节
    '78': "'4'|'0','0','0','7','0','0','0','0','0'",
    # 下午91011节
    '91011': "'5'|'0','0','0','0','9','0','0','0','0'",
    # 上午
    'am': "'6'|'1','3','0','0','0','0','0','0','0'",
    # 下午
    'pm': "'7'|'0','0','5','7','0','0','0','0','0'",
    # 晚上
    'night': "'8'|'0','0','0','0','9','0','0','0','0'",
    # 白天
    'daylight': "'9'|'1','3','5','7','0','0','0','0','0'",
    # 整天
    'wholeday': "'10'|'1','3','5','7','9','0','0','0','0'",

}

dsz_dict = {
    '0': '%CB%AB',
    '1': '%B5%A5',
}

classnum_dict = {
                 '博学北楼A101': '101A0101', '博学北楼A102': '101A0102', '博学北楼A103': '101A0103',
                 '博学北楼A104': '101A0104', '博学北楼A105': '101A0105', '博学北楼A109': '101A0106',
                 '博学北楼A201': '101A0201', '博学北楼A202': '101A0202', '博学北楼A203': '101A0203',
                 '博学北楼A204': '101A0204', '博学北楼A205': '101A0205', '博学北楼A209': '101A0206',
                 '博学北楼A301': '101A0301', '博学北楼A302': '101A0302', '博学北楼A303': '101A0303',
                 '博学北楼A304': '101A0304', '博学北楼A305': '101A0305', '博学北楼A309': '101A0306',
                 '博学北楼A401': '101A0401', '博学北楼A402': '101A0402', '博学北楼A403': '101A0403',
                 '博学北楼A405': '101A0404', '博学北楼A409': '101A0405', '博学北楼B101': '101B1101',
                 '博学北楼B103': '101B1102', '博学北楼B105': '101B1103', '博学北楼B107': '101B1104',
                 '博学北楼B109': '101B1105', '博学北楼B111': '101B1106', '博学北楼B113': '101B1107',
                 '博学北楼B115': '101B1108', '博学北楼B117': '101B1109', '博学北楼B201': '101B1201',
                 '博学北楼B203': '101B1202', '博学北楼B205': '101B1203', '博学北楼B207': '101B1204',
                 '博学北楼B209': '101B1205', '博学北楼B211': '101B1206', '博学北楼B213': '101B1207',
                 '博学北楼B215': '101B1208', '博学北楼B217': '101B1209', '博学北楼B301': '101B1301',
                 '博学北楼B303': '101B1302', '博学北楼B305': '101B1303', '博学北楼B307': '101B1304',
                 '博学北楼B309': '101B1305', '博学北楼B311': '101B1306', '博学北楼B313': '101B1307',
                 '博学北楼B315': '101B1308', '博学北楼B317': '101B1309', '博学北楼B401': '101B1401',
                 '博学北楼B403': '101B1402', '博学北楼B405': '101B1403', '博学北楼B407': '101B1404',
                 '博学北楼B409': '101B1405', '博学北楼B411': '101B1406', '博学北楼B413': '101B1407',
                 '博学北楼B415': '101B1408', '博学北楼B417': '101B1409', '博学北楼B501': '101B1501',
                 '博学北楼B503': '101B1502', '博学北楼B505': '101B1503', '博学北楼B507': '101B1504',
                 '博学北楼B509': '101B1505', '博学北楼B511': '101B1506', '博学北楼B513': '101B1507',
                 '博学北楼B515': '101B1508', '博学北楼B102': '101B2101', '博学北楼B104': '101B2102',
                 '博学北楼B106': '101B2103', '博学北楼B108': '101B2104', '博学北楼B110': '101B2105',
                 '博学北楼B112': '101B2106', '博学北楼B114': '101B2107', '博学北楼B116': '101B2108',
                 '博学北楼B118': '101B2109', '博学北楼B202': '101B2201', '博学北楼B204': '101B2202',
                 '博学北楼B206': '101B2203', '博学北楼B208': '101B2204', '博学北楼B210': '101B2205',
                 '博学北楼B212': '101B2206', '博学北楼B214': '101B2207', '博学北楼B218': '101B2208',
                 '博学北楼B302': '101B2301', '博学北楼B304': '101B2302', '博学北楼B306': '101B2303',
                 '博学北楼B308': '101B2304', '博学北楼B310': '101B2305', '博学北楼B312': '101B2306',
                 '博学北楼B314': '101B2307', '博学北楼B316': '101B2308', '博学北楼B318': '101B2309',
                 '博学北楼B402': '101B2401', '博学北楼B404': '101B2402', '博学北楼B406': '101B2403',
                 '博学北楼B408': '101B2404', '博学北楼B410': '101B2405', '博学北楼B412': '101B2406',
                 '博学北楼B414': '101B2407', '博学北楼B416': '101B2408', '博学北楼B418': '101B2409',
                 '博学北楼B502': '101B2501', '博学北楼B504': '101B2502', '博学北楼B506': '101B2503',
                 '博学北楼B508': '101B2504', '博学北楼B510': '101B2505', '博学北楼B512': '101B2506',
                 '博学北楼B514': '101B2507', '博学北楼B516': '101B2508', '博学北楼C101': '101C0101',
                 '博学北楼C102': '101C0102', '博学北楼C103': '101C0103', '博学北楼C105': '101C0104',
                 '博学北楼C106': '101C0105', '博学北楼C108': '101C0106', '博学北楼C201': '101C0201',
                 '博学北楼C202': '101C0202', '博学北楼C203': '101C0203', '博学北楼C205': '101C0204',
                 '博学北楼C206': '101C0205', '博学北楼C208': '101C0206', '博学北楼C301': '101C0301',
                 '博学北楼C302': '101C0302', '博学北楼C303': '101C0303', '博学北楼C305': '101C0304',
                 '博学北楼C306': '101C0305', '博学北楼C308': '101C0306', '博学北楼C406': '101C0405',
                 '博学北楼C408': '101C0406',
                # '行知楼B206': '1020080', '行知楼B207': '1020081',
                #  '行知楼B306': '1020082', '行知楼B307': '1020083', '笃行南楼200': '1020133',
                #  '笃行南楼300': '1020134',
                 '博学南楼A101': '102A0101', '博学南楼A102': '102A0102',
                 '博学南楼A103': '102A0103', '博学南楼A104': '102A0104', '博学南楼A201': '102A0201',
                 '博学南楼A202': '102A0202', '博学南楼A203': '102A0203', '博学南楼A204': '102A0204',
                 '博学南楼A206': '102A0205', '博学南楼A301': '102A0301', '博学南楼A302': '102A0302',
                 '博学南楼A303': '102A0303', '博学南楼A304': '102A0304', '博学南楼A401': '102A0401',
                 '博学南楼A402': '102A0402', '博学南楼A403': '102A0403', '博学南楼A404': '102A0404',
                 '博学南楼A406': '102A0405', '博学南楼B101': '102B0101', '博学南楼B103WD': '102B0102',
                 '博学南楼B104WD': '102B0103', '博学南楼B105WD': '102B0104', '博学南楼B106WD': '102B0105',
                 '博学南楼B107WD': '102B0106', '博学南楼B108WD': '102B0107', '博学南楼B109': '102B0108',
                 '博学南楼B201': '102B0201', '博学南楼B202': '102B0202', '博学南楼B203': '102B0203',
                 '博学南楼B204': '102B0204', '博学南楼B205': '102B0205', '博学南楼B206': '102B0206',
                 '博学南楼B207': '102B0207', '博学南楼B208': '102B0208', '博学南楼B209': '102B0209',
                 '博学南楼B301': '102B0301', '博学南楼B302': '102B0302', '博学南楼B303': '102B0303',
                 '博学南楼B304': '102B0304', '博学南楼B305': '102B0305', '博学南楼B306': '102B0306',
                 '博学南楼B307': '102B0307', '博学南楼B308': '102B0308', '博学南楼B401': '102B0401',
                 '博学南楼B403': '102B0402', '博学南楼B404': '102B0403', '博学南楼B405': '102B0404',
                 '博学南楼B406': '102B0405', '博学南楼B407': '102B0406', '博学南楼B408': '102B0407',
                 '博学南楼B409': '102B0408', '博学南楼B501': '102B0501', '博学南楼B502': '102B0502',
                 '博学南楼B503': '102B0503', '博学南楼B504': '102B0504', '博学南楼C101': '102C0101',
                 '博学南楼C103': '102C0102', '博学南楼C104': '102C0103', '博学南楼C105': '102C0104',
                 '博学南楼C106': '102C0105', '博学南楼C107': '102C0106', '博学南楼C108': '102C0107',
                 '博学南楼C109': '102C0108', '博学南楼C201': '102C0201', '博学南楼C202': '102C0202',
                 '博学南楼C203': '102C0203', '博学南楼C204': '102C0204', '博学南楼C205': '102C0205',
                 '博学南楼C206': '102C0206', '博学南楼C207': '102C0207', '博学南楼C208': '102C0208',
                 '博学南楼C209': '102C0209', '博学南楼C301': '102C0301', '博学南楼C302': '102C0302',
                 '博学南楼C303': '102C0303', '博学南楼C304': '102C0304', '博学南楼C305': '102C0305',
                 '博学南楼C306': '102C0306', '博学南楼C307': '102C0307', '博学南楼C308': '102C0308',
                 '博学南楼C401': '102C0401', '博学南楼C403': '102C0402', '博学南楼C404': '102C0403',
                 '博学南楼C405': '102C0404', '博学南楼C406': '102C0405', '博学南楼C407': '102C0406',
                 '博学南楼C408': '102C0407', '博学南楼C409': '102C0408', '博学南楼C501': '102C0501',
                 '博学南楼C502': '102C0502', '博学南楼D403': '102D0403', '博学南楼D404': '102D0404',
                 '博学南楼D405': '102D0405', '博学南楼D406': '102D0406', '博学南楼D407': '102D0407',
                 '博学南楼D408': '102D0408', '博学南楼D409': '102D0409',
                 # '艺术楼A107': '1040094',
                 # '艺术楼A105': '1040096', '社科楼B400': '105B0400', '理工楼B202': '109B0202',
                 # '理工楼C216': '109C0216', '人文楼A-101': '110A0001', '人文楼B102': '110B0102',
                 # '人文楼C410': '110C0410', '人文楼C412': '110C0412', '人文楼C501': '110C0501',
                 # '人文楼C502': '110C0502', '人文楼C503': '110C0503', '人文楼C505': '110C0505',
                 # '人文楼C507': '110C0507', '戏剧影视厅（黑匣子）': '1220006'
}

class Parse:
    def __init__(self, data, xh):
        self.data = data
        self.xh = xh

    def get_grades(self):
        try:
            coded_data = re.findall(r'b<.*?>', self.data)[0][2:-1]
            encodestr = base64.b64decode(str.encode(coded_data))
            score_string = encodestr.decode('utf-8', 'ignore')
            soup = BeautifulSoup(score_string, "lxml")
            score_list = []
            tables = soup.findAll('table')


            for item in tables:
                try:
                    score_dict = {}
                    item_string = str(item)
                    score_dict['course'] = item.kcmc.contents[0]
                    # if '足球-俱乐部制-男' in score_dict['course']:
                    #     print(item)
                    if 'pscj' in item_string:
                        score_dict['daily_score'] = item.pscj.contents[0]
                    elif 'sycj' in item_string:
                        score_dict['daily_score'] = item.sycj.contents[0]
                    if 'qmcj' in item_string:
                        score_dict['test_score'] = item.qmcj.contents[0]
                    elif 'sycj' in item_string:
                        score_dict['test_score'] = item.sycj.contents[0]
                    try:
                        score_dict['daily_score']
                        score_dict['test_score']
                    except:
                        score_dict['daily_score'] = item.zscj.contents[0]
                        score_dict['test_score'] = item.zscj.contents[0]

                    if 'qzcj' in item_string:
                        qzcj = item.qzcj.contents[0]
                        score_dict['test_score'] = '(' + qzcj + ')' + score_dict['test_score']

                    score_dict['final_score'] = item.zscj.contents[0]

                    score = Score()
                    score.code = item.kcdm.contents[0]
                    score.xh = self.xh
                    # score.xh = encode(self.xh)
                    score.name = item.kcmc.contents[0]
                    score.category = item.kcxz.contents[0]
                    score.xf = item.xf.contents[0]
                    score.daily_score = score_dict['daily_score']
                    score.test_score = score_dict['test_score']
                    score.final_score = score_dict['final_score']
                    try:
                        score.source = item.xymc.contents[0]
                    except:
                        pass

                    try:
                        score.save()
                    except:
                        pass
                    score_list.append(score_dict)
                except:
                    pass
                # score.save()
                # many to many
                # prerequisite: two objects already exists
                # Face error directly, think about it.
                # user = AHUUser.objects.filter(number=self.xh)[0]
                # score.number.add(user)
                # score.save()
        except:
            score_list = []
        return score_list

        # p1 = re.compile(r';l<(.*?);>>;>;;>;', re.S)
        # data1 = re.findall(p1, self.data)
        # data2 = [i for i in data1 if ((len(i) <= 30) & (len(i) >= 2))]  # 删除过长元素
        # # print(data1)
        # # print("________")
        # pattern1 = re.compile(r'[o<](.*?)[>]')
        # pattern2 = re.compile(r'&(.*?)\\')
        # pattern3 = re.compile(r'\\(.*?)e')
        # data3 = [unit for unit in data2 if
        #          ((pattern1.match(unit) == None) and (pattern2.match(unit) == None) and (pattern3.match(unit) == None))]
        # data4 = data3[8:-2]
        # while "理论课" in data4:
        #     data4.remove("理论课")
        # for i in range(len(data4)):
        #     if ((data4[i] == "体育军事教学部") or (data4[i] == "教务处") or (data4[i] == "大学外语教学部")):
        #         data4[i] = data4[i - 1]
        #     data4[i] = data4[i].lstrip()
        #     if (i + 2 <= len(data4)):
        #         if ((data4[i] == "素质教育选修课") & (data4[i + 1] == "素质教育选修课")):
        #             data4.remove(data4[i])
        #     if i + 1 == len(data4):
        #         break
        # pattern4 = re.compile(r'\d[.]\d')
        # data5 = []
        # # print(data4)
        # for i in range(len(data4)):
        #     if i + 4 == len(data4):
        #         break
        #     if data4[i][0] >= 'A' and data4[i][0] <= 'Z' and data4[i][2].isdigit():
        #         data5.append(data4[i + 1])
        #     if ((pattern4.match(data4[i]) != None) & (pattern4.match(data4[i + 1]) != None)):
        #         data5.append(data4[i + 2])
        #         data5.append(data4[i + 3])
        #         data5.append(data4[i + 4])
        #     if ((pattern4.match(data4[i - 1]) == None) & (pattern4.match(data4[i]) != None) & (
        #             pattern4.match(data4[i + 1]) == None)):
        #         data5.append(data4[i + 1])
        #         j = 0
        #         while (True):
        #             if i + j == len(data4):
        #                 break
        #             if (data4[i + j][0] >= 'A' and data4[i + j][0] <= 'Z' and data4[i + j][2].isdigit()) == False:
        #                 j = j + 1
        #             else:
        #                 break
        #         data5.append(data4[i + j - 4])
        #         data5.append(data4[i + j - 3])
        #         # print(data5)
        # score_list = []
        # for i in range(1, int(len(data5) / 4) + 1):
        #     score_dict = {}
        #     score_dict['course'] = data5[(i - 1) * 4]
        #     score_dict['daily_score'] = data5[(i - 1) * 4 + 1]
        #     score_dict['test_score'] = data5[(i - 1) * 4 + 2]
        #     score_dict['final_score'] = data5[(i - 1) * 4 + 3]
        #     model_grade = Top()
        #     model_grade.course = score_dict['course']
        #     model_grade.daily_score = score_dict['daily_score']
        #     model_grade.test_score = score_dict['test_score']
        #     model_grade.final_score = score_dict['final_score']
        #     model_grade.belongs_to = Auser.objects.filter(number=self.xh)[0]
        #     model_grade.save()
        #     score_list.append(score_dict)
        # return score_list

class Spider:

    def __init__(self, url):
        # create request headers
        self.Url = url
        agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        self.postUrl = self.Url + '/default2.aspx'
        self.headers = {
            'Referer': self.postUrl,
            'User-Agent': agent
        }
        self.session = requests.session()
        # proxies = {'http': 'http://127.0.0.1:8081'}
        # try:
        #     self.session.proxies = proxies
        # except:
        #     pass
        self.session.cookies = http.cookiejar.LWPCookieJar(filename='cookie')

    def getCheckCode(self):
        imgUrl = self.Url + '/CheckCode.aspx'
        img = self.session.get(imgUrl)
        with open('./checkCode.jpg', 'wb') as f:
            f.write(img.content)
        try:
            # image = Image.open('{}/checkCode.jpg'.format(os.getcwd()))
            # image.show()
            # code = input("验证码是:")
            code = recognizer.recognize_checkcode('./checkCode.jpg')
            return code
        except:
            return -1

    def killCheckCode(self):
        f1 = open('./kill_check_url', 'r')
        kill_url = f1.read()
        f1.close()
        files = {'img': ('checkCode.jpg', open('./checkCode.jpg', 'rb'), 'image/png')}
        res = requests.post(kill_url, files=files)
        return re.search(r"{{(....)}}", res.text).group(1)

    def login(self, xh, password):
        # create post data
        self.xh = xh
        self.password = password
        RadioButtonList1 = u"学生".encode('gb2312', 'replace')
        res = self.session.get(self.postUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        # if EC.alert_is_present:
        #    driver.switch_to_alert().accept()

        # viewstate = soup.find('input', id='__VIEWSTATE').get('value')
        viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        # try:
        #     eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
        # except:
        #     pass
        get_code = self.getCheckCode()
        if get_code == -1:
            return -1
        # 验证码识别错误
        else:
            postData = {
                'Button1': '',
                'RadioButtonList1': RadioButtonList1,
                'TextBox2': password,
                # '__EVENTVALIDATION': eventvalidation,
                '__VIEWSTATE': viewstate,
                'hidPdrs': '',
                'hidsc': '',
                'lbLanguage': '',
                'txtSecretCode': self.getCheckCode(),
                'txtUserName': xh
            }
        loginPage = self.session.post(self.postUrl, data=postData, headers=self.headers)
        self.session.cookies.save()

    def getInfo(self):
        infoUrl = self.Url + '/xsgrxx.aspx?xh=' + self.xh + '&'
        self.session.headers['Referer'] = self.Url + '/xs_main.aspx?xh=' + self.xh
        res = self.session.get(infoUrl)
        handler = info_Handler(res.text)
        self.name = handler.getInfo('name')
        self.xm = parse.quote(self.name.encode('gb2312'))

    def getCourseSchedule(self):
        # 03
        # csUrl = self.Url + '/xskbcx.aspx?xh=' + self.xh + '&xm=' + self.xm + '&gnmkdm=N121615'
        csUrl = self.Url + '/xsxkqk.aspx?xh=' + self.xh
        res = self.session.get(csUrl, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        postData = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddlXQ',
            '__VIEWSTATE': viewstate,
            'ddlXN': '2018-2019',
            'ddlXQ': '1',
        }
        res = self.session.post(csUrl, data=postData, headers=self.headers)

        res.encoding = 'gb2312'
        handler = courseSchedule_Handler(res.text)
        course = handler.handleCourse(res.text)
        # course = handleCourse(res.text)
        return course

    def getScore(self):
        # get Score
        # try:
        scoreUrl = self.Url + '/xscjcx.aspx?xh=' + self.xh + '&xm=' + '%CD%F5%D3%E5%B4%A8' + '&gnmkdm=N121605'
        print(scoreUrl)
        headers1 = {
            'Referer': 'http://jw3.ahu.cn/xs_main.aspx?xh=E31614002',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',

        }
        # self.session.headers['Referer'] = 'http://jw3.ahu.cn/xs_main.aspx?xh=E31614002'
        res = self.session.get(scoreUrl, headers=headers1)
        soup = BeautifulSoup(res.text, 'html.parser')
        print(res.text)
        # viewstate = soup.find('input', id='__VIEWSTATE').get('value')
        # __VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']

        viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']

        # eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
        postData = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            # '__EVENTVALIDATION': eventvalidation,
            '__VIEWSTATE': viewstate,
            'btn_zcj': u'历年成绩'.encode('gb2312', 'replace'),
            'ddlXN': '',
            'ddlXQ': '',
            'ddl_kcxz': '',
            'hidLanguage': ''
        }
        # except:
        #     scoreUrl = self.Url + '/xscjcx_dq.aspx?xh=' + self.xh + '&xm=' + '%CD%F5%D3%E5%B4%A8' + '&gnmkdm=N121605'
        #     self.session.headers['Referer'] = 'http://jw3.ahu.cn/xs_main.aspx?xh=E31614002'
        #     res = self.session.get(scoreUrl)
        #     soup = BeautifulSoup(res.text, 'html.parser')
        #     # viewstate = soup.find('input', id='__VIEWSTATE').get('value')
        #     # eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
        #     viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        #     postData = {
        #         '__EVENTARGUMENT': '',
        #         '__EVENTTARGET': '',
        #         # '__EVENTVALIDATION': eventvalidation,
        #         '__LASTFOCUS': '',
        #         '__VIEWSTATE': viewstate,
        #         'btnCx': u' 查  询 '.encode('gb2312', 'replace'),
        #         'ddlxn': u'全部'.encode('gb2312', 'replace'),
        #         'ddlxq': u'全部'.encode('gb2312', 'replace')
        #     }

        res = self.session.post(scoreUrl, data=postData, headers=self.headers)
        res.encoding = 'gb2312'
        handler = score_Handler(res.text)
        grades = handler.writeToFile('templates/score.html')
        print('grades:', grades)
        return grades

    def getHiddenScore(self):
        try:
            scoreUrl = self.Url + '/xscjcx.aspx?xh=' + self.xh
            self.session.headers['Referer'] = scoreUrl
            res = self.session.get(scoreUrl)
            soup = BeautifulSoup(res.text, 'html.parser')
            # viewstate = soup.find('input', id='__VIEWSTATE').get('value')
            # __VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']

            viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']

            # eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
            postData = {
                '__EVENTARGUMENT': '',
                '__EVENTTARGET': '',
                # '__EVENTVALIDATION': eventvalidation,
                '__VIEWSTATE': viewstate,
                'btn_zcj': u'历年成绩'.encode('gb2312', 'replace'),
                'ddlXN': '',
                'ddlXQ': '',
                'ddl_kcxz': '',
                'hidLanguage': ''
            }
        except:
            scoreUrl = self.Url + '/xscjcx_dq.aspx?xh=' + self.xh
            self.session.headers['Referer'] = scoreUrl
            res = self.session.get(scoreUrl)
            soup = BeautifulSoup(res.text, 'html.parser')
            # viewstate = soup.find('input', id='__VIEWSTATE').get('value')
            # eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
            viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
            postData = {
                '__EVENTARGUMENT': '',
                '__EVENTTARGET': '',
                # '__EVENTVALIDATION': eventvalidation,
                '__LASTFOCUS': '',
                '__VIEWSTATE': viewstate,
                'btnCx': u' 查  询 '.encode('gb2312', 'replace'),
                'ddlxn': u'全部'.encode('gb2312', 'replace'),
                'ddlxq': u'全部'.encode('gb2312', 'replace')
            }
        res = self.session.post(scoreUrl, data=postData, headers=self.headers)
        score_soup = BeautifulSoup(res.text, 'html.parser')
        viewstate = score_soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        encodestr = base64.b64decode(str.encode(viewstate))
        decoded = encodestr.decode('utf-8', 'ignore')


        # start = time.clock()
        parse = Parse(decoded, self.xh)
        grades = parse.get_grades()
        # 效率问题的疑问
        # elapsed = (time.clock() - start)

        return grades


    def get_empty_room(self, kssj, jssj, xqj, sdj, dsz):
        url = self.Url + '/xxjsjy.aspx?xh=' + self.xh + '&xm=' + '%CD%F5%D3%E5%B4%A8' + '&gnmkdm=N121611'
        self.session.headers['Referer'] = url
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        postData = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            '__VIEWSTATE': viewstate,
            'xiaoq': '1',
            'jslb': '%B6%E0%C3%BD%CC%E5%BD%CC%CA%D2',
            'min_zws': '0',
            'max_zws': '',
            'kssj': kssj,
            'jssj': jssj,
            'xqj': xqj,
            'ddlDsz': dsz,
            'sjd': sdj,
            'Button2': '%BF%D5%BD%CC%CA%D2%B2%E9%D1%AF',
            'dpDataGrid1%3AtxtChoosePage': '1',
            'dpDataGrid1%3AtxtPageSize': '300',
            'xn': '2018-2019',
            'xq': '1',
            'jsbh': '101A0101',
            'ddlSyXn': '2018-2019',
            'ddlSyxq': '1',
        }
        res = self.session.post(url, data=postData, headers=self.headers)
        doc = pq(res.text)
        score_soup = BeautifulSoup(res.text, 'html.parser')
        viewstate = score_soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        encodestr = base64.b64decode(str.encode(viewstate))

        decoded = encodestr.decode('utf-8', 'ignore')
        html = re.findall(r'b<(.*?)>', decoded)[0]
        new_html = base64.b64decode(str.encode(html))
        html_string = new_html.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html_string, "html.parser")
        tables = soup.findAll('table')
        for item in tables:
            room_dict = {}
            classroom_num_list = []
            classroom_name_list = []
            classroom_type_list = []
            college_list = []
            classroomsite_num_list = []
            testroomsite_num_list = []
            collegename_list = []
            item_string = str(item)
            classroom_num_list = re.findall('教室编号&gt;(.*?)<!--教室编号-->', item_string)
            classroom_name_list = re.findall('教室名称&gt;(.*?)<!--教室名称-->', item_string)
            classroom_type_list = re.findall('教室类别&gt;(.*?)<!--教室类别-->', item_string)
            college_list = re.findall('校区&gt;(.*?)<!--校区-->', item_string)
            classroomsite_num_list = re.findall('上课座位数&gt;(.*?)<!--上课座位数-->', item_string)
            testroomsite_num_list = re.findall('考试座位数&gt;(.*?)<!--考试座位数-->', item_string)
            collegename_list = re.findall('校区名称&gt;(.*?)<!--校区名称-->', item_string)

            # 检查是否有空字段
            if not classroom_num_list:
                classroom_num_list.append('')
            if not classroom_name_list:
                classroom_name_list.append('')
            if not classroom_type_list:
                classroom_type_list.append('')
            if not college_list:
                college_list.append('')
            if not classroomsite_num_list:
                classroomsite_num_list.append('')
            if not testroomsite_num_list:
                testroomsite_num_list.append('')
            if not collegename_list:
                collegename_list.append('')

            data = {
                'classroom_num': classroom_num_list[0],
                'classroom_name': classroom_name_list[0],
                'classroom_type': classroom_type_list[0],
                'college': college_list[0],
                'classroomsite_num': classroomsite_num_list[0],
                'testroomsite_num': testroomsite_num_list[0],
                'collegename': collegename_list[0],
                'time': doc('#lblbt').text(),
            }
            print(data)

    def get_useroom(self, kssj, jssj, xqj, sdj, jsbh):
        url = self.Url + '/xxjsjy.aspx?xh=' + self.xh + '&xm=' + '%CD%F5%D3%E5%B4%A8' + '&gnmkdm=N121611'
        # self.session.headers['Referer'] = Referer_url
        headers1 = {
            'Referer': 'http://jw3.ahu.cn/xs_main.aspx?xh=E31614002',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',

        }
        res = self.session.get(url, headers=headers1)
        soup = BeautifulSoup(res.text, 'html.parser')
        viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        postData = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            '__VIEWSTATE': viewstate,
            'xiaoq': '1',
            'jslb': "多媒体教室",
            'min_zws': '0',
            'max_zws': '',
            'ddlSyXn': '2018-2019',
            'ddlSyxq': '1',
            'Button1': "使用情况查询",
            'kssj': kssj,
            'jssj': jssj,
            'xqj': xqj,
            'ddlDsz': "单",
            'sjd': sdj,
            'xn': '2018-2019',
            'xq': '1',

        }
        data_gb2312 = urlencode(postData, encoding='gb2312')
        self.headers['Referer'] = 'http://jw3.ahu.cn/xxjsjy.aspx?xh=E31614002&xm=%CD%F5%D3%E5%B4%A8&gnmkdm=N121611'
        # self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        # self.headers['Origin'] = 'http://jw3.ahu.cn'
        # self.headers['Host'] = 'jw3.ahu.cn'
        # self.headers['Connection'] = 'close'
        # self.headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
        # self.headers['Cookie'] = 'ASP.NET_SessionId=gstmpuass2lomx45rka5fv45; tabId=ext-comp-1004'

        res1 = self.session.post(url, data=data_gb2312, headers=self.headers)
        doc = pq(res1.text, parser="html")
        viewstate1 = doc('#Form1 > input[type="hidden"]:nth-child(3)').attr("value")

        postData1 = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            '__VIEWSTATE': viewstate1,
            'xiaoq': '1',
            'jslb': "多媒体教室",
            'min_zws': '0',
            'max_zws': '',
            'jsbh': jsbh,
            'ddlSyXn': '2018-2019',
            'ddlSyxq': '1',
            'Button1': "使用情况查询",
            'dpDatagrid3:txtChoosePage': '1',
            'dpDatagrid3:txtPageSize': '300',
            'kssj': kssj,
            'jssj': jssj,
            'xqj': xqj,
            'ddlDsz': "单",
            'sjd': sdj,
            'xn': '2018-2019',
            'xq': '1',

        }
        data_gb2312_1 = urlencode(postData1, encoding='gb2312')
        res2 = self.session.post(url, data=data_gb2312_1, headers=self.headers)
        doc1 = pq(res2.text, parser="html")
        viewstate2 = doc1('#Form1 > input[type="hidden"]:nth-child(3)').attr("value")
        encodestr1 = base64.b64decode(str.encode(viewstate2))

        decoded = encodestr1.decode('utf-8', 'ignore')
        html = re.findall(r'b<(.*?)>', decoded)[0]
        new_html = base64.b64decode(str.encode(html))
        html_string = new_html.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html_string, "html.parser")
        tables = soup.findAll('table')
        data_list = []
        for item in tables:
            item_string = str(item)
            begin_list = re.findall('开始周&gt;(.*?)<!--开始周-->', item_string)
            end_list = re.findall('结束周&gt;(.*?)<!--结束周-->', item_string)
            weekday_list = re.findall('星期几&gt;(.*?)<!--星期几-->', item_string)
            detailtime_list = re.findall('具体时间&gt;(.*?)<!--具体时间-->', item_string)
            week_list = re.findall('单双周&gt;(.*?)<!--单双周-->', item_string)
            howuse_list = re.findall('使用方式&gt;(.*?)<!--使用方式-->', item_string)

            # 检查是否有空字段
            if not begin_list:
                begin_list.append('')
            if not end_list:
                end_list.append('')
            if not weekday_list:
                weekday_list.append('')
            if not detailtime_list:
                detailtime_list.append('')
            if not week_list:
                week_list.append('')
            if not howuse_list:
                howuse_list.append('')
            data = {
                'begin_list': begin_list[0],
                'end_list': end_list[0],
                'weekday_list': weekday_list[0],
                'detailtime_list': detailtime_list[0],
                'week_list': week_list[0],
                'howuse_list': howuse_list[0],
            }
            data_list.append(data)
            print(data)
        return data_list

import ast
import re
import json

def out(info):
    name = info[0]
    position = info[3]
    ls = info[2]
    start_number = info[5]
    week_day = info[4]
    if '周一' in info[1]:
        week_day = 1
    elif '周二' in info[1]:
        week_day = 2

    elif '周三' in info[1]:
        week_day = 3
    elif '周四' in info[1]:
        week_day = 4
    elif '周五' in info[1]:
        week_day = 5
    elif '周六' in info[1]:
        week_day = 6
    elif '周七' in info[1]:
        week_day = 7
    if info[1][0] != '{':
        number = []
        tmp = ''
        for i in info[1]:
            if i.isdigit():
                tmp = tmp + i
            else:
                if tmp != '':
                    number.append(tmp)
                tmp = ''

        if number.__len__() == 5:
            long = str(3)
        elif number.__len__() == 4:
            long = str(2)
        else:
            long = str(1)

        if number != []:
            start_week = number[-2]
            end_week = number[-1]



    else:
        number = []
        tmp = ''
        for i in info[1]:
            if i.isdigit():
                tmp = tmp + i
            else:
                if tmp != '':
                    number.append(tmp)
                tmp = ''
        # length = number.__len__()
        # if length == 3:
        #     long = str(1)
        # elif length = 4:
        #     long = str(2)
        # else:
        #     long = str(3)
        # long = chr(ord(info[1][5]) - ord(info[1][3]) + 1 + ord('0'))
        long = number[-1]
        start_week = number[0]
        end_week = number[1]

    if info[1].find('单') != -1:
        dsz = '1'
    elif info[1].find('双') != -1:
        dsz = '2'
    else:
        dsz = '0'

    ans = {}
    ans['xqj'] = week_day
    ans['skjc'] = start_number
    ans['skcd'] = long
    ans['kcmc'] = name
    ans['kcdd'] = position
    ans['qszs'] = start_week
    ans['jszs'] = end_week
    ans['dsz'] = str(dsz)
    ans['ls'] = ls
    ans['append_info'] = info[6]

    return ans


def start(day):
    if re.findall(r"第(.+?)", day):
        return re.findall(r"第(.+?)", day)[0]
    else:
        return ''


def length(day):
    info_list = re.findall(r"第(.+?)节{第", day)
    number = []
    for info in info_list:
        for n in info.split(','):
            number.append(n)
    return int(number[-1]) - int(number[0]) + 1


def start_week(day):
    if re.findall(r"\{第(.+?)\-", day):
        return re.findall(r"\{第(.+?)\-", day)[0]
    else:
        return ''


def end_week(day):
    if re.findall(r"\-(.+?)周", day):
        return re.findall(r"\-(.+?)周", day)[0]
    else:
        return ''


def flag(day):
    if re.findall(r"\|(.+?)周", day):
        f = re.findall(r"\|(.+?)周", day)[0]
        if f == '单':
            return 1
        elif f == '双':
            return 2
    else:
        return 0

def weekday(info):
    if '周一' in info:
        week_day = 1
    elif '周二' in info:
        week_day = 2

    elif '周三' in info:
        week_day = 3
    elif '周四' in info:
        week_day = 4
    elif '周五' in info:
        week_day = 5
    elif '周六' in info:
        week_day = 6
    elif '周日' in info:
        week_day = 7
    return week_day


class courseSchedule_Handler:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.table = self.soup.find('table', class_='datelist')

    def handleCourse(self, html):
        soup = self.table
        tr_list = soup.findAll('tr')
        course_list = []
        for tr in tr_list:
            course_dict = {}
            try:
                if 'datelisthead' not in str(tr):
                    td_list = tr.findAll('td')
                    info = td_list[8].find('span').contents[0]
                    info_list = info.split(';')
                    postion_list = td_list[9].contents[0].split(';')
                    # if info_list.__len__() == 2 and weekday(info_list[0]) != weekday(info_list[1]):
                    for info in info_list:
                        course_dict = {}

                        # if start_week(info)
                        course_dict["kcmc"] = td_list[2].find('a').contents[0]

                        # teacher
                        course_dict["ls"] = td_list[5].find('a').contents[0]

                        # start
                        course_dict["skjc"] = int(start(info))
                        # course length
                        course_dict["skcd"] = int(length(info))

                        # start week
                        course_dict["qszs"] = int(start_week(info))
                        # end week
                        course_dict["jszs"] = int(end_week(info))
                        # 单双周flag
                        course_dict["dsz"] = flag(info)
                        # position
                        # course_dict["kcdd"] = parse_position(td_list[9].contents[0])
                        course_dict["kcdd"] = postion_list[info_list.index(info)]
                        # weekday
                        course_dict["xqj"] = int(weekday(info))
                        course_list.append(course_dict)
            except:
                pass

        course_collect = []
        add_flag = [0] * course_list.__len__()
        for course in course_list:
            try:
                i = course_list.index(course)
                for course_diff in course_list:
                    j = course_list.index(course_diff)
                    if (course["kcmc"] == course_diff["kcmc"] and course["xqj"] == course_diff["xqj"] and (
                            course["qszs"] == course_diff["qszs"] or course["jszs"] == course_diff["jszs"]) and course[
                        "skjc"] != course_diff["skjc"] and add_flag[i] == 0 and add_flag[j] == 0 and (course["skjc"] + course["skcd"] == course_diff["skjc"] or course["skjc"] == course_diff["skjc"]+course_diff["skcd"])):
                        # 两个课程对象的start week == end week, add_flag 都置为1

                        if (course["qszs"] == course_diff["qszs"] and course["jszs"] == course_diff["jszs"]):
                            if (add_flag[i] == 0 and add_flag[j] == 0):
                                tmp = {}
                                add_flag[i] = add_flag[j] = 1
                                tmp = course
                                tmp["skcd"] = course["skcd"] + course_diff["skcd"]
                                course_collect.append(tmp)
                                break
                        # 情况比较复杂, 可以借用数轴, 使用画图的方式思考问题
                        # 其中一个的start week大, 说明一个是另一个的子集. 把start week大的那个课程对象, add_flag 置 1, 并把start week小的那个课程的start week赋值为.
                        if (course["qszs"] > course_diff["qszs"]):
                            course_diff["jszs"] = course["qszs"] - 1
                            if (add_flag[i] == 0 and add_flag[j] == 0):
                                add_flag[i] = 1
                                tmp = course
                                tmp["skjc"] = min(course["skjc"], course_diff["skjc"])
                                tmp["skcd"] = course["skcd"] + course_diff["skcd"]
                                course_collect.append(tmp)
                                tmp = {}
                                break

                        if (course["jszs"] < course_diff["jszs"]):

                            course_diff["qszs"] = course["jszs"] + 1
                            if (add_flag[i] == 0 and add_flag[j] == 0):
                                add_flag[i] = 1
                                tmp = course
                                tmp["skjc"] = min(course["skjc"], course_diff["skjc"])
                                tmp["skcd"] = course["skcd"] + course_diff["skcd"]
                                course_collect.append(tmp)
                                tmp = {}
                                break
                        if (course["qszs"] < course_diff["qszs"]):
                            course["jszs"] = course_diff["qszs"] - 1
                            if (add_flag[i] == 0 and add_flag[j] == 0):
                                add_flag[j] = 1
                                tmp = course_diff
                                tmp["skjc"] = min(course["skjc"], course_diff["skjc"])
                                tmp["skcd"] = course["skcd"] + course_diff["skcd"]
                                course_collect.append(tmp)
                                tmp = {}
                                break
                        if (course["jszs"] > course_diff["jszs"]):
                            course["qszs"] = course_diff["jszs"] + 1
                            add_flag[j] = 1
                            tmp = course_diff
                            tmp["skjc"] = min(course["skjc"], course_diff["skjc"])
                            tmp["skcd"] = course["skcd"] + course_diff["skcd"]
                            course_collect.append(tmp)
                            tmp = {}
                            break
                if (add_flag[i] == 0):
                    course_collect.append(course)
                    add_flag[i] == 1
            except:
                pass
            #     print(course)

        # 减少由于bug导致的异常

        # for course in course_collect:
        #     i = course_list.index(course)
        #     if (add_flag[i] == 0):
        #         course_collect.append(course)
        for course in course_collect:
            if (course["skcd"] > 4):
                course["skcd"] = 4
        return course_collect

    def writeToFile(self):
        soup = self.table
        tr_list = soup.findAll('tr')

        i = -1
        course_list = []
        for tr in tr_list:
            if i < 1:
                pass
            else:
                tr = str(tr)
                tr = BeautifulSoup(tr, "lxml")

                td_list = tr.findAll('td')
                week_day = 0

                tmp = []
                for td in td_list:

                    td = str(td)
                    if re.match('<td>第\d{1,2}节</td>', td) or 'style="width:1%' in td:
                        # if td.__len__() < 70:
                        continue
                    week_day = week_day + 1
                    td = td[:-5] + '<br/>' + str(week_day) + td[-5:]
                    td = td[:-5] + '<br/>' + str(i) + td[-5:]

                    if td.__len__() > 70:
                        tmp.append(td)

                for td in tmp:

                    soup = BeautifulSoup(td, "lxml")
                    string = soup.td.contents

                    cnt = 0

                    info = [""] * 7

                    for x in string:
                        x = str(x)

                        if cnt == -1:
                            cnt = 0
                            continue
                        if str(x) == '<br/>':
                            continue
                        if '<font' in str(x):
                            info[6] = str(x)[18:-7]
                            continue

                        info[cnt] = x
                        cnt = cnt + 1
                        if cnt == 4:
                            info[4] = string[-3]

                            info[5] = string[-1]

                            cnt = -1
                            try:
                                ans = out(info)
                            except:
                                continue
                            course_list.append(ans)

                            for course in course_list:

                                tmp2 = course
                                # course = ast.literal_eval(course)
                                for course_diff in course_list:
                                    tmp = course_diff

                                    # course_diff = ast.literal_eval(course_diff)
                                    if course['kcmc'] == course_diff['kcmc'] and course['skjc'] != course_diff[
                                        'skjc'] and course['xqj'] == course_diff['xqj']:
                                        course['skcd'] = str(int(course['skcd']) + int(course_diff['skcd']))
                                        # new_course = json.dumps(course, ensure_ascii=False)
                                        course_list.remove(tmp)
                                        course_list.remove(tmp2)
                                        course_list.append(course)
                                    if course['xqj'] == course_diff['xqj'] and course['skjc'] == course_diff['skjc'] and \
                                            course['kcmc'] == course_diff['kcmc']:
                                        if course['append_info'] == "":
                                            course['append_info'] = course_diff['append_info']
                                        else:
                                            course_diff['append_info'] = course['append_info']

            i = i + 1

        return course_list


class info_Handler:

    def __init__(self, html):
        self.Info = {}
        soup = BeautifulSoup(html, 'html.parser')
        self.Info['name'] = soup.find('table', 'formlist').find_all('tr')[1].find_all('td')[1].find('span').text

    def getInfo(self, Attr):
        return self.Info[Attr]


from decimal import *


class score_Handler:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.table = self.soup.find('table', class_='datelist')

    def writeToFile(self, filename):
        try:
            grades = []
            grade_list = []
            grade_dict = {}
            scores = []
            soup = self.table
            tr_list = soup.findAll('tr')
            tr_list = tr_list[1:]
            total_credit = 0
            total = 0
            term_total_credit = 0
            term_total = 0
            year_total_credit = 0
            year_total = 0
            tr = tr_list[-1]
            td_list = tr.findAll('td')
            term_year = str(td_list[0])[4:-5]
            term_num = str(td_list[1])[4:-5]
            grade_dict['term_year'] = term_year
            grade_dict['term_num'] = term_num
            getcontext().prec = 16
            for tr in tr_list:
                tr = str(tr)
                tr = BeautifulSoup(tr, "lxml")

                td_list = tr.findAll('td')
                if str(td_list[0])[4:-5] == term_year:
                    if str(td_list[1])[4:-5] == term_num:
                        score = {}
                        score['subject'] = str(td_list[3])[4:-5]
                        score['property'] = str(td_list[4])[4:-5]
                        score['credit'] = str(td_list[6])[4:-5]
                        score['grade'] = str(td_list[8])[4:-5]
                        score['pa'] = str(td_list[7])[7:-5]
                        scores.append(score)
                        term_total_credit = term_total_credit + Decimal(score['credit'])
                        term_total = term_total + Decimal(score['pa']) * Decimal(score['credit'])

                    year_total_credit = year_total_credit + Decimal(str(td_list[6])[4:-5])
                    year_total = year_total + Decimal(str(td_list[7])[7:-5]) * Decimal(str(td_list[6])[4:-5])

                total_credit = total_credit + Decimal(str(td_list[6])[4:-5])
                total = total + Decimal(str(td_list[7])[7:-5]) * Decimal(str(td_list[6])[4:-5])

            grade_dict['GPA'] = str(total / total_credit)[:4]
            grade_dict['term_num_GPA'] = str(term_total / term_total_credit)[:4]
            grade_dict['term_year_GPA'] = str(year_total / year_total_credit)[:4]
            grade_list.append(grade_dict)
            grades.append(grade_list)
            grades.append(scores)
        except:
            grades = []
        return grades



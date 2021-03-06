from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyquery import PyQuery as pq
from django.utils.safestring import mark_safe
import time
from spider.spiderClass import *


def TestSpider1(request, username, password):
    context = {}

    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chromeOption.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    chromeOption.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chromeOption.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chromeOption.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chromeOption.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

    browser = webdriver.Chrome(executable_path='E:\Blog\chrome\chromedriver.exe', options=chromeOption)
    browser.get('http://zf.ahu.cn/')
    browser.implicitly_wait(10)  # 等待网页加载
    browser.find_element_by_id('username').clear()
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').clear()
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_id('btnLogin').click()

    browser.get('http://zf.ahu.cn/ksgl/student/KSCX/KSCXIndex')
    browser.implicitly_wait(10)  # 等待网页加载
    pageList = []
    Select(browser.find_element_by_id('XQ')).select_by_value('1')
    time.sleep(2)
    doc = pq(browser.page_source, parser="html")
    items = doc('#KSCXdataTable > tbody > tr').items()
    th = '''
        <tr>
            <td style="text-align: left;">选课课号</td>
            <td style="text-align: left;">课程名称</td>
            <td style="text-align: left;">姓名</td>
            <td style="text-align: left;">考试时间</td>
            <td style="text-align: left;">考试地点</td>
            <td style="text-align: left;">考试形式</td>
            <td style="text-align: left;">座位号</td>
            <td style="text-align: left;">校区</td>
        </tr>
    '''
    pageList.append(th)
    for item in items:
        pageList.append(str(item))

    pageStr = "".join(pageList)
    pageStr = mark_safe(pageStr)
    context['pageStr'] = pageStr
    browser.close()  # 关闭浏览器
    return render(request, 'spider/SpiderResult.html', context)

def TestSpider(request):
    if request.method == 'POST':
        return TestSpider1(request, request.POST.get("username"), request.POST.get("password"))
    return render(request, 'spider/TestSpider.html')


def EducationSpider1(request, username, password):
    context = {}

    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chromeOption.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    chromeOption.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chromeOption.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chromeOption.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chromeOption.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

    browser = webdriver.Chrome(executable_path='E:\Blog\chrome\chromedriver.exe', options=chromeOption)
    browser.get('http://zf.ahu.cn/')
    browser.implicitly_wait(10)  # 等待网页加载
    browser.find_element_by_id('username').clear()
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').clear()
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_id('btnLogin').click()

    browser.get('http://zf.ahu.cn/cjgl/Student/CJCX/KCCJCX')
    browser.implicitly_wait(10)  # 等待网页加载
    doc = pq(browser.page_source, parser="html")
    pageList = []
    items = doc('#KCTJFX > .panel-body > table > tbody > tr').items()
    for item in items:
        pageList.append(str(item))

    pageStr = "".join(pageList)
    pageStr = mark_safe(pageStr)
    context['pageStr'] = pageStr
    browser.close()  # 关闭浏览器
    return render(request, 'spider/SpiderResult.html', context)


def EducationSpider(request):
    if request.method == 'POST':
        return EducationSpider1(request, request.POST.get("username"), request.POST.get("password"))
    return render(request, 'spider/EducationSpider.html')


def mainspider(request):
    return render(request, 'spider/index.html')

def SchoolSpider(request):
    if request.method == 'POST':
        spider = Spider('http://jw3.ahu.cn')
        xh = request.POST.get("username")
        password = request.POST.get("password")
        print(xh, password)
        if xh and password:
            spider.login(xh, password)
            # spider.getScore()

            for week in range(17, 19):  # 爬取17-18周
                djz = str(week)
                dsz = dsz_dict[str(week % 2)]
                for day in range(1, 8):  # 周一到周末
                    xqj = str(day)
                    for index in sdj_dict:  # 从早到晚
                        sdj = sdj_dict[index]
                        kssj = xqj + djz
                        jssj = xqj + djz
                        # print(index)
                        # print(kssj, jssj, xqj, sdj, dsz)
                        html = spider.get_empty_room(kssj, jssj, xqj, sdj, dsz)




            # spider.get_useroom()
            return render(request, 'spider/SpiderResult.html')

        else:
            print("No name or password!")



        # spider = Spider('http://jw3.ahu.cn')
        # xh = 'E31614002'
        # password = 'wang921207'
        # spider.login(xh, password)
        #
        # kssj = '117'
        # jssj = '117'
        # xqj = '1'
        # sdj = "'7'|'0','0','5','7','0','0','0','0','0'"
        # for num in classnum_dict:
        #     useromm_dict = {
        #         'ClassRoomName': num,
        #     }
        #     jsbh = classnum_dict[num]
        #     data_list = spider.get_useroom(kssj, jssj, xqj,  sdj, jsbh)
        #     useromm_dict['data'] = data_list
            # 存储数据
            # mycol.insert_one(useromm_dict)



# /
#         for week in range(17, 19):  # 爬取17-18周
#             djz = str(week)
#             dsz = dsz_dict[str(week % 2)]
#             for day in range(1, 8):  # 周一到周末
#                 xqj = str(day)
#                 for index in sdj_dict:  # 从早到晚
#                     sdj = sdj_dict[index]
#                     kssj = xqj + djz
#                     jssj = xqj + djz
#                     # print(index)
#                     # print(kssj, jssj, xqj, sdj, dsz)
#                     html = spider.get_empty_room(kssj, jssj, xqj, sdj, dsz)

    return render(request, 'spider/SchoolSpider.html')




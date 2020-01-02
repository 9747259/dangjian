# -*- coding:utf-8 -*-
# author:xinfei
#import json
from random import randint
import time
import threading
import logging

#import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
#from PIL import Image
#from convert import getverify1
import base64
from questionBank import dataBank
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.WARNING,
                    filename="./log/log.txt",
                    filemode="w",
                    format=DATE_FORMAT,
                    datefmt=DATE_FORMAT)

driver = webdriver.Chrome()

first_url = 'https://www.dangjianwang.com/login'
driver.get(first_url)
driver.implicitly_wait(30)

'''---------------------正式账号登录-------------------------'''
def login():
    driver.maximize_window()
    #driver.find_element_by_tag_name("账号密码").click()
    #driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[2]').click()
    time.sleep(2)
    driver.find_element_by_id("uname").send_keys("18016131821")
    driver.find_element_by_id("pwd").clear()
    driver.find_element_by_id("pwd").send_keys("xinfei240546")
    validate_code()
    #driver.find_element_by_id("verifyCode").send_keys(text)
    with open(r'.//picture//bb.png', 'rb') as f:
        ls_f = base64.b64encode(f.read())
        text=tencent_api(ls_f)
        driver.find_element_by_id("captcha").send_keys(text)
    driver.find_element_by_tag_name("button").click()
    '''
    for x in range(2):
        if driver.current_url == 'http://www.dangjianwang.com/login':
            driver.find_element_by_class_name("layui-layer-btn0").click()
            driver.find_element_by_id("captcha-img").click()
            login()
        else:
            break
    '''
'''-------------------测试账号登录--------------------------------'''
def login_test():
    driver.maximize_window()
    driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/li[2]').click()
    driver.find_element_by_id("uname").clear()
    driver.find_element_by_id("uname").send_keys("18016131821")
    driver.find_element_by_id("pwd").clear()
    driver.find_element_by_id("pwd").send_keys("xinfei240546")
    #time.sleep(8)

'''----------------腾讯云验证码识别API接口-------------------------'''
def tencent_api(ls_f):
    import ssl, hmac, base64, hashlib
    from datetime import datetime as pydatetime

    try:
        from urllib import urlencode
        from urllib2 import Request, urlopen
    except ImportError:
        from urllib.parse import urlencode
        from urllib.request import Request, urlopen

    # 云市场分配的密钥Id
    secretId = "AKID9Uvx2LW59BiMilsuMOKbJDHI69DMGU5o2ggQ"  # 云市场分配的密钥Key
    secretKey = "crU2g45qdx8fC2jCu623wqGO4s89PJql7OKO0Xc"
    source = "market"

    # 签名
    datetime = pydatetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signStr = "x-date: %s\nx-source: %s" % (datetime, source)
    sign = base64.b64encode(hmac.new(secretKey.encode('utf-8'), signStr.encode('utf-8'), hashlib.sha1).digest())
    auth = 'hmac id="%s", algorithm="hmac-sha1", headers="x-date x-source", signature="%s"' % (
    secretId, sign.decode('utf-8'))

    # 请求方法
    method = 'POST'  # 请求头
    headers = {
        'X-Source': source,
        'X-Date': datetime,
        'Authorization': auth,
    }
    # 查询参数
    queryParams = {
        'img_base64': ls_f }
    # body参数（POST方法下存在）
    bodyParams = {
    }
    # url参数拼接
    url = 'https://service-7hz6ctvz-1255468759.ap-shanghai.apigateway.myqcloud.com/release/logicCheckCode'
    if len(queryParams.keys()) > 0:
        url = url + '?' + urlencode(queryParams)

    request = Request(url, headers=headers)
    request.get_method = lambda: method
    if method in ('POST', 'PUT', 'PATCH'):
        request.data = urlencode(bodyParams).encode('utf-8')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urlopen(request, context=ctx)
        content = response.read()
    if content:
        data = eval(content.decode('utf-8'))
        data_need=data["showapi_res_body"]["Result"]
        print(data_need)
        return data_need

'''----------------最早版本函数，不能使用，可以作为参考--------------------------'''
def study_information():
    # driver.find_element_by_xpath("/html/body/div[2]/div/ul[1]/li[5]/a").click()
    # driver.find_element_by_class_name("dot").click()
    # driver.find_element_by_class_name("ellipsis").click()
    seed = [randint(14, 27) for _ in range(3)]
    driver.get('https://www.dangjianwang.com/Study/MaterialDetail?mid=88{}'.format(seed[0]))
    try:
        information = driver.find_element_by_xpath('//*[@id="all-list"]/div/p[3]').text
        print(information)
        driver.find_element_by_xpath('//*[@id="content-text"]').send_keys(information)
        driver.find_element_by_xpath('//*[@id="content-submit"]').click()
        while True:
            element = WebDriverWait(driver, 1000, poll_frequency=0.5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "layui-layer-btn0")))
            element[0].click()
    except:
        print("没有同事提交信息")
        driver.quit()

def information():
    x = 0
    while x<10:
        seed = [randint(793,830) for _ in range(2)]
        driver.get('https://www.dangjianwang.com/News/show/21{}'.format(seed[0]))
        try:
            message = driver.find_element_by_xpath('//p[@class="message down"]').text
            driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/form/textarea').send_keys(message)
            driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/form/div').click()
            time.sleep(3)
        except:
            time.sleep(3)
            continue
        x += 1
'''------------------------------------------------------------------'''


def validate_code():
    time.sleep(2)
    driver.save_screenshot('d://platform//dangjian//picture//login.png')
    imgelement = driver.find_element_by_xpath('//*[@id="captcha-img"]')
    location = imgelement.location
    size = imgelement.size
    rangle = (int(location['x']), int(location['y']),int(location['x'] + size['width']),int(location['y'] + size['height']))
    #rangle=(800,300,1000,500)
    i = Image.open('d://platform//dangjian//picture//login.png')
    bb = i.crop(rangle)
    bb.save('d://platform//dangjian//picture//bb.png')
    #text = getverify1('.//picture//', 'bb.jpg')
    #print(text)


'''----------------回答问题4分--------------------'''
def answer_question():
    time.sleep(1)
    driver.get("https://www.dangjianwang.com/study#/exam?id=18&type=2&enterType=1&name=%E5%8D%81%E4%B9%9D%E5%A4%A7%E6%8A%A5%E5%91%8A100%E9%A2%98")
    i=1
    try:
        while i<=5:
            time.sleep(2)
            data1=driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/div[1]/div/div[2]/div[1]/span[2]").text
            time.sleep(2)
            for key, value in dataBank.data_bank.items():
                if key == data1:
                    chioce_option(value,i)
            '''
            else:
                    driver.find_element_by_xpath("//*[text()='B']/preceding-sibling::span[1]").click()
                    time.sleep(1)
                    driver.find_element_by_xpath("//*[@class='btn'][2]").click()
            '''
            i = i+1
    except:
        driver.refresh()
        time.sleep(3)
        answer_question()

    driver.refresh()
    time.sleep(2)

def chioce_option(value,i):
    if isinstance(value, str):
        if value == "A":
            driver.find_element_by_xpath("//*[text()='A']/preceding-sibling::span[1]").click()
        elif value == "B":
            driver.find_element_by_xpath("//*[text()='B']/preceding-sibling::span[1]").click()
        elif value == "C":
            driver.find_element_by_xpath("//*[text()='C']/preceding-sibling::span[1]").click()
        elif value == "D":
            driver.find_element_by_xpath("//*[text()='D']/preceding-sibling::span[1]").click()
        time.sleep(2)
        if i <= 4:
            driver.find_element_by_xpath("//*[@class='btn next']").click()
            time.sleep(1)
    else:
        for data2 in value:
            if data2 == "A":
                driver.find_element_by_xpath("//*[text()='A']/preceding-sibling::span[1]").click()
            elif data2 == "B":
                driver.find_element_by_xpath("//*[text()='B']/preceding-sibling::span[1]").click()
            elif data2 == "C":
                driver.find_element_by_xpath("//*[text()='C']/preceding-sibling::span[1]").click()
            elif data2 == "D":
                driver.find_element_by_xpath("//*[text()='D']/preceding-sibling::span[1]").click()
            elif data2 == "E":
                driver.find_element_by_xpath("//*[text()='E']/preceding-sibling::span[1]").click()
            elif data2 == "F":
                driver.find_element_by_xpath("//*[text()='F']/preceding-sibling::span[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//button").click()
        time.sleep(2)
        if i <= 4:
            driver.find_element_by_xpath("//*[@class='btn next']").click()
            time.sleep(1)

'''----------------------新闻学习10分------------------'''
def news_study(message_web):
    time.sleep(2)
    driver.get(message_web)
    time.sleep(2)
    try:
        driver.find_element_by_tag_name("textarea").send_keys("关注")
        time.sleep(2)
        driver.find_element_by_xpath("//*[@class='tf-comment-btn cursor']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[text()='刚刚']/following-sibling::span[1]").click()
        time.sleep(2)
        driver.find_elements_by_tag_name("button")[3].click()
        time.sleep(2)
        driver.refresh()
        return 1
    except:
        return 0

'''---------------------签名5分--------------------------'''
def sign_name():
    try:
        driver.get("https://www.dangjianwang.com/news#/news?system_id=8081783f16befa6e694e4732667acd1b&menu_id=0495acb06d34106ac7f68b6afa180b19&code=1102&template=2")
        #driver.find_element_by_class_name("check-box-btn").click()
        #driver.find_elements("//*[class='check-box-btn']").click()
        driver.find_element_by_css_selector(".check-box-btn.cursor.inline-block").click()
    except:
        print("签名错误")

'''---------------------党员视角4分---------------------------'''
def view_angle():
    driver.get("https://www.dangjianwang.com/moments#/")
    time.sleep(2)
    try:
        driver.find_element_by_tag_name("textarea").send_keys("学习习近平总书记讲话")
        time.sleep(1)
        driver.find_element_by_tag_name("button").click()
        time.sleep(2)
        mouse = driver.find_element_by_xpath("//*[@class='handle-icon icon-down']")
        #mouse = WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_element_located(By.CLASS_NAME, "handle-icon icon-down"))
        ActionChains(driver).move_to_element(mouse).perform()
        time.sleep(2)
        #ActionChains(driver).move_to_element_with_offset(mouse,-2,0).click()
        driver.find_element_by_css_selector(".hidden-btn").click()
        time.sleep(2)
        #driver.find_elements_by_class_name("tf-dyview-del-btn")[1].click()
        #driver.find_elements_by_tag_name("button")[6].click()
        driver.find_element_by_xpath("//*[@type='button'][2]").click()
        return 1
    except:
        print("党员视角点击失败")
        return 0


'''-----------------党员论坛2分----------------------'''
def forum(web_single):
    driver.get(web_single)
    time.sleep(2)
    try:
        driver.find_element_by_tag_name("textarea").send_keys("好")
        driver.find_element_by_tag_name("button").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[text()='刚刚']/following-sibling::span[1]").click()
        time.sleep(1)
        driver.find_elements_by_tag_name("button")[4].click()
        return 1
    except:
        return 0

'''--------------------------学习回复100字5分--------------------------------'''
def study_reply():
    driver.get("https://www.dangjianwang.com/study#/materialDetail/ae8df47feb0aef7d05b57fc05e244176")
    time.sleep(2)
    try:
        driver.find_element_by_tag_name("textarea").send_keys("坚持以上率下，巩固拓展落实中央八项规定精神成果，继续整治四风问题，坚决反对特权思想和特权现象。重点强化政治纪律和组织纪律，带动廉洁纪律、群众纪律、工作纪律、生活纪律严起来。坚持开展批评与自我批评，坚持惩前毖后、治病救人，运用监督执纪“四种形态”，抓早抓小、防微杜渐，强化监督执纪问责。")
        time.sleep(2)
        driver.find_element_by_xpath("//*[@class='post']/span[2]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[text()='刚刚']/following-sibling::span[1]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@class='ivu-modal-confirm-footer']/button[2]").click()
        return 1
    except:
        return 0

'''--------------挂时间5分--------------------'''
def hang_time():
    driver.get("https://www.dangjianwang.com/study#/materialDetail/ae8df47feb0aef7d05b57fc05e244176")
    while True:
        element = WebDriverWait(driver, 1000, poll_frequency=0.5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btns")))
        element[0].click()

def main_login():
    #--------------------签名5分------------------------
    #time.sleep(2)
    #sign_name()
    #--------------------回答问题2分--------------------
    for _ in range(2):
        answer_question()
    #--------------------新闻回复10分--------------------
    for message_web in dataBank.message_webs:
        news_study(message_web)
    #--------------------党员视角（发图片）4分----------------
    count_view_angle = 1
    total_view_angle = 1
    while count_view_angle <= 1 and total_view_angle <= 2:
        if view_angle() == 1:
            count_view_angle += 1
        total_view_angle += 1

    #---------------------论坛回复2分----------------------
    '''
    count_forum = 1
    total_forum = 1
    while count_forum <= 2 and total_forum <= 3:
        if forum() == 1:
            count_forum += 1
        total_forum += 1
    '''
    #--------------------长评论（100字以上）5分---------------
    count_study_reply = 1
    total_study_reply = 1
    while count_study_reply <= 1 and total_study_reply <= 2:
        if study_reply() == 1:
            count_study_reply += 1
        total_study_reply += 1

    #--------------------挂学习时间5分-----------------------
    time.sleep(2)
    hang_time()

'''--------------------主程序------------------------'''
if __name__ == '__main__':
    #login()
    login_test()
    time.sleep(15)
    main_login()
    '''
    if driver.current_url == "https://www.dangjianwang.com/news#/news?system_id=8081783f16befa6e694e4732667acd1b&menu_id=0495acb06d34106ac7f68b6afa180b19&code=1102&template=2":
        main_login()
    else:
        driver.refresh()
        time.sleep(3)
        login()
        main_login()
    '''


'''---------------不能使用的函数-----------------'''
   # study_information()



from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle
import sys
import time
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.setting.userAgent'] = ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
obj = webdriver.PhantomJS(executable_path='E:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',desired_capabilities=dcap)
# obj.set_window_size(1980,1080)
# obj.get('http://weibo.com')
# obj.find_element_by_xpath('//*[@id="loginname"]').send_keys('13424333758')
# obj.find_element_by_xpath('//*[@id="loginname"]').clear()
# obj.find_element_by_xpath('//*[@type="password"]').send_keys('yx123456')
# obj.find_element_by_xpath('//*[@type="password"]').clear()
# print("保存验证码：", obj.save_screenshot("screenshot\\YZM.png"))
# obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys('gmd2z')
# obj.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
# obj.close()
# obj.delete_all_cookies()
# print(obj.current_url)
# output = open('cookies\\13424333758', 'wb+')
# pickle.dump(obj.get_cookies(), output)
# output.close()

#先获得网址然后删除所有cookie
obj.get('https://weibo.com')
obj.implicitly_wait(10)
obj.delete_all_cookies()
input = open('cookies\\14715399742', 'rb')
cookieList = pickle.load(input)
input.close()
for cookie in cookieList:
    # fix the problem-> "errorMessage":"Unable to set Cookie"
    for k in ('name', 'value', 'domain', 'path', 'expiry'):
        if k not in list(cookie.keys()):
            if k == 'expiry':
                t = time.time()
                cookie[k] = int(t) # 时间戳 秒
    obj.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path', 'expiry') if k in cookie})

obj.get('https://weibo.com')

#添加完cookie之后再重新加载该网站
print(len(obj.get_cookies()))
obj.get('http://s.weibo.com/weibo/byd&typeall=1&suball=1&timescope=custom:2017-12-?sudaref=weibo.com&c=spr_sinamkt_buy_hyww_weibo_t113')
obj.implicitly_wait(10)
obj.save_screenshot("bbbbbbbkkkkk.png")
print(obj.current_url)
obj.implicitly_wait(10)
print(obj.current_url)

# 6430770365
# 14715399742



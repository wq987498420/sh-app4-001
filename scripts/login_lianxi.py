from selenium.webdriver.common.by import By

from Base.get_driver import get_driver
from Page.page import Page


# 实例化page类
page_obj = Page(get_driver("com.yunmall.lc", "com.yunmall.ymctoc.ui.activity.MainActivity"))
# 点击我的
page_obj.get_home_page_obj().click_my_btn()
# 点击已有账号去登录
page_obj.get_sign_page_obj().click_exit_account_btn()
# 登录操作
page_obj.get_login_page_obj().login("111", "111")

# 启动参数添加 desired_caps['automationName'] = 'Uiautomator2'
# def get_toast(mess):
#     # 定位错误提示消息
#     mess_xpath = "//*[contains(@text,'{}')]".format(mess)
#
#     message = page_obj.get_login_page_obj().search_element((By.XPATH, mess_xpath), timeout=5, poll_frequency=0.5).text
#     return message

# print(get_toast("此用户"))

print(page_obj.get_login_page_obj().get_toast("此用户"))
# 退出driver
page_obj.driver.quit()

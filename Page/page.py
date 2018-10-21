from Page.home_page import Home_Page
from Page.login_page import Login_Page
from Page.person_page import Person_Page
from Page.setting_page import Setting_Page
from Page.sign_page import Sign_Page

class Page:
    def __init__(self, driver):
        self.driver = driver

    def get_home_page_obj(self):
        # 返回首页实例化对象
        return Home_Page(self.driver)

    def get_login_page_obj(self):
        # 返回登录页面实例化对象
        return Login_Page(self.driver)

    def get_person_page_obj(self):
        # 返回个人中心页面实例化对象
        return Person_Page(self.driver)

    def get_setting_page_obj(self):
        # 返回设置页面实例化对象
        return Setting_Page(self.driver)

    def get_sign_page_obj(self):
        # 返回注册页面对象
        return Sign_Page(self.driver)
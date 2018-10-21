from Base.Base import Base
import Page

class Login_Page(Base):
    def __init__(self, driver):
        Base.__init__(self, driver)

    def login(self, name, passwd):
        """登陆操作"""
        # 输入用户名
        self.send_element(Page.login_account_id, name)
        # 输入密码
        self.send_element(Page.login_passwd_id, passwd)
        # 点击登录按钮
        self.click_element(Page.login_btn_id)
    def if_login_btn_exits(self):
        # 判断登录按钮是否存在 存在返回True 不存在返回False
        try:
            self.search_element(Page.login_btn_id)
            return True
        except Exception as e:
            return False
    def close_login_page(self):
        # 关闭登录页
        self.click_element(Page.login_close_btn_id)

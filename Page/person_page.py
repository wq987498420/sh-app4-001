from Base.Base import Base
import Page

class Person_Page(Base):

    def __init__(self, driver):
        Base.__init__(self, driver)

    def get_coupons_text(self):
        """返回我的优惠券文本"""
        return self.search_element(Page.person_coupons_id).text
    def click_setting_btn(self):
        """点击设置按钮"""
        self.click_element(Page.setting_btn_id)
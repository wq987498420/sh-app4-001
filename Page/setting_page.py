from Base.Base import Base
import Page, time

class Setting_Page(Base):

    def __init__(self, driver):
        Base.__init__(self, driver)

    def click_logout_btn(self, tag=1):
        """退出操作
            :keyword tag=1 确认退出
        """
        time.sleep(2)
        # 向上滑动
        self.scree_scroll(1)
        # 点击退出按钮
        self.click_element(Page.logout_btn_id)
        if tag == 1:
            # 点击确认退出
            self.click_element(Page.logout_acc_btn_id)
        else:
            # 取消确认退出按钮
            self.click_element(Page.log_out_miss_btn_id)
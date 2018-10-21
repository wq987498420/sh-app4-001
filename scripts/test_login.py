import sys, os, time
sys.path.append(os.getcwd())
import pytest
from Base.get_driver import get_driver
from Base.get_data import Get_Data
from Page.page import Page
from selenium.common.exceptions import TimeoutException

"""
[(用例编号,手机号,密码,tag,tag_message,预期结果)]
"""
def get_login_data():
    # 结果列表
    login_list = []
    data = Get_Data().get_yaml_data("aolai.yml")
    # return data
    for i in data.keys():
        login_list.append((i, data.get(i).get("phone"), data.get(i).get("passwd"),
                           data.get(i).get("tag"), data.get(i).get("tag_message"),
                           data.get(i).get("expect_result")))
    return login_list

class Test_Login:
    def setup_class(self):
        self.page_obj = Page(get_driver("com.yunmall.lc", "com.yunmall.ymctoc.ui.activity.MainActivity"))

    def teardown_class(self):
        self.page_obj.driver.quit()

    @pytest.mark.parametrize("test_num,phone,passwd,tag,tag_message,expect_result", get_login_data())
    def test_login(self, test_num, phone, passwd, tag, tag_message, expect_result):
        """
        :param test_num: 用例编号
        :param phone: 输入手机号
        :param passwd: 输入密码
        :param tag: 标记成功用例 1 成功用例  None 失败用例
        :param tag_message: 获取toast消息方法参数
        :param expect_result:预期结果
        :return:
        """
        # 点击我
        self.page_obj.get_home_page_obj().click_my_btn()
        # 点击已有账号，去登录
        self.page_obj.get_sign_page_obj().click_exit_account_btn()
        # 登陆操作
        self.page_obj.get_login_page_obj().login(phone, passwd)
        # 判断成功失败用例
        if tag:
            # 预期成功用例
            try:
                # 优惠券
                coupons = self.page_obj.get_person_page_obj().get_coupons_text()
                try:
                    # 断言
                    assert coupons == expect_result
                except AssertionError as e:
                    print(e.__str__())
                # 执行退出操作
                # 点击设置
                self.page_obj.get_person_page_obj().click_setting_btn()
                # 退出
                self.page_obj.get_setting_page_obj().click_logout_btn()

            except TimeoutException as e:
                # 关闭登录页面
                self.page_obj.get_login_page_obj().close_login_page()
                assert False

        else:
            # 预期失败的用例
            try:
                # 获取toast消息
                toast_message = self.page_obj.get_login_page_obj().get_toast(tag_message)
                # 获取登录按钮是否存在
                if_login = self.page_obj.get_login_page_obj().if_login_btn_exits()
                # 断言
                assert if_login and toast_message == expect_result

            except TimeoutException as e:
                assert False

            finally:
                # 关闭登录页面
                self.page_obj.get_login_page_obj().close_login_page()



from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Base:

    def __init__(self, driver):
        self.driver = driver

    def search_element(self,loc, timeout=15, poll_frequency=1.0):
        """
        定位单个元素
        :param loc: 元祖 定位类型 (By.ID,ID属性值) (By.CLASS_NAME,CLASS属性值) (By.XPATH,XPATH语句)
        :return: 返回定为对象
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(lambda x: x.find_element(*loc))

    def search_elements(self, loc, timeout=15, poll_frequency=1.0):
        """
        定位一组元素
        :param loc: 元祖 定位类型 (By.ID,ID属性值) (By.CLASS_NAME,CLASS属性值) (By.XPATH,XPATH语句)
        :return: 返回定为对象
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(lambda x: x.find_elements(*loc))

    def click_element(self, loc, timeout=15, poll_frequency=1.0):
        """
        点击一个元素
        :param loc: 元祖 定位类型 (By.ID,ID属性值) (By.CLASS_NAME,CLASS属性值) (By.XPATH,XPATH语句)
        :param timeout: 查找元素超时时间
        :param poll_frequency: 搜索间隔
        :return:
        """
        self.search_element(loc, timeout, poll_frequency).click()
    def send_element(self, loc, text, timeout=15, poll_frequency=1.0):
        """
        点击一个元素
        :param loc: 元祖 定位类型 (By.ID,ID属性值) (By.CLASS_NAME,CLASS属性值) (By.XPATH,XPATH语句)
        :param timeout: 查找元素超时时间
        :param poll_frequency: 搜索间隔
        :param text: 输入文本内容
        :return:
        """
        input_element = self.search_element(loc, timeout, poll_frequency)
        # 清空
        input_element.clear()
        # 输入
        input_element.send_keys(text)

    def scree_scroll(self, tag):
        """swip 屏幕滑动
            :keyword tag=1 向上  tag=2 向下 tag=3 向左 tag=4 向右
        """
        # 屏幕分辨率 ('width', 'height')
        screen_size = self.driver.get_window_size()

        width = screen_size.get("width")
        height = screen_size.get("height")

        if tag ==1:
            self.driver.swipe(width * 0.5, height * 0.8, width * 0.5, height * 0.3,1000)
        if tag ==2:
            self.driver.swipe(width * 0.5, height * 0.3, width * 0.5, height * 0.8,1000)
        if tag ==3:
            self.driver.swipe(width * 0.8, height * 0.5, width * 0.3, height * 0.5,1000)
        if tag ==4:
            self.driver.swipe(width * 0.3, height * 0.5, width * 0.8, height * 0.5,1000)

    def get_toast(self, mess):
        """
        获取toast消息
        :param mess: tost消息text文本
        :return: toast 消息
        """
        # 定位错误提示消息
        toast_xpath = "//*[contains(@text,'{}')]".format(mess)
        toast_message = self.search_element((By.XPATH, toast_xpath), timeout=5, poll_frequency=0.5).text
        return toast_message
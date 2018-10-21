from appium import webdriver

def get_driver(pac, act):
    """
    返回driver对象
    :param pac: 包名
    :param act: 启动名
    :return:
    """
    desired_caps = {}
    # 设备信息
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '5.1'
    desired_caps['deviceName'] = '192.168.56.101:5555'
    # app的信息
    # desired_caps['appPackage'] = 'com.android.mms'
    # desired_caps['appActivity'] = '.ui.ConversationList'
    desired_caps['automationName'] = 'Uiautomator2'
    desired_caps['appPackage'] = pac
    desired_caps['appActivity'] = act

    # 声明我们的driver对象
    return webdriver.Remote('http://192.168.45.23/wd/hub', desired_caps)

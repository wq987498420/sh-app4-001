from selenium.webdriver.common.by import By


"""首页"""

# 我的按钮
my_btn_id = (By.ID, "com.yunmall.lc:id/tab_me")

"""注册页面"""

# 已有账号去登录
exits_account_id = (By.ID, "com.yunmall.lc:id/gotologon")

"""登录页面"""

# 用户
login_account_id = (By.ID, "com.yunmall.lc:id/logon_account_textview")
# 密码
login_passwd_id = (By.ID, "com.yunmall.lc:id/logon_password_textview")
# 登录按钮
login_btn_id = (By.ID, "com.yunmall.lc:id/logon_button")
# 关闭登录也按钮
login_close_btn_id = (By.ID, "com.yunmall.lc:id/ymtitlebar_left_btn_image")

"""个人中心页面"""

# 我的优惠券
person_coupons_id = (By.ID, "com.yunmall.lc:id/txt_my_coupons")
# 设置按钮
setting_btn_id = (By.ID, "com.yunmall.lc:id/ymtitlebar_left_btn_image")

"""设置页面"""

# 退出按钮
logout_btn_id = (By.ID, "com.yunmall.lc:id/setting_logout")
# 退出弹窗-确认退出按钮
logout_acc_btn_id = (By.ID, "com.yunmall.lc:id/ymdialog_right_button")
# 退出弹窗-取消退出按钮
log_out_miss_btn_id = (By.ID, "com.yunmall.lc:id/ymdialog_left_button")
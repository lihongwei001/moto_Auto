import time

from common.base_page import BasePage

class CallPage(BasePage):
    # 元素定位
    call_btn = "resourceId:com.android.dialer:id/lable_sim0"
    hangup_btn = "resourceId:com.android.dialer:id/videocall_end_call"
    # hangup_btn = "resourceId:com.android.dialer:id/incall_end_call"
    accept_call_btn = "textContains:接听"

    # ===== 新增：拨号键盘数字按钮定位 =====
    num_0 = "resourceId:com.android.dialer:id/zero"
    num_1 = "resourceId:com.android.dialer:id/one"
    num_2 = "resourceId:com.android.dialer:id/two"
    num_3 = "resourceId:com.android.dialer:id/three"
    num_4 = "resourceId:com.android.dialer:id/four"
    num_5 = "resourceId:com.android.dialer:id/five"
    num_6 = "resourceId:com.android.dialer:id/six"
    num_7 = "resourceId:com.android.dialer:id/seven"
    num_8 = "resourceId:com.android.dialer:id/eight"
    num_9 = "resourceId:com.android.dialer:id/nine"
    num_star = "resourceId:com.android.dialer:id/star"
    num_hash = "resourceId:com.android.dialer:id/pound"
    def open_call_app(self):
        """打开拨号APP"""
        self.driver.app_start("com.android.dialer", stop=True)
        time.sleep(5)

    def input_number_by_click(self, phone_number):
        """
        【核心方法】遍历号码，逐个点击数字按键
        :param phone_number: 字符串号码，例如 "10010"
        """
        # 数字映射字典：字符 -> 定位符
        num_map = {
            "0": self.num_0,
            "1": self.num_1,
            "2": self.num_2,
            "3": self.num_3,
            "4": self.num_4,
            "5": self.num_5,
            "6": self.num_6,
            "7": self.num_7,
            "8": self.num_8,
            "9": self.num_9,
            "*": self.num_star,
            "#": self.num_hash
        }
        for char in phone_number:
            selector = num_map[char]
            self.click_element(selector)

    def make_call(self):
        """发起呼叫"""
        self.click_element(self.call_btn)

    def hang_up(self):
        """挂断"""
        self.click_element(self.hangup_btn)

    def accept_incoming_call(self):
        """接听来电"""
        self.click_element(self.accept_call_btn)

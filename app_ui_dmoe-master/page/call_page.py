import time

from common.base_page import BasePage

class CallPage(BasePage):
    # 元素定位
    # call_btn = "resourceId:com.android.dialer:id/lable_sim1"
    call_btn = "resourceId:com.android.dialer:id/sim_card_0"
    hangup_videoRingtone_btn = "resourceId:com.android.dialer:id/videocall_end_call"
    hangup_btn = "resourceId:com.android.dialer:id/incall_end_call"
    accept_call_btn = "textContains:接听"
    disaccept_call_btn = "textContains:拒接"
    call_hold_btn = "textContains:保持"
    call_add_btn = "textContains:添加通话"
    call_switch_video_btn = "textContains:视频通话"
    call_mute_btn = "textContains:静音"
    call__speaker_btn = "xpath:(//android.widget.RelativeLayout)[2]"
    call_keyboard_btn = "resourceId:com.android.dialer:id/incall_dialpad"

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
        if self.is_element_exist(self.hangup_videoRingtone_btn):
            self.click_element(self.hangup_videoRingtone_btn)
        elif self.is_element_exist(self.hangup_btn):
            self.click_element(self.hangup_btn)
    def accept_incoming_call(self):
        """接听来电"""
        self.click_element(self.accept_call_btn)
    def disaccept_incoming_call(self):
        "拒接来电"
        self.click_element(self.disaccept_call_btn)

    def hold_call(self):
        '呼叫保持'
        self.click_element(self.call_hold_btn)

    def add_call(self):
        "添加通话"
        self.click_element(self.call_add_btn)

    def switch_to_videoCall(self):
        "升级为视频通话"
        self.click_element(self.call_switch_video_btn)

    def mute(self):
        "静音"
        self.click_element(self.call_mute_btn)

    def call_speaker(self):
        "扬声器"
        self.click_element(self.call__speaker_btn)

    def call_keyboard(self):
        "通话界面键盘"
        self.click_element(self.call_keyboard_btn)

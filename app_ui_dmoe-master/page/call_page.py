import re

from common.base_page import BasePage
from common.driver_util import DriverUtil
from common.log_util import logger

class CallPage(BasePage):
    # 元素定位
    # call_btn = "resourceId:com.android.dialer:id/lable_sim1"
    call_btn = "resourceId:com.android.dialer:id/sim_card_0"
    hangup_videoRingtone_btn = "resourceId:com.android.dialer:id/videocall_end_call"
    hangup_btn = "resourceId:com.android.dialer:id/incall_end_call"
    accept_call_btn = "xpath://*[@content-desc='接听']"
    disaccept_call_btn = "textContains:拒接"
    answer_video_call = "xpath://*[@content-desc='视频通话']"
    call_hold_btn = "textContains:保持"
    call_add_btn = "textContains:添加通话"
    call_switch_video_btn = "textContains:视频通话"
    call_mute_btn = "textContains:静音"
    call__speaker_btn = "xpath:(//android.widget.RelativeLayout)[2]"
    call_keyboard_btn = "resourceId:com.android.dialer:id/incall_dialpad"
    latest_number = "xpath:(//android.widget.LinearLayout)[43]"
    video_call_button = "resourceId:com.android.dialer:id/third_icon"
    video_call_sim1 = "xpath://*[@resource-id='com.android.dialer:id/icon']"
    video_call_sim2 = "xpath:(//*[@resource-id='com.android.dialer:id/icon'])[2]"

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
        self.wait_element(self.num_0)

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

    def hang_up(self, timeout=10):
        """挂断"""
        def read_target():
            for selector in (self.hangup_btn, self.hangup_videoRingtone_btn):
                if self.is_element_exist(selector, timeout=0):
                    return {"selector": selector, "states": None}
            return {
                "selector": None,
                "states": [self.get_call_state(slot)["call_state"] for slot in (1, 2)],
            }

        target = self.wait_until(
            read_target,
            lambda value: value["selector"] is not None or value["states"] == [0, 0],
            "挂断按钮出现或两张 SIM 均空闲", timeout,
        )
        if target["selector"] is None:
            logger.info("设备已空闲，无需挂断")
            return
        self.click_element(target["selector"], timeout=0)
        self.wait_until(
            lambda: [self.get_call_state(slot)["call_state"] for slot in (1, 2)],
            lambda states: states == [0, 0],
            "挂断后两张 SIM 均空闲", timeout,
        )

    def accept_incoming_call(self, timeout=30):
        """接听来电"""
        self.click_element(self.accept_call_btn, timeout=timeout)
    def answer_video(self):
        "接听视频来电"
        self.click_element(self.answer_video_call)
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
    def click_latest_number(self):
        "点击最近通话号码"
        self.click_element(self.latest_number)
    def click_video_call_button(self):
        "点击视频通话按钮"
        self.click_element(self.video_call_button)
    def click_video_call_sim1(self):
        "点击视频通话卡1"
        self.click_element(self.video_call_sim1)
    def click_video_call_sim2(self):
        "点击视频通话卡2"
        self.click_element(self.video_call_sim2)

    def wait_call_state(self, sim_slot, expected, timeout=30):
        if expected not in (0, 1, 2):
            raise ValueError("expected 只能为 0（空闲）、1（响铃）、2（通话中）")
        return self.wait_until(
            lambda: self.get_call_state(sim_slot),
            lambda state: state["call_state"] == expected,
            f"SIM{sim_slot} 通话状态变为 {expected}", timeout,
        )

    def get_call_state(self, sim_slot=1):

        """
        获取指定 SIM 卡的通话状态。

        sim_slot: 1 表示 SIM1，2 表示 SIM2。

        返回示例：
        {
            "sim_slot": 1,
            "call_state": 2,
            "call_state_name": "通话中",
            "background_call_state": 2,
            "is_holding": True,
        }

        注意：按当前设备约定，将每个字段的第一条记录视为 SIM1，
        第二条记录视为 SIM2。
        """
        if sim_slot not in (1, 2):
            raise ValueError("sim_slot 只能为 1 或 2")

        output = DriverUtil.device_shell(self.driver, "dumpsys telephony.registry")
        call_states = re.findall(
            r"\bmCallState\s*=\s*(\d+)\b",
            output,
        )
        background_states = re.findall(
            r"\bmBackgroundCallState\s*=\s*(\d+)\b",
            output,
        )

        if len(call_states) != 2 or len(background_states) != 2:
            raise RuntimeError(
                "通话状态记录数量不符合预期，应各有两条："
                f"mCallState={call_states}，"
                f"mBackgroundCallState={background_states}"
            )

        index = sim_slot - 1
        call_state = int(call_states[index])
        background_state = int(background_states[index])

        state_names = {
            0: "空闲",
            1: "响铃",
            2: "通话中",
        }

        if call_state not in state_names:
            raise RuntimeError(f"未识别的 mCallState：{call_state}")

        return {
            "sim_slot": sim_slot,
            "call_state": call_state,
            "call_state_name": state_names[call_state],
            "background_call_state": background_state,
            "is_holding": background_state == 2,
        }
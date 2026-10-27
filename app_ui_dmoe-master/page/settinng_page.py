import time
import os
import common.base_page
from common.base_page import BasePage
from uiautomator2.exceptions import UiObjectNotFoundError
# import logger
import subprocess

class SettingPage(BasePage):
    #元素定位一级界面
    network = "textContains:移动网络"
    securityPrivacy = "textContains:安全与密码"
    about_phone = "textContains:关于手机"

    def open_Setting_app(self):
        """打开设置"""
        self.driver.app_start("com.android.settings", stop=True)
        time.sleep(2)
    def close_Setting_app(self):
        """关闭设置"""
        self.driver.app_stop("com.android.settings")
        self.driver.press("back")
        time.sleep(2)
    def click_network(self):
        """打开网络与互联网"""
        self.click_element(self.network)
        time.sleep(2)
    def click_securityPrivacy(self,max_times=5):
        """打开安全与密码"""
        for i in range(max_times):
                self.swipe_up()
                time.sleep(1)
        self.click_element(self.securityPrivacy)
        time.sleep(2)

    #”移动网络“下的二级界面元素定位
    APM = "textContains:飞行模式"
    mobileData = "text:移动数据"
    simCard = "textContains:SIM 卡和移动网络"
    network_speed = "textContains:实时网速"
    def click_APM(self):
        self.click_element(self.APM)
        time.sleep(2)

    def click_mobileData(self):
        self.click_element(self.mobileData)
        time.sleep(2)
    def click_simCard(self):
        self.click_element(self.simCard)
        time.sleep(2)
    def click_network_speed(self):
        self.click_element(self.network_speed)
        time.sleep(2)
    #”移动数据“下的三级界面元素定位
    mobileData_button = "textContains:使用移动数据"
    switch_sim1 = "xpath://*[@content-desc='Sim 卡 1']"
    switch_sim2 = "xpath://*[@content-desc='Sim 卡 2']"
    switch_Confirm = "text:确定"
    switch_cancel = "text:取消"
    switch_auto = "textContains:自动切换 SIM 卡"
    def click_mobileData_button(self):
        self.click_element(self.mobileData_button)
        time.sleep(2)
    def click_switch_sim1(self):
        self.click_element(self.switch_sim1)
        time.sleep(2)
        self.click_element(self.switch_Confirm)
        time.sleep(2)
    def click_switch_sim2(self):
        self.click_element(self.switch_sim2)
        time.sleep(2)
        self.click_element(self.switch_Confirm)
        time.sleep(2)
    def click_switch_auto(self):
        self.click_element(self.switch_auto)
        time.sleep(2)
    #"SIM卡和移动网络"下的三级界面元素定位
    operator_interface1 = "xpath:(//android.view.View)[6]"
    operator_interface2 = "xpath:(//android.view.View)[15]"
    switch_call_card1 = "xpath://*[@content-desc='Sim 卡 1']"
    switch_call_card2 = "xpath://*[@content-desc='Sim 卡 2']"
    intelligent_card_selection = "textContains:智能选卡"
    close_ics_button = "textContains:将其关闭"
    open_ics_button = "xpath://android.widget.Button"
    switch_sms_card1 = "xpath:(//*[@content-desc='Sim 卡 1'])[2]"
    switch_sms_card2 = "xpath:(//*[@content-desc='Sim 卡 2'])[2]"


    def click_operator_interface1(self):
        self.click_element(self.operator_interface1)
        time.sleep(2)
    def click_operator_interface2(self):
        self.click_element(self.operator_interface2)
        time.sleep(2)
    def click_switch_call_card1(self):
        self.click_element(self.switch_call_card1)
        time.sleep(2)
    def click_switch_call_card2(self):
        self.click_element(self.switch_call_card2)
        time.sleep(2)
    def click_intelligent_card_selection(self):
        self.click_element(self.intelligent_card_selection)
        time.sleep(2)
    def click_close_ics_button(self):
        self.click_element(self.close_ics_button)
        time.sleep(2)

    def click_open_ics_button(self):
        self.click_element(self.open_ics_button)
        time.sleep(2)
    def click_switch_sms_card1(self):
        self.click_element(self.switch_sms_card1)
        time.sleep(2)
    def click_switch_sms_card2(self):
        self.click_element(self.switch_sms_card2)
        time.sleep(2)
    #运营商下的四级界面元素定位
    network_tyep = "textContains:首选网络类型"
    network_5g = "textContains:5G"
    network_4g = "textContains:4G"
    button_5g = "xpath:(//android.widget.RelativeLayout)[7]"
    smart_network_switch = "textContains:智能数据模式"
    use_SA = "textContains:使用 SA"
    on_off_SIM_button = "resourceId:android:id/switch_widget"
    confirmButton = "resourceId:android:id/button1"
    cancelButton = "resourceId:android:id/button2"
    # mobile_Network_security = "textContains:移动网络安全"
    def click_network_tyep(self,max_times=2):
        for i in range(max_times):
            self.swipe_up()
            time.sleep(1)
        self.click_element(self.network_tyep)
        time.sleep(2)
    def click_network_5g(self):
        self.click_element(self.network_5g)
        time.sleep(2)
    def click_network_4g(self):
        self.click_element(self.network_4g)
        time.sleep(2)
    def click_button_5g(self):
        self.click_element(self.button_5g)
        time.sleep(2)

    def click_smart_network_switch(self):
        self.click_element(self.smart_network_switch)
        time.sleep(2)
    def click_use_SA(self):
        self.click_element(self.use_SA)
        time.sleep(2)
    def click_on_off_SIM_button(self):
        self.click_element(self.on_off_SIM_button)
        time.sleep(2)
    def click_confirmButton(self):
        self.click_element(self.confirmButton)
        time.sleep(2)
    def click_cancelButton(self):
        self.click_element(self.cancelButton)
        time.sleep(2)

    def click_Hotspot(self):
        self.click_element(self.mobile_Network_security)
        time.sleep(2)

    def get_sim_network_type(self):
        """
        Determine the SIM card network types for SIM1 and SIM2 using adb and uiautomator2.

        :return: A dictionary with network types for SIM1 and SIM2 (e.g., {"SIM1": "5G_NR", "SIM2": "LTE"}).
        """
        try:
            # Execute adb command to get network type
            result = self.driver.shell("getprop gsm.network.type")[0].strip()

            # Initialize network type dictionary
            network_types = {"SIM1": "Unknown", "SIM2": "Unknown"}

            # Parse the result for SIM1 and SIM2
            lines = result.split(",")
            if len(lines) > 0:
                if "NR" in lines[0] or "5G" in lines[0]:
                    network_types["SIM1"] = "5G_NR"
                elif "LTE" in lines[0]:
                    network_types["SIM1"] = "LTE"

            if len(lines) > 1:
                if "NR" in lines[1] or "5G" in lines[1]:
                    network_types["SIM2"] = "5G_NR"
                elif "LTE" in lines[1]:
                    network_types["SIM2"] = "LTE"

            return network_types
        except Exception as e:
            print(f"Error while determining network types: {e}")
            return {"SIM1": "Error", "SIM2": "Error"}

    moreSetting = "textContains:更多安全设置"
    simCasdProtect = "textContains:保护 SIM 卡"
    lockSIM1 = "xpath://android.widget.Switch"
    lockSIM2 = "xpath:(//android.widget.Switch)[2]"
    enterPIN1 = "xpath://android.widget.EditText"
    changePIN1_sim1 = "xpath://*[@text='更改 SIM 卡 PIN 码']"
    changePIN1_sim2 = "xpath:(//*[@text='更改 SIM 卡 PIN 码'])[2]"

    def click_more_security_Setting(self,max_times=3):
        for i in range(max_times):
            time.sleep(1)
        self.click_element(self.moreSetting)
        time.sleep(2)
    def click_simCasdProtect(self,max_times=4):
        # for i in range(max_times):
            # self.swipe_up()
            # time.sleep(1)
        self.click_element(self.simCasdProtect)
        time.sleep(2)
    def click_lockSIM1(self):
        self.click_element(self.lockSIM1)
        time.sleep(1)

    def click_lockSIM2(self):
        self.click_element(self.lockSIM2)
        time.sleep(1)

    def click_confirmButton(self):
        self.click_element(self.confirmButton)
        time.sleep(1)
    def inputPIN1(self,PIN1):
        self.input_text(self.enterPIN1,PIN1)
        time.sleep(1)
    def click_cancelButton(self):
        self.click_element(self.cancelButton)
        time.sleep(1)
    def click_changePIN1(self):
        self.click_element(self.changePIN1)
        time.sleep(1)

    def check_pin_status(self,sim):
        if sim == 1:
            self.click_element(self.changePIN1_sim1)
            if self.wait_element(self.enterPIN1, timeout=5):
                print("SIM1 PIN1已启用")
            else:
                print("SIM1 PIN1未启用")
        elif sim == 2:
            self.click_element(self.changePIN1_sim2)
            if self.wait_element(self.enterPIN1, timeout=5):
                print("SIM2 PIN1已启用")
            else:
                print("SIM2 PIN1未启用")

    #关于手机界面元素
    details_information = "textContains:设备详细信息"
    #设备详细信息界面元素
    sim1_status = "textContains:SIM 卡 1 状态"
    sim2_status = "textContains:SIM 卡 2 状态"
    data_status = "resourceId:com.android.settings:id/data_state_value"
    def check_dds_status(self,sim):
        for i in range(5):
            self.swipe_up()
            time.sleep(1)
        self.click_element(self.about_phone)
        self.click_element(self.details_information)
        if sim == 1:
            self.click_element(self.sim1_status)
            dds_status = self.get_element_text(self.data_status)
            print(f"SIM1 数据状态: {dds_status}")
        elif sim == 2:
            self.click_element(self.sim2_status)
            dds_status = self.get_element_text(self.data_status)
            print(f"SIM2 数据状态: {dds_status}")
import time

import common.base_page
from common.base_page import BasePage
from uiautomator2.exceptions import UiObjectNotFoundError
# import logger

class SettingPage(BasePage):
    #元素定位一级界面
    network = "textContains:移动网络"
    securityPrivacy = "textContains:安全与密码"

    def open_Setting_app(self):
        """打开设置"""
        self.driver.app_start("com.android.settings", stop=True)
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
    simCard = "textContains:SIM卡和移动网络"
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

    def click_operator_interface1(self):
        self.click_element(self.operator_interface1)
        time.sleep(2)
    def click_operator_interface2(self):
        self.click_element(self.operator_interface2)
        time.sleep(2)
    #运营商下的四级界面元素定位
    network_tyep = "textContains:首选网络类型"
    network_5g = "textContains:5G/4G/3G/2G"
    network_4g = "textContains:4G/3G/2G"
    button_5g = "xpath:(//android.widget.RelativeLayout)[7]"
    smart_network_switch = "textContains:智能数据模式"
    use_SA = "textContains:使用 SA"
    on_off_SIM_button = "resourceId:android:id/switch_widget"
    confirmButton = "resourceId:android:id/button1"
    cancelButton = "resourceId:android:id/button2"
    # mobile_Network_security = "textContains:移动网络安全"
    def click_network_tyep(self):
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

    moreSetting = "textContains:更多安全设置"
    simCasdProtect = "textContains:保护 SIM 卡"
    lockSIM1 = "xpath://android.widget.Switch"
    lockSIM2 = "xpath:(//android.widget.Switch)[2]"
    enterPIN1 = "xpath://android.widget.EditText"
    changePIN1 = "textContains:更改 SIM 卡 PIN 码"

    def click_more_security_Setting(self,max_times=3):
        for i in range(max_times):
            self.swipe_up()
            time.sleep(1)
        self.click_element(self.moreSetting)
        time.sleep(2)
    def click_simCasdProtect(self,max_times=4):
        for i in range(max_times):
            self.swipe_up()
            time.sleep(1)
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

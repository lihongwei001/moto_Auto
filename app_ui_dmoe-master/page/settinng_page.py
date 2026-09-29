import time
from common.base_page import BasePage
from uiautomator2.exceptions import UiObjectNotFoundError
import logger

class SettingPage(BasePage):
    #元素定位
    network = "textContains:网络与互联网"
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
        # for i in range(max_times):
        #     if self.is_element_exist(self.securityPrivacy):
        #         self.click_element(self.securityPrivacy)
        #         time.sleep(1)
        #     else:
        #         self.swipe_up()
        #         time.sleep(1)

        self.click_element(self.securityPrivacy)
        time.sleep(2)


    APM = "textContains:飞行模式"
    mobileData = "textContains:移动数据"
    simCard = "textContains:SIM卡和移动网络"
    Hotspot = "textContains:热点和网络共享"

    def click_APM(self):
        self.click_element(self.APM)
        time.sleep(2)

    def click_mobileData(self):
        self.click_element(self.mobileData)
        time.sleep(2)

    def click_simCard(self):
        self.click_element(self.simCard)
        time.sleep(2)

    def click_Hotspot(self):
        self.click_element(self.Hotspot)
        time.sleep(2)

    moreSetting = "textContains:更多安全设置"
    simCasdProtect = "textContains:保护 SIM 卡"
    lockSIM = "textContains:锁定 SIM 卡"
    enterPIN1 = "xpath://android.widget.EditText"
    confirmButton = "resourceId:android:id/button1"
    cancelButton = "resourceId:android:id/button2"
    changePIN1 = "textContains:更改 SIM 卡 PIN 码"

    def click_more_security_Setting(self):
        self.click_element(self.moreSetting)
        time.sleep(2)
    def click_simCasdProtect(self):
        self.click_element(self.simCasdProtect)
        time.sleep(2)
    def click_lockSIM(self):
        self.click_element(self.lockSIM)
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
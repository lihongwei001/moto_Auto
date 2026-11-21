import time

from common.base_page import BasePage, WaitTimeoutError
from common.driver_util import DriverUtil
from common.log_util import logger

class SettingPage(BasePage):
    #元素定位一级界面
    network = "textContains:移动网络"
    securityPrivacy = "textContains:安全与密码"
    about_phone = "textContains:关于手机"

    def open_Setting_app(self):
        """打开设置"""
        self.driver.app_start("com.android.settings", stop=True)
    def close_Setting_app(self):
        """关闭设置"""
        self.driver.app_stop("com.android.settings")
        # self.driver.press("back")
    def click_network(self):
        """打开网络与互联网"""
        self.wait_element(self.network)
        self.click_element(self.network)
    def click_securityPrivacy(self,max_times=5):
        """打开安全与密码"""
        self.scroll_to_element(self.securityPrivacy, max_swipes=max_times)
        self.click_element(self.securityPrivacy)

    #”移动网络“下的二级界面元素定位
    APM = "textContains:飞行模式"
    mobileData = "text:移动数据"
    simCard = "textContains:SIM 卡和移动网络"
    network_speed = "textContains:实时网速"
    def click_APM(self):
        self.click_element(self.APM)

    def click_mobileData(self):
        self.click_element(self.mobileData)
    def click_simCard(self):
        self.click_element(self.simCard)
    def click_network_speed(self):
        self.click_element(self.network_speed)
    #”移动数据“下的三级界面元素定位
    mobileData_button = "textContains:使用移动数据"
    switch_sim1 = "xpath://*[@content-desc='Sim 卡 1']"
    switch_sim2 = "xpath://*[@content-desc='Sim 卡 2']"
    switch_Confirm = "text:确定"
    switch_cancel = "text:取消"
    switch_auto = "textContains:自动切换 SIM 卡"
    def click_mobileData_button(self):
        self.click_element(self.mobileData_button)
    def click_switch_sim1(self):
        self._click_switch_sim(self.switch_sim1)
    def click_switch_sim2(self):
        self._click_switch_sim(self.switch_sim2)
    def _click_switch_sim(self, selector):
        for attempt in range(3):
            if self.is_element_exist(self.switch_Confirm, timeout=0):
                break
            self.click_element(selector)
            try:
                self.wait_element(self.switch_Confirm, timeout=3)
                break
            except WaitTimeoutError:
                if attempt == 2:
                    raise WaitTimeoutError(
                        f"设备 {self.driver.serial} 切换 DDS 失败："
                        f"{selector} 已点击 3 次，每次等待 3s，仍未出现确认弹窗"
                    ) from None
                logger.warning(
                    f"DDS 第 {attempt + 1} 次点击后未出现确认弹窗，将重试：{selector}"
                )
        self.click_element(self.switch_Confirm)
        self.wait_element_gone(self.switch_Confirm)
    def click_switch_auto(self):
        self.click_element(self.switch_auto)
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
    def click_operator_interface2(self):
        self.click_element(self.operator_interface2)
    def click_switch_call_card1(self):
        self.click_element(self.switch_call_card1)
    def click_switch_call_card2(self):
        self.click_element(self.switch_call_card2)
    def click_intelligent_card_selection(self):
        self.click_element(self.intelligent_card_selection)
    def click_close_ics_button(self):
        self.click_element(self.close_ics_button)

    def click_open_ics_button(self):
        self.click_element(self.open_ics_button)
    def click_switch_sms_card1(self):
        self.click_element(self.switch_sms_card1)
    def click_switch_sms_card2(self):
        self.click_element(self.switch_sms_card2)
    #运营商下的四级界面元素定位
    # network_tyep = "textContains:首选网络类型"
    # network_5g = "textContains:5G"
    # network_4g = "textContains:4G"
    button_5g = "xpath:(//android.widget.RelativeLayout)[7]"
    smart_network_switch = "textContains:智能数据模式"
    use_SA = "textContains:使用 SA"
    on_off_SIM_button = "resourceId:android:id/switch_widget"
    confirmButton = "resourceId:android:id/button1"
    cancelButton = "resourceId:android:id/button2"
    # mobile_Network_security = "textContains:移动网络安全"
    #采用*#*#4636拨号盘打开的电话服务设置更改networkType
    phoneID = "resourceId:com.android.phone:id/phoneIndex"
    phoneName = "xpath://*[@resource-id='android:id/text1']"
    phone0 = "xpath://*[@text='Phone 0']"
    phone1 = "xpath://*[@text='Phone 1']"
    settNetworkTepe = "resourceId:com.android.phone:id/preferredNetworkType"
    LTEonly = "xpath://*[@text='LTE/GSM']"
    # LTEonly = "xpath://*[@text='LTE only']"
    NRonly = "xpath://*[@text='NR only']"
    sim_data_service = "resourceId:com.android.phone:id/gprs"
    def open_phone_service(self):
        self.driver.app_start(
            "com.android.phone",
            activity="com.android.phone.settings.RadioInfo",
            stop=False,
        )
        self.scroll_to_element_down(self.phoneID, max_swipes=5, timeout=1)
    def close_phone_service(self):
        self.driver.app_stop("com.android.phone")
        self.driver.press("back")
    def click_phoneID(self):
        self.scroll_to_element_down(self.phoneID, max_swipes=5, timeout=1)
        self.click_element(self.phoneID)
    def click_phone0(self):
        self.click_element(self.phone0)
    def click_phone1(self):
        self.click_element(self.phone1)
    def select_phone(self, sim):
        if sim not in (1, 2):
            raise ValueError("sim 只能为 1 或 2")
        expected = f"Phone {sim - 1}"
        option = self.phone0 if sim == 1 else self.phone1

        def read_selection():
            return self.get_element_text(self.phoneName, timeout=0).strip()

        for attempt in range(3):
            if read_selection() == expected:
                return
            # 按钮文字尚非目标值，此时目标文字只用于查找下拉选项。
            if not self.is_element_exist(option, timeout=0):
                self.click_phoneID()
                self.wait_element(option)
            self.click_element(option)
            try:
                self.wait_until(
                    read_selection,
                    lambda text: text == expected,
                    f"电话信息页 phoneIndex 显示 SIM{sim}（{expected}）",
                    timeout=5,
                )
                return
            except WaitTimeoutError:
                if attempt == 1:
                    raise
                logger.warning(f"SIM{sim} 选卡确认超时，将重试一次")
    def click_settNetworkTepe(self):
        self.scroll_to_element(self.settNetworkTepe, max_swipes=5)
        self.wait_element(self.settNetworkTepe)
        self.click_element(self.settNetworkTepe)
    def click_LTEonly(self):
        # self.scroll_to_element_down(self.LTEonly, max_swipes=5)
        self.click_element(self.LTEonly)
    def click_NRonly(self):
        self.click_element(self.NRonly)

    # def click_network_tyep(self,max_times=2):
    #     self.scroll_to_element(self.network_tyep, max_swipes=max_times)
    #     self.click_element(self.network_tyep)
    # def click_network_5g(self):
    #     self.click_element(self.network_5g)
    # def click_network_4g(self):
    #     self.click_element(self.network_4g)
    # def click_button_5g(self):
    #     self.click_element(self.button_5g)

    def click_smart_network_switch(self):
        self.click_element(self.smart_network_switch)
    def click_use_SA(self):
        self.click_element(self.use_SA)
    def click_on_off_SIM_button(self):
        self.click_element(self.on_off_SIM_button)
    def click_confirmButton(self):
        self.click_element(self.confirmButton)
    def click_cancelButton(self):
        self.click_element(self.cancelButton)

    def click_Hotspot(self):
        self.click_element(self.mobile_Network_security)

    def get_sim_network_type(self):
        """查询当前网络制式，不代表用户配置的首选网络类型。"""
        output = DriverUtil.device_shell(self.driver, "getprop gsm.network.type")
        values = output.split(",")
        if len(values) > 2:
            raise RuntimeError(f"设备 {self.driver.serial} 网络制式记录超过两条：{output!r}")
        network_types = {"SIM1": "Unknown", "SIM2": "Unknown"}
        for index, value in enumerate(values, start=1):
            if "NR" in value or "5G" in value:
                network_types[f"SIM{index}"] = "5G_NR"
            elif "LTE" in value:
                network_types[f"SIM{index}"] = "LTE"
            else:
                logger.warning(
                    f"设备 {self.driver.serial} SIM{index} 网络制式未识别：{value!r}"
                )
        return network_types

    def wait_sim_network_type(self, sim, expected, timeout=30):
        if sim not in (1, 2):
            raise ValueError("sim 只能为 1 或 2")
        if expected not in ("5G_NR", "LTE"):
            raise ValueError("expected 只能为 5G_NR 或 LTE")
        return self.wait_until(
            self.get_sim_network_type,
            lambda states: states[f"SIM{sim}"] == expected,
            f"SIM{sim} 当前网络制式变为 {expected}", timeout,
        )

    moreSetting = "textContains:更多安全设置"
    simCasdProtect = "textContains:保护 SIM 卡"
    lockSIM1 = "xpath://android.widget.Switch"
    lockSIM2 = "xpath:(//android.widget.Switch)[2]"
    enterPIN1 = "xpath://android.widget.EditText"
    changePIN1_sim1 = "xpath://*[@text='更改 SIM 卡 PIN 码']"
    changePIN1_sim2 = "xpath:(//*[@text='更改 SIM 卡 PIN 码'])[2]"

    def click_more_security_Setting(self,max_times=3):
        self.scroll_to_element(self.moreSetting, max_swipes=max_times)
        self.click_element(self.moreSetting)
    def click_simCasdProtect(self,max_times=4):
        self.scroll_to_element(self.simCasdProtect, max_swipes=max_times)
        self.click_element(self.simCasdProtect)
    def click_lockSIM1(self):
        self.click_element(self.lockSIM1)

    def click_lockSIM2(self):
        self.click_element(self.lockSIM2)
    def inputPIN1(self,PIN1):
        self.input_text(self.enterPIN1,PIN1)
    def click_changePIN1(self):
        self.click_element(self.changePIN1)

    def check_pin_status(self,sim):
        if sim not in (1, 2):
            raise ValueError("sim 只能为 1 或 2")
        self.wait_element_gone(self.enterPIN1)
        selector = self.lockSIM1 if sim == 1 else self.lockSIM2
        checked = self.wait_element(selector).info.get("checked")
        if not isinstance(checked, bool):
            raise RuntimeError(f"设备 {self.driver.serial} SIM{sim} 锁定开关缺少 checked 状态")
        logger.info(f"SIM{sim} PIN 锁定状态：{checked}")
        return checked

    # #关于手机界面元素
    # details_information = "textContains:设备详细信息"
    # #设备详细信息界面元素
    # sim1_status = "textContains:SIM 卡 1 状态"
    # sim2_status = "textContains:SIM 卡 2 状态"
    # data_status = "resourceId:com.android.settings:id/data_state_value"
    #判断dds状态
    def check_dds_status(self,sim):
        if sim not in (1, 2):
            raise ValueError("sim 只能为 1 或 2")
        self.open_phone_service()
        self.select_phone(sim)
        dds_status = self.get_element_text(self.sim_data_service)
        logger.info(f"SIM{sim} 数据状态: {dds_status}")
        return dds_status
    def settSIM1_dds(self):
        if self.check_dds_status(1) != "已连接":
            self.open_Setting_app()
            time.sleep(2)
            if self.is_element_exist(self.mobileData_button, timeout=0):
                logger.info("已在移动数据界面")
                self.click_switch_sim1()
            else:
                self.click_network()
                self.click_mobileData()
                self.click_switch_sim1()
        else:
            logger.info("SIM1已是dds，无需切换")
    def settSIM2_dds(self):
        if self.check_dds_status(2) != "已连接":
            self.open_Setting_app()
            if self.is_element_exist(self.mobileData_button, timeout=0):
                logger.info("已在移动数据界面")
            else:
                self.click_network()
                self.click_mobileData()
            self.click_switch_sim2()
        else:
            logger.info("SIM2已是dds，无需切换")

    def settSIM1_LTE(self):
        self.open_phone_service()
        self.select_phone(1)
        self.click_settNetworkTepe()
        self.click_LTEonly()
    def settSIM1_NR(self):
        self.open_phone_service()
        self.select_phone(1)
        self.click_settNetworkTepe()
        self.click_NRonly()
    def settSIM2_LTE(self):
        self.open_phone_service()
        self.select_phone(2)
        self.click_settNetworkTepe()
        self.click_LTEonly()
    def settSIM2_NR(self):
        self.open_phone_service()
        self.select_phone(2)
        self.click_settNetworkTepe()
        self.click_NRonly()

    def ping_data(self):
        """ping测试"""
        output = DriverUtil.device_shell(self.driver, "ping -c 4 www.baidu.com")
        if "4 packets transmitted, 4 received" in output:
            logger.info(f"设备 {self.driver.serial} ping 测试成功")
            return True
        else:
            logger.warning(f"设备 {self.driver.serial} ping 测试失败，输出：{output}")
            return False
    def ping_ipv6_data(self):
        """ping测试"""
        output = DriverUtil.device_shell(self.driver, "ping6 -c 4 www.baidu.com")
        if "4 packets transmitted, 4 received" in output:
            logger.info(f"设备 {self.driver.serial} ipv6 ping 测试成功")
            return True
        else:
            logger.warning(f"设备 {self.driver.serial} ipv6 ping 测试失败，输出：{output}")
            return False
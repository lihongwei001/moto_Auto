import allure
from page.settinng_page import *

@allure.feature("PIN1模块")
@allure.story("PIN1测试")
def test_PIN1(driver,pin1_data):
    setting_page = SettingPage(driver)
    data = pin1_data["PIN1"]
    with allure.step("打开设置"):
        setting_page.open_Setting_app()
    with allure.step("打开锁定SIM卡"):
        setting_page.click_securityPrivacy()
        setting_page.click_more_security_Setting()
        setting_page.click_simCasdProtect()
        setting_page.click_lockSIM1()
        # setting_page.click_lockSIM2()
        setting_page.inputPIN1(data)
        setting_page.click_confirmButton()

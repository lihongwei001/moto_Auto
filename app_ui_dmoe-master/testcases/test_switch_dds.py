import allure
from page.settinng_page import *

@allure.feature("切换DDS模块")
@allure.story("切换DDS测试")
def test_switch_sim2_dds(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("切换dds为sim2"):
        setting_page.settSIM2_dds()
def test_switch_sim1_dds(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("切换dds为sim1"):
        setting_page.settSIM1_dds()
        # setting_page.wait_element(setting_page.switch_sim1)
        # setting_page.click_element(setting_page.switch_sim1)
        # setting_page.click_element(setting_page.switch_Confirm)
        # setting_page.wait_element_gone(setting_page.switch_Confirm)
# import allure
# from page.settinng_page import *
#
# @allure.feature("切换DDS模块")
# @allure.story("切换DDS测试")
# def switch_dds(driver):
#     setting_page = SettingPage(driver)
#     with allure.step("打开设置"):
#         setting_page.open_Setting_app()
#     with allure.step("切换DDS"):
#         setting_page.click_network()
#         setting_page.switch_sim2()
#
import allure
from page.settinng_page import *

@allure.feature("切换DDS模块")
@allure.story("切换DDS测试")
def test_switch_dds(driver):
    setting_page = SettingPage(driver)
    with allure.step("打开设置"):
        setting_page.open_Setting_app()
    with allure.step("切换dds为sim2"):
        setting_page.click_network()
        setting_page.click_mobileData()
        setting_page.click_switch_sim2()
        setting_page.click_switch_sim1()

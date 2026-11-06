import allure
from page.settinng_page import *

@allure.feature("切换DDS模块")
@allure.story("切换DDS测试")
def test_switch_dds(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("打开设置"):
        setting_page.open_Setting_app()
    with allure.step("切换dds为sim2"):
        setting_page.click_network()
        setting_page.click_mobileData()
        setting_page.click_switch_sim2()
        # setting_page.click_switch_sim1()
    with allure.step("检查dds状态"):
        setting_page.close_Setting_app()
        setting_page.open_Setting_app()
        setting_page.check_dds_status(2)

import allure
from page.settinng_page import *
import sys
sys.stdout.reconfigure(encoding='utf-8')

@allure.feature("切换sim卡首选网络类型模块")
@allure.story("切换sim卡首选网络类型测试")
def test_switch_call_sim(driver):
    main_driver, sup_driver = driver
    setting_page = SettingPage(main_driver)
    with allure.step("切换首选网络类型为4g"):
        # setting_page.click_network()
        # setting_page.click_simCard()
        # setting_page.click_operator_interface1()
        # setting_page.click_network_tyep()
        # setting_page.click_network_4g()
        # setting_page.click_network_tyep()
        # setting_page.click_network_5g()
        # setting_page.click_button_5g()
        network_type = setting_page.get_sim_network_type()
        print(f"当前SIM卡首选网络类型: {network_type}")
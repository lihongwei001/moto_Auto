import allure
from page.settinng_page import *

@allure.feature("ping模块")
@allure.story("ping测试")

def test_ping(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("ping测试"):
        ping_result = setting_page.ping_data()
        assert ping_result, "Ping测试失败"
def test_ping_ipv6(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("ping IPv6测试"):
        ping_result = setting_page.ping_ipv6_data()
        assert ping_result, "Ping IPv6测试失败"
import allure
from page.settinng_page import *
import sys
sys.stdout.reconfigure(encoding='utf-8')

@allure.feature("切换sim卡首选网络类型模块")
@allure.story("切换sim卡首选网络类型测试")

def settSIM1_5G(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("切换SIM1网络类型为5G"):
        setting_page.settSIM1_NR()
        network_type = setting_page.wait_sim_network_type(
            sim=1, expected="5G_NR", timeout=30
        )
        print(f"当前SIM卡网络类型: {network_type}")
        assert network_type["SIM1"] == "5G_NR", (
            f"SIM1切换5G失败，预期: 5G_NR，实际: {network_type}"
        )
def settSIM1_4G(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("切换SIM1网络类型为4G"):
        setting_page.settSIM1_LTE()
        network_type = setting_page.wait_sim_network_type(
            sim=1, expected="LTE", timeout=30
        )
        print(f"当前SIM卡网络类型: {network_type}")
        assert network_type["SIM1"] == "LTE", (
            f"SIM1切换4G失败，预期: LTE，实际: {network_type}"
        )
def settSIM2_5G(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("切换SIM2网络类型为5G"):
        setting_page.settSIM2_NR()
        network_type = setting_page.wait_sim_network_type(
            sim=2, expected="5G_NR", timeout=30
        )
        print(f"当前SIM卡网络类型: {network_type}")
        assert network_type["SIM2"] == "5G_NR", (
            f"SIM2切换5G失败，预期: 5G_NR，实际: {network_type}"
        )
def settSIM2_4G(main_driver):
    setting_page = SettingPage(main_driver)
    with allure.step("切换SIM2网络类型为4G"):
        setting_page.settSIM2_LTE()
        network_type = setting_page.wait_sim_network_type(
            sim=2, expected="LTE", timeout=30
        )
        print(f"当前SIM卡网络类型: {network_type}")
        assert network_type["SIM2"] == "LTE", (
            f"SIM2切换4G失败，预期: LTE，实际: {network_type}"
        )

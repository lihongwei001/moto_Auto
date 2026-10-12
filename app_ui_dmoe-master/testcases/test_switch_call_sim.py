import allure
from page.settinng_page import *

@allure.feature("切换首选通话sim卡模块")
@allure.story("切换首选通话sim卡测试")
def test_switch_call_sim(driver):
    setting_page = SettingPage(driver)
    # with allure.step("打开设置"):
    #     setting_page.open_Setting_app()
    with allure.step("切换首选通话sim卡为sim1,最终设置为'总询问'"):
        setting_page.click_network()
        setting_page.click_simCard()
        setting_page.click_intelligent_card_selection()
        setting_page.click_close_ics_button()
        setting_page.click_switch_call_card1()
        setting_page.click_switch_call_card2()
        setting_page.click_intelligent_card_selection()
        setting_page.click_open_ics_button()